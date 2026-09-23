# Reference and next steps

[Course home](README.md)

## A small vocabulary

| Term | Meaning in this course |
| --- | --- |
| Specification | A precise statement of required behavior |
| Model | A mathematical description of relevant system behavior |
| Precondition | An assumption required before an operation |
| Postcondition | A property guaranteed afterward under the precondition |
| Invariant | A property established initially and preserved by the transitions being considered |
| Proposition | A logical statement |
| Hypothesis | Evidence or an assumption available in a proof context |
| Goal | The proposition you currently need to prove |
| Counterexample | A case that falsifies a claim |
| Tactic | An instruction used to construct proof evidence |
| Kernel | The core checker for Lean's proof terms |
| Definitional equality | Equality Lean recognizes by its built-in reduction rules |
| Induction hypothesis | Evidence for the smaller case in an induction step |
| Axiom | A proposition accepted as an assumption rather than proved in the theory |
| Mathlib | A large community mathematical library for Lean; not required here |

## Tactics used here

This is a reminder after the lessons, not a list to memorize first.

| When you see... | Consider... | What it does |
| --- | --- | --- |
| `h : P`, goal P | `exact h` | Supply evidence that already fits |
| Goal `P → Q` | `intro hP` | Assume its input evidence and prove Q |
| Goal `∀ n, R n` | `intro n` | Introduce an arbitrary input |
| Goal `P ∧ Q` or `P ↔ Q` | `constructor` | Prove the required components/directions |
| Goal `P ∨ Q` | `left` or `right` | Choose an alternative to prove |
| `h : P ∨ Q` | `cases h with ...` | Handle every form of the evidence |
| `h : P → Q`, goal Q | `apply h` | Change the task to proving P |
| Goal `∃ n, R n` | `exists value` | Choose a witness, then discharge its property |
| Equalities that compute to the same thing | `rfl` | Prove definitional equality |
| `h : a = b` | `rw [h]` | Rewrite using that equality |
| An opaque-looking custom definition | `unfold name` | Expose its defining expression |
| Routine simplification | `simp [name, h]` | Use simplification rules and the listed facts |
| An `if` after unfolding | `split` | Split into cases with branch-condition evidence |
| A linear Nat/Int arithmetic goal | `omega` | Construct an arithmetic proof |
| A concrete decidable proposition | `decide` | Prove it by computing a decision procedure |
| A recursive family | `induction n with ...` | Prove base and successor cases |
| A useful intermediate fact | `have h : P := ...` | Name and establish that fact |

Use `import Std.Tactic` for the course's arithmetic examples. Names and exact behavior can evolve across releases; the [official tactic reference](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference/) is a broader reference, while this project pins 4.23.0.

## Commands

```bash
# Build the shared teaching modules; does not complete student exercises.
lake build

# Check worked demonstrations.
bash scripts/check.sh examples

# Check one completed exercise file; choose 01 through 05.
bash scripts/check.sh 03

# Check all your exercise files, including a self-authored extension.
bash scripts/check.sh all

# Independently check the reference solutions.
bash scripts/check.sh solutions
```

Inside Lean:

```text
#check expression          -- display its type
#eval expression           -- evaluate it
#print theoremName         -- inspect a declaration
#print axioms theoremName  -- inspect its axiom dependencies
```

## When stuck

| Message or situation | Likely issue |
| --- | --- |
| `unsolved goals` | One or more proof obligations remain; inspect each goal |
| `type mismatch` | Your supplied term has a different type from the required evidence |
| Rewrite did not find the pattern | The equality's direction, expression shape, or location differs |
| `unknown identifier` | A spelling, namespace, import, or scope problem |
| `no goals to be solved` | An earlier tactic already finished; remove the extra tactic |
| `declaration uses 'sorry'` | There is a proof hole; file acceptance alone is not completion |
| `omega` fails | Check assumptions, unfold definitions, or use a different argument |
| A natural-number calculation is surprising | Remember that subtraction stops at zero |

For installation and import problems, see [setup](lessons/00_SETUP.md).

## What to read afterward

These are first-party resources. You can finish the exercises here without reading them all. Installation and reference links were consulted while preparing the course; online documentation may target newer Lean releases.

| Resource | Use it for |
| --- | --- |
| [Lean installation](https://lean-lang.org/install/) | Current editor and toolchain setup |
| [Theorem Proving in Lean 4](https://lean-lang.org/theorem_proving_in_lean4/) | A deeper treatment of the logical foundations and proof language |
| [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/) | Learning Lean as a programming language |
| [Lean language reference](https://lean-lang.org/doc/reference/latest/) | Precise details once you know which feature you need |
| [Lean live editor](https://live.lean-lang.org/) | Small experiments without local installation |
| [TLA+ high-level view](https://lamport.azurewebsites.net/tla/high-level-view.html) | Another approach centered on system states and transitions |

Suggested next sequence: learn more list proofs; specify and verify a small transformation; study dependent types; then choose mathematical formalization or program verification as your next direction. For concurrent and distributed behavior, explore explicit state-machine models and temporal properties as well.
