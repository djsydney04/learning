"""The few dimensions needed by our character-level transformer."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TransformerConfig:
    vocab_size: int
    context_length: int = 32
    d_model: int = 48
    n_heads: int = 4
    n_layers: int = 2
    d_ff: int = 192
    dropout: float = 0.0

    def __post_init__(self) -> None:
        for name in ("vocab_size", "context_length", "d_model", "n_heads", "n_layers", "d_ff"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"{name} must be a positive integer; got {value!r}")
        if self.d_model % self.n_heads:
            raise ValueError("d_model must divide evenly into n_heads")
        if not 0.0 <= self.dropout < 1.0:
            raise ValueError("dropout must be at least 0 and less than 1")

    def to_dict(self) -> dict:
        """Plain values suitable for saving alongside model weights."""
        return asdict(self)
