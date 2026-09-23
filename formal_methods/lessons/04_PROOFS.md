# 04 — Build proofs by reading the goal

[Course home](../README.md) · Previous: [Lean basics](03_LEAN_BASICS.md) · Next: [Induction](05_INDUCTION.md)

Read this in two passes: logical proofs before Lab 02, equality and arithmetic before Lab 03. Examples that use `Course` definitions assume the project is built; the checkable example blocks below include their imports when needed.

## Introduce an assumption

```lean
example (P : Prop) : P → P := by
  intro hP
  exact hP
```

The proof develops like this:

```text
Before intro:    P : Prop                goal: P → P
After intro:     P : Prop, hP : P        goal: P
After exact:                            no remaining goals
```

`intro hP` names the input evidence of the implication. The theorem still means “if P, then P”; it does not establish P without a premise. For a universal goal such as `∀ n : Nat, ...`, `intro n` similarly introduces an arbitrary input.

## Split a goal into parts

```lean
example (P : Prop) : P → P ∧ P := by
  intro hP
  constructor
  · exact hP
  · exact hP
```

To produce a conjunction, you must produce each component. `constructor` creates those two goals. The `·` bullets focus on one goal at a time. Both must be solved.

To use a conjunction already in your context, take its components. If `h : P ∧ Q`, then `h.left : P` and `h.right : Q`.

For a disjunction goal, `left` chooses its left alternative and `right` chooses its right alternative. By contrast, if your **hypothesis** is a disjunction, you cannot arbitrarily assume one side. Handle both possibilities:

```lean
example (P Q R : Prop) (h : P ∨ Q)
    (fromP : P → R) (fromQ : Q → R) : R := by
  cases h with
  | inl hP => exact fromP hP
  | inr hQ => exact fromQ hQ
```

The branch names `inl` and `inr` refer to the two ways to construct an `Or`. In the first branch you receive evidence of P; in the second you receive evidence of Q. Both branches must establish R.

## Work forward or backward

With `hPQ : P → Q` and `hQR : Q → R`, you can work forward: construct Q from P, then construct R from Q.

```lean
example (P Q R : Prop) (hP : P) (hPQ : P → Q) (hQR : Q → R) : R := by
  have hQ : Q := hPQ hP
  exact hQR hQ
```

`have` records an intermediate result. You can also work backward from your goal:

```lean
example (P Q R : Prop) (hP : P) (hPQ : P → Q) (hQR : Q → R) : R := by
  apply hQR
  apply hPQ
  exact hP
```

Applying the rule `Q → R` to the goal R changes the task to proving Q. You are saying, “This rule will finish the job if I can supply its input.”

Use `exact` when you already have the complete evidence. Use `apply` when you want Lean to turn the missing inputs into goals.

## Provide a witness

```lean
example : ∃ n : Nat, n = 6 := by
  exists 6
```

For an existence claim, choose an actual object. Here `exists 6` supplies the witness and closes its reflexive equality. In a more complicated example, Lean may leave the witness's property as a new goal. Always inspect the result rather than assuming a tactic finished everything.

If `h : ¬ P` and `hp : P`, `h hp` is evidence of `False`. This is ordinary function application because negation means `P → False`.

**Now do L1–L6** in [02_Logic.lean](../exercises/02_Logic.lean). Aim to explain every intermediate goal. The official [tactics chapter](https://lean-lang.org/theorem_proving_in_lean4/Tactics/) provides further examples.

## Rewrite an equality

```lean
import Course.Models
open Course

example (a b : Nat) (h : a = b) : bump a = bump b := by
  rw [h]
```

`rw [h]` uses the equality to replace `a` by `b` in the goal. The resulting equality is reflexive, so this tactic finishes it. `rw [← h]` uses the same equality in the reverse direction.

Rewriting is not guessing that two values are similar. You must have an equality theorem or hypothesis justifying the replacement.

## Definitions and known theorems do different work

```lean
import Course.Models
open Course

example (n : Nat) : twice n = n + n := by
  rfl

example (n : Nat) : 0 + n = n := by
  exact Nat.zero_add n
```

The first equality follows directly from the definition of `twice`. The second uses a theorem about addition. With Lean's natural-number addition, `0 + n = n` for an arbitrary `n` is not solved just by the same reflexivity trick. Do not interpret a failed `rfl` as proof that a statement is false.

`simp` rewrites using a selected collection of simplification theorems. `simp [twice]` additionally unfolds `twice`. It is useful for routine cleanup, but spend a moment understanding what it simplified.

## Use arithmetic automation after understanding the claim

```lean
import Course.Models
import Std.Tactic
open Course

example (n : Nat) : n < bump n := by
  unfold bump
  omega
```

The first line exposes `n + 1`. The goal is now a natural-number arithmetic fact. `omega` proves suitable linear arithmetic claims over natural numbers and integers. It does not solve arbitrary mathematics, nonlinear products of unknowns, or every property of your custom function. It produces proof evidence that is checked.

Predict the statement in ordinary language first: increasing a natural number by one makes it larger. The automation is handling the bookkeeping of that known argument.

Now consider:

```text
For every n : Nat, n - 1 + 1 = n.
```

Try `n = 0`. Natural subtraction stops at zero, so the left side is one. This universal claim is false. Adding a tactic cannot repair the statement. A useful corrected claim requires `1 ≤ n`.

**Now do E1–E4** in [03_Equality.lean](../exercises/03_Equality.lean). For E4, explain exactly which input its assumption excludes.

## A debugging procedure

1. Read the goal after `⊢`, including the types of its variables.
2. List the useful hypotheses above it.
3. Describe one valid reasoning step in English.
4. Choose a tactic that expresses that step.
5. Inspect the new goals before adding more code.

If the goal seems impossible, try small inputs or inspect missing assumptions. If `exact` fails, compare the term's type with the goal. If `rw` fails, check the direction and whether the expression to replace is actually present. If a branch remains open, read that branch's hypotheses independently.

**Ready to continue:** complete Labs 02 and 03, and explain the difference between an incorrect proof attempt and a false theorem statement.
