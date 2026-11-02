import LeanPortMcaComposition4096

/-!
# External support-witness W_a bridge (KoalaBear, a = 1116048)

Single falsifiable hypothesis: the kernel-checked local SupportWiseBad
construction implies the support-witness projection W_a(f,g) stated in
przchojecki/rs-mca/experimental/notes/m2/m2_line_decoding_mca_bridge.md.

The two received words are fixed across ALL slopes. The direction is
not RS-explained on the witness support, so the pair cannot both be
RS-explained there. The theorem counts distinct slopes, not supports.

This mirrors the published support-wise predicate in a local Lean model.
It does NOT import an official rs-mca formal definition, establish
independent acceptance, or improve the official n=2^18 benchmark.
Original 512-fibre construction: proximity-prize PR #38, including erdkocak.
-/

namespace OrbitPencilLiftWaBridge4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftAgreementCount4096
open OrbitPencilLiftMcaComposition4096

noncomputable def receivedBase (alpha : Sextic) (U0 : Finset Small)
    (j : Index) : Sextic :=
  coreLocator.eval (node6 j) *
    (V y6 U0).eval ((node6 j)^4096) /
      ((node6 j)^4096 * ((node6 j)^4096 - alpha))

noncomputable def receivedDirection (alpha : Sextic)
    (j : Index) : Sextic :=
  -coreLocator.eval (node6 j) / ((node6 j)^4096 - alpha)

theorem lineAt_eq_base_add (alpha : Sextic) (U0 : Finset Small)
    (z : Sextic) (j : Index) :
    lineAt alpha U0 z j =
      receivedBase alpha U0 j + z * receivedDirection alpha j := by
  rfl

/-- Literal RS support-witness W_a(f,g), with a=1116048.
A point on f+zg is explained on S, but no pair of RS messages
simultaneously explains f and g on that same support. -/
def W (f g : Index → Sextic) (S : Finset Index) (z : Sextic) : Prop :=
  1116048 ≤ S.card ∧
  (∃ c : Polynomial Sextic,
    c.natDegree ≤ 1048575 ∧
    ∀ j ∈ S, f j + z * g j = c.eval (node6 j)) ∧
  ¬ ∃ cf cg : Polynomial Sextic,
    cf.natDegree ≤ 1048575 ∧
    cg.natDegree ≤ 1048575 ∧
    (∀ j ∈ S, f j = cf.eval (node6 j)) ∧
    (∀ j ∈ S, g j = cg.eval (node6 j))

/-- Projection of W_a(f,g) onto the finite slope parameter. -/
def BadSlope (f g : Index → Sextic) (z : Sextic) : Prop :=
  ∃ S : Finset Index, W f g S z

/-- The local sufficient witness gives the exact per-support noncontainment
conjunction in W_a; only the direction part is needed for contradiction. -/
theorem supportWiseBad_implies_W (alpha : Sextic)
    (U0 : Finset Small) (z : Sextic)
    (h : SupportWiseBad alpha U0 z) :
    BadSlope (receivedBase alpha U0) (receivedDirection alpha) z := by
  rcases h with ⟨S, c, hScard, hcdeg, hmatch, hnot⟩
  refine ⟨S, ?_, ?_, ?_⟩
  · omega
  · refine ⟨c, hcdeg, ?_⟩
    intro j hj
    rw [← lineAt_eq_base_add]
    exact hmatch j hj
  · rintro ⟨cf, cg, _hcf, hcg, _hf, hg⟩
    exact hnot ⟨cg, hcg, hg⟩

/-- A SINGLE received line has more than the proposed B* distinct
support-wise bad slopes at agreement 1116048, in the local KoalaBear
RS evaluation model. This is a source-mirrored W_a theorem, NOT an
official benchmark ProtocolClaim or an independent-verifier certificate. -/
theorem exists_many_W_bad_slopes :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      274980728111395087 < Z.card ∧
      alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      ∀ z ∈ Z,
        BadSlope (receivedBase alpha U0) (receivedDirection alpha) z := by
  obtain ⟨alpha, U0, Z, hZ, halpha, havoid, hbad⟩ :=
    exists_many_supportwise_bad_slopes
  refine ⟨alpha, U0, Z, ?_, halpha, havoid, ?_⟩
  · have htwo : (2 : ℕ)^59 = 576460752303423488 := by norm_num
    omega
  · intro z hz
    exact supportWiseBad_implies_W alpha U0 z (hbad z hz)

#print axioms OrbitPencilLiftWaBridge4096.lineAt_eq_base_add
#print axioms OrbitPencilLiftWaBridge4096.supportWiseBad_implies_W
#print axioms OrbitPencilLiftWaBridge4096.exists_many_W_bad_slopes

end OrbitPencilLiftWaBridge4096
