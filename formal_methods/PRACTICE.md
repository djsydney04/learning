# The labs

[Course home](README.md) · [Hints](HINTS.md) · [Journal](JOURNAL.md)

Work in `exercises/`. Keep the theorem statements unchanged and replace only their proof bodies. You may add `#eval`, `#check`, scratch examples, and explanatory comments. Do not finish a task by introducing an `axiom`, using `sorry` or `admit`, or assuming the desired conclusion.

For each theorem: translate it into English, predict the argument, try it in Lean, then explain the checked proof. You may use any valid proof after making an honest attempt with the concepts for that lab. A short automated proof is useful only if you understand the claim it establishes.

## Lab 01 — First contact

Read [Lean basics](lessons/03_LEAN_BASICS.md). Edit [01_Warmup.lean](exercises/01_Warmup.lean).

| Exercise | Your task | Main idea |
| --- | --- | --- |
| W1 | Show bumping four gives five | Compute an equality |
| W2 | State bump's result for arbitrary n | Unfold a definition conceptually |
| W3 | Reason about two nested calls | Reduce definitions more than once |
| W4 | Return supplied evidence of P | Use a hypothesis |

Run `bash scripts/check.sh 01`. Then change the expected answer in W1 from five to six, observe Lean's complaint, and **restore the original statement**. Describe why the original proof stops working.

Your checkpoint: four checked proofs and a sentence explaining each. This is enough for a first session; use the discussion prompts in [START_HERE.md](START_HERE.md) when you want to work through your results together.

## Lab 02 — Logic as evidence

Read [Logic](lessons/02_LOGIC.md) and the first part of [Building proofs](lessons/04_PROOFS.md). Edit [02_Logic.lean](exercises/02_Logic.lean).

| Exercise | Your task | Main idea |
| --- | --- | --- |
| L1 | Assemble P and Q | Conjunction introduction |
| L2 | Swap the components of a conjunction | Use and rebuild evidence |
| L3 | Follow two implication rules | Function application / apply |
| L4 | Swap the alternatives of a disjunction | Handle both cases |
| L5 | Rule out P together with not-P | Produce a contradiction |
| L6 | Exhibit a number equal to n + 1 | Choose an existential witness |

Run `bash scripts/check.sh 02`.

Written task: for L4, explain why choosing `left` immediately after introducing the premise cannot by itself handle all possible evidence of `P ∨ Q`. For L5, identify which expression represents a function to `False`.

## Lab 03 — Equality and a false conjecture

Read the rest of [Building proofs](lessons/04_PROOFS.md). Edit [03_Equality.lean](exercises/03_Equality.lean).

| Exercise | Your task | Main idea |
| --- | --- | --- |
| E1 | Equal inputs give equal doubled outputs | Rewrite |
| E2 | Zero on the left of addition changes nothing | Use an existing theorem |
| E3 | Bumping a natural number gives a positive result | Unfold, then arithmetic |
| E4 | Subtracting one then restoring it works when n ≥ 1 | Use a necessary assumption |

Run `bash scripts/check.sh 03`.

Written task: find a counterexample to “for every natural number n, `n * n > n`.” Give a concrete input and evaluate both sides. You are not asked to prove this false claim. Can you state a plausible corrected claim? No Lean proof of that correction is required yet.

## Lab 04 — Infinite families, finite proofs

Read [Induction](lessons/05_INDUCTION.md). Edit [04_Induction.lean](exercises/04_Induction.lean).

Before typing a tactic, fill in this table for each exercise in your journal:

| Part | I1: recursive doubling | I2: list counting |
| --- | --- | --- |
| Base-case input | | |
| Base-case equality | | |
| Induction hypothesis | | |
| Step-case equality | | |

Then prove I1 and I2 and run `bash scripts/check.sh 04`.

Experiment: change I1's recursive increment from `2` to `3`. Recheck and describe which step no longer matches the specification. Restore `2` and recheck before continuing.

## Lab 05 — A program contract

Read [Verified program](lessons/06_VERIFIED_PROGRAM.md). Edit [05_SafeCounter.lean](exercises/05_SafeCounter.lean).

Prove C1–C4 first. Use C3, rather than redoing its arithmetic, in the induction proof for C5. Run `bash scripts/check.sh 05`.

### Find a missing assumption

The stronger-looking claim `step limit count ≤ limit` with no assumption on the initial count is false. Find concrete values that demonstrate this. Evaluate the function, and explain why the original C3 theorem remains meaningful.

### Make a bug visible

After your proofs pass:

1. Note the original `step` definition in [Course/Models.lean](Course/Models.lean).
2. Change its condition from `count < limit` to `count ≤ limit`.
3. Run `bash scripts/check.sh 05` again. Identify a failed property; predict a counterexample before evaluating it.
4. Explain in words why allowing an increment **at** the limit is wrong.
5. Restore `<` and rerun the checker until it passes.

You changed the implementation while keeping the contracts. A failed proof alerts you that the old justification no longer applies; the concrete counterexample establishes that this particular change violates the contract. A failed tactic alone would not always establish a bug, because a correct change might merely require a different proof.

### Add something of your own

Create `exercises/06_Extension.lean` yourself, starting with:

```lean
import Course.Models
import Std.Tactic

namespace Exercises.Extension
open Course

-- Add your definition and theorems here.

end Exercises.Extension
```

Choose one:

- **Small:** define a reset operation that returns zero. Prove its result is within every natural-number limit. Explain why this is not a suitable replacement for incrementing.
- **Medium:** prove a safe count is unchanged by `step` if and only if it equals the limit. Write the precise statement before the proof. Remember that `↔` needs two directions.
- **Stretch:** prove enough repeated steps reach the limit when starting at zero. Specify how many steps are sufficient and prove your claim by a strategy you can explain.

Check your extension directly after building the project:

```bash
lake build
lake env lean -DwarningAsError=true exercises/06_Extension.lean
```

The `all` checker also includes any new `.lean` file in `exercises/`. The numbered shortcuts are provided for 01–05 only.

## Finish the course

Run `bash scripts/check.sh all`, then answer without looking at the lessons:

1. What is the exact assumption in the counter's safety theorem?
2. Why is “returns a number no greater than the limit” too weak by itself?
3. What does the induction hypothesis in C5 assert?
4. Why can Lean accept an unfinished file with warnings?
5. Name a real-world behavior this counter model leaves out.
6. Describe one place in your own programming where a precise contract would help.

Bring back your proof files, the checker output, and any explanation you are unsure about. If you get stuck, include the theorem, the current hypotheses and goal, your attempted step, and Lean's exact message.
