# Personal learning context

This directory is the user's personal formal methods and Lean learning workspace within the larger `learning` repository. The surrounding repository explores GPU foundations, CUDA, transformers, and computer hardware through local explanations and runnable experiments.

## Learner and purpose

- The user has some programming experience and is new to proofs. Do not infer mathematical or systems expertise from the other directories.
- The user wants explanations in Markdown and practical work they can do themselves to understand how things work.
- Treat the material as self-paced personal study. Keep the tone direct and conversational; use checkpoints and discussion rather than grading, deadlines, or formal hand-ins.
- Connect formal methods to familiar programming ideas: inputs, types, conditions, functions, contracts, state changes, and bugs. Define mathematical vocabulary before relying on it.

## How to help

- Read the relevant lesson, exercise attempt, and journal entries before choosing the next step. An existing solution file is not evidence that the user has completed or understood an exercise.
- Explain the idea in plain language, show a small worked example, then give the user a manageable task with a concrete way to check it.
- When reviewing a proof, explain the hypotheses, goal, and why each step is valid. Help the user reason about the proof state instead of merely offering a tactic to paste.
- Start with a targeted hint when the user wants help learning. Give a complete solution when they ask for one; do not impose a rigid tutoring restriction.
- Preserve the user's proof attempts and journal answers. Intentional `sorry` placeholders in learner exercises are work for the user, not defects to automatically fill in during maintenance.
- Keep reference solutions separate from exercises. Do not weaken theorem statements, add assumptions, or introduce axioms merely to make a check pass.
- Adapt depth and pacing to the user's questions. The sequence in `README.md` is a suggested path, not a requirement to finish every lesson before exploring an interest.

## Project map and verification

- `README.md` maps the material; `START_HERE.md` gives the first session.
- `lessons/` explains the concepts; `PRACTICE.md` describes the experiments.
- `exercises/` and `JOURNAL.md` contain the user's work. `HINTS.md` and `solutions/` provide support.
- `Course/Models.lean` and `Course/Examples.lean` contain shared definitions and worked demonstrations.
- `lean-toolchain` pins Lean 4.23.0. The project uses bundled Lean libraries without Mathlib.
- `lake build` checks the shared library, not the learner exercises. Use `bash scripts/check.sh examples`, a lab number from `01` to `05`, `solutions`, or `all` for the corresponding strict check.
- Unfinished exercises are expected to fail the strict check. Distinguish that expected result from broken teaching code.
- Prior validation used a temporary toolchain. Verify the current environment before claiming the user's Lean installation or editor setup is working.
- Preserve unrelated work in the surrounding learning repository.
