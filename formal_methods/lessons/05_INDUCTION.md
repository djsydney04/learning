# 05 — Recursion and induction

[Course home](../README.md) · Previous: [Building proofs](04_PROOFS.md) · Next: [Verified program](06_VERIFIED_PROGRAM.md)

## Why checking more examples is not enough

Suppose a recursive function works at inputs `0`, `1`, `2`, and `100`. What about `101`, or a much larger number? Natural numbers form an infinite family.

Induction covers that family with two obligations:

1. Prove the property at zero: the **base case**.
2. For arbitrary `k`, assume the property at `k` and prove it at `k + 1`: the **inductive step**.

The temporary assumption at `k` is the **induction hypothesis**. It is not permission to assume the goal at `k + 1`.

Why is this sufficient? Every natural number is reached from zero by finitely many successor steps. Establishing the first case and preserving the property through an arbitrary step reaches all of them. Lean's inductive definition of natural numbers supplies this reasoning principle.

## A recursive function to inspect

```lean
def climb : Nat → Nat
  | 0 => 0
  | n + 1 => climb n + 1

#eval climb 3
```

The vertical bars separate pattern-matching cases. `=>` gives each case's result. The successor case calls the function on a smaller natural number.

Expand the call by hand:

```text
climb 3
= climb 2 + 1
= (climb 1 + 1) + 1
= ((climb 0 + 1) + 1) + 1
= ((0 + 1) + 1) + 1
= 3
```

Now conjecture: for every `n`, `climb n = n`. Our task is to justify the whole family of equalities.

## Write the proof on paper first

Base case: `climb 0` is zero by its definition.

Step: suppose `climb k = k`. By the definition, `climb (k + 1) = climb k + 1`. Substitute the hypothesis to obtain `k + 1`, which is exactly the required result.

Notice the order: unfold the function for the larger input, use a fact about the smaller input, finish the larger case.

## The same argument in Lean

This standalone block includes the definition again so you can paste it into a scratch file:

```lean
def climb : Nat → Nat
  | 0 => 0
  | n + 1 => climb n + 1

theorem climb_eq (n : Nat) : climb n = n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    simp [climb, ih]
```

`induction n` generates the base and step cases. The names `k` and `ih` are names we choose; `ih` is a common abbreviation for induction hypothesis. In the step, its type is `climb k = k`.

`simp [climb, ih]` exposes the recursive equation and replaces `climb k` using `ih`. The remaining equality is reflexive. This is the short machine-checked expression of the paper argument above.

**Exercise before proceeding:** temporarily remove `ih` from the simplifier list in this example. Inspect the result. Can you identify the smaller-input fact the step needs? Restore the original proof afterward.

## Lists have induction too

A list is either empty, written `[]`, or a head followed by a tail, written `x :: xs`. The list `[4, 7]` is `4 :: 7 :: []`.

Our counting function is:

```lean
def countEntries : List Nat → Nat
  | [] => 0
  | _ :: xs => countEntries xs + 1
```

The `_` means the head's value is not used. We count an element regardless of whether its value is zero, four, or a million. `xs.length` is Lean's standard list-length operation.

To prove a property about every list, show it for the empty list, then show that adding a head preserves it assuming it holds for the tail. The induction cases are `nil` and `cons`:

```text
induction xs with
| nil => ...
| cons x xs ih => ...
```

The second branch receives a head `x`, a tail `xs`, and evidence `ih` about the tail. This is structural induction: the argument follows the way the data is built.

## Recursion must make progress

Lean requires termination for ordinary recursive definitions used in its logic. These examples recurse on structurally smaller data: a predecessor or a list tail. A definition that keeps calling itself on exactly the same input would not be accepted in this form.

Termination of a definition and correctness of its result are separate obligations. Counting down guarantees you eventually stop; it does not by itself prove you counted correctly. Later Lean features support more general recursion, but we do not need them here. See the official [induction and recursion chapter](https://docs.lean-lang.org/theorem_proving_in_lean4/induction_and_recursion.html).

## Your turn

Complete [04_Induction.lean](../exercises/04_Induction.lean):

- **I1:** the function adds two at each recursive step. Prove its result is `2 * n`. `Nat.mul_succ` connects `2 * (k + 1)` with `2 * k + 2`.
- **I2:** prove `countItems xs = xs.length` for every list of natural numbers.

Before using Lean, write the base case, the precise induction hypothesis, and the step goal for each theorem. After checking, explain why a proof for lists of length at most ten would be weaker.

```bash
bash scripts/check.sh 04
```

**Ready to continue:** you can state what `ih` means in each branch and explain why it is not circular reasoning.
