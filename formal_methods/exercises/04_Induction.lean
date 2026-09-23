import Course.Models

namespace Exercises.Induction
open Course

-- I1: Practice your own recursive definition: count by twos.
def doubleRec : Nat → Nat
  | 0 => 0
  | n + 1 => doubleRec n + 2

-- Nat.mul_succ describes multiplication by a successor.
theorem doubleRec_eq (n : Nat) : doubleRec n = 2 * n := by
  sorry

-- I2: Use induction xs with nil / cons x xs ih.
theorem countItems_eq_length (xs : List Nat) : countItems xs = xs.length := by
  sorry

end Exercises.Induction
