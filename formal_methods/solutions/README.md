# Reference solutions

Open a solution only after attempting its exercise and reading a targeted hint. The learner files intentionally remain unfinished. There can be many correct proofs of the same statement.

| File | Reasoning to notice |
| --- | --- |
| [01_Warmup.lean](01_Warmup.lean) | `rfl` reduces definitions; `exact` supplies evidence already available |
| [02_Logic.lean](02_Logic.lean) | Proofs assemble, transform, or analyze logical evidence |
| [03_Equality.lean](03_Equality.lean) | Different equalities need rewriting, known theorems, or arithmetic |
| [04_Induction.lean](04_Induction.lean) | Every step uses the smaller case through `ih` |
| [05_SafeCounter.lean](05_SafeCounter.lean) | The repeated-run proof reuses the one-step contract |

The solutions use a separate namespace so they do not define the exercise theorems for you. The exercise files never import them.

Check all reference solutions from the project root:

```bash
bash scripts/check.sh solutions
```

When comparing, ask:

1. Does my proof establish exactly the same claim with the same assumptions?
2. Can I explain what each tactic does to the context or goal?
3. Can I close this file and reconstruct the argument tomorrow?

For `run_safe`, the base case uses the initial bound. The successor case passes the intermediate count and its induction hypothesis to `preserves_bound`. Its axiom listing may include standard Lean foundations; it should not include `sorryAx`.

Written assignments and the extension deliberately have no complete answer sheet. Bring your reasoning back for discussion.
