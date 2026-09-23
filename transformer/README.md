# Build a transformer, one operation at a time

A beginner's programming guide to transformers in PyTorch. Read the Markdown lessons, inspect their embedded PNG diagrams, run small experiments, and build a character-level text generator yourself. No prior Python, linear algebra, or machine-learning knowledge is assumed.

**Start with [the setup and first session](guide/00-start.md).** The project environment is already prepared in `.venv` on this machine. Your first command, from this folder, is:

```sh
source .venv/bin/activate
python -m labs.01_python
```

Open [lesson 1](guide/01-python.md) beside [the first lab](labs/01_python.py). Change one value, save, rerun, and explain the difference. Use your editor's Markdown preview to see the embedded images. There is no separate website to start.

![A transformer converts characters to vectors, combines context with attention, transforms features with feed-forward networks, and predicts the next character.](assets/01-transformer-overview.png)

## The route

| Lesson | You learn | You do |
|---|---|---|
| [0 · Start here](guide/00-start.md) | Terminal, environment, course workflow | Run your first program. |
| [1 · Python](guide/01-python.md) | Variables, lists, loops, functions, classes | Edit lab 01. |
| [2 · Tensors](guide/02-tensors.md) | Vectors, matrices, shapes, axes, matrix multiplication | Predict and check lab 02 outputs. |
| [3 · Learning](guide/03-learning.md) | Linear layers, gradients, loss, optimization | Train a line to fit data in lab 03. |
| [4 · Embeddings](guide/04-embeddings.md) | Character IDs, learned vectors, positions | Lab 04; implement E01. |
| [5 · Attention](guide/05-attention.md) | Queries, keys, values, scaling, causal masks, softmax | Lab 05; calculate a row by hand; implement E02. |
| [6 · Multiple heads](guide/06-multihead.md) | Parallel attention and correct reshaping | Implement E03. |
| [7 · Feed-forward](guide/07-feedforward.md) | Shared positionwise networks, GELU, feature expansion | Lab 06; implement E04. |
| [8 · Transformer blocks](guide/08-block.md) | Residuals, LayerNorm, stacked blocks, logits | Implement E05–E06. |
| [9 · Training and generation](guide/09-training.md) | Shifted targets, cross-entropy, updates, sampling | Implement E07–E10. |
| [10 · Your project](guide/10-project.md) | Put everything together and investigate it | Train, reload, generate, inspect, and rebuild the scaffolding. |

Each lesson includes diagrams, concrete numbers, code, experiments, and a checkpoint. Use [hints](guide/hints.md) when stuck, [debugging](guide/debugging.md) when code fails, and [the glossary](guide/glossary.md) when a term is unfamiliar. Keep your results in [the experiment notebook](guide/experiments.md). [References](guide/references.md) connect the lessons to official documentation and the original paper.

## Your implementation workbench

- [student.py](transformer_lab/student.py): six transformer exercises, from embeddings to vocabulary scores.
- [student_training.py](transformer_lab/student_training.py): four exercises for shifted data, loss, one optimizer step, and sampling.
- [reference.py](transformer_lab/reference.py) and [reference_training.py](transformer_lab/reference_training.py): complete solutions to consult after trying.
- [data/tiny_stories.txt](data/tiny_stories.txt): forty short original passages, supplied locally.

Your TODOs are intentionally unfinished. Checks select the student implementation by default:

```sh
python -m transformer_lab.check --stage attention
python -m transformer_lab.check_training --stage loss
```

For an immediate working demonstration of the destination:

```sh
python -m transformer_lab.train --implementation reference --steps 300
python -m transformer_lab.generate --checkpoint artifacts/reference/model.pt --prompt "the " --new-tokens 120
```

After your exercises pass, omit `--implementation reference` to train your own model. See [the final project](guide/10-project.md) for the complete student test commands and second pass where you rebuild the supplied constructors, batch sampler, and generation loop.

## What has been verified

The six runnable labs, reference checkpoints, 34 behavioral tests, checkpoint reload, generation, and a 300-step CPU training run passed. The reference run's training loss fell from **3.52 to 1.78**, and validation loss from **3.52 to 1.82**. These are measurements on the small bundled practice corpus, not a fluency benchmark. [Exact results and embedded plots](examples/RESULTS.md) include the configuration and limitations.

All guide content is local Markdown with embedded PNGs. Diagram sources are in [scripts/render_diagrams.py](scripts/render_diagrams.py); regenerate them with `python scripts/render_diagrams.py` after setup. Training also creates real PNG plots you can embed in your own Markdown notes.
