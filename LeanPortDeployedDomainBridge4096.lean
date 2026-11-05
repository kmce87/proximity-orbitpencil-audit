import LeanPortDomainTransport4096

/-!
Lane A: preserve the deployed RS[D,2^20] explaining polynomial degree
<= 1048575 while separately retaining the stronger degree <= 1048576
noncontainment. This is a candidate source, NOT yet kernel-checked.
-/

namespace OrbitPencilLiftDeployedDomain4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096
open OrbitPencilLiftDomainTransport4096

/-- The explaining code is deployed RS[D,k], degree < k.
    Noncontainment is tested even against auxiliary RS[D,k+1]. -/
def DeployedBad (f g : D → Sextic) (z : Sextic) : Prop :=
  ∃ (S : Finset D) (c : Polynomial Sextic),
    1118207 ≤ S.card ∧
    c.natDegree ≤ 1048575 ∧
    (∀ x ∈ S, f x + z * g x = c.eval x.val) ∧
    ¬ ∃ cf cg : Polynomial Sextic,
      cf.natDegree ≤ 1048576 ∧
      cg.natDegree ≤ 1048576 ∧
      (∀ x ∈ S, f x = cf.eval x.val) ∧
      (∀ x ∈ S, g x = cg.eval x.val)

/-- This bridge does not infer a degree < k witness by code inclusion:
    it carries the original polynomial c from SupportWiseBad. -/
theorem supportWise_to_deployed
    (alpha : Sextic) (U0 : Finset Small) (z : Sextic)
    (h : OrbitPencilLiftMcaComposition4096.SupportWiseBad alpha U0 z) :
    DeployedBad
      (fun x => receivedBase alpha U0 (indexEquiv.symm x))
      (fun x => receivedDirection alpha (indexEquiv.symm x)) z := by
  classical
  rcases h with ⟨S, c, hcard, hdeg, hmatch, hnot⟩
  have hWeak :
      W (receivedBase alpha U0) (receivedDirection alpha) S z := by
    refine ⟨by omega, ⟨c, by omega, ?_⟩, ?_⟩
    · intro j hj
      rw [← lineAt_eq_base_add]
      exact hmatch j hj
    · rintro ⟨cf, cg, _hcf, hcg, _hf, hg⟩
      apply hnot
      refine ⟨cg, hcg, ?_⟩
      intro j hj
      exact (hg j hj).symm
  have hDomain := W_to_domain
    (receivedBase alpha U0) (receivedDirection alpha) S z hWeak
  rcases hDomain with ⟨_hthreshold, _hexpl, hnon⟩
  refine ⟨S.image indexEquiv, c, ?_, hdeg, ?_, hnon⟩
  · rw [Finset.card_image_of_injective _ indexEquiv.injective]
    exact hcard
  · intro x hx
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hx
    simpa only [Equiv.symm_apply_apply, indexEquiv_val] using
      (show receivedBase alpha U0 j + z * receivedDirection alpha j =
        c.eval (node6 j) by
        rw [← lineAt_eq_base_add]
        exact hmatch j hj)

/-- One fixed received line, > 2^59 distinct slopes, deployed-degree witnesses. -/
theorem exists_many_deployed_bad_slopes :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      2^59 < Z.card ∧
      alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      ∀ z ∈ Z,
        DeployedBad
          (fun x => receivedBase alpha U0 (indexEquiv.symm x))
          (fun x => receivedDirection alpha (indexEquiv.symm x)) z := by
  obtain ⟨alpha, U0, Z, hcard, hα, havoid, hbad⟩ :=
    OrbitPencilLiftMcaComposition4096.exists_many_supportwise_bad_slopes
  refine ⟨alpha, U0, Z, hcard, hα, havoid, ?_⟩
  intro z hz
  exact supportWise_to_deployed alpha U0 z (hbad z hz)

#print axioms OrbitPencilLiftDeployedDomain4096.supportWise_to_deployed
#print axioms OrbitPencilLiftDeployedDomain4096.exists_many_deployed_bad_slopes

end OrbitPencilLiftDeployedDomain4096
