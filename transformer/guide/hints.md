# Hints: reveal only the step you need

Return to [the project](10-project.md). Try writing each expected shape before reading its hint. The final answers live in `reference.py` and `reference_training.py`; these hints stop short of reproducing every function.

## E01 · Embeddings

<details>
<summary>First hint</summary>

IDs are table indices. The token table produces `[B,T,C]`; positions `0..T-1` index the position table and produce `[T,C]`. Addition broadcasts the latter across B. You do not concatenate these tables.

</details>

<details>
<summary>More direct hint</summary>

Create positions with `torch.arange(ids.shape[1], device=ids.device)`. Use the two supplied embedding modules as functions, add their outputs, and pass the sum to the supplied dropout. Preserve the validation of input sequence length.

</details>

## E02 · Scaled attention

<details>
<summary>First hint</summary>

The weight matrix needs one row per query and one column per key. Transpose the last two axes of K, not all axes. Scale by the square root of the query/key feature width. Causality forbids column index greater than row index.

</details>

<details>
<summary>More direct hint</summary>

Make an upper-triangular boolean matrix with `triu(diagonal=1)`: `True` then means forbidden. `masked_fill(forbidden, -inf)` happens before `softmax(..., dim=-1)`. Multiply the weights by V. For the first row of causal self-attention, the result must equal the first value vector.

</details>

## E03 · Heads

<details>
<summary>Hint</summary>

Each projection begins `[B,T,C]`. Reshape it to `[B,T,H,D]`, then transpose axes 1 and 2. After attention, reverse that transpose before joining H and D. This is a grouping operation, so test numbered values as well as shapes. The final learned output projection mixes head features.

</details>

## E04 · Feed-forward

<details>
<summary>Hint</summary>

`self.net` is already a callable neural network. Apply it to X. Explain why `nn.Linear` preserves the B and T axes. The second pass asks you to reconstruct the supplied layers too.

</details>

## E05 · Block

<details>
<summary>Hint</summary>

There are two additions. First update X using attention on its normalized features. Then update that new X using the FFN on its normalized features. Normalize inside each branch, preserving the bypass input.

</details>

## E06 · Whole model

<details>
<summary>Hint</summary>

Embed IDs. Loop over the supplied blocks in order, replacing X with each result. Normalize once more and apply `lm_head`. Return logits with shape `[B,T,V]`. No softmax belongs in this forward method.

</details>

## E07 · Shifted targets

<details>
<summary>Hint</summary>

For a row `[a,b,c,d]`, X is `[a,b,c]` and Y is `[b,c,d]`. Preserve every batch row with `:` on the first axis; slice the second axis with `:-1` and `1:`.

</details>

## E08 · Loss

<details>
<summary>Hint</summary>

Vocabulary width is `logits.shape[-1]`. Reshape logits to `[B*T,V]` and labels to `[B*T]`; call `F.cross_entropy` with those tensors. Return a scalar tensor that still has a gradient graph. Uniform logits give loss `ln(V)`.

</details>

## E09 · Update

<details>
<summary>Hint</summary>

Clear old gradients first. Call the model, then your loss function. Backward computes gradients; the optimizer applies them. Only convert loss to a Python float after you have used its backward graph. The trainer supplies training mode; this helper should not silently change it to evaluation.

</details>

## E10 · Sampling

<details>
<summary>Hint</summary>

Softmax the temperature-scaled logits over the last axis. Use `torch.multinomial` to draw one ID per batch row and preserve `[B,1]` shape. Pass through the supplied generator. `argmax` is a different decoding rule and will fail the intent of the sampling exercise.

</details>

If a hint still feels mysterious, return to the numbered example in the relevant lesson. Debug a single tensor before debugging the entire training loop.
