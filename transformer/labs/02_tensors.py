"""Run: python -m labs.02_tensors

Experiment: change B, T, C below to 2, 4, 6. Predict every shape first.
Do not change the small dot/matmul examples; their checks are arithmetic checks.
"""

import torch

B, T, C = 2, 3, 4


def main():
    torch.set_printoptions(precision=2, sci_mode=False)
    scalar = torch.tensor(7.0)
    vector = torch.tensor([1.0, 2.0, 3.0])
    matrix = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    print("scalar, vector, matrix shapes:", scalar.shape, vector.shape, matrix.shape)

    other = torch.tensor([4.0, 5.0, 6.0])
    print("elementwise product:", vector * other)
    print("dot product:", (vector @ other).item())
    assert (vector @ other).item() == 32.0

    weights = torch.tensor([[2.0, 0.0, 1.0], [0.0, 3.0, 1.0]])
    projected = matrix @ weights
    print("matrix product [2, 2] @ [2, 3]:\n", projected)
    assert torch.equal(projected, torch.tensor([[2.0, 6.0, 3.0], [6.0, 12.0, 7.0]]))

    x = torch.arange(B * T * C, dtype=torch.float32).reshape(B, T, C)
    bias = torch.arange(C, dtype=torch.float32)
    positions = torch.arange(T, dtype=torch.float32).reshape(T, 1)
    y = x + bias + positions
    print("x [B, T, C]:", tuple(x.shape))
    print("one token x[0, 1]:", x[0, 1])
    print("first token after broadcasts:", y[0, 0])
    assert y.shape == x.shape
    assert torch.equal(y[0, 1], x[0, 1] + bias + 1)

    transposed = x.transpose(1, 2)
    reshaped = x.reshape(B, C, T)
    print("transpose(1, 2):", tuple(transposed.shape))
    print("reshape(B, C, T):", tuple(reshaped.shape))
    # Same shape, different meaning: transpose follows coordinates.
    assert transposed[0, 2, 1] == x[0, 1, 2]
    assert not torch.equal(transposed, reshaped)
    print("same shape means same values?", torch.equal(transposed, reshaped))

    ids = torch.tensor([[0, 1, 2]], dtype=torch.long)
    print("token dtype:", ids.dtype, "feature dtype:", x.dtype)
    print("All tensor checks passed.")


if __name__ == "__main__":
    main()
