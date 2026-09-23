"""Complete versions of the four training-mechanics exercises."""

import math

import torch
from torch.nn import functional as F


def shifted_targets(windows: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """E07: a [B,T+1] window supplies T inputs and their T next-token targets."""
    if windows.ndim != 2 or windows.shape[1] < 2 or windows.dtype != torch.long:
        raise ValueError("windows must be a torch.long tensor [B,T+1] with at least two positions")
    return windows[:, :-1], windows[:, 1:]


def language_model_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """E08: one scalar cross entropy for all B*T next-character predictions."""
    if logits.ndim != 3 or targets.shape != logits.shape[:2]:
        raise ValueError("Expected logits [B,T,V] and targets [B,T]")
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))


def train_step(model, optimizer, x: torch.Tensor, y: torch.Tensor) -> float:
    """E09: clear gradients, predict, measure, differentiate, update."""
    model.train()
    optimizer.zero_grad(set_to_none=True)
    logits = model(x)
    loss = language_model_loss(logits, y)
    if not torch.isfinite(loss):
        raise ValueError("Training loss became nonfinite; try a smaller learning rate")
    loss.backward()
    optimizer.step()
    return loss.item()


def sample_next(
    logits: torch.Tensor,
    temperature: float,
    generator: torch.Generator | None = None,
) -> torch.Tensor:
    """E10: convert [B,V] last-position scores into one sampled ID per batch."""
    if logits.ndim != 2 or logits.shape[1] == 0:
        raise ValueError("logits must have shape [B,V] with a nonempty vocabulary")
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be positive and finite")
    probabilities = torch.softmax(logits / temperature, dim=-1)
    return torch.multinomial(probabilities, num_samples=1, generator=generator)
