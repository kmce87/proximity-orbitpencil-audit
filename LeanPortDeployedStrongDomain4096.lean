import LeanPortDomainTransport4096

/-!
Lane A: strong deployed-degree transport candidate.
Hypothesis: transport SupportWiseBad directly rather than through W,
retaining natDegree <= 1048575 for the explaining polynomial.
This file is NOT kernel-checked until the pinned Lean 4.34 gate runs.
-/ 

namespace OrbitPencilLiftDeployedStrongDomain4096
open Polynomial
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096
open OrbitPencilLiftGeometry
open OrbitPencilLiftWaBridge4096
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftDomainTransport4096

def DeployedBadOnDomain (f g : D → Sextic) (S : Finset D)
    (z : Sextic) : Prop :=
  1118207 ≤ S.card ∧
  (∃ c : Polynomial Sextic,
    c.natDegree ≤ 1048575 ∧
    ∀ x ∈ S, f x + z * g x = c.eval x.val) ∧
  ¬ ∃ cf cg : Polynomial Sextic,
    cf.natDegree ≤ 1048576 ∧
    cg.natDegree ≤ 1048576 ∧
    (∀ x ∈ S, f x = cf.eval x.val) ∧
    (∀ x ∈ S, g x = cg.eval x.val)

def DeployedBadSlopeOnDomain (f g : D → Sextic) (z : Sextic) : Prop :=
  ∃ S : Finset D, DeployedBadOnDomain f g S z

theorem supportwise_to_deployed_domain
    (alpha : Sextic) (U0 : Finset Small) (z : Sextic)
    (h : OrbitPencilLiftMcaComposition4096.SupportWiseBad alpha U0 z) :
    DeployedBadSlopeOnDomain
      (fun x => receivedBase alpha U0 (indexEquiv.symm x))
      (fun x => receivedDirection alpha (indexEquiv.symm x)) z := by
  classical
  rcases h with ⟨S, c, hcard, hdeg, hmatch, hnot⟩
  refine ⟨S.image indexEquiv, ?_, ⟨c, hdeg, ?_⟩, ?_⟩
  · rw [Finset.card_image_of_injective _ indexEquiv.injective]
    exact hcard
  · intro x hx
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hx
    rw [← lineAt_eq_base_add]
    simpa only [Equiv.symm_apply_apply, indexEquiv_val] using hmatch j hj
  · rintro ⟨cf, cg, _hcf, hcg, _hf, hg⟩
    apply hnot
    refine ⟨cg, hcg, ?_⟩
    intro j hj
    have hj' : indexEquiv j ∈ S.image indexEquiv :=
      Finset.mem_image.mpr ⟨j, hj, rfl⟩
    have hd := hg (indexEquiv j) hj'
    simpa only [Equiv.symm_apply_apply, indexEquiv_val, receivedDirection] using hd.symm

theorem exists_many_deployed_bad_slopes :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      2^59 < Z.card ∧
      alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      ∀ z ∈ Z,
        DeployedBadSlopeOnDomain
          (fun x => receivedBase alpha U0 (indexEquiv.symm x))
          (fun x => receivedDirection alpha (indexEquiv.symm x)) z := by
  obtain ⟨alpha, U0, Z, hZ, hα, havoid, hbad⟩ :=
    OrbitPencilLiftMcaComposition4096.exists_many_supportwise_bad_slopes
  exact ⟨alpha, U0, Z, hZ, hα, havoid,
    fun z hz => supportwise_to_deployed_domain alpha U0 z (hbad z hz)⟩

#print axioms OrbitPencilLiftDeployedStrongDomain4096.supportwise_to_deployed_domain
#print axioms OrbitPencilLiftDeployedStrongDomain4096.exists_many_deployed_bad_slopes
end OrbitPencilLiftDeployedStrongDomain4096
