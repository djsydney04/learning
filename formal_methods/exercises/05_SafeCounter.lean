import Course.Models
import Std.Tactic

namespace Exercises.SafeCounter
open Course

-- C1: No room remains at the limit.
theorem at_limit (limit : Nat) : step limit limit = limit := by
  sorry

-- C2: If there is room, exactly one is added.
theorem advances (limit count : Nat) (h : count < limit) :
    step limit count = count + 1 := by
  sorry

-- C3: Preserve the invariant. The starting-state assumption matters!
theorem preserves_bound (limit count : Nat) (h : count ≤ limit) :
    step limit count ≤ limit := by
  sorry

-- C4: The count never goes backwards, including for invalid starting states.
theorem never_decreases (limit count : Nat) : count ≤ step limit count := by
  sorry

-- C5: From a safe starting state, any finite number of steps is safe.
-- Use induction steps and your preserves_bound theorem.
theorem run_safe (limit count steps : Nat) (h : count ≤ limit) :
    run limit steps count ≤ limit := by
  sorry

end Exercises.SafeCounter
