"""Your workbench: fill in E01--E06, then train a transformer you understand.

The layer constructors and sampling loop are supplied. Implement the forward
passes yourself. A TODO raises on purpose; this file never imports the answers.
Shape vocabulary: B=batch, T=positions, C=d_model, H=heads, D=C/H, V=vocabulary.
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
    """E02: q [...,T,D], k [...,S,D], v [...,S,Dv] -> (mixed, weights).

    1. Multiply each query by every key; divide by sqrt(D).
    2. If causal, replace scores for key_position > query_position with -inf.
       Construct the mask on q.device. Query/key positions both start at zero.
    3. softmax over KEYS, the last axis: each query's weights must sum to one.
    4. Use those weights to mix values, returning (mixed_values, weights).

    Useful operations: @, transpose(-2, -1), math.sqrt, torch.ones,
    triu(diagonal=1), masked_fill, torch.softmax(..., dim=-1).
    Check: python -m transformer_lab.check --stage attention
    """
    raise NotImplementedError("E02: implement scaled dot-product attention and its causal mask")


class TokenPositionEmbedding(nn.Module):
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.context_length = config.context_length
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.position_embedding = nn.Embedding(config.context_length, config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        """E01: turn IDs [B,T] into vectors [B,T,C].

        Create positions 0..T-1 on ids.device. Look up both embeddings, add
        them (broadcasting positions over batches), then apply self.dropout.
        Check: python -m transformer_lab.check --stage embeddings
        """
        if ids.ndim != 2 or not 1 <= ids.shape[1] <= self.context_length:
            raise ValueError("ids must have shape [B, T] with 1 <= T <= context_length")
        raise NotImplementedError("E01: add token and position embeddings")


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
        """E03: run causal attention in several learned feature subspaces.

        Project x into queries, keys, values using q_proj/k_proj/v_proj.
        For each, reshape [B,T,C] -> [B,T,H,D], then transpose to [B,H,T,D].
        Call YOUR scaled_attention. Transpose its result back to [B,T,H,D]
        BEFORE joining heads into [B,T,C]. Apply out_proj, then dropout.
        Return output, or (output, weights) when return_weights is True.

        weights must have shape [B,H,T,T]. C = H * D.
        Check: python -m transformer_lab.check --stage heads
        """
        batch, length, width = x.shape
        raise NotImplementedError("E03: project, split heads, attend, join heads, project again")


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
        """E04: apply self.net to x. Explain WHY positions do not mix here.

        nn.Linear changes the last dimension; it preserves B and T.
        Trace [B,T,C] -> [B,T,d_ff] -> [B,T,C]. GELU is nonlinear.
        Check: python -m transformer_lab.check --stage feedforward
        """
        raise NotImplementedError("E04: apply the supplied feed-forward network")


class TransformerBlock(nn.Module):
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.norm1 = nn.LayerNorm(config.d_model)
        self.attention = MultiHeadAttention(config)
        self.norm2 = nn.LayerNorm(config.d_model)
        self.feed_forward = FeedForward(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """E05: write two residual updates; each branch normalizes its input.

        First: x + attention(norm1(x)).
        Then use that UPDATED x in: x + feed_forward(norm2(x)).
        Each branch and residual must preserve [B,T,C].
        Check: python -m transformer_lab.check --stage block
        """
        raise NotImplementedError("E05: combine pre-normalization and two residual additions")


class TinyTransformer(nn.Module):
    def __init__(self, config: TransformerConfig):
        super().__init__()
        self.config = config
        self.embedding = TokenPositionEmbedding(config)
        self.blocks = nn.ModuleList([TransformerBlock(config) for _ in range(config.n_layers)])
        self.final_norm = nn.LayerNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        """E06: IDs -> embeddings -> every block -> final_norm -> lm_head.

        Return raw logits [B,T,V], one score per possible NEXT character.
        Do not apply softmax here: the training loss expects logits.
        Check: python -m transformer_lab.check --stage model
        """
        raise NotImplementedError("E06: connect the embeddings, transformer blocks, and language head")

    @torch.no_grad()
    def generate(
        self, ids: torch.Tensor, max_new_tokens: int = 80, temperature: float = 1.0
    ) -> torch.Tensor:
        """Supplied: repeatedly sample the next character from the last position.

        The context is cropped; learned positions restart at zero in each window.
        Follow this code after E06. It recomputes attention without a KV cache.
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
