# 03 — Read and write your first Lean

[Course home](../README.md) · Previous: [Logic](02_LOGIC.md) · Next: [Building proofs](04_PROOFS.md)

## A function, one piece at a time

Here is a complete definition and a few commands:

```lean
def addOne (n : Nat) : Nat := n + 1

#check addOne
#eval addOne 6
```

| Piece | Meaning |
| --- | --- |
| `def` | Introduce a definition |
| `addOne` | Its name |
| `(n : Nat)` | An input named n, of type Nat |
| `: Nat` | The result's type |
| `:= n + 1` | The expression defining the result |

`#check` asks for an expression's type. `#eval` runs an expression and prints a result. The evaluation above prints `7`. Function application uses spaces: `addOne 6`, rather than requiring `addOne(6)`.

Values are immutable. This definition describes a function from inputs to outputs; it does not update a variable `n`. For a function with several inputs, you will see `step limit count`.

`Nat` contains nonnegative whole numbers of arbitrary size. `Int` also includes negative integers. As a result, natural-number subtraction behaves differently from integer subtraction:

```lean
#eval (0 : Nat) - 1  -- 0: subtraction stops at zero
#eval (0 : Int) - 1  -- -1
```

Types are part of the problem, not merely annotations for the compiler. “Subtract one, then add one” needs a precondition for `Nat`.

## A theorem has a type too

```lean
theorem seven_is_seven : (7 : Nat) = 7 := by
  rfl
```

The proposition after the colon is the claim. `:= by` begins a proof written with **tactics**, commands that construct proof evidence. `rfl` closes an equality when both sides are the same under Lean's notion of definitional equality, which includes reducing definitions.

The numeral example is intentionally easy. Now try a variable:

```lean
def plusTwo (n : Nat) : Nat := n + 2

theorem plusTwo_spec (n : Nat) : plusTwo n = n + 2 := by
  rfl
```

There is no loop over numbers here. The function definition makes the left side reduce to the right side for an arbitrary `n`.

`rfl` is not a general mathematics solver. Equal expressions do not always reduce to the same expression by definition. Some equalities require another theorem, rewriting, or induction.

## Data versus proof evidence

Compare these two declarations:

```lean
def keepNumber (n : Nat) : Nat := n

theorem keepEvidence (P : Prop) (hP : P) : P := by
  exact hP
```

`keepNumber` returns a number it received. `keepEvidence` returns evidence it received. The tactic `exact` finishes the current goal by supplying a term of the required type.

The second theorem does not manufacture evidence of an arbitrary proposition. It explicitly requires `hP : P`. If you remove that hypothesis, you are asking for a much stronger and generally impossible result.

You will see both `theorem` and `example`. A theorem has a name you can reuse. An example is an unnamed declaration that Lean still checks.

## Read a proof state

A proof state might display:

```text
P Q : Prop
hP : P
hPQ : P → Q
⊢ Q
```

Above `⊢` is the context: variables and evidence you may use. After it is the current goal. Read this as: “Given evidence of P and a way to turn P into Q, produce evidence of Q.”

The expression `hPQ hP` does that. You can write `exact hPQ hP`. If you write `exact hP`, Lean reports a type mismatch: you supplied evidence of P when it needed Q.

An error is useful information about the current task. Read the expected type, the actual type, and the available hypotheses before trying another tactic.

## Editing conventions

- `--` starts a line comment. `/- ... -/` encloses a block comment.
- Indent lines inside a `by` proof, usually by two spaces.
- `namespace` groups names; `open Course` lets you use `bump` instead of `Course.bump`.
- `import Course.Models` loads our definitions. Run `lake build` first so local imports are available.
- `sorry` temporarily fills a proof hole and produces a warning. It supplies no proof you should count as complete.

In the Lean extension, type a backslash sequence followed by space or Tab to enter many symbols:

| Type | Get |
| --- | --- |
| `\to` | `→` |
| `\and` | `∧` |
| `\or` | `∨` |
| `\not` | `¬` |
| `\forall` | `∀` |
| `\exists` | `∃` |
| `\le` | `≤` |

Copying symbols is also fine. Unicode entry should not be the hard part of learning proofs.

## Your turn

Complete **W1–W4** in [01_Warmup.lean](../exercises/01_Warmup.lean), then run:

```bash
bash scripts/check.sh 01
```

For each proof, state whether you supplied existing evidence or used equality by computation. Explain why `#eval` and `rfl` have different jobs.

Optional reading: [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/) introduces the programming side in more depth.
