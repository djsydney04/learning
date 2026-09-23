"""Run: python -m labs.03_learning

Experiment 1: change LEARNING_RATE to 0.01; compare convergence after 80 steps.
Experiment 2: change it to 0.6; the slope diverges for this particular dataset.
The final accuracy assertion is expected to fail for some experiments.
"""

import torch
from torch import nn

LEARNING_RATE = 0.1
STEPS = 80


class Line(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)


def main():
    # A derivative is a local slope: here PyTorch computes d(loss)/d(w).
    w = torch.tensor(0.0, requires_grad=True)
    prediction = w * 2
    loss = (prediction - 6) ** 2
    loss.backward()
    print("one example: loss =", loss.item(), "gradient =", w.grad.item())
    assert w.grad.item() == -24.0
    with torch.no_grad():
        w -= 0.1 * w.grad
    print(f"one manual update: w = {w.item():.1f}")

    # Learn y = 2*x + 1 from five examples, starting from w=b=0.
    x = torch.tensor([[-2.0], [-1.0], [0.0], [1.0], [2.0]])
    targets = 2 * x + 1
    model = Line()
    with torch.no_grad():
        model.linear.weight.zero_()
        model.linear.bias.zero_()
    optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)
    model.train()
    for step in range(STEPS):
        optimizer.zero_grad(set_to_none=True)
        predictions = model(x)
        loss = ((predictions - targets) ** 2).mean()
        loss.backward()
        optimizer.step()
        if step in (0, 1, 9, STEPS - 1):
            print(f"step {step:2d}: loss before update = {loss.item():.6f}")

    # eval changes the mode of layers such as dropout; no_grad stops recording
    # operations for backward. This simple model has no mode-dependent layers.
    model.eval()
    with torch.no_grad():
        final_loss = ((model(x) - targets) ** 2).mean().item()
        answer = model(torch.tensor([[3.0]])).item()
    print(f"learned weight = {model.linear.weight.item():.4f}")
    print(f"learned bias = {model.linear.bias.item():.4f}")
    print(f"prediction for x=3: {answer:.4f}")
    print("ReLU([-2, 0, 2]):", torch.relu(torch.tensor([-2.0, 0.0, 2.0])).tolist())
    assert final_loss < 1e-8, "Try the default learning rate and step count."
    assert abs(answer - 7.0) < 1e-3
    print("All learning checks passed.")


if __name__ == "__main__":
    main()
