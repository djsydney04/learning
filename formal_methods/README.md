# Learning formal methods and Lean

Formal methods use precise mathematical descriptions to reason about systems. Lean is a programming language and proof assistant: you can write a function, state a property of it, and build a proof that Lean checks.

This is **your personal learning workspace**, built around your background: some programming experience and no experience writing proofs. You do not need calculus, advanced algebra, or previous Lean knowledge. The aim is to learn how to turn “I think this works” into a precise claim with explicit assumptions and checked reasoning.

It sits alongside your [other learning projects](../README.md). Here, the focus is understanding why programs satisfy their intended behavior. Work at your own pace, keep experiments and questions in your journal, and use the exercises as things to discuss rather than formal assignments. [AGENTS.md](AGENTS.md) records this context for future assistance in this directory.

**Start with [your first session](START_HERE.md).** It gives you a small assignment to finish today. You do not need to read the whole course first.

## The route

The times are suggestions, not deadlines. Expect to spend more time trying proofs than reading.

| Session | Read | Do | Suggested time |
| --- | --- | --- | --- |
| 1 | [What formal methods are](lessons/01_FORMAL_METHODS.md), [setup](lessons/00_SETUP.md), [Lean basics](lessons/03_LEAN_BASICS.md) | Warmup W1–W4 | 45–75 minutes, plus installation |
| 2 | [Logic from zero](lessons/02_LOGIC.md), [building proofs](lessons/04_PROOFS.md) through logical proofs | Logic L1–L6 | 60–90 minutes |
| 3 | [Equality and arithmetic](lessons/04_PROOFS.md) | Equality E1–E4; find a counterexample | 45–75 minutes |
| 4 | [Recursion and induction](lessons/05_INDUCTION.md) | Induction I1–I2 | 60–90 minutes |
| 5 | [Verify a small program](lessons/06_VERIFIED_PROGRAM.md) | Counter C1–C5; change a bug and watch a proof fail | 75–120 minutes |

There are **21 unfinished proofs**, plus written and programming experiments. The full assignment instructions are in [PRACTICE.md](PRACTICE.md).

## How to use the files

- `lessons/`: explanations, worked examples, and questions to answer aloud.
- `exercises/`: your Lean files. Replace `sorry` with proofs.
- [Course/Models.lean](Course/Models.lean): the small functions you will reason about.
- [Course/Examples.lean](Course/Examples.lean): working demonstrations.
- [HINTS.md](HINTS.md): incremental hints to use after a real attempt.
- [REFERENCE.md](REFERENCE.md): symbols, tactics, troubleshooting, and further reading.
- [JOURNAL.md](JOURNAL.md): a place for your answers and proof attempts.
- `solutions/`: completed proofs; open these after attempting an exercise.

Use this loop: **predict → write → read Lean's goal → revise → explain**. A proof you can explain is a better learning milestone than a tactic sequence you copied.

## What “working” means

The project pins **Lean 4.23.0** as a reproducible teaching version; it does not track the newest release. It uses Lean's bundled libraries and no Mathlib dependency. See the [official release](https://github.com/leanprover/lean4/releases/tag/v4.23.0).

After setup, from this folder:

```bash
bash scripts/check.sh examples
bash scripts/check.sh 01
```

The examples should pass. Exercise 01 should initially fail because its proofs contain `sorry`. That is intentional. Lean normally accepts `sorry` with a warning; this checker turns warnings into errors. A normal `lake build` checks the teaching library only, **not your unfinished exercise files**.

Finish an exercise file, check it by number, then explain each proof without looking at the solution. Do not change a theorem's statement or add assumptions just to get it accepted. The checker checks Lean correctness; it is not a tamper-resistant grader and does not judge whether you changed the intended specification.

At the end, you should be able to state a contract, find an invalid claim, read a proof state, prove small logical facts, use induction, and explain exactly what a verified program property does and does not guarantee.

## Preparation checks

The teaching library, all 21 reference proofs, and all 24 Markdown Lean blocks were checked with Lean 4.23.0 on this Mac. The starter files elaborate with intentional proof-hole warnings. The strict checker rejects those holes; a separate completed copy passes, and changing the counter's `<` to `≤` makes its contract proofs fail. All local Markdown links resolve.

These checks used a temporary toolchain, without installing Elan globally or configuring your editor. Installing your own toolchain and confirming the VS Code Infoview are still part of [your first session](START_HERE.md). The editor setup and browser fallback were not exercised through their interfaces.
