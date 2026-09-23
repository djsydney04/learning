# 9. Teach the model to predict the next character

Before this lesson: [the transformer block](08-block.md). Finish E06, then implement E07–E10 in [student_training.py](../transformer_lab/student_training.py). This lesson connects the architecture to a learning problem.

## Turn text into many prediction tasks

Suppose the text is `cats!`. For a context length of four, take five characters, then make two overlapping slices:

```text
position       0     1     2     3
input x        c     a     t     s
target y       a     t     s     !
available      c     ca    cat   cats
context
```

At position 0, the model sees `c` and predicts `a`. At position 2, it sees `cat` and predicts `s`. We can compute all four predictions in one forward pass because the mask enforces the context rule. The correct earlier characters are supplied during training; the model's sampled predictions are not fed back into this training window. This is often called **teacher forcing**.

During generation, future correct characters are unavailable. The model must feed back its own choices. That is why a model can have a decreasing training loss while still producing awkward text when its earlier guesses lead to unfamiliar contexts.

The raw text is split before sampling windows: first 90% for training, last 10% for validation. Training updates use only the training portion. This avoids overlapping sampled windows that straddle the boundary. The vocabulary uses the whole file's alphabet, a deliberately simple convention explained in [the data note](../data/README.md).

## E07: implement the shifted slices

Your function receives a tensor `windows` of shape `[B,T+1]`. Return two tensors of shape `[B,T]`: all but the last position for X, and all but the first for Y. You are shifting along the sequence axis, not the batch axis.

```sh
python -m transformer_lab.check_training --stage data
```

The production batch sampler also chooses random start positions; this exercise isolates the shift so you can inspect it without randomness. The sampler is supplied in [data.py](../transformer_lab/data.py). After completing the course, rebuild that sampler using your `shifted_targets` helper.

## E08: compare predictions with labels

For `B=2`, `T=4`, and a vocabulary of `V=5`, the model returns `[2,4,5]`: five next-character scores at each of eight prediction positions. Targets have shape `[2,4]` and contain integer IDs, not five-element probability vectors.

```text
                         one position
logits                  [1.0, -0.5, 2.0, 0.0, 0.5]
softmax probabilities   [ ... five positive values summing to 1 ... ]
correct label            2
loss                    -log(probability assigned to label 2)
```

The natural logarithm makes a confident wrong answer expensive. Giving the correct token probability 0.5 yields loss about 0.693; probability 0.1 yields about 2.303. Lower is better. With V equally likely choices, loss is `ln(V)`.

PyTorch's cross-entropy accepts logits and computes the necessary log-softmax internally. **Do not apply softmax to the logits first.** Flatten B and T while keeping vocabulary as the class axis:

```python
import math
import torch
from torch.nn import functional as F

logits = torch.zeros(2, 4, 5, requires_grad=True)
targets = torch.tensor([[0, 1, 2, 3], [4, 0, 1, 2]], dtype=torch.long)
loss = F.cross_entropy(logits.reshape(-1, 5), targets.reshape(-1))
print(loss.item())  # about 1.609438, or ln(5)
assert abs(loss.item() - math.log(5)) < 1e-6
loss.backward()
print(logits.grad.shape)  # [2,4,5]
```

`reshape(-1, V)` asks PyTorch to infer the first dimension, here `B*T`. Targets must be `torch.long`. Return the **loss tensor**, not `loss.item()`, from E08: converting to a Python number would disconnect the calculation from autograd before backward.

```sh
python -m transformer_lab.check_training --stage loss
```

These input conventions follow [PyTorch's CrossEntropyLoss documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html).

## E09: one training step

![Training predicts scores, measures error, computes gradients, and updates model parameters.](../assets/03-training-loop.png)

The input character IDs stay fixed. Training changes embeddings, projections, FFN weights and biases, and normalization scales/offsets.

The training helper receives a model, an optimizer, X, and Y. Implement these operations in order:

1. `optimizer.zero_grad(set_to_none=True)` clears gradients left from the previous step. PyTorch normally accumulates gradients.
2. `model(x)` runs the forward computation and builds the computation graph.
3. Your E08 computes one mean cross-entropy loss from logits and Y.
4. `loss.backward()` computes gradients of that loss with respect to learned parameters. It does **not** update their values.
5. `optimizer.step()` changes parameters using those gradients.
6. Return `loss.item()` for logging. This number describes the loss computed **before** the update.

```sh
python -m transformer_lab.check_training --stage train
```

An **optimizer** implements a parameter update rule. The first learning lab used SGD: subtract the learning rate times the gradient. The transformer trainer uses AdamW, which maintains running gradient statistics and applies weight decay. You can treat its internal rule as supplied for now; you still implement when gradients are cleared, calculated, and applied.

The **learning rate** controls update size. Too high can cause unstable or nonfinite loss; too low can make learning very slow. More steps are not a substitute for fixing an incorrect causal mask or shifted target.

## Measure learning fairly

Training loss asks how well the model predicts the data it learns from. Validation loss asks how well it predicts held-out text from this small corpus. If training loss falls while validation loss rises, the model may be fitting training details that do not generalize: **overfitting**.

Our trainer evaluates a fixed set of sampled train and validation windows at step 0, every 50 updates, and the final update. Fixed windows make the curve easier to compare. Separate random generators choose training and evaluation windows so adding an evaluation does not change which training batches follow. These measurements are sample estimates, not exact averages over every possible text window.

Evaluation needs two distinct controls:

```python
model.eval()             # dropout becomes inactive
with torch.no_grad():    # do not build a gradient graph
    logits = model(x)
model.train()            # resume training behavior afterward
```

This is a context snippet: `model` and `x` come from the trainer. `eval()` alone does not disable autograd; `no_grad()` alone does not disable dropout. The supplied evaluation helper restores the mode it found, including when called on an already-evaluating model.

**Perplexity** is `exp(mean cross-entropy)` when loss uses natural logs. It is another way to express predictive uncertainty: a uniform distribution over V characters has perplexity V. Compare perplexities only for the same tokenization and task. You can skip this metric on your first pass and use loss.

## E10: choose a next token

For generation we use the logits at the **last** position. For one sequence, that is the model's distribution for the token after the entire supplied prefix.

```text
prompt → model → logits at last position → softmax → sample an ID
  ↑                                                       │
  └──────────────── append the new character ──────────────┘
```

Your E10 receives `[B,V]` logits. Divide them by a positive **temperature**, softmax over V, and use `torch.multinomial(..., num_samples=1, generator=generator)` to return `[B,1]` IDs. The supplied generator makes an experiment repeatable; pass it through to the sampler.

Lower temperature, such as 0.5, makes the distribution more concentrated. Higher temperature, such as 1.5, makes it flatter. Temperature changes sampling, not trained weights. Setting it to zero would divide by zero, so this project rejects nonpositive temperatures. To try greedy decoding, use `argmax` as a separate experiment rather than temperature zero.

```sh
python -m transformer_lab.check_training --stage sample
```

The full generation loop in `student.py` is supplied. It crops to the most recent `context_length` characters before each forward call, resets learned positions to zero within that window, appends one sampled ID, and repeats. The returned sequence includes the original prompt. It uses evaluation/no-grad and restores the previous model mode. This simple version recomputes the whole context each step; it has no key/value cache.

E10 isolates sampling so you can implement the operation yourself. After it passes, replace the supplied loop's sampling lines with your helper, then rebuild the entire loop from the description above.

## First real run

The complete commands and experiments are in [the final project](10-project.md). For a working reference baseline while learning:

```sh
python -m transformer_lab.train --implementation reference --steps 300
```

The run saves `artifacts/reference/model.pt`, `metrics.csv`, and `loss.png`. A checkpoint stores the config, exact character-to-ID order, and learned state so a new process can reconstruct the same model. This is an inference checkpoint; it does not save AdamW's optimizer state for exact training continuation.

Below is a recorded run from this project, not a promised result for every machine or dataset. Exact settings and measurements are in [the run notes](../examples/RESULTS.md).

![Recorded training and validation loss across a 300-step CPU run of the reference transformer.](../examples/loss.png)

Checkpoint: explain why the first position predicts the *second* character, why loss needs logits, what backward changes, and why generation feeds back its own choices.

Next: [build your transformer](10-project.md).
