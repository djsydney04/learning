"""Run reference tests, or set TRANSFORMER_IMPL=student after finishing E01--E06."""

import importlib
import os
import unittest

import torch
from torch.nn import functional as F

from transformer_lab.check import CHECKS
from transformer_lab.config import TransformerConfig
from transformer_lab.data import CharacterTokenizer, make_batch, split_data


IMPLEMENTATION_NAME = os.environ.get("TRANSFORMER_IMPL", "reference")
if IMPLEMENTATION_NAME not in ("reference", "student"):
    raise ValueError("TRANSFORMER_IMPL must be 'reference' or 'student'")
implementation = importlib.import_module(f"transformer_lab.{IMPLEMENTATION_NAME}")


def small_config(**overrides):
    values = dict(vocab_size=9, context_length=8, d_model=12, n_heads=3, n_layers=2, d_ff=24)
    values.update(overrides)
    return TransformerConfig(**values)


class DataTests(unittest.TestCase):
    def test_tokenizer_round_trip_including_whitespace(self):
        text = "cat\n cat!"
        tokenizer = CharacterTokenizer(text)
        self.assertEqual(tokenizer.decode(tokenizer.encode(text)), text)
        self.assertEqual(tokenizer.chars, sorted(set(text)))
        self.assertEqual(len(tokenizer), len(set(text)))

    def test_restored_vocabulary_keeps_its_order(self):
        tokenizer = CharacterTokenizer.from_chars(["b", "a", " "])
        self.assertEqual(tokenizer.encode("ab "), [1, 0, 2])
        self.assertEqual(tokenizer.decode(torch.tensor([1, 0, 2])), "ab ")

    def test_tokenizer_rejects_invalid_inputs(self):
        for chars in ([], ["a", "a"], ["word"], [1]):
            with self.subTest(chars=chars), self.assertRaises(ValueError):
                CharacterTokenizer.from_chars(chars)
        with self.assertRaises(ValueError):
            CharacterTokenizer("")
        tokenizer = CharacterTokenizer("ab")
        with self.assertRaises(ValueError):
            tokenizer.encode("c")
        for ids in ([-1], [2]):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                tokenizer.decode(ids)

    def test_batch_inputs_and_targets_are_shifted(self):
        data = torch.arange(50)
        x, y = make_batch(data, batch_size=5, context_length=8)
        self.assertEqual(x.shape, (5, 8))
        self.assertEqual(x.dtype, torch.long)
        torch.testing.assert_close(y, x + 1)
        torch.testing.assert_close(x[:, 1:], y[:, :-1])

    def test_batch_minimum_length_and_seed(self):
        data = torch.arange(9)
        x, y = make_batch(data, 3, 8)
        torch.testing.assert_close(x, torch.arange(8).expand(3, 8))
        torch.testing.assert_close(y, torch.arange(1, 9).expand(3, 8))
        data = torch.arange(100)
        first = make_batch(data, 6, 8, torch.Generator().manual_seed(17))
        second = make_batch(data, 6, 8, torch.Generator().manual_seed(17))
        for a, b in zip(first, second):
            torch.testing.assert_close(a, b)

    def test_bad_batches_are_rejected(self):
        for data, batch_size, context in (
            (torch.arange(8), 1, 8),
            (torch.arange(10).float(), 1, 8),
            (torch.zeros(2, 10, dtype=torch.long), 1, 8),
            (torch.arange(10), 0, 8),
            (torch.arange(10), 1, 0),
        ):
            with self.subTest(shape=data.shape, batch_size=batch_size, context=context), self.assertRaises(ValueError):
                make_batch(data, batch_size, context)

    def test_split_precedes_sampling(self):
        train, valid = split_data("abcdefghij", 0.7)
        self.assertEqual((train, valid), ("abcdefg", "hij"))
        for fraction in (0, 1, -0.1, 1.1):
            with self.subTest(fraction=fraction), self.assertRaises(ValueError):
                split_data("abc", fraction)
        with self.assertRaises(ValueError):
            split_data("a")


class ConfigTests(unittest.TestCase):
    def test_invalid_dimensions_and_dropout(self):
        for overrides in (
            {"vocab_size": 0}, {"d_model": 13}, {"n_heads": 0},
            {"context_length": -1}, {"n_layers": 0}, {"d_ff": 0},
            {"dropout": -0.1}, {"dropout": 1}, {"d_model": True},
        ):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                small_config(**overrides)

    def test_config_round_trip(self):
        config = small_config()
        self.assertEqual(TransformerConfig(**config.to_dict()), config)


class TransformerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)

    def setUp(self):
        torch.manual_seed(73)

    def test_learning_checkpoints(self):
        for stage, (_, check) in CHECKS.items():
            with self.subTest(stage=stage):
                check(implementation)

    def test_attention_batches_heads_and_rectangular_lengths(self):
        q = torch.zeros(2, 3, 4, 5)
        k = torch.zeros(2, 3, 6, 5)
        v = torch.randn(2, 3, 6, 7)
        output, weights = implementation.scaled_attention(q, k, v, causal=False)
        self.assertEqual(output.shape, (2, 3, 4, 7))
        self.assertEqual(weights.shape, (2, 3, 4, 6))
        torch.testing.assert_close(output, v.mean(-2, keepdim=True).expand_as(output))
        causal_output, causal_weights = implementation.scaled_attention(q, k, v, causal=True)
        for position in range(4):
            torch.testing.assert_close(causal_output[:, :, position], v[:, :, : position + 1].mean(-2))
        self.assertEqual(torch.count_nonzero(causal_weights.triu(1)).item(), 0)

    def test_attention_future_keys_and_values_cannot_affect_prefix(self):
        q = torch.randn(2, 3, 5, 4)
        k = torch.randn(2, 3, 5, 4)
        v = torch.randn(2, 3, 5, 4)
        first, _ = implementation.scaled_attention(q, k, v)
        k[:, :, 3:] += 100
        v[:, :, 3:] -= 100
        changed, _ = implementation.scaled_attention(q, k, v)
        torch.testing.assert_close(first[:, :, :3], changed[:, :, :3])

    def test_attention_numerical_gradients(self):
        values = tuple(torch.randn(1, 3, 2, dtype=torch.double, requires_grad=True) for _ in range(3))
        self.assertTrue(torch.autograd.gradcheck(lambda q, k, v: implementation.scaled_attention(q, k, v)[0], values))

    def test_heads_match_independently_calculated_head_outputs(self):
        config = small_config()
        module = implementation.MultiHeadAttention(config)
        x = torch.randn(2, 5, config.d_model)
        output, weights = module(x, return_weights=True)
        q, k, v = module.q_proj(x), module.k_proj(x), module.v_proj(x)
        expected = torch.empty_like(x)
        width = config.d_model // config.n_heads
        # Deliberately slow loops make an oracle independent of the batched reshape.
        for batch in range(2):
            for head in range(config.n_heads):
                features = slice(head * width, (head + 1) * width)
                for position in range(5):
                    scores = k[batch, : position + 1, features] @ q[batch, position, features] / width**0.5
                    probabilities = scores.softmax(dim=0)
                    expected[batch, position, features] = probabilities @ v[batch, : position + 1, features]
                    torch.testing.assert_close(weights[batch, head, position, : position + 1], probabilities)
        torch.testing.assert_close(output, module.out_proj(expected))

    def test_feedforward_gradient_stays_within_its_position(self):
        module = implementation.FeedForward(small_config())
        x = torch.randn(2, 5, 12, requires_grad=True)
        module(x)[0, 2].sum().backward()
        self.assertEqual(torch.count_nonzero(x.grad[1]).item(), 0)
        self.assertEqual(torch.count_nonzero(x.grad[0, [0, 1, 3, 4]]).item(), 0)
        self.assertGreater(torch.count_nonzero(x.grad[0, 2]).item(), 0)

    def test_model_prefix_is_causal_for_each_position(self):
        model = implementation.TinyTransformer(small_config()).eval()
        ids = torch.randint(0, 9, (2, 8))
        full = model(ids)
        for length in range(1, 9):
            with self.subTest(length=length):
                torch.testing.assert_close(full[:, :length], model(ids[:, :length]), atol=1e-6, rtol=1e-5)

    def test_model_overfits_a_tiny_fixed_batch(self):
        model = implementation.TinyTransformer(small_config(n_layers=1))
        optimizer = torch.optim.AdamW(model.parameters(), lr=0.02)
        ids = torch.tensor([[0, 1, 2, 3], [3, 2, 1, 0]])
        targets = torch.tensor([[1, 2, 3, 4], [2, 1, 0, 4]])
        initial = F.cross_entropy(model(ids).reshape(-1, 9), targets.reshape(-1)).item()
        for _ in range(30):
            optimizer.zero_grad(set_to_none=True)
            loss = F.cross_entropy(model(ids).reshape(-1, 9), targets.reshape(-1))
            loss.backward()
            optimizer.step()
        final = F.cross_entropy(model(ids).reshape(-1, 9), targets.reshape(-1)).item()
        self.assertLess(final, initial * 0.3, "Connected gradients should let this small model memorize eight targets.")

    def test_generation_crops_context_and_preserves_prompt_and_mode(self):
        config = small_config(dropout=0.5)
        model = implementation.TinyTransformer(config)
        prompt = torch.randint(0, 9, (2, 11))
        observed = []
        handle = model.register_forward_pre_hook(lambda module, args: observed.append((args[0].shape[1], module.training, torch.is_grad_enabled())))
        for was_training in (True, False):
            model.train(was_training)
            generated = model.generate(prompt, max_new_tokens=3)
            self.assertEqual(generated.shape, (2, 14))
            torch.testing.assert_close(generated[:, :11], prompt)
            self.assertEqual(model.training, was_training)
            self.assertTrue(((generated >= 0) & (generated < config.vocab_size)).all())
        handle.remove()
        self.assertEqual(observed, [(8, False, False)] * 6)

    def test_generation_restores_mode_on_error(self):
        model = implementation.TinyTransformer(small_config())
        def fail(module, args):
            raise RuntimeError("test failure during forward")
        handle = model.register_forward_pre_hook(fail)
        with self.assertRaisesRegex(RuntimeError, "test failure"):
            model.generate(torch.zeros(1, 1, dtype=torch.long), max_new_tokens=1)
        handle.remove()
        self.assertTrue(model.training)

    def test_generation_and_context_validation(self):
        model = implementation.TinyTransformer(small_config())
        prompt = torch.zeros(1, 2, dtype=torch.long)
        torch.testing.assert_close(model.generate(prompt, max_new_tokens=0), prompt)
        for temperature in (0, -1, float("nan"), float("inf")):
            with self.subTest(temperature=temperature), self.assertRaises(ValueError):
                model.generate(prompt, temperature=temperature)
        for tokens in (-1, 1.5):
            with self.subTest(tokens=tokens), self.assertRaises(ValueError):
                model.generate(prompt, max_new_tokens=tokens)
        for bad in (torch.zeros(1, 9, dtype=torch.long), torch.zeros(1, 0, dtype=torch.long), torch.zeros(4, dtype=torch.long)):
            with self.subTest(shape=bad.shape), self.assertRaises(ValueError):
                model(bad)
        with self.assertRaises(ValueError):
            model.generate(torch.zeros(1, 0, dtype=torch.long))

    def test_student_and_reference_weights_are_compatible(self):
        # Loading a reference checkpoint must not require any student forward pass.
        from transformer_lab import reference, student
        solved = reference.TinyTransformer(small_config())
        learner = student.TinyTransformer(small_config())
        learner.load_state_dict(solved.state_dict(), strict=True)
        solved.load_state_dict(learner.state_dict(), strict=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
