"""Training mechanics, reproducible evaluation, and the saved-checkpoint workflow."""

from contextlib import redirect_stdout
import csv
import importlib
import io
import math
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import torch
from torch import nn

from transformer_lab.check_training import CHECKS
from transformer_lab.config import TransformerConfig
from transformer_lab.generate import main as generate_main
from transformer_lab.inspect import main as inspect_main
from transformer_lab.plotting import write_attention_plot, write_loss_plot
from transformer_lab.reference import TinyTransformer
from transformer_lab.runtime import load_checkpoint, setup_cpu
from transformer_lab.train import evaluate_loss, fixed_batches, main as train_main


IMPLEMENTATION_NAME = os.environ.get("TRANSFORMER_IMPL", "reference")
implementation = importlib.import_module(f"transformer_lab.{IMPLEMENTATION_NAME}_training")


def _config(**kwargs):
    values = dict(vocab_size=6, context_length=5, d_model=8, n_heads=2, n_layers=1, d_ff=16)
    values.update(kwargs)
    return TransformerConfig(**values)


class TrainingMechanicsTests(unittest.TestCase):
    def setUp(self):
        setup_cpu(41)

    def test_learning_checkpoints(self):
        for stage, (_, check) in CHECKS.items():
            with self.subTest(stage=stage):
                check(implementation)

    def test_shifted_views_match_interior_targets(self):
        windows = torch.arange(14).reshape(2, 7)
        x, y = implementation.shifted_targets(windows)
        self.assertEqual(x.shape, (2, 6))
        torch.testing.assert_close(x[:, 1:], y[:, :-1])
        torch.testing.assert_close(y[:, -1], windows[:, -1])

    def test_loss_gradient_matches_uniform_cross_entropy(self):
        logits = torch.zeros(2, 3, 4, requires_grad=True)
        targets = torch.tensor([[0, 1, 2], [3, 0, 1]])
        loss = implementation.language_model_loss(logits, targets)
        loss.backward()
        expected = torch.full_like(logits, 0.25)
        expected.scatter_add_(-1, targets.unsqueeze(-1), -torch.ones(2, 3, 1))
        expected /= 6
        torch.testing.assert_close(logits.grad, expected)

    def test_optimizer_step_clears_preexisting_gradients(self):
        first = nn.Sequential(nn.Embedding(4, 8), nn.Linear(8, 4))
        second = nn.Sequential(nn.Embedding(4, 8), nn.Linear(8, 4))
        second.load_state_dict(first.state_dict())
        for parameter in second.parameters():
            parameter.grad = torch.full_like(parameter, 100.0)
        first_optimizer = torch.optim.SGD(first.parameters(), lr=0.05)
        second_optimizer = torch.optim.SGD(second.parameters(), lr=0.05)
        x = torch.tensor([[0, 1, 2, 3]])
        y = torch.tensor([[1, 2, 3, 0]])
        implementation.train_step(first, first_optimizer, x, y)
        implementation.train_step(second, second_optimizer, x, y)
        for a, b in zip(first.parameters(), second.parameters()):
            torch.testing.assert_close(a, b, msg="Each step must clear earlier gradients before backward.")

    def test_temperature_changes_sampling_distribution(self):
        logits = torch.tensor([[0.0, 1.0]]).expand(2000, 2)
        cold = implementation.sample_next(logits, 0.1, torch.Generator().manual_seed(7))
        hot = implementation.sample_next(logits, 100.0, torch.Generator().manual_seed(7))
        self.assertGreater(cold.float().mean().item(), 0.98)
        self.assertGreater(hot.float().mean().item(), 0.4)
        self.assertLess(hot.float().mean().item(), 0.6)

    def test_sampling_with_generator_does_not_advance_global_rng(self):
        before = torch.get_rng_state().clone()
        implementation.sample_next(torch.zeros(20, 4), 1.0, torch.Generator().manual_seed(11))
        torch.testing.assert_close(torch.get_rng_state(), before)

    def test_training_inputs_are_validated(self):
        for windows in (torch.zeros(2, 1, dtype=torch.long), torch.zeros(3, dtype=torch.long), torch.zeros(2, 3)):
            with self.subTest(shape=windows.shape), self.assertRaises(ValueError):
                implementation.shifted_targets(windows)
        with self.assertRaises(ValueError):
            implementation.language_model_loss(torch.zeros(2, 3, 4), torch.zeros(2, 4, dtype=torch.long))
        for temperature in (0, -1, float("nan"), float("inf")):
            with self.subTest(temperature=temperature), self.assertRaises(ValueError):
                implementation.sample_next(torch.zeros(2, 3), temperature)


class TrainingWorkflowTests(unittest.TestCase):
    def setUp(self):
        setup_cpu(71)

    def test_fixed_evaluation_preserves_rng_and_mode(self):
        data = torch.arange(60) % 6
        before_windows = torch.get_rng_state().clone()
        batches = fixed_batches(data, 3, 5, 3, 91)
        torch.testing.assert_close(torch.get_rng_state(), before_windows)
        repeated = fixed_batches(data, 3, 5, 3, 91)
        for first, second in zip(batches, repeated):
            for a, b in zip(first, second):
                torch.testing.assert_close(a, b)
        model = TinyTransformer(_config(dropout=0.5))
        for was_training in (True, False):
            model.train(was_training)
            rng_before = torch.get_rng_state().clone()
            first_loss = evaluate_loss(model, batches)
            second_loss = evaluate_loss(model, batches)
            self.assertEqual(first_loss, second_loss)
            self.assertEqual(model.training, was_training)
            torch.testing.assert_close(torch.get_rng_state(), rng_before)
            self.assertTrue(all(parameter.grad is None for parameter in model.parameters()))

    def test_evaluation_restores_mode_after_exception(self):
        model = TinyTransformer(_config())
        def fail(module, args):
            raise RuntimeError("test evaluation failure")
        handle = model.register_forward_pre_hook(fail)
        with self.assertRaisesRegex(RuntimeError, "test evaluation failure"):
            evaluate_loss(model, [(torch.zeros(1, 3, dtype=torch.long), torch.zeros(1, 3, dtype=torch.long))])
        handle.remove()
        self.assertTrue(model.training)

    def test_training_checkpoint_generation_and_attention_workflow(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            data = base / "corpus.txt"
            data.write_text("the cat sat.\nthe dog sat.\n" * 80, encoding="utf-8")
            output = base / "run"
            args = [
                "--implementation", IMPLEMENTATION_NAME, "--data", str(data), "--out-dir", str(output),
                "--steps", "40", "--batch-size", "4", "--context-length", "8", "--d-model", "12",
                "--n-heads", "3", "--n-layers", "1", "--d-ff", "24", "--eval-every", "20", "--eval-batches", "2", "--lr", "0.02",
            ]
            with redirect_stdout(io.StringIO()):
                self.assertEqual(train_main(args), 0)
            with (output / "metrics.csv").open() as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual([int(row["step"]) for row in rows], [0, 20, 40])
            self.assertTrue(all(math.isfinite(float(row[key])) for row in rows for key in ("train_loss", "val_loss")))
            self.assertLess(float(rows[-1]["train_loss"]), float(rows[0]["train_loss"]) * 0.65)
            self.assertEqual((output / "loss.png").read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            checkpoint_path = output / "model.pt"
            model, tokenizer, metadata = load_checkpoint(checkpoint_path)
            self.assertEqual(metadata["step"], 40)
            self.assertEqual(metadata["implementation"], IMPLEMENTATION_NAME)
            self.assertFalse(model.training)
            restored, restored_tokenizer, _ = load_checkpoint(checkpoint_path)
            ids = torch.tensor([tokenizer.encode("the cat")])
            torch.testing.assert_close(model(ids), restored(ids))
            self.assertEqual(restored_tokenizer.chars, tokenizer.chars)
            for changed in ("reference", "student"):
                overridden, _, _ = load_checkpoint(checkpoint_path, changed)
                self.assertEqual(type(overridden).__module__, f"transformer_lab.{changed}")
            capture = io.StringIO()
            with redirect_stdout(capture):
                self.assertEqual(generate_main(["--checkpoint", str(checkpoint_path), "--prompt", "the ", "--new-tokens", "8"]), 0)
            self.assertTrue(capture.getvalue().startswith("the "))
            self.assertEqual(len(capture.getvalue()), 13)  # 4 prompt + 8 new + print newline.
            with redirect_stdout(io.StringIO()):
                self.assertEqual(inspect_main(["--checkpoint", str(checkpoint_path), "--text", "the cat"]), 0)
            self.assertEqual((output / "attention.png").read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            for invalid in (["--head", "3"], ["--text", "the cat sat."]):
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(inspect_main(["--checkpoint", str(checkpoint_path), *invalid]), 1)

    def test_unfinished_student_stops_with_help_and_no_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            data = base / "corpus.txt"
            data.write_text("the cat sat.\n" * 100, encoding="utf-8")
            output = base / "untouched"
            capture = io.StringIO()
            # This preserves the intended failure test after the learner solves E06.
            with patch("transformer_lab.train.build_model", side_effect=NotImplementedError("E06: test exercise")), redirect_stdout(capture):
                result = train_main(["--data", str(data), "--out-dir", str(output), "--steps", "1"])
            self.assertEqual(result, 1)
            self.assertIn("--implementation reference", capture.getvalue())
            self.assertIn("Student work remains", capture.getvalue())
            self.assertNotIn("Traceback", capture.getvalue())
            self.assertFalse(output.exists())

    def test_checkpoint_metadata_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.pt"
            torch.save({"format_version": 2}, path)
            with self.assertRaisesRegex(ValueError, "format_version=1"):
                load_checkpoint(path)
            torch.save({"format_version": 1}, path)
            with self.assertRaisesRegex(ValueError, "must contain"):
                load_checkpoint(path)

    def test_plot_validation_and_character_labels(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plot.png"
            with self.assertRaises(ValueError):
                write_loss_plot([], path)
            with self.assertRaises(ValueError):
                write_loss_plot([{"step": 0, "train_loss": float("nan"), "val_loss": 1}], path)
            with self.assertRaises(ValueError):
                write_attention_plot([[1, 0]], ["a", "b"], path)
            write_attention_plot([[1, 0, 0], [0.5, 0.5, 0], [0.2, 0.3, 0.5]], ["<", " ", "\n"], path)
            self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
