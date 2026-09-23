import Course.Models
import Std.Tactic

namespace Exercises.Equality
open Course

-- E1: Rewrite using the equality hypothesis.
theorem equal_inputs (a b : Nat) (h : a = b) : twice a = twice b := by
  sorry

-- E2: Use the existing theorem Nat.zero_add, or simp.
theorem left_zero (n : Nat) : 0 + n = n := by
  sorry

-- E3: Expose bump before doing arithmetic.
theorem bump_positive (n : Nat) : 0 < bump n := by
  sorry

-- E4: Natural-number subtraction needs this precondition.
theorem subtract_then_restore (n : Nat) (h : 1 ≤ n) : n - 1 + 1 = n := by
  sorry

end Exercises.Equality
