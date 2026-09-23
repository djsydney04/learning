"""Your second workbench: data targets, loss, optimization, and sampling.

The trainer calls your train_step (E09), which should call your loss (E08).
E07 and E10 are focused exercises; the supplied batching and generation utilities
already perform those operations so you can study them separately.
"""

import math

import torch
from torch.nn import functional as F


def shifted_targets(windows: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """E07: [B,T+1] -> two [B,T] tensors, offset by one position.

    For [[2, 4, 6, 8]], return x=[[2, 4, 6]], y=[[4, 6, 8]].
    Slice the sequence axis: inputs omit the last item, targets omit the first.
    Check: python -m transformer_lab.check_training --stage data
    """
    if windows.ndim != 2 or windows.shape[1] < 2 or windows.dtype != torch.long:
        raise ValueError("windows must be a torch.long tensor [B,T+1] with at least two positions")
    raise NotImplementedError("E07: create input windows and one-position-shifted targets")


def language_model_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """E08: reduce logits [B,T,V] and integer targets [B,T] to one scalar loss.

    Merge batch and time: logits become [B*T,V], targets become [B*T].
    Use F.cross_entropy on RAW logits. Return the Tensor, not loss.item(),
    because the optimizer still needs its connection to autograd.
    Check: python -m transformer_lab.check_training --stage loss
    """
    if logits.ndim != 3 or targets.shape != logits.shape[:2]:
        raise ValueError("Expected logits [B,T,V] and targets [B,T]")
    raise NotImplementedError("E08: flatten predictions and targets, then calculate cross entropy")


def train_step(model, optimizer, x: torch.Tensor, y: torch.Tensor) -> float:
    """E09: perform exactly one parameter update and return the numeric loss.

    model.train(); clear old gradients with optimizer.zero_grad(set_to_none=True);
    call model(x); call YOUR language_model_loss; call loss.backward();
    call optimizer.step(); return loss.item().
    Check: python -m transformer_lab.check_training --stage train
    """
    raise NotImplementedError("E09: run zero_grad, forward, loss, backward, and optimizer.step")


def sample_next(
    logits: torch.Tensor,
    temperature: float,
    generator: torch.Generator | None = None,
) -> torch.Tensor:
    """E10: last-position logits [B,V] -> one sampled token ID [B,1].

    Divide by temperature; softmax over the vocabulary (dim=-1); then use
    torch.multinomial(..., num_samples=1, generator=generator).
    Lower positive temperature concentrates mass on high-scoring tokens.
    Check: python -m transformer_lab.check_training --stage sample
    """
    if logits.ndim != 2 or logits.shape[1] == 0:
        raise ValueError("logits must have shape [B,V] with a nonempty vocabulary")
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be positive and finite")
    raise NotImplementedError("E10: turn temperature-scaled logits into probabilities and sample")
