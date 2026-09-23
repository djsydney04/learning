# 10. Build your transformer

Your goal: train a tiny character-level language model whose tensor operations you can explain. You will implement ten small milestones, then run the complete system and investigate its behavior. The guide remains Markdown, with embedded PNG diagrams; Python files are the project you edit and execute.

## What is supplied, and what you implement

Open [student.py](../transformer_lab/student.py) and [student_training.py](../transformer_lab/student_training.py). The constructors and command-line plumbing are supplied so your first pass can focus on the calculations. Every unfinished operation raises an explicit `NotImplementedError`; it never silently uses the reference answer.

The complete versions are [reference.py](../transformer_lab/reference.py) and [reference_training.py](../transformer_lab/reference_training.py). Use them after trying a milestone and its [hints](hints.md). Reading a solution is useful if you close it and reconstruct the operation yourself afterward.

| Milestone | Your implementation | Read | Check stage |
|---|---|---|---|
| E01 | Token + position vectors | [4](04-embeddings.md) | `check --stage embeddings` |
| E02 | Scores, scale, causal mask, softmax, value mixture | [5](05-attention.md) | `check --stage attention` |
| E03 | Q/K/V projections, split heads, attention, merge | [6](06-multihead.md) | `check --stage heads` |
| E04 | Apply and explain the positionwise FFN | [7](07-feedforward.md) | `check --stage feedforward` |
| E05 | Both pre-norm residual updates | [8](08-block.md) | `check --stage block` |
| E06 | Embeddings → blocks → final norm → vocabulary logits | [8](08-block.md) | `check --stage model` |
| E07 | Shift input windows into X/Y prediction pairs | [9](09-training.md) | `check_training --stage data` |
| E08 | Flatten B/T and compute mean cross-entropy | [9](09-training.md) | `check_training --stage loss` |
| E09 | Clear gradients, forward, loss, backward, update | [9](09-training.md) | `check_training --stage train` |
| E10 | Temperature, softmax, sample one next ID | [9](09-training.md) | `check_training --stage sample` |

The check column is the tail of a command: for example, `python -m transformer_lab.check --stage attention`. E03 needs E02; E05 needs E02–E04; E06 needs E01–E05. The training checks use a tiny independent model so you can work on E07–E10 separately.

E04 is a short first-pass task because the constructor already defines the FFN. Your second pass below removes that scaffolding. E07 and E10 isolate data slicing and sampling; the supplied batch sampler and generation loop implement the surrounding plumbing. The student trainer calls **your** E09, which uses **your** E08 loss.

## Establish a known working baseline

Run from the project root with the virtual environment active:

```sh
python -m transformer_lab.check --stage all --implementation reference
python -m transformer_lab.check_training --stage all --implementation reference
python -m transformer_lab.train --implementation reference --steps 300
python -m transformer_lab.generate --checkpoint artifacts/reference/model.pt --prompt "the " --new-tokens 120 --temperature 0.8
python -m transformer_lab.inspect --checkpoint artifacts/reference/model.pt --text "the cat" --head 0
```

This checks the complete answer, trains it, reloads the saved model in another process, produces text, and exports an attention picture. Reference success says the workbench works; it does not mean your student TODOs are complete.

The default model uses context length 32, feature width 48, four attention heads, two blocks, and FFN width 192. It runs on CPU. The original local text is intentionally small, so outputs can remain misspelled or repetitive after 300 steps. You are testing a learning mechanism and learning to diagnose it; fluent stories are not the graduation criterion.

## Complete your milestones

For each exercise, write a shape comment before the operation, predict the output for a small example, implement it, and run its check. If it fails, print actual values for one sequence and head. Solve a three-token example before changing the full model.

After E01–E10:

```sh
python -m transformer_lab.check --stage all
python -m transformer_lab.check_training --stage all
```

Fresh files will report TODOs. That is intentional. Run the behavioral test suite against your implementation when the checks pass:

```sh
TRANSFORMER_IMPL=student python -m unittest discover -s tests -v
```

In PowerShell, set `$env:TRANSFORMER_IMPL="student"` first, then run the `python -m unittest ...` command. Without this variable, the suite tests the reference implementation. The command-line checkpoint tools select student by default.

Tests check more than output size: hand-calculated attention, probabilities summing to one, no future leakage, correct head grouping, positionwise FFN behavior, finite gradients, updates that reduce a fixed-batch loss, checkpoint loading, and generation beyond the context length.

Now run **your** model and training step:

```sh
python -m transformer_lab.train --steps 300
python -m transformer_lab.generate --checkpoint artifacts/student/model.pt --prompt "the " --new-tokens 120 --temperature 0.8
python -m transformer_lab.inspect --checkpoint artifacts/student/model.pt --text "the cat" --head 0
```

The commands save student outputs to a separate folder. Repeating a run with the same output folder replaces its checkpoint and measurements; use `--out-dir artifacts/my-experiment` to keep a comparison. The generator defaults to the implementation recorded in the checkpoint.

## Read your outputs

| File | What you can learn from it |
|---|---|
| `metrics.csv` | Numeric train/validation loss at each evaluation step. |
| `loss.png` | Whether learning is progressing and whether train/validation diverge. |
| `model.pt` | The weights, vocabulary order, and configuration used to reload the model. |
| `attention.png` | One selected head in block 0 for your exact supplied text. |

Open PNGs directly in your editor, or embed an experiment plot in your notes using `![Loss curve](../artifacts/student/loss.png)` from a Markdown file under `guide/`.

![Attention weights for head 0 in the first block of the recorded reference model on the text the cat. Rows are receivers and columns are source characters.](../examples/attention.png)

Read a row as “where this position takes value information from.” Above-diagonal weights must be zero. The first row must put all weight on its own position. The heatmap's shape cannot tell you whether every other implementation detail is correct, and the largest weight does not by itself explain a final prediction.

The inspector uses the real model's token/position embedding and first pre-norm attention input. It rejects text longer than the context limit so it does not silently show a cropped example. Generation, by contrast, deliberately crops its context while retaining the full generated result.

## Second pass: implement the supplied scaffolding too

After the milestones pass, make a working copy of your completed files before these experiments. Keep the public class/function signatures so you can reuse the checks.

1. **Rebuild constructors.** In `student.py`, recreate the module definitions from the diagrams: token and position tables, separate Q/K/V/output projections, two LayerNorms, FFN layers, ModuleList of blocks, and vocabulary projection. Match the existing attribute names so saving/loading stays compatible. Do not use `nn.Transformer` or `nn.MultiheadAttention`.
2. **Expand the FFN.** Replace its `Sequential` expression in a scratch experiment with explicit first linear, GELU, and second linear calls. Copy the original parameters before comparison; two freshly randomized models are not expected to match. Preserve the original attribute names in the main project if you want old checkpoints to load.
3. **Build batches.** Rewrite the random window extraction in `data.py` using your E07 helper. Keep the split before sampling and preserve `make_batch`'s signature. Re-run the data boundary tests.
4. **Rebuild sampling.** Use E10 in the student generation loop, then reconstruct the loop from a blank function body. Preserve context cropping, mode restoration, and no-grad behavior. Run the long-prompt and generation tests again.
5. **Reconstruct a training script.** Start with an empty scratch file and write imports, data loading, model creation, optimizer, and the step loop using your E09. Then add validation and saving using the provided trainer as a checklist. Explain each line before copying it.

PyTorch still supplies automatic differentiation, `nn.Linear`, embeddings, LayerNorm, and the optimizer. Implementing tensor kernels or an autograd engine is a different project. Here, “from scratch” means composing and understanding the transformer and learning loop from these primitives.

## Controlled experiments

Change one variable at a time. Record the configuration, seed, final losses, generated sample, and your prediction in [the experiment notebook](experiments.md).

| Experiment | What to change | What to investigate |
|---|---|---|
| Temperature | Generate at 0.5, 0.8, 1.2 with the same checkpoint/seed. | How do repetition and unusual characters change? |
| Context length | Train with `--context-length 8`, then 32. | Does extra context help on this corpus? Compare time as well. |
| More updates | Train with `--steps 1000`. | Does validation keep improving as training improves? |
| Width | Try `--d-model 32 --d-ff 128 --n-heads 4`. | How do capacity and runtime affect learning? |
| Heads | Try one head, keeping model width fixed. | Parameter count stays the same here; does behavior change? |
| Regularization | Try `--dropout 0.1`. | Is held-out loss better for the same step budget? |

The following are **intentional broken-model experiments**. Use a copy and restore the correct implementation afterward:

- Remove the causal mask. Training may look easier because positions can see answers; the causality check should fail. Do not report this as a valid language-model improvement.
- Remove the FFN activation. Check that shapes still pass, then compare learning. Shape correctness does not prove architectural equivalence.
- Zero the position embedding weights. Ask what information about order remains through the causal structure, then compare predictions. Do not claim that causal attention becomes completely order-blind; the mask itself exposes position-dependent context.

## You have completed this project when

- [ ] All ten student checkpoints pass.
- [ ] The full test suite passes with `TRANSFORMER_IMPL=student`.
- [ ] A student training run writes finite measurements and its training loss decreases from step 0.
- [ ] You reload its checkpoint and generate characters in a new process.
- [ ] You inspect a real head and explain the zero upper triangle.
- [ ] You explain Q, K, V, head shapes, FFN sharing, residuals, and shifted labels without opening the guide.
- [ ] You record two controlled experiments and explain an unexpected result.
- [ ] You rebuild the supplied model constructors and sampling/training loop on your second pass.

Next, once this feels familiar: subword tokenization, encoder attention without a causal mask, encoder–decoder cross-attention, rotary positions, gated FFNs, and efficient attention kernels. Each extends a specific part of the model you now know where to find. See [the source map](references.md).
