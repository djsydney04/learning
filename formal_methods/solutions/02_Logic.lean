namespace Solutions.Logic

theorem pair_evidence (P Q : Prop) (hP : P) (hQ : Q) : P ∧ Q := by
  constructor
  · exact hP
  · exact hQ

theorem swap_evidence (P Q : Prop) : P ∧ Q → Q ∧ P := by
  intro h
  constructor
  · exact h.right
  · exact h.left

theorem chain (P Q R : Prop) (hPQ : P → Q) (hQR : Q → R) : P → R := by
  intro hP
  exact hQR (hPQ hP)

theorem swap_alternatives (P Q : Prop) : P ∨ Q → Q ∨ P := by
  intro h
  cases h with
  | inl hP =>
    right
    exact hP
  | inr hQ =>
    left
    exact hQ

theorem cannot_have_both (P : Prop) : ¬ (P ∧ ¬ P) := by
  intro h
  exact h.right h.left

theorem next_exists (n : Nat) : ∃ m : Nat, m = n + 1 := by
  exists n + 1

end Solutions.Logic
