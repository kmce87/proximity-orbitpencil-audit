/-
Lane A: a standalone finite-set quantifier bridge to the local LD_sw predicate.
SOURCE PROPOSAL, NOT COMPILED. This deliberately does not construct a KoalaBear
instance, establish field/domain equivalence, or claim independent acceptance.
-/
import Mathlib

namespace McaBridgeQuantifiers

variable {F : Type*} [Field F] [Fintype F] [DecidableEq F]

def Explains (C : Set (F → F)) (S : Set F) (h : F → F) : Prop :=
  ∃ c ∈ C, ∀ x ∈ S, h x = c x

def SupportBad (C : Set (F → F)) (S : Set F)
    (f g : F → F) (z : F) : Prop :=
  Explains C S (fun x => f x + z * g x) ∧
    ¬ (Explains C S f ∧ Explains C S g)

/-- This is the *local* support-wise slope predicate corresponding to
the rs-mca M2 bridge, not a proof that a particular concrete RS domain
has been encoded faithfully. -/
def LocalBadSlope (C : Set (F → F)) (D : Set F) (a : ℕ)
    (f g : F → F) (z : F) : Prop :=
  ∃ S : Finset F, (S : Set F) ⊆ D ∧
    a ≤ S.card ∧ SupportBad C (S : Set F) f g z

def LocalNumerator (C : Set (F → F)) (D : Set F) (a : ℕ)
    (f g : F → F) : ℕ :=
  (Finset.univ.filter (fun z => LocalBadSlope C D a f g z)).card

/-- Explicitly turn per-slope witnesses for one fixed f,g into a lower
bound on the cardinality of distinct support-wise bad slopes.
The distinctness comes from Z being a Finset; no slope counting is
proved unless the caller supplies the size of Z. -/
theorem distinct_witnesses_lower_bound
    (C : Set (F → F)) (D : Set F) (a : ℕ)
    (f g : F → F) (Z : Finset F)
    (support : F → Finset F)
    (hsub : ∀ z ∈ Z, (support z : Set F) ⊆ D)
    (hsize : ∀ z ∈ Z, a ≤ (support z).card)
    (hbad : ∀ z ∈ Z, SupportBad C (support z : Set F) f g z) :
    Z.card ≤ LocalNumerator C D a f g := by
  unfold LocalNumerator
  apply Finset.card_le_card
  intro z hz
  apply Finset.mem_filter.mpr
  constructor
  · exact Finset.mem_univ z
  · exact ⟨support z, hsub z hz, hsize z hz, hbad z hz⟩

/-- The strict >2^59 numerator conclusion is only conditional on the
actual slope count and actual witness premises. -/
theorem numerator_gt_two_pow_59
    (C : Set (F → F)) (D : Set F) (a : ℕ)
    (f g : F → F) (Z : Finset F)
    (support : F → Finset F)
    (hsub : ∀ z ∈ Z, (support z : Set F) ⊆ D)
    (hsize : ∀ z ∈ Z, a ≤ (support z).card)
    (hbad : ∀ z ∈ Z, SupportBad C (support z : Set F) f g z)
    (hcount : 2^59 < Z.card) :
    2^59 < LocalNumerator C D a f g := by
  have hle := distinct_witnesses_lower_bound C D a f g Z support
    hsub hsize hbad
  omega

end McaBridgeQuantifiers
