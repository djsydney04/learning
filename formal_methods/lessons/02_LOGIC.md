# 02 — Logic from zero

[Course home](../README.md) · Previous: [Formal methods](01_FORMAL_METHODS.md) · Next: [Lean basics](03_LEAN_BASICS.md)

## Statements and evidence

A **proposition** is a statement that can be true or false. “`7` is larger than `3`” is a proposition. “Please add one” is an instruction. “`n` is larger than `3`” describes a property whose truth depends on `n`.

In Lean:

```text
P : Prop       P is a proposition
hP : P         hP is evidence proving P
n : Nat        n is a natural number
```

Naming a proposition `P` does not assert it. Having a hypothesis `hP : P` gives you evidence you may use within that proof.

This is an instance of **propositions as types**: a proposition can be treated as the type of its proofs. You establish it by constructing a term of that type. See the official chapter on [propositions and proofs](https://lean-lang.org/theorem_proving_in_lean4/Propositions-and-Proofs/).

## Build bigger claims

Let `P` mean “the request is authenticated” and `Q` mean “the user may edit this document.”

| Notation | Read it | What a proof must provide |
| --- | --- | --- |
| `P ∧ Q` | P and Q | Evidence of both |
| `P ∨ Q` | P or Q, possibly both | Evidence of at least one side, identifying that side |
| `P → Q` | If P, then Q | A way to turn any evidence of P into evidence of Q |
| `¬ P` | Not P | A way to turn evidence of P into a contradiction |
| `P ↔ Q` | P if and only if Q | Both P → Q and Q → P |
| `False` | Contradiction | No constructor supplies a proof of it |

Logical implication does not mean causation or a sequence in time. `P → Q` is a claim that rules out P holding while Q fails. It does not assert P, and it does not imply `Q → P`.

Suppose a rule says, “If someone is an administrator, they may edit.” Seeing permission to edit does not prove they are an administrator; another role might grant it. That is the difference between an implication and its converse.

## An implication proof, in ordinary words

Claim: if you have both P and Q, then you have Q and P.

1. Assume you are given evidence of P and Q.
2. Extract evidence of P.
3. Extract evidence of Q.
4. Combine them in the order Q, then P.

We did not assume the conclusion. We assumed the premise of an implication and showed how to produce its conclusion. That construction works whenever the premise is supplied.

Now compare “if P, then P.” Its proof is simply: assume evidence of P, and return that same evidence. You will write that pattern as `intro hP` followed by `exact hP`.

## Negation and contradiction

Lean's `¬ P` means `P → False`. If you have `hP : P` and `hNotP : ¬ P`, applying `hNotP` to `hP` produces `False`.

To prove `¬ (P ∧ ¬ P)`, assume someone supplies both P and its negation. Their two pieces of evidence contradict each other. That shows no such pair can exist.

Do not confuse `False : Prop` with `false : Bool`. `Bool` holds the two data values `true` and `false`. A proposition expresses a logical claim and may require reasoning rather than a Boolean calculation. Lean can decide some propositions computationally; it cannot decide every possible proposition by a general algorithm.

## “Every” versus “some”

| Notation | Meaning | Proof task |
| --- | --- | --- |
| `∀ n : Nat, R n` | R holds for every natural number | Work with arbitrary n, prove R n |
| `∃ n : Nat, R n` | Some natural number satisfies R | Choose a witness n and prove R n |

A **predicate** such as `R : Nat → Prop` assigns a proposition to each input. For example, it might express “n is at least ten.”

For “there is a natural number equal to `4 + 1`,” choose `5` as the witness. For “every natural number equals `4 + 1`,” no proof is possible in a consistent system: `0` is a counterexample. An example proves an existence claim, but normally not a universal claim.

Quantifier order matters:

```text
∀ n : Nat, ∃ m : Nat, n < m
```

You may choose a different `m` for each `n`; choosing `n + 1` works.

```text
∃ m : Nat, ∀ n : Nat, n < m
```

Now you must choose one `m` that is larger than every natural number. Choosing `n = m` defeats that claim. The second statement asks for something much stronger.

The official [quantifiers and equality chapter](https://lean-lang.org/theorem_proving_in_lean4/Quantifiers-and-Equality/) develops the corresponding proof rules.

## Equality is a claim too

`a = b` states that two expressions denote equal values. A proof `h : a = b` lets you replace an occurrence of one by the other in a suitable expression.

Equality is not assignment. Lean's `:=` introduces a definition or supplies its body. `=` appears in a proposition. A Boolean equality test is usually written `==`; that produces a `Bool` when the type supports it.

## Your turn

1. Translate “if the input is valid and permission is granted, the action is allowed” using three proposition names and parentheses.
2. Does `P ∨ Q` say that exactly one holds?
3. Which direction is missing if you have only `P → Q` but need `P ↔ Q`?
4. Explain why a single natural number with a property proves `∃ n, R n` but not generally `∀ n, R n`.
5. Explain the error in: “Every administrator can edit. Sam can edit. Therefore Sam is an administrator.”

**Ready to continue:** read `P ∧ Q → Q ∧ P` aloud and describe how to prove it before writing tactics.
