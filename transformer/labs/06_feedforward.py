"""Run: python -m labs.06_feedforward

Experiment: replace nn.ReLU() with nn.Identity(). Predict the output.
The absolute-value assertion should then fail: two linear maps alone cancel
for these particular weights. Restore ReLU after the experiment.
"""

import torch
from torch import nn


class FeedForward(nn.Module):
    def __init__(self):
        super().__init__()
        self.expand = nn.Linear(2, 4, bias=False)
        # ReLU is used for exact hand arithmetic. The project can use GELU;
        # both keep the same per-position shape and independence properties.
        self.activation = nn.ReLU()
        self.project = nn.Linear(4, 2, bias=False)
        with torch.no_grad():
            self.expand.weight.copy_(torch.tensor([[1., 0.], [0., 1.], [-1., 0.], [0., -1.]]))
            self.project.weight.copy_(torch.tensor([[1., 0., 1., 0.], [0., 1., 0., 1.]]))

    def forward(self, x):
        return self.project(self.activation(self.expand(x)))


def main():
    torch.set_printoptions(precision=1, sci_mode=False)
    x = torch.tensor([[[2.0, -3.0], [2.0, -3.0], [-4.0, 1.0]]])
    model = FeedForward()
    expanded = model.expand(x)
    activated = model.activation(expanded)
    output = model(x)
    print("input [B=1, T=3, C=2]:\n", x)
    print("expanded [1, 3, 4]:\n", expanded.detach())
    print("after ReLU:\n", activated.detach())
    print("projected back [1, 3, 2]:\n", output.detach())
    assert torch.equal(output, x.abs())
    assert torch.equal(output[:, 0], output[:, 1])

    changed_x = x.clone()
    changed_x[:, -1] += 100
    changed_output = model(changed_x)
    assert torch.equal(output[:, :2], changed_output[:, :2])
    print("changing token 2 changes token 0?", not torch.equal(output[:, 0], changed_output[:, 0]))
    print("trainable parameters:", sum(parameter.numel() for parameter in model.parameters()))
    assert sum(parameter.numel() for parameter in model.parameters()) == 16
    print("All feed-forward checks passed.")


if __name__ == "__main__":
    main()
