import LeanPortWaNormalization4096

/-!
# Indexed KoalaBear MCA witnesses transported to actual evaluation-domain points

Falsifiable target: the local indexed `W` witness at n=2^21 transports to a
support of DISTINCT elements of the concrete sextic evaluation domain, with
the same degree cutoff, agreement count, and fixed received affine line.

This is a genuine model change from `Fin 2097152` indices to a subset of
KoalaBear.Ext6. It does NOT yet identify this domain with an independently
formalized `rs-mca` definition, and is NOT an official ArkLib ProtocolClaim.

Original 512-fibre rational-pencil construction: official OrbitPencil PR #38,
with credit to its original contributors, including erdkocak.
-/

namespace OrbitPencilLiftDomainTransport4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096
open OrbitPencilLiftWaBridge4096

/-- The exact evaluation domain as a SET of sextic field elements, rather
than the index type. This is not the entire sextic field. -/
def D : Set Sextic := Set.range node6

/-- The prime-field embedding cannot identify two distinct NTT nodes. -/
theorem node6_injective : Function.Injective node6 := by
  intro i j h
  apply node21_injective
  exact (RingHom.injective baseToSextic) h

/-- A genuine equivalence between the finite index type and the actual
evaluation-domain subtype. In particular, no two indices are silently
identified as one field element. -/
noncomputable def indexEquiv : Index ≃ D := by
  refine Equiv.ofBijective
    (fun j : Index => (⟨node6 j, ⟨j, rfl⟩⟩ : D)) ?_
  constructor
  · intro i j h
    exact node6_injective (congrArg Subtype.val h)
  · intro x
    rcases x with ⟨x, hx⟩
    change ∃ j, node6 j = x at hx
    rcases hx with ⟨j, hj⟩
    refine ⟨j, Subtype.ext ?_⟩
    exact hj

@[simp] theorem indexEquiv_val (j : Index) :
    (indexEquiv j).val = node6 j := rfl

/-- This is a literal domain-based RS support witness: the support consists
of field elements, and each codeword is polynomial evaluation at that
element, not at a separately supplied index. -/
def WOnDomain (f g : D → Sextic) (S : Finset D)
    (z : Sextic) : Prop :=
  1116048 ≤ S.card ∧
  (∃ c : Polynomial Sextic,
    c.natDegree ≤ 1048575 ∧
    ∀ x ∈ S, f x + z * g x = c.eval x.val) ∧
  ¬ ∃ cf cg : Polynomial Sextic,
    cf.natDegree ≤ 1048575 ∧
    cg.natDegree ≤ 1048575 ∧
    (∀ x ∈ S, f x = cf.eval x.val) ∧
    (∀ x ∈ S, g x = cg.eval x.val)

def BadSlopeOnDomain (f g : D → Sextic) (z : Sextic) : Prop :=
  ∃ S : Finset D, WOnDomain f g S z

/-- The indexed W_a witness transports without weakening the endpoint or
changing either received word. No large finite set is enumerated. -/
theorem W_to_domain (f g : Index → Sextic) (S : Finset Index)
    (z : Sextic) (h : W f g S z) :
    WOnDomain
      (fun x => f (indexEquiv.symm x))
      (fun x => g (indexEquiv.symm x))
      (S.image indexEquiv) z := by
  classical
  rcases h with ⟨hcard, ⟨c, hcdeg, hmatch⟩, hnot⟩
  have hsize : (S.image indexEquiv).card = S.card :=
    Finset.card_image_of_injective _ indexEquiv.injective
  refine ⟨?_, ⟨c, hcdeg, ?_⟩, ?_⟩
  · rw [hsize]
    exact hcard
  · intro x hx
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hx
    simpa only [Equiv.symm_apply_apply, indexEquiv_val] using hmatch j hj
  · rintro ⟨cf, cg, hcf, hcg, hf, hg⟩
    apply hnot
    refine ⟨cf, cg, hcf, hcg, ?_, ?_⟩
    · intro j hj
      have hj' : indexEquiv j ∈ S.image indexEquiv :=
        Finset.mem_image.mpr ⟨j, hj, rfl⟩
      simpa only [Equiv.symm_apply_apply, indexEquiv_val] using
        hf (indexEquiv j) hj'
    · intro j hj
      have hj' : indexEquiv j ∈ S.image indexEquiv :=
        Finset.mem_image.mpr ⟨j, hj, rfl⟩
      simpa only [Equiv.symm_apply_apply, indexEquiv_val] using
        hg (indexEquiv j) hj'

theorem BadSlope_to_domain (f g : Index → Sextic) (z : Sextic)
    (h : BadSlope f g z) :
    BadSlopeOnDomain
      (fun x => f (indexEquiv.symm x))
      (fun x => g (indexEquiv.symm x)) z := by
  classical
  rcases h with ⟨S, hS⟩
  exact ⟨S.image indexEquiv, W_to_domain f g S z hS⟩

/-- The EXISTING >B* witness now lives on the concrete set of sextic
evaluation points, rather than merely on an indexed array. Every slope
uses the SAME pair of received words. The Z cardinality is unchanged. -/
theorem exists_many_domain_bad_slopes :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      274980728111395087 < Z.card ∧
      alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      ∀ z ∈ Z,
        BadSlopeOnDomain
          (fun x => receivedBase alpha U0 (indexEquiv.symm x))
          (fun x => receivedDirection alpha (indexEquiv.symm x))
          z := by
  obtain ⟨alpha, U0, Z, hZ, hα, havoid, hbad⟩ :=
    exists_many_W_bad_slopes
  refine ⟨alpha, U0, Z, hZ, hα, havoid, ?_⟩
  intro z hz
  exact BadSlope_to_domain
    (receivedBase alpha U0) (receivedDirection alpha) z (hbad z hz)

#print axioms OrbitPencilLiftDomainTransport4096.node6_injective
#print axioms OrbitPencilLiftDomainTransport4096.indexEquiv
#print axioms OrbitPencilLiftDomainTransport4096.W_to_domain
#print axioms OrbitPencilLiftDomainTransport4096.exists_many_domain_bad_slopes

end OrbitPencilLiftDomainTransport4096
