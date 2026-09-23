import Course.Models

namespace Solutions.Induction
open Course

def doubleRec : Nat → Nat
  | 0 => 0
  | n + 1 => doubleRec n + 2

theorem doubleRec_eq (n : Nat) : doubleRec n = 2 * n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    simp [doubleRec, ih, Nat.mul_succ]

theorem countItems_eq_length (xs : List Nat) : countItems xs = xs.length := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp [countItems, ih]

end Solutions.Induction
