"""Run: python -m labs.05_attention

Experiment: replace ALLOW_FUTURE = False with True. Inspect row zero.
Then change the final value vector from [4, 4] to [400, 400].
Can an earlier position's output change when the mask is present?
"""

import math

import torch

ALLOW_FUTURE = False


def attend(q, k, v, causal=True):
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1])
    if causal:
        allowed = torch.ones(scores.shape[-2:], dtype=torch.bool).tril()
        scores = scores.masked_fill(~allowed, float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    return weights @ v, weights


def main():
    torch.set_printoptions(precision=4, sci_mode=False)
    # Single sequence, single head. The full model adds batch and head axes.
    q = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    k = q.clone()
    v = torch.tensor([[10.0, 0.0], [0.0, 8.0], [4.0, 4.0]])
    output, weights = attend(q, k, v, causal=not ALLOW_FUTURE)
    print("attention weights (row receives, column supplies):\n", weights)
    print("each row sums to:", weights.sum(dim=-1))
    print("weighted value vectors:\n", output)
    assert torch.allclose(weights.sum(dim=-1), torch.ones(3))

    # An ASCII heatmap: a longer bar means a larger attention weight.
    # Its effect on the output also depends on the value vector being weighted.
    for row in range(3):
        for column in range(3):
            weight = weights[row, column].item()
            print(f"receiver {row} <- source {column}: {'#' * round(weight * 20):20s} {weight:.3f}")

    changed_v = v.clone()
    changed_v[-1] += 1000
    changed_output, _ = attend(q, k, changed_v, causal=not ALLOW_FUTURE)
    earlier_unchanged = torch.allclose(output[:2], changed_output[:2])
    print("changing final value leaves earlier outputs unchanged:", earlier_unchanged)
    if not ALLOW_FUTURE:
        assert torch.equal(weights.triu(diagonal=1), torch.zeros_like(weights))
        assert torch.equal(output[0], v[0])
        assert earlier_unchanged
    else:
        assert not earlier_unchanged
    print("All attention checks passed.")


if __name__ == "__main__":
    main()
