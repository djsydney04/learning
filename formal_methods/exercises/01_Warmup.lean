import Course.Models

namespace Exercises.Warmup
open Course

-- Read lessons/03_LEAN_BASICS.md. Replace each sorry with your proof.
-- W1: First evaluate bump 4 using #eval, then prove its exact result.
theorem bump_four : bump 4 = 5 := by
  sorry

-- W2: A variable stands for an arbitrary natural number.
theorem bump_unfolds (n : Nat) : bump n = n + 1 := by
  sorry

-- W3: Unfolding can compute through nested function calls.
theorem bump_twice (n : Nat) : bump (bump n) = (n + 1) + 1 := by
  sorry

-- W4: A proposition and a proof of that proposition have different roles.
theorem return_evidence (P : Prop) (hP : P) : P := by
  sorry

end Exercises.Warmup
