"""Text becomes integer IDs; shifted windows become prediction exercises."""

from collections.abc import Iterable, Sequence

import torch


class CharacterTokenizer:
    """One ID per distinct character, including spaces and newlines.

    This tokenizer has no special tokens. It is intentionally much simpler than
    the subword tokenizers used by most large language models.
    """

    def __init__(self, text: str):
        if not text:
            raise ValueError("Build the tokenizer from nonempty text")
        self._set_chars(sorted(set(text)))

    def _set_chars(self, chars: Sequence[str]) -> None:
        if not chars or any(not isinstance(char, str) or len(char) != 1 for char in chars):
            raise ValueError("chars must contain one-character strings")
        if len(set(chars)) != len(chars):
            raise ValueError("chars must not contain duplicates")
        self.chars = list(chars)
        self.stoi = {char: index for index, char in enumerate(self.chars)}

    @classmethod
    def from_chars(cls, chars: Sequence[str]) -> "CharacterTokenizer":
        """Restore the saved vocabulary in its original order, without sorting."""
        tokenizer = cls.__new__(cls)
        tokenizer._set_chars(chars)
        return tokenizer

    @property
    def vocab_size(self) -> int:
        return len(self.chars)

    def __len__(self) -> int:
        return self.vocab_size

    def encode(self, text: str) -> list[int]:
        try:
            return [self.stoi[char] for char in text]
        except KeyError as error:
            raise ValueError(f"Character {error.args[0]!r} is not in this tokenizer's vocabulary") from None

    def decode(self, ids: Iterable[int]) -> str:
        characters = []
        for token_id in ids:
            index = int(token_id)
            if not 0 <= index < len(self.chars):
                raise ValueError(f"Token ID {index} is outside the vocabulary")
            characters.append(self.chars[index])
        return "".join(characters)


def split_data(text: str, train_fraction: float = 0.9) -> tuple[str, str]:
    """Keep a contiguous ending for validation; split before sampling windows."""
    if not 0.0 < train_fraction < 1.0:
        raise ValueError("train_fraction must be between 0 and 1")
    cut = int(len(text) * train_fraction)
    if cut == 0 or cut == len(text):
        raise ValueError("Text must be long enough for two nonempty splits")
    return text[:cut], text[cut:]


def make_batch(
    data: torch.Tensor,
    batch_size: int,
    context_length: int,
    generator: torch.Generator | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Sample windows and the same windows shifted one character to the right.

    For data [0, 1, 2, 3, 4] and a window beginning at zero:
        x = [0, 1, 2]     y = [1, 2, 3]
    Both outputs have shape [batch_size, context_length]. Sampling indices are
    drawn on the CPU, so use a CPU generator even when data lives on an accelerator.
    """
    if data.ndim != 1 or data.dtype != torch.long:
        raise ValueError("data must be a one-dimensional torch.long tensor")
    if batch_size <= 0 or context_length <= 0:
        raise ValueError("batch_size and context_length must be positive")
    if len(data) <= context_length:
        raise ValueError("Each data split needs at least context_length + 1 characters")
    starts = torch.randint(len(data) - context_length, (batch_size,), generator=generator)
    x = torch.stack([data[start : start + context_length] for start in starts.tolist()])
    y = torch.stack([data[start + 1 : start + context_length + 1] for start in starts.tolist()])
    return x, y
