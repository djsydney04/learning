"""Shared setup and safe loading for this project's own checkpoints."""

import importlib
from pathlib import Path

import torch

from .config import TransformerConfig
from .data import CharacterTokenizer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMPLEMENTATIONS = ("student", "reference")


def setup_cpu(seed: int) -> None:
    """Tiny matrix operations are often faster with one CPU thread."""
    torch.set_num_threads(1)
    torch.manual_seed(seed)


def build_model(config: TransformerConfig, implementation: str):
    if implementation not in IMPLEMENTATIONS:
        raise ValueError("implementation must be 'student' or 'reference'")
    module = importlib.import_module(f"transformer_lab.{implementation}")
    return module.TinyTransformer(config)


def load_checkpoint(path: str | Path, implementation: str | None = None):
    """Load only our tensor-and-primitive format, without arbitrary pickle code.

    Returns (model, tokenizer, checkpoint_metadata). The model starts in eval
    mode. An implementation override lets you test completed student code with
    weights produced by the reference implementation, and vice versa.
    """
    checkpoint = torch.load(Path(path), map_location="cpu", weights_only=True)
    if not isinstance(checkpoint, dict) or checkpoint.get("format_version") != 1:
        raise ValueError("Expected a format_version=1 checkpoint saved by transformer_lab.train")
    required = ("config", "chars", "state_dict", "implementation")
    if any(key not in checkpoint for key in required):
        raise ValueError(f"Checkpoint must contain {', '.join(required)}")
    config = TransformerConfig(**checkpoint["config"])
    tokenizer = CharacterTokenizer.from_chars(checkpoint["chars"])
    if config.vocab_size != tokenizer.vocab_size:
        raise ValueError("Checkpoint vocabulary does not match its model configuration")
    selected = implementation if implementation is not None else checkpoint["implementation"]
    model = build_model(config, selected)
    model.load_state_dict(checkpoint["state_dict"], strict=True)
    model.eval()
    return model, tokenizer, checkpoint
