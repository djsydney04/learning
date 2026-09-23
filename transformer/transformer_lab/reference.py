"""Complete implementation. Try each student exercise before reading its answer.

Shape vocabulary: B=batch, T=positions, C=d_model, H=heads, D=C/H, V=vocabulary.
Every attention score, head reshape, residual, and prediction is explicit here.
"""

import math

import torch
from torch import nn

from .config import TransformerConfig


def scaled_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    causal: bool = True,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Mix value vectors using query/key similarity.

    q: [..., T, D]; k: [..., S, D]; v: [..., S, Dv].
    Returns (mixed values [..., T, Dv], attention weights [..., T, S]).
    Leading dimensions may include batch and head axes. A causal mask treats
    query and key positions as starting at zero (this is not a cached decoder).
    """
    # transpose only the last two axes: each query needs a score for every key.
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1])
    if causal:
        future = torch.ones(
            q.shape[-2], k.shape[-2], dtype=torch.bool, device=q.device
        ).triu(diagonal=1)
        scores = scores.masked_fill(future, float("-inf"))
    # Each query's row is a distribution over the available key positions.
    weights = torch.softmax(scores, dim=-1)
    return weights @ v, weights


class TokenPositionEmbedding(nn.Module):
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.context_length = config.context_length
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.position_embedding = nn.Embedding(config.context_length, config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        if ids.ndim != 2 or not 1 <= ids.shape[1] <= self.context_length:
            raise ValueError("ids must have shape [B, T] with 1 <= T <= context_length")
        positions = torch.arange(ids.shape[1], device=ids.device)
        # [B,T,C] + [T,C]: PyTorch broadcasts positions across the batch.
        return self.dropout(self.token_embedding(ids) + self.position_embedding(positions))


class MultiHeadAttention(nn.Module):
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.n_heads = config.n_heads
        self.head_dim = config.d_model // config.n_heads
        self.q_proj = nn.Linear(config.d_model, config.d_model)
        self.k_proj = nn.Linear(config.d_model, config.d_model)
        self.v_proj = nn.Linear(config.d_model, config.d_model)
        self.out_proj = nn.Linear(config.d_model, config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor, return_weights: bool = False):
        batch, length, width = x.shape
        # Linear projections learn a different view of x for each purpose.
        # [B,T,C] -> [B,T,H,D] -> [B,H,T,D]
        q = self.q_proj(x).reshape(batch, length, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).reshape(batch, length, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).reshape(batch, length, self.n_heads, self.head_dim).transpose(1, 2)
        mixed, weights = scaled_attention(q, k, v, causal=True)
        # Restore positions before joining heads: [B,H,T,D] -> [B,T,H,D] -> [B,T,C].
        mixed = mixed.transpose(1, 2).contiguous().reshape(batch, length, width)
        output = self.dropout(self.out_proj(mixed))
        return (output, weights) if return_weights else output


class FeedForward(nn.Module):
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.d_model, config.d_ff),
            nn.GELU(),
            nn.Linear(config.d_ff, config.d_model),
            nn.Dropout(config.dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Linear operates on the last dimension; positions do not mix here.
        return self.net(x)


class TransformerBlock(nn.Module):
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.norm1 = nn.LayerNorm(config.d_model)
        self.attention = MultiHeadAttention(config)
        self.norm2 = nn.LayerNorm(config.d_model)
        self.feed_forward = FeedForward(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pre-norm: normalize the input to each branch, then add its result.
        x = x + self.attention(self.norm1(x))
        x = x + self.feed_forward(self.norm2(x))
        return x


class TinyTransformer(nn.Module):
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.config = config
        self.embedding = TokenPositionEmbedding(config)
        self.blocks = nn.ModuleList([TransformerBlock(config) for _ in range(config.n_layers)])
        self.final_norm = nn.LayerNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        x = self.embedding(ids)
        for block in self.blocks:
            x = block(x)
        # Raw logits, not probabilities: cross_entropy applies log-softmax.
        return self.lm_head(self.final_norm(x))

    @torch.no_grad()
    def generate(
        self, ids: torch.Tensor, max_new_tokens: int = 80, temperature: float = 1.0
    ) -> torch.Tensor:
        """Append sampled characters. Only the most recent context enters the model.

        Cropped windows restart learned position indices at zero. This simple
        teaching decoder recomputes all attention each step, without a KV cache.
        """
        if ids.ndim != 2 or ids.shape[1] == 0:
            raise ValueError("Provide a nonempty prompt with shape [B, T]")
        if not isinstance(max_new_tokens, int) or max_new_tokens < 0:
            raise ValueError("max_new_tokens must be a nonnegative integer")
        if not math.isfinite(temperature) or temperature <= 0:
            raise ValueError("temperature must be positive and finite")
        was_training = self.training
        self.eval()
        try:
            for _ in range(max_new_tokens):
                window = ids[:, -self.config.context_length :]
                next_logits = self(window)[:, -1, :] / temperature
                probabilities = torch.softmax(next_logits, dim=-1)
                next_id = torch.multinomial(probabilities, num_samples=1)
                ids = torch.cat((ids, next_id), dim=1)
        finally:
            self.train(was_training)
        return ids
