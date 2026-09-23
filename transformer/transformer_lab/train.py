"""Train a tiny character-level transformer on a local text file.

The default is YOUR student implementation, including the E08/E09 training
helpers. Use --implementation reference to establish a working baseline first.
"""

import argparse
import csv
import importlib
import math
from pathlib import Path

import torch
from torch.nn import functional as F

from .config import TransformerConfig
from .data import CharacterTokenizer, make_batch, split_data
from .plotting import write_loss_plot
from .runtime import IMPLEMENTATIONS, PROJECT_ROOT, build_model, setup_cpu


def fixed_batches(data, batch_size: int, context_length: int, count: int, seed: int):
    """Materialize repeatable evaluation windows using their own CPU generator."""
    generator = torch.Generator().manual_seed(seed)
    return [make_batch(data, batch_size, context_length, generator) for _ in range(count)]


@torch.no_grad()
def evaluate_loss(model, batches) -> float:
    """Measure without dropout, gradients, or changes to the training RNG stream."""
    if not batches:
        raise ValueError("Evaluation needs at least one batch")
    was_training = model.training
    model.eval()
    total_loss = 0.0
    total_tokens = 0
    try:
        for x, y in batches:
            logits = model(x)
            loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), y.reshape(-1), reduction="sum")
            total_loss += loss.item()
            total_tokens += y.numel()
    finally:
        model.train(was_training)
    return total_loss / total_tokens


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation", choices=IMPLEMENTATIONS, default="student")
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--context-length", type=int, default=32)
    parser.add_argument("--d-model", type=int, default=48)
    parser.add_argument("--n-heads", type=int, default=4)
    parser.add_argument("--n-layers", type=int, default=2)
    parser.add_argument("--d-ff", type=int, default=192)
    parser.add_argument("--dropout", type=float, default=0.0)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--eval-every", type=int, default=50)
    parser.add_argument("--eval-batches", type=int, default=8)
    parser.add_argument("--data", type=Path, default=PROJECT_ROOT / "data" / "tiny_stories.txt")
    parser.add_argument("--out-dir", type=Path, default=None, help="Default: artifacts/<implementation> inside this project")
    return parser


def run_training(args: argparse.Namespace) -> Path:
    if args.steps < 0:
        raise ValueError("--steps must be nonnegative")
    if args.batch_size <= 0 or args.eval_every <= 0 or args.eval_batches <= 0:
        raise ValueError("--batch-size, --eval-every, and --eval-batches must be positive")
    if not math.isfinite(args.lr) or args.lr <= 0:
        raise ValueError("--lr must be positive and finite")
    setup_cpu(args.seed)
    text = args.data.read_text(encoding="utf-8")
    # Alphabet convention: we know all character TYPES, but train on only the
    # first 90% of the text. This avoids an unknown-character mechanism here.
    tokenizer = CharacterTokenizer(text)
    train_text, valid_text = split_data(text)
    config = TransformerConfig(
        vocab_size=tokenizer.vocab_size,
        context_length=args.context_length,
        d_model=args.d_model,
        n_heads=args.n_heads,
        n_layers=args.n_layers,
        d_ff=args.d_ff,
        dropout=args.dropout,
    )
    if min(len(train_text), len(valid_text)) <= config.context_length:
        raise ValueError("Each 90/10 text split needs at least context_length + 1 characters; use more text or a shorter context")
    train_data = torch.tensor(tokenizer.encode(train_text), dtype=torch.long)
    valid_data = torch.tensor(tokenizer.encode(valid_text), dtype=torch.long)
    evaluation = {
        "train_loss": fixed_batches(train_data, args.batch_size, config.context_length, args.eval_batches, args.seed + 1),
        "val_loss": fixed_batches(valid_data, args.batch_size, config.context_length, args.eval_batches, args.seed + 2),
    }
    training_generator = torch.Generator().manual_seed(args.seed + 3)
    model = build_model(config, args.implementation)
    training = importlib.import_module(f"transformer_lab.{args.implementation}_training")
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    model.train()
    metrics = []

    def record(step: int) -> None:
        row = {"step": step, **{name: evaluate_loss(model, batches) for name, batches in evaluation.items()}}
        if not all(math.isfinite(row[name]) for name in ("train_loss", "val_loss")):
            raise ValueError("Loss became nonfinite; try a smaller learning rate")
        metrics.append(row)
        print(f"step {step:4d} | train loss {row['train_loss']:.4f} | validation loss {row['val_loss']:.4f}")

    # This preflight is before any output files: fresh student TODOs stop cleanly.
    record(0)
    print(f"CPU | {sum(parameter.numel() for parameter in model.parameters()):,} parameters | {tokenizer.vocab_size} characters")
    print("Alphabet from the whole file; text split 90/10 before sampling. Evaluation windows stay fixed.")
    for step in range(1, args.steps + 1):
        x, y = make_batch(train_data, args.batch_size, config.context_length, training_generator)

        # YOUR E09 performs zero_grad -> forward -> E08 loss -> backward -> step.
        loss = training.train_step(model, optimizer, x, y)
        if not math.isfinite(loss):
            raise ValueError("Training loss became nonfinite; try a smaller learning rate")

        if step % args.eval_every == 0 or step == args.steps:
            record(step)

    output_dir = args.out_dir if args.out_dir is not None else PROJECT_ROOT / "artifacts" / args.implementation
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_dir / "model.pt"
    torch.save(
        {
            "format_version": 1,
            "implementation": args.implementation,
            "config": config.to_dict(),
            "chars": tokenizer.chars,
            "state_dict": model.state_dict(),
            "step": args.steps,
            "seed": args.seed,
            "data_name": args.data.name,
        },
        checkpoint_path,
    )
    with (output_dir / "metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["step", "train_loss", "val_loss"])
        writer.writeheader()
        writer.writerows(metrics)
    write_loss_plot(metrics, output_dir / "loss.png")
    print(f"Saved {checkpoint_path}")
    print(f"Recorded measurements: {output_dir / 'metrics.csv'}")
    print(f"Loss plot: {output_dir / 'loss.png'}")
    return checkpoint_path


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    try:
        run_training(args)
    except NotImplementedError as error:
        print(f"Student work remains: {error}")
        print("Complete the model in transformer_lab/student.py and E08/E09 in transformer_lab/student_training.py.")
        print("Run python -m transformer_lab.check --stage all and python -m transformer_lab.check_training --stage all.")
        print("To see a working baseline now, add --implementation reference.")
        return 1
    except (ValueError, OSError) as error:
        print(f"Training could not start or finish: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
