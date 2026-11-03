/-
Lane A MCA certificate: one-file, source-replayable abstraction.
This is a LOCAL predicate, NOT a proof of equivalence to rs-mca LD_sw.
Not compiled or Lean-kernel checked as of 2026-11-03.
All definitions are local: no missing Mca.* import or duplicate namespace declarations.
-/
import Mathlib

namespace McaSelfContained
open Polynomial

variable {F : Type*} [Field F] [Fintype F] [DecidableEq F]

def Explains (C : Set (F → F)) (S : Set F) (h : F → F) : Prop :=
  ∃ c ∈ C, ∀ x ∈ S, h x = c x

def Bad (C : Set (F → F)) (S : Set F)
    (f g : F → F) (z : F) : Prop :=
  Explains C S (fun x => f x + z * g x) ∧
    ¬ (Explains C S f ∧ Explains C S g)

def RSFunctions (D : Set F) (k : ℕ) : Set (F → F) :=
  {c | ∃ p : Polynomial F, p.natDegree < k ∧
    ∀ x ∈ D, c x = p.eval x}

theorem rs_inclusion (D : Set F) (k : ℕ) :
    RSFunctions D k ⊆ RSFunctions D (k + 1) := by
  intro c hc
  rcases hc with ⟨p, hp, he⟩
  exact ⟨p, by omega, he⟩

theorem deployed_bad_from_polynomial
    (D S : Set F) (k : ℕ) (f g : F → F) (z : F)
    (p : Polynomial F)
    (hdegree : p.natDegree < k)
    (hsupport : S ⊆ D)
    (hagree : ∀ x ∈ S, f x + z * g x = p.eval x)
    (hexclude : ¬ (Explains (RSFunctions D (k+1)) S f ∧
                    Explains (RSFunctions D (k+1)) S g)) :
    Bad (RSFunctions D k) S f g z := by
  constructor
  · refine ⟨(fun x => p.eval x), ?_, ?_⟩
    · exact ⟨p, hdegree, fun x hx => rfl⟩
    · exact hagree
  · intro h
    apply hexclude
    constructor
    · rcases h.1 with ⟨c, hc, he⟩
      exact ⟨c, rs_inclusion D k hc, he⟩
    · rcases h.2 with ⟨c, hc, he⟩
      exact ⟨c, rs_inclusion D k hc, he⟩

/-- Fixed f,g and domain D. Z is a Finset, so slopes are distinct.
The large support, deployed-degree witness, augmented noncontainment, and
strict slope count are separate premises, NOT results of the transfer lemma. -/
theorem finite_support_certificate
    (D : Set F) (k a : ℕ) (f g : F → F)
    (Z : Finset F) (support : F → Finset F)
    (witness : F → Polynomial F)
    (hsize : ∀ z ∈ Z, a ≤ (support z).card)
    (hdegree : ∀ z ∈ Z, (witness z).natDegree < k)
    (hsub : ∀ z ∈ Z, (support z : Set F) ⊆ D)
    (hagree : ∀ z ∈ Z, ∀ x ∈ support z,
      f x + z * g x = (witness z).eval x)
    (hexclude : ∀ z ∈ Z,
      ¬ (Explains (RSFunctions D (k+1)) (support z : Set F) f ∧
         Explains (RSFunctions D (k+1)) (support z : Set F) g))
    (hcount : 2^59 < Z.card) :
    (2^59 < Z.card) ∧
    (∀ z ∈ Z, a ≤ (support z).card ∧
      Bad (RSFunctions D k) (support z : Set F) f g z) := by
  refine ⟨hcount, ?_⟩
  intro z hz
  refine ⟨hsize z hz, ?_⟩
  exact deployed_bad_from_polynomial D (support z : Set F) k f g z
    (witness z) (hdegree z hz) (hsub z hz)
    (by
      intro x hx
      exact hagree z hz x hx)
    (hexclude z hz)

end McaSelfContained
