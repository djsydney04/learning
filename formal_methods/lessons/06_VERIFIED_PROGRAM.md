# 06 — Verify a bounded counter

[Course home](../README.md) · Previous: [Induction](05_INDUCTION.md) · [Lab instructions](../PRACTICE.md)

## Start from the requirement

We want a counter with a fixed limit. If there is room, add one. Once full, keep the count. For an initially valid count, an increment must preserve the bound.

This is a small sequential model. It could describe a bounded tally or a simplified capacity counter. We have no concurrent updates, decrements, changing limits, persistence, or external inputs beyond the natural-number arguments.

The implementation in [Course/Models.lean](../Course/Models.lean) is:

```lean
def step (limit count : Nat) : Nat :=
  if count < limit then count + 1 else count

#eval step 3 0  -- 1
#eval step 3 2  -- 3
#eval step 3 3  -- 3
```

The mathematical comparison `count < limit` is decidable for natural numbers, so Lean can use it in an `if` expression.

Predict the result for limit zero, and for a count already greater than the limit. The function does not validate or repair arbitrary stored data; its behavior on those inputs still has a precise meaning.

## Write several useful properties

| Property | Assumption | Guarantee |
| --- | --- | --- |
| At the limit | count = limit | The count remains limit |
| Progress | count < limit | The result is exactly count + 1 |
| Bound preservation | count ≤ limit | The result is ≤ limit |
| Monotonicity of one step | None beyond Nat inputs | The result is ≥ count |

The bound alone is too weak: a function returning zero always satisfies it. Progress prevents that implementation from meeting the whole contract.

This resembles a **Hoare triple**, often written `{P} command {Q}`: when precondition P holds, executing the command establishes postcondition Q, with termination handled according to the chosen correctness notion. Here our Lean function already terminates, and our theorem relates its input and output values. We are not introducing a separate imperative program logic.

## Plan the main proof in words

Assume `count ≤ limit`. There are two cases.

1. If `count < limit`, the result is `count + 1`. For natural numbers, strict inequality means there is at least one unit of room, so `count + 1 ≤ limit`.
2. Otherwise, the result is `count`. The original assumption already says `count ≤ limit`.

Nothing about this argument depends on one particular limit or count.

In Lean, `unfold step` exposes the `if`, and `split` creates the two branches. Each branch gets evidence about its condition. Inspect those hypotheses; the first branch is suitable for `omega`, while the second already has the needed bound.

Use this tactic shape in C3, filling in the reasoning yourself:

```text
unfold step
split
· ...  -- count < limit; prove the increment fits
· ...  -- count is unchanged; use the original bound
```

## From one operation to many

The course also provides:

```lean
import Course.Models
open Course

#eval run 3 0 0   -- 0 steps from count 0: result 0
#eval run 3 2 0   -- 2 steps from count 0: result 2
#eval run 3 10 0  -- 10 steps from count 0: result 3
```

The argument order is `run limit steps initialCount`. Its equations are:

```text
run limit 0 count       = count
run limit (k + 1) count = step limit (run limit k count)
```

Prove safety by induction on the number of steps:

- Base case: after zero operations, the count is the initial count, which is safe by assumption.
- Step case: the induction hypothesis says the result after `k` steps is safe. Apply your one-step preservation theorem to that result.

This connects a local operation contract to an invariant over arbitrarily long finite executions. It does not enumerate them.

If the step goal's recursive expression is hard to read, `change step limit (run limit k count) ≤ limit` can expose the form you need. `change` is allowed when the proposed goal is definitionally equal to the original; it cannot replace a goal with an unrelated easier claim.

## Understand the boundary of the theorem

The final claim is:

```text
For any limit, initial count, and finite number of steps:
if initial count ≤ limit,
then run limit steps initial count ≤ limit.
```

It is not a theorem that all inputs start valid. It does not prove eventual arrival at the limit, simultaneous update safety, or correctness of a deployed counter service. Those require different statements and models.

“Never exceed the limit” is a **safety** property. “Eventually reach the limit” is a **liveness**-style requirement and depends on taking enough steps. For example, a scheduler that performs no updates need not fill the counter. This course proves the stated bound over finite runs.

## Check what evidence you relied on

In your completed exercise file, inside its namespace and after `run_safe`, you may add:

```text
#print axioms run_safe
```

This reports axiom dependencies. `sorryAx` means an unfinished proof has contaminated the result. An `axiom` you introduce also assumes a claim rather than proving it. Standard foundational names such as `propext`, `Quot.sound`, or `Classical.choice` have a different role; their appearance is not a proof hole. Learn what a dependency means before treating an axiom list as a verdict. The official [axioms and computation chapter](https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/) explains these foundations.

The strict checker catches the usual `sorry` warnings; it is not a complete audit of arbitrary new assumptions or changes to the specification. For these exercises, keep the statements and shared definitions as given except during the explicit bug experiment.

## Your turn

Complete **C1–C5** in [05_SafeCounter.lean](../exercises/05_SafeCounter.lean), then do the bug experiment in [PRACTICE.md](../PRACTICE.md).

```bash
bash scripts/check.sh 05
```

**Ready to finish:** explain why C5 uses C3, identify the initial-state assumption, and give one useful counter behavior that these theorems do not yet prove.
