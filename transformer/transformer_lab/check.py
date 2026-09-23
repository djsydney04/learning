"""Small, explanatory checkpoints for your implementation.

Run one stage while learning, or run --stage all before training. These checks
use hand-computable results and behavioral properties rather than importing the
reference answers. A failure is a useful clue, not a grade.
"""

import argparse
import importlib
import math
import sys
from types import ModuleType

import torch
from torch.nn import functional as F

from .config import TransformerConfig


def _config(**overrides) -> TransformerConfig:
    values = dict(vocab_size=7, context_length=8, d_model=8, n_heads=2, n_layers=2, d_ff=16)
    values.update(overrides)
    return TransformerConfig(**values)


def check_embeddings(implementation: ModuleType) -> None:
    module = implementation.TokenPositionEmbedding(_config())
    with torch.no_grad():
        # A token contributes its ID; a position contributes ten times its index.
        module.token_embedding.weight.copy_(torch.arange(7).float()[:, None].expand(7, 8))
        module.position_embedding.weight.copy_((10 * torch.arange(8)).float()[:, None].expand(8, 8))
    ids = torch.tensor([[2, 2, 4], [1, 3, 1]])
    actual = module(ids)
    expected = torch.tensor([[2, 12, 24], [1, 13, 21]]).float().unsqueeze(-1).expand(2, 3, 8)
    torch.testing.assert_close(actual, expected, msg="Add the token vector AND the position vector at every position.")
    actual.sum().backward()
    assert module.token_embedding.weight.grad is not None, "Embedding lookups must remain connected to autograd."


def check_attention(implementation: ModuleType) -> None:
    # D=4: [2,0,0,0] dot [1,0,0,0] / sqrt(4) = 1.
    q = torch.tensor([[2.0, 0, 0, 0], [4.0, 0, 0, 0]])
    k = torch.tensor([[1.0, 0, 0, 0], [0.0, 0, 0, 0]])
    v = torch.tensor([[10.0], [20.0]])
    output, weights = implementation.scaled_attention(q, k, v, causal=False)
    expected = torch.tensor([[(10 * math.e + 20) / (math.e + 1)], [(10 * math.e**2 + 20) / (math.e**2 + 1)]])
    torch.testing.assert_close(output, expected, msg="Check the dot product, sqrt(D) scaling, softmax axis, and weighted values.")
    torch.testing.assert_close(weights.sum(-1), torch.ones(2), msg="Normalize each query's row over key positions.")
    causal_output, causal_weights = implementation.scaled_attention(q, k, v, causal=True)
    torch.testing.assert_close(causal_output[0], v[0], msg="Position zero may attend only to position zero.")
    assert causal_weights[0, 1].item() == 0, "Future keys must receive exactly zero probability."
    # A mask must change scores before softmax, so available weights still sum to one.
    torch.testing.assert_close(causal_weights.sum(-1), torch.ones(2))
    torch.testing.assert_close(causal_output[1], expected[1])


def check_heads(implementation: ModuleType) -> None:
    module = implementation.MultiHeadAttention(_config())
    with torch.no_grad():
        # Uniform scores and identity values make the answer a running mean.
        for projection in (module.q_proj, module.k_proj):
            projection.weight.zero_()
            projection.bias.zero_()
        for projection in (module.v_proj, module.out_proj):
            projection.weight.copy_(torch.eye(8))
            projection.bias.zero_()
    x = torch.arange(2 * 3 * 8).float().reshape(2, 3, 8)
    output, weights = module(x, return_weights=True)
    expected = x.cumsum(dim=1) / torch.arange(1, 4)[None, :, None]
    torch.testing.assert_close(output, expected, msg="Restore [B,T,H,D] before joining the head and feature axes.")
    assert weights.shape == (2, 2, 3, 3), "Attention weights must be [B,H,T,T]."
    torch.testing.assert_close(module(x), output, msg="The default return value must be the output tensor alone.")


def check_feedforward(implementation: ModuleType) -> None:
    module = implementation.FeedForward(_config())
    x = torch.randn(2, 4, 8)
    actual = module(x)
    assert actual.shape == x.shape, "The feed-forward branch must return to d_model."
    expected = module.net(x)
    torch.testing.assert_close(actual, expected, msg="Run the supplied Linear -> GELU -> Linear -> Dropout sequence.")
    changed = x.clone()
    changed[:, 2, :] += 5
    updated = module(changed)
    torch.testing.assert_close(actual[:, [0, 1, 3]], updated[:, [0, 1, 3]], msg="Feed-forward networks process positions independently.")


def check_block(implementation: ModuleType) -> None:
    module = implementation.TransformerBlock(_config())
    x = torch.randn(2, 4, 8, requires_grad=True)
    actual = module(x)
    after_attention = x + module.attention(module.norm1(x))
    expected = after_attention + module.feed_forward(module.norm2(after_attention))
    torch.testing.assert_close(actual, expected, msg="Apply pre-norm, attention residual, then pre-norm and feed-forward residual to the updated x.")
    # With both branches zeroed, the residual path must carry the exact input.
    with torch.no_grad():
        for branch in (module.attention, module.feed_forward):
            for parameter in branch.parameters():
                parameter.zero_()
    torch.testing.assert_close(module(x), x, msg="Zero branches should leave x unchanged through the residual path.")


def check_model(implementation: ModuleType) -> None:
    config = _config()
    model = implementation.TinyTransformer(config)
    ids = torch.tensor([[0, 1, 2, 3], [3, 2, 1, 0]])
    logits = model(ids)
    assert logits.shape == (2, 4, 7), "Return [batch, positions, vocabulary] logits."
    # Alter the future: earlier predictions must remain identical.
    changed = ids.clone()
    changed[:, 2:] = 6
    torch.testing.assert_close(logits[:, :2], model(changed)[:, :2], msg="A future character leaked into an earlier prediction. Check the causal mask.")
    targets = (ids + 1) % config.vocab_size
    loss = F.cross_entropy(logits.reshape(-1, config.vocab_size), targets.reshape(-1))
    loss.backward()
    missing = [name for name, parameter in model.named_parameters() if parameter.grad is None]
    assert not missing, f"These trainable parameters are disconnected from the loss: {missing}"
    assert all(torch.isfinite(p.grad).all() for p in model.parameters()), "All gradients must be finite."
    # Sampling must crop long prompts and restore the prior train/eval setting.
    prompt = torch.zeros(1, config.context_length + 2, dtype=torch.long)
    generated = model.generate(prompt, max_new_tokens=2)
    assert generated.shape == (1, config.context_length + 4), "Append exactly max_new_tokens IDs."
    assert model.training, "Generation must restore the previous training mode."


CHECKS = {
    "embeddings": ("E01", check_embeddings),
    "attention": ("E02", check_attention),
    "heads": ("E03", check_heads),
    "feedforward": ("E04", check_feedforward),
    "block": ("E05", check_block),
    "model": ("E06", check_model),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=[*CHECKS, "all"], default="all")
    parser.add_argument("--implementation", choices=["student", "reference"], default="student")
    args = parser.parse_args(argv)
    torch.set_num_threads(1)
    torch.manual_seed(42)
    implementation = importlib.import_module(f"transformer_lab.{args.implementation}")
    selected = list(CHECKS) if args.stage == "all" else [args.stage]
    failures = 0
    for stage in selected:
        exercise, check = CHECKS[stage]
        try:
            check(implementation)
        except NotImplementedError as error:
            failures += 1
            print(f"TODO {exercise} {stage}: {error}")
        except Exception as error:
            failures += 1
            print(f"FAIL {exercise} {stage}: {type(error).__name__}: {error}")
        else:
            print(f"PASS {exercise} {stage}")
    if failures:
        print(f"\n{failures} checkpoint(s) need work in {args.implementation}.py.")
        return 1
    print(f"\nAll {len(selected)} selected checkpoint(s) passed ({args.implementation}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
