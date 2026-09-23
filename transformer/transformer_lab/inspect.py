"""Export one head's actual first-block attention from a saved model to PNG."""

import argparse
from pathlib import Path

import torch

from .plotting import write_attention_plot
from .runtime import IMPLEMENTATIONS, load_checkpoint, setup_cpu


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--text", default="the cat")
    parser.add_argument("--head", type=int, default=0)
    parser.add_argument("--output", type=Path, default=None, help="Default: attention.png beside the checkpoint; .svg is also supported")
    parser.add_argument("--implementation", choices=IMPLEMENTATIONS, default=None)
    args = parser.parse_args(argv)
    try:
        setup_cpu(1337)
        model, tokenizer, _ = load_checkpoint(args.checkpoint, args.implementation)
        if not 1 <= len(args.text) <= model.config.context_length:
            raise ValueError(f"--text must contain 1 to {model.config.context_length} characters")
        if not 0 <= args.head < model.config.n_heads:
            raise ValueError(f"--head must be between 0 and {model.config.n_heads - 1}")
        ids = torch.tensor([tokenizer.encode(args.text)], dtype=torch.long)
        with torch.no_grad():
            x = model.embedding(ids)
            first_block = model.blocks[0]
            # This is exactly the first attention branch's input during forward.
            _, weights = first_block.attention(first_block.norm1(x), return_weights=True)
        output = args.output if args.output is not None else args.checkpoint.parent / "attention.png"
        write_attention_plot(weights[0, args.head].tolist(), list(args.text), output, head=args.head)
        print(f"Saved {output}")
        print("Rows = query/receiving positions; columns = key/source positions. This is measured first-block attention.")
    except NotImplementedError as error:
        print(f"Complete the student embedding and attention exercises before inspecting: {error}")
        return 1
    except (ValueError, OSError, RuntimeError) as error:
        print(f"Could not inspect attention: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
