/-
Lane A: proposed domain-level asymmetric transfer, Lean 4.34 / Mathlib.
NOT COMPILED OR KERNEL CHECKED. This explicitly requires a degree < k
explaining polynomial; a degree <= k polynomial alone is insufficient.
-/ 
import Mathlib
import McaDeployedTransfer

namespace McaDomainTransfer

open Polynomial McaDeployedTransfer

variable {F : Type*} [Field F]

def RSFunctions (D : Set F) (k : ℕ) : Set (F → F) :=
  { c | ∃ p : Polynomial F, p.natDegree < k ∧
      ∀ x ∈ D, c x = p.eval x }

theorem rs_inclusion (D : Set F) (k : ℕ) :
    RSFunctions D k ⊆ RSFunctions D (k + 1) := by
  intro c hc
  rcases hc with ⟨p, hp, he⟩
  exact ⟨p, by omega, he⟩

/-- The polynomial witness must lie in deployed RS[D,k].
The exclusion is checked against the larger auxiliary RS[D,k+1].
The support can depend on z; f and g cannot. -/
theorem deployed_bad_from_polynomial
    (D S : Set F) (k : ℕ) (f g : F → F) (z : F)
    (p : Polynomial F)
    (hdegree : p.natDegree < k)
    (hsupport : S ⊆ D)
    (hagree : ∀ x ∈ S, f x + z * g x = p.eval x)
    (hexclude : ¬ (Explains (RSFunctions D (k+1)) S f ∧
                    Explains (RSFunctions D (k+1)) S g)) :
    Bad (RSFunctions D k) S f g z := by
  apply bad_of_asymmetric_witness
    (RSFunctions D k) (RSFunctions D (k+1)) S f g z
  · exact rs_inclusion D k
  · refine ⟨(fun x => p.eval x), ?_, ?_⟩
    · exact ⟨p, hdegree, fun x hx => rfl⟩
    · exact hagree
  · exact hexclude

/-- Quantifier order and distinct slopes remain explicit in the finite set Z. -/
theorem deployed_fixed_line
    (D : Set F) (k : ℕ) (f g : F → F)
    (Z : Finset F) (support : F → Set F)
    (witness : F → Polynomial F)
    (hdegree : ∀ z ∈ Z, (witness z).natDegree < k)
    (hsub : ∀ z ∈ Z, support z ⊆ D)
    (hagree : ∀ z ∈ Z, ∀ x ∈ support z,
      f x + z * g x = (witness z).eval x)
    (hexclude : ∀ z ∈ Z,
      ¬ (Explains (RSFunctions D (k+1)) (support z) f ∧
         Explains (RSFunctions D (k+1)) (support z) g)) :
    ∀ z ∈ Z, Bad (RSFunctions D k) (support z) f g z := by
  intro z hz
  exact deployed_bad_from_polynomial D (support z) k f g z
    (witness z) (hdegree z hz) (hsub z hz)
    (hagree z hz) (hexclude z hz)

end McaDomainTransfer
