import Course.Models

namespace Solutions.Warmup
open Course

theorem bump_four : bump 4 = 5 := by
  rfl

theorem bump_unfolds (n : Nat) : bump n = n + 1 := by
  rfl

theorem bump_twice (n : Nat) : bump (bump n) = (n + 1) + 1 := by
  rfl

theorem return_evidence (P : Prop) (hP : P) : P := by
  exact hP

end Solutions.Warmup
