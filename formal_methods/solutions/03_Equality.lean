import Course.Models
import Std.Tactic

namespace Solutions.Equality
open Course

theorem equal_inputs (a b : Nat) (h : a = b) : twice a = twice b := by
  rw [h]

theorem left_zero (n : Nat) : 0 + n = n := by
  exact Nat.zero_add n

theorem bump_positive (n : Nat) : 0 < bump n := by
  unfold bump
  omega

theorem subtract_then_restore (n : Nat) (h : 1 ≤ n) : n - 1 + 1 = n := by
  omega

end Solutions.Equality
