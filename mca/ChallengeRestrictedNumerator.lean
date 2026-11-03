/-
Lane A: challenge-set restriction of the local support-wise numerator.
SOURCE PROPOSAL ONLY: not compiled or kernel checked.
The upstream rs-mca manuscript uses B^MCA_{C,Gamma}; the earlier local
bridge counts all F slopes.  No assertion is made that the concrete
KoalaBear challenge Gamma is proper or that the lift lies outside it.
-/
import Mathlib

namespace McaChallengeRestriction

variable {F : Type*} [Field F] [Fintype F] [DecidableEq F]

def Explains (C : Set (F → F)) (S : Set F) (h : F → F) : Prop :=
  ∃ c ∈ C, ∀ x ∈ S, h x = c x

def BadOnSupport (C : Set (F → F)) (S : Set F)
    (f g : F → F) (z : F) : Prop :=
  Explains C S (fun x => f x + z * g x) ∧
    ¬ (Explains C S f ∧ Explains C S g)

def BadSlope (C : Set (F → F)) (D : Set F) (a : ℕ)
    (f g : F → F) (z : F) : Prop :=
  ∃ S : Finset F, (S : Set F) ⊆ D ∧
    a ≤ S.card ∧ BadOnSupport C (S : Set F) f g z

noncomputable def RestrictedNumerator (C : Set (F → F)) (D : Set F)
    (a : ℕ) (f g : F → F) (Gamma : Finset F) : ℕ := by
  classical
  exact (Gamma.filter (BadSlope C D a f g)).card

/-- A fixed line plus a set of certified, *eligible* distinct slopes
lower-bounds the numerator restricted to the challenge set Gamma. -/
theorem certified_subset_lower_bound
    (C : Set (F → F)) (D : Set F) (a : ℕ)
    (f g : F → F) (Gamma Z : Finset F)
    (hgamma : Z ⊆ Gamma)
    (hbad : ∀ z ∈ Z, BadSlope C D a f g z) :
    Z.card ≤ RestrictedNumerator C D a f g Gamma := by
  classical
  unfold RestrictedNumerator
  apply Finset.card_le_card
  intro z hz
  apply Finset.mem_filter.mpr
  exact ⟨hgamma hz, hbad z hz⟩

/-- The all-field count is only an upper bound for a restricted numerator;
the reverse implication is not available without Gamma membership. -/
theorem restricted_le_all
    (C : Set (F → F)) (D : Set F) (a : ℕ)
    (f g : F → F) (Gamma : Finset F) :
    RestrictedNumerator C D a f g Gamma ≤
      RestrictedNumerator C D a f g Finset.univ := by
  classical
  unfold RestrictedNumerator
  apply Finset.card_le_card
  intro z hz
  apply Finset.mem_filter.mpr
  exact ⟨Finset.mem_univ z, (Finset.mem_filter.mp hz).2⟩

end McaChallengeRestriction
