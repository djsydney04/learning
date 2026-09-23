# 01 — What formal methods are

[Course home](../README.md) · Next: [Logic](02_LOGIC.md)

## Start with a familiar programming problem

Suppose you write a counter that should stop at a limit. You try a few inputs, and its outputs look right. What exactly have you learned?

You have evidence about the runs you tried. To reason about every permitted input, you need to say what “right” means, describe the program precisely, and justify the connection. Formal methods give you tools for doing that.

A **specification** states the behavior you require. An **implementation** is a program intended to provide that behavior. A **proof** explains, using explicit rules, why a stated claim follows from stated assumptions.

For the counter, a possible contract is:

```text
Input: natural numbers limit and count
Precondition: count ≤ limit
Operation: increment if count < limit; otherwise keep count
Postcondition: result ≤ limit
```

The precondition is what must hold before the operation. The postcondition is what the operation guarantees under that precondition. Natural numbers are `0, 1, 2, ...`.

Ask whether this is the whole intended specification. A function that always returns zero satisfies the bound. It fails to count. We also want “increment by exactly one when there is room” and “stay at the limit when full.” Correctness has several parts because requirements have several parts.

## Three different kinds of evidence

| Approach | What you do | What the result means |
| --- | --- | --- |
| Testing | Run chosen inputs and inspect outputs | Those runs behaved as checked; failures expose bugs |
| Model checking | Explore states of a mathematical model | A property holds across the explored state space, or a counterexample is found |
| Deductive proof | Derive a property from definitions and assumptions | The statement follows for all cases covered by the theorem |

Property-based testing generates many inputs and searches for failures. It is useful, but a finite collection of passing tests is not usually a proof of an unbounded claim. Exhaustively checking a genuinely finite domain can establish a property of that domain; the issue is coverage, not a slogan that “tests can never prove anything.”

Model checking can exhaust a finite model; bounded exploration of a larger or infinite system gives a narrower result. Deductive proofs can handle infinite families, such as every natural number, but may require human guidance.

Formal methods also include specification languages, static analyses, and solver-assisted verification. Different tools trade off automation, expressiveness, and the kinds of models they handle. For a separate introduction to state-based specification, see [Leslie Lamport's high-level view of TLA+](https://lamport.azurewebsites.net/tla/high-level-view.html).

## Where Lean fits

Lean is both a functional programming language and an interactive theorem prover. You state a theorem and supply a proof. Tactics help construct the proof; a small core called the **kernel** checks the resulting proof against Lean's rules. The [official introduction](https://lean-lang.org/theorem_proving_in_lean4/introduction.html) describes this role.

For example:

```lean
def addOne (n : Nat) : Nat := n + 1

example (n : Nat) : addOne n = n + 1 := by
  rfl
```

Read the theorem as: “For any natural number `n`, `addOne n` equals `n + 1`.” The proof works because the function's definition makes both sides the same expression. You did not test all natural numbers. You reasoned with an arbitrary one.

That theorem is deliberately small. It teaches the mechanics; useful verification often relates a more complicated implementation to a simpler specification.

## What a proof does not automatically establish

Imagine proving that the counter stays below its limit, then connecting it to a web service. Several questions remain:

- Does the service actually run the operation you modeled?
- Can two requests update the same count concurrently?
- Can stored data start above the limit?
- Does “count” mean requests received, requests completed, or current occupants?
- Is the real program using unbounded natural numbers or a fixed-width integer?

Our Lean model uses `Nat`, with no fixed-width wraparound. A proof about it does not automatically prove a translated `UInt32` or C implementation correct. Nor does a source-level functional theorem by itself verify the compiler, database, network, or hardware.

Lean checks the formal statement you wrote, relative to its foundations and any assumptions you used. It cannot tell whether that statement captures the requirement you meant. Reviewing the specification is part of the work.

## Assumptions can hide the problem

Consider these two claims:

```text
For every count and limit, step limit count ≤ limit.

For every count and limit, if count ≤ limit,
then step limit count ≤ limit.
```

The first claims repair of every invalid starting state. The second claims preservation of an existing bound. They are different requirements. Later, you will prove the second and find a counterexample to the first.

An **invariant** is a property preserved across the relevant transitions. To show every reachable state is safe, establish it initially, then show each transition preserves it. “Safe now” alone is not enough, and preservation alone says nothing about where you start.

Also beware an impossible precondition. “If a natural number is less than zero, the output is safe” covers no permitted natural-number input. The implication can be true while being useless. This is called **vacuous truth**.

## Your turn — no Lean needed

Write your answers in [JOURNAL.md](../JOURNAL.md).

1. An array lookup promises to return the element at index `i`. What condition on `i` and the array length is needed? Assume indexing starts at zero.
2. A sorting specification says only “the output is sorted.” What bad implementation would satisfy it? What additional requirement is missing?
3. “The counter is always safe” is ambiguous. Write a version that explicitly mentions its initial state and permitted operations.
4. Pick one function you have written. Give it one precondition and two useful postconditions. If it needs no precondition beyond input types, say so.

**Ready to continue:** you can distinguish a test, a specification, and a proof, and you can explain why assumptions matter.
