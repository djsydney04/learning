# My formal methods journal

Write your answers here. Imperfect explanations are useful: they reveal what to revisit.

## First session

Date:

1. One evaluated input versus a proof for every input:

   My answer:

2. How a checked proof could describe the wrong application behavior:

   My answer:

3. What a precondition means:

   My answer:

4. Why `rfl` works for W2:

   My answer:

5. My checker output or setup issue:

```text
Paste it here.
```

## Specifications before code

- Array lookup precondition:
- A bad implementation allowed by “the result is sorted”:
- A stronger sorting specification, including repeated elements:
- My own function and its intended behavior:
- Input types and preconditions:
- Two postconditions:

## Logic in my own words

- A proposition versus evidence of it:
- An implication versus its converse:
- Why L4 needs two cases:
- How L5 reaches a contradiction:
- Why quantifier order changes meaning:

## Counterexamples

False claim:

Input that breaks it:

Actual result:

Corrected claim or missing assumption:

## Induction plans

| Part | I1 | I2 |
| --- | --- | --- |
| Base-case input | | |
| Base-case equality | | |
| Induction hypothesis | | |
| Step-case equality | | |

Why the step does not assume its own conclusion:

## Verified counter

- Initial-state assumption:
- Meaning of `ih` in C5:
- Property that failed after changing `<` to `≤`:
- Concrete counterexample to the changed program:
- Confirmation that I restored `<` and rechecked:
- A behavior the model does not cover:
- My extension's specification and proof plan:

## A proof I got stuck on

Theorem:

```lean
-- Paste the declaration and your attempt here.
```

Current context and goal:

```text
Paste Lean's proof state here.
```

The reasoning step I intended:

Lean's message:

What finally made it work:
