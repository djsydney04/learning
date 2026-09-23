import Course.Models
import Std.Tactic

namespace Course.Examples

#check (5 : Nat)
#check (5 = 5)
#eval bump 8

theorem concrete : bump 8 = 9 := by
  rfl

theorem identity (P : Prop) : P → P := by
  intro hP
  exact hP

theorem duplicate (P : Prop) : P → P ∧ P := by
  intro hP
  constructor
  · exact hP
  · exact hP

theorem implication_chain (P Q R : Prop)
    (hPQ : P → Q) (hQR : Q → R) : P → R := by
  intro hP
  apply hQR
  exact hPQ hP

theorem rewrite_input (a b : Nat) (h : a = b) : bump a = bump b := by
  rw [h]

theorem twice_unfolds (n : Nat) : twice n = n + n := by
  rfl

theorem bump_grows (n : Nat) : n < bump n := by
  unfold bump
  omega

-- A fresh recursive definition for the induction lesson.
def climb : Nat → Nat
  | 0 => 0
  | n + 1 => climb n + 1

theorem climb_eq (n : Nat) : climb n = n := by
  induction n with
  | zero => rfl
  | succ k ih =>
    simp [climb, ih]

-- This is a proof of a specific counterexample, not just printed output.
theorem decrement_counterexample : (0 : Nat) - 1 + 1 ≠ 0 := by
  decide

theorem bad_initial_state : step 3 8 = 8 := by
  rfl

end Course.Examples
