import Course.Models
import Std.Tactic

namespace Solutions.SafeCounter
open Course

theorem at_limit (limit : Nat) : step limit limit = limit := by
  simp [step]

theorem advances (limit count : Nat) (h : count < limit) :
    step limit count = count + 1 := by
  simp [step, h]

theorem preserves_bound (limit count : Nat) (h : count ≤ limit) :
    step limit count ≤ limit := by
  unfold step
  split
  · omega
  · exact h

theorem never_decreases (limit count : Nat) : count ≤ step limit count := by
  unfold step
  split
  · omega
  · exact Nat.le_refl count

theorem run_safe (limit count steps : Nat) (h : count ≤ limit) :
    run limit steps count ≤ limit := by
  induction steps with
  | zero => exact h
  | succ k ih =>
    exact preserves_bound limit (run limit k count) ih

#print axioms run_safe

end Solutions.SafeCounter
