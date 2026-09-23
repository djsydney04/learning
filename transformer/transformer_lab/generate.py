"""Sample text from a checkpoint produced by transformer_lab.train."""

import argparse
from pathlib import Path

import torch

from .runtime import IMPLEMENTATIONS, load_checkpoint, setup_cpu


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--prompt", default="the ")
    parser.add_argument("--new-tokens", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--implementation", choices=IMPLEMENTATIONS, default=None, help="Default: the implementation recorded in the checkpoint")
    args = parser.parse_args(argv)
    try:
        setup_cpu(args.seed)
        model, tokenizer, _ = load_checkpoint(args.checkpoint, args.implementation)
        if not args.prompt:
            raise ValueError("--prompt must contain at least one character")
        ids = torch.tensor([tokenizer.encode(args.prompt)], dtype=torch.long)
        generated = model.generate(ids, max_new_tokens=args.new_tokens, temperature=args.temperature)
        print(tokenizer.decode(generated[0].tolist()))
    except NotImplementedError as error:
        print(f"Complete the student forward passes before generating: {error}")
        return 1
    except (ValueError, OSError, RuntimeError) as error:
        print(f"Could not generate text: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
