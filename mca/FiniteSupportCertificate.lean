/-
Lane A: support-cardinality audit and strengthened local finite certificate.
SOURCE PROPOSAL ONLY: not compiled or Lean-kernel checked.
Depends on mca/DomainPolynomialTransfer.lean at commit 020bbe36...
-/ 
import Mathlib
import Mca.DomainPolynomialTransfer

namespace McaFiniteCertificate
open McaDeployedTransfer McaDomainTransfer
open Polynomial

variable {F : Type*} [Field F] [Fintype F] [DecidableEq F]

/-- The slope set is a Finset (hence distinct by construction).
Every slope has its own support of at least a points, but f and g are fixed.
This is a local-model certificate, NOT yet an identification with rs-mca LD_sw. -/
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
         Explains (RSFunctions D (k+1)) (support z : Set F) g)) :
    ∀ z ∈ Z, a ≤ (support z).card ∧
      Bad (RSFunctions D k) (support z : Set F) f g z := by
  intro z hz
  refine ⟨hsize z hz, ?_⟩
  exact deployed_bad_from_polynomial D (support z : Set F) k f g z
    (witness z) (hdegree z hz) (hsub z hz)
    (by
      intro x hx
      exact hagree z hz x hx)
    (hexclude z hz)

/-- A separate finite-set counting assumption is required; the transfer
    theorem alone does not prove |Z| > 2^59. -/
theorem many_distinct_local_bad_slopes
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
    2^59 < (Z.filter (fun z =>
      a ≤ (support z).card ∧
      Bad (RSFunctions D k) (support z : Set F) f g z)).card := by
  have hall := finite_support_certificate D k a f g Z support witness
    hsize hdegree hsub hagree hexclude
  have heq : Z.filter (fun z =>
      a ≤ (support z).card ∧
      Bad (RSFunctions D k) (support z : Set F) f g z) = Z := by
    apply Finset.filter_true_of_mem
    intro z hz
    exact hall z hz
  rw [heq]
  exact hcount

end McaFiniteCertificate
