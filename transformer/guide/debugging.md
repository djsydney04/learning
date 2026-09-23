# Debug by asking which assumption failed

Start with the last error line, then find the referenced line in your own code. In this project, most early mistakes concern an axis, an operation's order, or which Python environment is running.

| Symptom | Likely cause | First useful action |
|---|---|---|
| `No module named torch` | Wrong environment or dependencies not installed. | Activate `.venv`; run `python -c "import sys; print(sys.executable)"`. |
| No compatible Torch wheel | Python version or machine architecture mismatch. | Use the Python 3.12 environment described in [setup](00-start.md); check `platform.machine()`. |
| `No module named transformer_lab` | Command run outside the project root. | Check `pwd`; use `python -m transformer_lab...` from this folder. |
| `NotImplementedError: E...` | A student exercise is unfinished. | Implement that milestone or explicitly select `--implementation reference` for a demo. |
| Matrix multiplication shape error | Contracted dimensions do not agree. | Print Q/K shapes; check K's last-two-axis transpose. |
| Right shape but wrong numbers | Reshape grouped positions and heads incorrectly. | Track `torch.arange(...)` values through split and merge. |
| Embedding wants Long/Int indices | Token IDs became floating point. | Use `torch.tensor(ids, dtype=torch.long)`. |
| Embedding index out of range | ID outside vocabulary or position outside context. | Print ID min/max and T; compare config limits. |
| `view` incompatible with strides | A transpose changed memory layout. | Use `reshape`, or make a contiguous copy before `view`. |
| Attention rows do not sum to one | Wrong softmax axis or masking afterward. | Sum over `dim=-1`; mask scores before softmax. |
| Earlier outputs change after future input changes | Causality broken. | Check mask orientation, head merge, and no normalization over time. |
| All attention values are NaN | A row may be fully masked. | Keep the diagonal allowed and inspect scores before softmax. |
| Model never improves | No gradients, no update, or learning/data bug. | Check loss requires grad, then parameter gradients and update order. |
| Loss has no `backward` | Converted to a Python number too early. | Return loss tensor from E08; use `.item()` only for reporting. |
| Loss explodes | Learning rate too high or accumulating old gradients. | Restore defaults; check zero_grad and finite inputs. |
| Cross-entropy target mismatch | Wrong class axis or shifted label shape. | Flatten logits to `[B*T,V]` and labels to `[B*T]`. |
| Good training loss, poor validation | Possible overfitting or train/validation mismatch. | Inspect the corpus and both curves; try less capacity or dropout. |
| Prompt character not in vocabulary | Often uppercase text in a lowercase corpus. | Start with `the `; inspect the saved tokenizer's characters. |
| Checkpoint parameter names do not match | Changed constructors or architecture. | Use the matching code/config; retrain after incompatible edits. |
| `.png` is not shown in Markdown | Viewing raw Markdown or wrong relative path. | Open Markdown preview; images resolve relative to the `.md` file. |

## A reliable inspection pattern

Inside a forward method, temporarily print shapes and a small slice:

```python
print("x:", x.shape, x.dtype, x.device)
print("first position:", x[0, 0])
```

These lines assume X exists in the current function. Print a few values, not the entire model. In attention, inspect one batch/head pair with `weights[0,0]`. Use `torch.testing.assert_close` for floating-point results; exact equality is often inappropriate after arithmetic.

Use the smallest example that can expose the mistake: one sequence, three positions, and two features is enough to diagnose many attention errors. Re-run the relevant stage after each change. When it passes, run the full student checks to catch downstream effects.

## Read the failure as evidence

A shape check establishes dimensions. A numerical check establishes agreement for particular inputs. A causality check establishes a behavior under a perturbation. A learning test establishes that parameters can move in a useful direction on that task. No one test proves everything; together they give much better evidence than “the code ran.”
