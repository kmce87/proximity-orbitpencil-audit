import LeanPortDomainTransport4096

/-!
# Published support-wise MCA predicate at the *original* RS dimension k=2^20

The rs-mca M2 line-decoding bridge defines C = RS[F,D,k] with
polynomial degree STRICTLY below k, and support-wise bad slopes as the
projection of witnesses (S,z) on a SINGLE received line f+zg.

The existing WOnDomain theorem uses the larger auxiliary code with
polynomial degree <= 2^20 (i.e. k+1).  This module separately checks
the original, smaller code with degree < 2^20, using the actual
stronger degree <= 2^20-1 message already constructed and the
noncontainment even against degree <= 2^20 direction polynomials.

No assertion of external prize-verifier acceptance or novelty.
Original 512-fibre pencil: proximity-prize/proximity-prize PR #38.
Published support-wise definition: przchojecki/rs-mca,
experimental/notes/m2/m2_line_decoding_mca_bridge.md.
-/

namespace OrbitPencilLiftPublishedMcaBridge4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftAgreementCount4096
open OrbitPencilLiftMcaComposition4096
open OrbitPencilLiftWaBridge4096
open OrbitPencilLiftDomainTransport4096

/-- Punctured Reed--Solomon membership for the published base code
C = RS[Sextic,D,2^20].  Degree is STRICTLY less than 2^20. -/
def RSOnSupport (S : Finset D) (w : D → Sextic) : Prop :=
  ∃ c : Polynomial Sextic,
    c.natDegree < 1048576 ∧
    ∀ x ∈ S, w x = c.eval x.val

/-- Literally the support-wise noncontained slope predicate from the
rs-mca M2 note, specialized to n=2^21, k=2^20, a=1116048.
There is one fixed pair f,g for all slopes; S may depend on z. -/
def PublishedBadSlope (f g : D → Sextic) (z : Sextic) : Prop :=
  ∃ S : Finset D,
    1116048 ≤ S.card ∧
    RSOnSupport S (fun x => f x + z * g x) ∧
    ¬ (RSOnSupport S f ∧ RSOnSupport S g)

/-- The fixed-line 4096-fibre construction satisfies the *smaller*
published RS code's bad-slope predicate, not merely the auxiliary
K=k+1 predicate. -/
theorem supportWiseBad_implies_published (alpha : Sextic)
    (U0 : Finset Small) (z : Sextic)
    (h : SupportWiseBad alpha U0 z) :
    PublishedBadSlope
      (fun x => receivedBase alpha U0 (indexEquiv.symm x))
      (fun x => receivedDirection alpha (indexEquiv.symm x)) z := by
  classical
  rcases h with ⟨S, c, hsize, hdeg, hmatch, hnot⟩
  refine ⟨S.image indexEquiv, ?_, ?_, ?_⟩
  · rw [Finset.card_image_of_injective _ indexEquiv.injective]
    omega
  · refine ⟨c, by omega, ?_⟩
    intro x hx
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hx
    have hline := hmatch j hj
    rw [lineAt_eq_base_add] at hline
    simpa only [Equiv.symm_apply_apply, indexEquiv_val] using hline
  · rintro ⟨_hf, hg⟩
    rcases hg with ⟨cg, hcgdeg, hgmatch⟩
    apply hnot
    refine ⟨cg, by omega, ?_⟩
    intro j hj
    have hmem : indexEquiv j ∈ S.image indexEquiv :=
      Finset.mem_image.mpr ⟨j, hj, rfl⟩
    have heq := hgmatch (indexEquiv j) hmem
    have heq2 : receivedDirection alpha j = cg.eval (node6 j) := by
      simpa only [Equiv.symm_apply_apply, indexEquiv_val] using heq
    change cg.eval (node6 j) = receivedDirection alpha j
    exact heq2.symm

/-- The source-mirrored finite support-wise MCA numerator exceeds B*
at the original RS degree < 2^20, for one affine line in the actual
KoalaBear sextic evaluation domain.  The external LD_sw maximum is
at least the cardinality exhibited here; that final supremum
translation is still documented separately, not imported from rs-mca. -/
theorem exists_many_published_k_bad_slopes :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      274980728111395087 < Z.card ∧
      alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      ∀ z ∈ Z,
        PublishedBadSlope
          (fun x => receivedBase alpha U0 (indexEquiv.symm x))
          (fun x => receivedDirection alpha (indexEquiv.symm x)) z := by
  obtain ⟨alpha, U0, Z, hZ, hα, havoid, hbad⟩ :=
    exists_many_supportwise_bad_slopes
  have htwo : (2 : ℕ)^59 = 576460752303423488 := by norm_num
  refine ⟨alpha, U0, Z, ?_, hα, havoid, ?_⟩
  · omega
  · intro z hz
    exact supportWiseBad_implies_published alpha U0 z (hbad z hz)

#print axioms OrbitPencilLiftPublishedMcaBridge4096.supportWiseBad_implies_published
#print axioms OrbitPencilLiftPublishedMcaBridge4096.exists_many_published_k_bad_slopes

end OrbitPencilLiftPublishedMcaBridge4096
