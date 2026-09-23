import Course.Models

namespace Exercises.Logic

-- L1: Build a conjunction from two pieces of evidence.
theorem pair_evidence (P Q : Prop) (hP : P) (hQ : Q) : P ∧ Q := by
  sorry

-- L2: Use h.left and h.right.
theorem swap_evidence (P Q : Prop) : P ∧ Q → Q ∧ P := by
  sorry

-- L3: Compose two implications.
theorem chain (P Q R : Prop) (hPQ : P → Q) (hQR : Q → R) : P → R := by
  sorry

-- L4: Analyze both ways that an inclusive 'or' can hold.
theorem swap_alternatives (P Q : Prop) : P ∨ Q → Q ∨ P := by
  sorry

-- L5: Negation means a route to False.
theorem cannot_have_both (P : Prop) : ¬ (P ∧ ¬ P) := by
  sorry

-- L6: Supply a witness, then prove its property.
theorem next_exists (n : Nat) : ∃ m : Nat, m = n + 1 := by
  sorry

end Exercises.Logic
