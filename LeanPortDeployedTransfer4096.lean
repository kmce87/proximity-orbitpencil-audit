import LeanPortDomainTransport4096

/-!
# Deployed k=2^20 support-wise MCA transfer

A stronger domain-level statement than WOnDomain: the explaining polynomial
has natDegree <= 1048575 (degree < k), while noncontainment excludes
polynomials with natDegree <= 1048576 (degree < k+1).

This does not identify the result with any external manuscript's definition,
and is not an official Proximity Prize ProtocolClaim.
-/

namespace OrbitPencilLiftDeployedTransfer4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftWaBridge4096
open OrbitPencilLiftDomainTransport4096
open OrbitPencilLiftMcaComposition4096

def WDeployed (f g : D → Sextic) (S : Finset D) (z : Sextic) : Prop :=
  1118207 ≤ S.card ∧
  (∃ c : Polynomial Sextic,
    c.natDegree ≤ 1048575 ∧
    ∀ x ∈ S, f x + z * g x = c.eval x.val) ∧
  ¬ ∃ cf cg : Polynomial Sextic,
    cf.natDegree ≤ 1048576 ∧
    cg.natDegree ≤ 1048576 ∧
    (∀ x ∈ S, f x = cf.eval x.val) ∧
    (∀ x ∈ S, g x = cg.eval x.val)

def BadDeployed (f g : D → Sextic) (z : Sextic) : Prop :=
  ∃ S : Finset D, WDeployed f g S z

theorem supportWiseBad_to_deployed (alpha : Sextic)
    (U0 : Finset Small) (z : Sextic)
    (h : SupportWiseBad alpha U0 z) :
    BadDeployed
      (fun x => receivedBase alpha U0 (indexEquiv.symm x))
      (fun x => receivedDirection alpha (indexEquiv.symm x)) z := by
  classical
  rcases h with ⟨S, c, hcard, hcdeg, hmatch, hnot⟩
  refine ⟨S.image indexEquiv, ?_, ⟨c, hcdeg, ?_⟩, ?_⟩
  · rw [Finset.card_image_of_injective _ indexEquiv.injective]
    exact hcard
  · intro x hx
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hx
    simpa only [Equiv.symm_apply_apply, indexEquiv_val, ← lineAt_eq_base_add]
      using hmatch j hj
  · rintro ⟨cf, cg, _hcf, hcg, _hf, hg⟩
    apply hnot
    refine ⟨cg, hcg, ?_⟩
    intro j hj
    have hj' : indexEquiv j ∈ S.image indexEquiv :=
      Finset.mem_image.mpr ⟨j, hj, rfl⟩
    have hgj := hg (indexEquiv j) hj'
    simpa only [Equiv.symm_apply_apply, indexEquiv_val, receivedDirection]
      using hgj.symm

theorem exists_many_deployed_bad_slopes :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      2^59 < Z.card ∧
      alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      ∀ z ∈ Z,
        BadDeployed
          (fun x => receivedBase alpha U0 (indexEquiv.symm x))
          (fun x => receivedDirection alpha (indexEquiv.symm x)) z := by
  obtain ⟨alpha, U0, Z, hZ, hα, havoid, hbad⟩ :=
    exists_many_supportwise_bad_slopes
  exact ⟨alpha, U0, Z, hZ, hα, havoid,
    fun z hz => supportWiseBad_to_deployed alpha U0 z (hbad z hz)⟩

#print axioms OrbitPencilLiftDeployedTransfer4096.supportWiseBad_to_deployed
#print axioms OrbitPencilLiftDeployedTransfer4096.exists_many_deployed_bad_slopes

end OrbitPencilLiftDeployedTransfer4096
