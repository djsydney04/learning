# Hints — open one at a time

[Course home](README.md) · [Labs](PRACTICE.md)

Try an exercise for about ten minutes before using a hint. These are strategy prompts; complete proofs are in `solutions/`. If your Markdown viewer does not collapse the sections, scroll only to the exercise you need.

<details>
<summary>W1–W3: equality by reducing definitions</summary>

Read `bump` in `Course/Models.lean`. Replace each call with its defining expression on paper. Does that make the two sides the same? The tactic for this kind of equality has three letters and was introduced in the basics lesson.

</details>

<details>
<summary>W4: the goal is already available</summary>

Compare the type of `hP` with the goal. Use the tactic that supplies complete evidence of exactly the requested type.

</details>

<details>
<summary>L1: two goals</summary>

`constructor` splits a conjunction goal into its left and right components. Which hypothesis has the required type in each branch?

</details>

<details>
<summary>L2: introduce, extract, rebuild</summary>

Introduce the implication's premise as `h`. Its components are `h.left` and `h.right`. The conclusion asks for them in the other order.

</details>

<details>
<summary>L3: start and end of the chain</summary>

After introducing evidence of P, apply `hPQ` to get Q. Feed that result to `hQR`. Alternatively, use `apply` to work backward from R.

</details>

<details>
<summary>L4: you have two possible sources of evidence</summary>

Use `cases h with` after introducing the disjunction premise. In the `inl hP` branch, the target is still `Q ∨ P`: which alternative can you prove? In `inr hQ`, choose the other alternative. See the branching example in lesson 04.

</details>

<details>
<summary>L5: negation is a function</summary>

Introduce the supposed conjunction. Its right component has type `P → False`; its left component has type P. Apply the former to the latter.

</details>

<details>
<summary>L6: choose before proving</summary>

What natural number could make `m = n + 1` true by definition? Use `exists` to supply it. Check whether any goal remains before adding another tactic.

</details>

<details>
<summary>E1: substitute equal inputs</summary>

Use the given equality `h` in a rewrite. No arithmetic about doubling is needed.

</details>

<details>
<summary>E2: search by the operation</summary>

Try `#check Nat.zero_add` in the file. It states the family of equalities you need. Supply `n` as its argument, or let `simp` use known simplification rules.

</details>

<details>
<summary>E3: reveal the arithmetic</summary>

Unfold `bump`. You should now see a goal involving `0`, `n`, `+ 1`, and `<`. The arithmetic tactic from lesson 04 handles it.

</details>

<details>
<summary>E4: use the assumption, not examples</summary>

`omega` can reason about this natural-number subtraction using `1 ≤ n`. Explain first why that assumption removes the bad case.

</details>

<details>
<summary>I1: match the recursive structure</summary>

Induct on `n`. The base case computes. In the successor case, expose `doubleRec`, replace the smaller call using `ih`, and rewrite multiplication by a successor. A simplifier list can include the definition, `ih`, and `Nat.mul_succ`.

</details>

<details>
<summary>I2: empty list, then a head and tail</summary>

Induct on `xs` with cases `nil` and `cons x xs ih`. The base case computes. In the cons case, both counting and length contribute one plus the tail's count. Simplify using `countItems` and the tail's induction hypothesis.

</details>

<details>
<summary>C1: evaluate the condition symbolically</summary>

No natural number is less than itself. `simp [step]` knows that fact and can reduce the `if`.

</details>

<details>
<summary>C2: tell the simplifier which branch applies</summary>

Unfolding `step` reveals a condition that is exactly your hypothesis `h`. Include both `step` and `h` in the simplifier's list.

</details>

<details>
<summary>C3: two branches with different evidence</summary>

Use `unfold step` and `split`. In the first branch, combine strict inequality with natural-number arithmetic. In the second, the result is the original count and your input hypothesis proves the goal.

</details>

<details>
<summary>C4: unchanged or increased</summary>

Again expose and split the conditional. The first branch is arithmetic. The second is reflexivity of `≤`; `Nat.le_refl count` supplies that evidence. `rfl` is the equality tactic, so use the order theorem here.

</details>

<details>
<summary>C5: reuse a proven contract</summary>

Induct on `steps`. At zero the input bound suffices. At `k + 1`, the intermediate count is `run limit k count`, and `ih` proves it is within the limit. Feed those arguments to `preserves_bound`. Lean can unfold the recursive call when matching the result to the goal.

</details>
