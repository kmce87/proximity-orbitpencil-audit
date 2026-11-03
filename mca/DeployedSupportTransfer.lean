/-
Lane A: abstract support-wise MCA transfer, independent of polynomial encoding.
This file is a proposed Lean 4.34 lemma, NOT yet compiled/kernel checked.
A degree-<k explaining witness plus degree-<k+1 exclusion transfers
from augmented RS[D,k+1] to deployed RS[D,k].
-/
import Mathlib

namespace McaDeployedTransfer

variable {D F : Type*} [Field F]
variable (small large : Set (D → F)) (S : Set D)
variable (f g : D → F) (z : F)

def Explains (C : Set (D → F)) (S : Set D) (h : D → F) : Prop :=
  ∃ c ∈ C, ∀ x ∈ S, h x = c x

def Bad (C : Set (D → F)) (S : Set D)
    (f g : D → F) (z : F) : Prop :=
  Explains C S (fun x => f x + z * g x) ∧
    ¬ (Explains C S f ∧ Explains C S g)

/-- Transfer works with an explaining polynomial from the SMALL code and
noncontainment certified against the LARGE code. Merely knowing that the
line is explained in the large code would NOT suffice. -/
theorem bad_of_asymmetric_witness
    (hsub : small ⊆ large)
    (hsmall : Explains small S (fun x => f x + z * g x))
    (hlarge : ¬ (Explains large S f ∧ Explains large S g)) :
    Bad small S f g z := by
  constructor
  · exact hsmall
  · intro h
    apply hlarge
    constructor
    · obtain ⟨c, hc, he⟩ := h.1
      exact ⟨c, hsub hc, he⟩
    · obtain ⟨c, hc, he⟩ := h.2
      exact ⟨c, hsub hc, he⟩

/-- The fixed line and distinct slope set transfer pointwise, preserving
the quantifier order: one fixed f,g; for each slope an existential support. -/
theorem fixed_line_transfer
    (hsub : small ⊆ large)
    (Z : Finset F)
    (support : F → Set D)
    (hexplain : ∀ z ∈ Z, Explains small (support z)
      (fun x => f x + z * g x))
    (hexclude : ∀ z ∈ Z,
      ¬ (Explains large (support z) f ∧
         Explains large (support z) g)) :
    ∀ z ∈ Z, Bad small (support z) f g z := by
  intro z hz
  exact bad_of_asymmetric_witness small large (support z) f g z
    hsub (hexplain z hz) (hexclude z hz)

end McaDeployedTransfer
