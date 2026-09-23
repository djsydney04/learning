# Your first session

Today's goal: run Lean and complete four small proofs. Leave the later exercises for another session.

## 1. Get the idea first — 10 minutes

Read [the formal methods primer](lessons/01_FORMAL_METHODS.md). Then write short answers in [your journal](JOURNAL.md):

1. What is the difference between checking `bump 4 = 5` and proving `bump n = n + 1` for every natural number `n`?
2. Why could a checked proof still describe the wrong behavior for a real application?
3. In your own words, what is a precondition?

Do not aim for textbook wording. Explain it as if to a programmer who has never used Lean.

## 2. Make Lean run — 10–25 minutes, plus downloads

Follow [setup](lessons/00_SETUP.md). Open the entire `formal_methods` folder in VS Code.

In its terminal, run:

```bash
bash scripts/check.sh examples
```

You should see `PASS: examples`. Open [the examples file](Course/Examples.lean), put your cursor inside `identity`, and find the assumptions and goal in Lean's Infoview.

If installation takes longer, the setup guide has a browser route. Keep the local exercise checks for when the project is installed.

## 3. Make a prediction — 5 minutes

Read [Lean basics](lessons/03_LEAN_BASICS.md). Open [01_Warmup.lean](exercises/01_Warmup.lean).

Before changing anything, predict what this will print, then add it after `open Course`:

```lean
#eval bump 4
```

Change `4` to `0`, then to `12`. Explain why three successful evaluations still do not establish a claim about every input.

## 4. Complete W1–W4 — 15–25 minutes

Replace one `sorry` at a time. You need just `rfl` and `exact` for this file; the basics lesson explains both.

After each edit, inspect Lean's feedback. After all four proofs are done, run:

```bash
bash scripts/check.sh 01
```

Do not use the strict checker as a per-proof progress bar: it reports the other unfinished proofs in the same file too. Use the editor's goals while you work.

If stuck for about ten minutes, open only the corresponding entry in [HINTS.md](HINTS.md). If you use a complete solution, close it and reproduce the proof later from the statement.

## 5. Check that you learned it

- [ ] I can explain what `n : Nat` means.
- [ ] I can distinguish a proposition `P` from evidence `hP : P`.
- [ ] I know why `sorry` is unfinished work.
- [ ] All four Warmup proofs pass the strict check.
- [ ] I can explain why `rfl` works for W2 without trying many numbers.

**For our next conversation:** share your W1–W4 attempts, the checker output, and whatever you wrote for the three questions. If you get stuck, share the exact goal and error message. We can work through your reasoning together and choose the next step at your pace.
