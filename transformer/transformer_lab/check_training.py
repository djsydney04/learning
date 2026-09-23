"""Behavioral checkpoints for E07--E10, independent of the model exercises."""

import argparse
import importlib
import math

import torch
from torch import nn


def check_data(implementation) -> None:
    windows = torch.tensor([[2, 4, 6, 8], [1, 3, 5, 7]])
    x, y = implementation.shifted_targets(windows)
    torch.testing.assert_close(x, torch.tensor([[2, 4, 6], [1, 3, 5]]))
    torch.testing.assert_close(y, torch.tensor([[4, 6, 8], [3, 5, 7]]))


def check_loss(implementation) -> None:
    logits = torch.zeros(2, 3, 5, requires_grad=True)
    targets = torch.tensor([[0, 1, 2], [3, 4, 0]])
    loss = implementation.language_model_loss(logits, targets)
    assert loss.ndim == 0, "Return one scalar loss Tensor, not a Python number."
    torch.testing.assert_close(loss, torch.tensor(math.log(5)), msg="Five equally likely choices have loss ln(5).")
    loss.backward()
    assert logits.grad is not None and torch.isfinite(logits.grad).all(), "Keep the loss connected to autograd."
    confident = torch.full((2, 3, 5), -4.0)
    confident.scatter_(-1, targets.unsqueeze(-1), 4.0)
    assert implementation.language_model_loss(confident, targets).item() < 0.01, "Confident correct predictions should have low loss."


def check_train(implementation) -> None:
    # A tiny independent classifier keeps this stage separate from E01--E06.
    model = nn.Sequential(nn.Embedding(4, 8), nn.Linear(8, 4))
    optimizer = torch.optim.SGD(model.parameters(), lr=0.3)
    x = torch.tensor([[0, 1, 2, 3]])
    y = torch.tensor([[1, 2, 3, 0]])
    first = implementation.train_step(model, optimizer, x, y)
    assert isinstance(first, float) and math.isfinite(first), "Return loss.item() after the update."
    for _ in range(15):
        last = implementation.train_step(model, optimizer, x, y)
    assert last < first * 0.5, "Repeated optimizer steps should lower loss on this fixed batch."


def check_sample(implementation) -> None:
    # Only token 1 has probability mass, so the result is deterministic.
    logits = torch.tensor([[float("-inf"), 0.0, float("-inf")]]).expand(4, 3)
    sampled = implementation.sample_next(logits, 0.7, torch.Generator().manual_seed(7))
    torch.testing.assert_close(sampled, torch.ones(4, 1, dtype=torch.long))
    uniform = torch.zeros(20, 5)
    first = implementation.sample_next(uniform, 1.0, torch.Generator().manual_seed(19))
    second = implementation.sample_next(uniform, 1.0, torch.Generator().manual_seed(19))
    torch.testing.assert_close(first, second, msg="Pass the supplied generator to torch.multinomial.")
    assert first.shape == (20, 1) and first.dtype == torch.long, "Return one integer ID per batch row."


CHECKS = {
    "data": ("E07", check_data),
    "loss": ("E08", check_loss),
    "train": ("E09", check_train),
    "sample": ("E10", check_sample),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=[*CHECKS, "all"], default="all")
    parser.add_argument("--implementation", choices=["student", "reference"], default="student")
    args = parser.parse_args(argv)
    torch.set_num_threads(1)
    torch.manual_seed(42)
    implementation = importlib.import_module(f"transformer_lab.{args.implementation}_training")
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
    print(f"\n{len(selected) - failures}/{len(selected)} selected training checkpoints passed ({args.implementation}).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
