/- Small definitions shared by the lessons and exercises. No external packages. -/
namespace Course

def bump (n : Nat) : Nat := n + 1

def twice (n : Nat) : Nat := n + n

-- Walk over a list, counting one for every element.
def countItems : List Nat → Nat
  | [] => 0
  | _ :: xs => countItems xs + 1

-- Increment only when there is room below the limit.
def step (limit count : Nat) : Nat :=
  if count < limit then count + 1 else count

-- Apply step repeatedly. The recursive argument k gets smaller.
def run (limit : Nat) : Nat → Nat → Nat
  | 0, count => count
  | k + 1, count => step limit (run limit k count)

end Course
