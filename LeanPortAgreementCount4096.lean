import LeanPortTypedSupport4096

/-!
# Single-line agreement endpoint: composition gate

Falsifiable target: compose the concrete 4096-fibre polynomial factorization,
pointwise rational-pencil identity, and typed logical-support injection into a
single theorem asserting >= 1,118,207 *distinct domain positions* where ONE
received affine line point agrees with an RS polynomial of degree < 2^20.

This theorem is conditional on a chosen same-key pair and alpha. It does not
yet prove that the received-line direction is outside the RS code, that the
gamma values are distinct MCA-bad slopes, or that the old safe bound is false.
Original 512-fibre construction: accepted Proximity Prize PR #38, with
contributors including erdkocak.
-/

namespace OrbitPencilLiftAgreementCount4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftPencil4096
open OrbitPencilLiftPointwiseSupport4096
open OrbitPencilLiftTypedSupport4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

/-- The same received affine line is used for every candidate U:
only its slope varies. -/
noncomputable def lineAt (alpha : Sextic) (U0 : Finset Small)
    (slope : Sextic) (j : Index) : Sextic :=
  coreLocator.eval (node6 j) *
    (V y6 U0).eval ((node6 j)^4096) /
      ((node6 j)^4096 * ((node6 j)^4096 - alpha)) +
    slope * (-coreLocator.eval (node6 j) / ((node6 j)^4096 - alpha))

/-- For every same-key pair, an admissible degree-<2^20 polynomial
agrees with the same received line at >=1,118,207 distinct indices.
This combines the actual KoalaBear domain, pointwise algebra, and the
typed-support injection; no large Finset image elimination is needed. -/
theorem exists_message_agreement_1118207
    (alpha : Sextic) (hα : alpha ≠ 0) (havoid : alpha ∉ projected6)
    (U0 U : Finset Small)
    (hU0 : U0 ∈ Candidates) (hU : U ∈ Candidates)
    (hk : key projectedNode U0 = key projectedNode U) :
    ∃ c : Polynomial Sextic,
      c.natDegree ≤ 1048575 ∧
      1118207 ≤ Fintype.card
        {j : Index // lineAt alpha U0 (gamma alpha U0 U) j =
          c.eval (node6 j)} := by
  classical
  obtain ⟨Q, hfactor, hdegree⟩ := exists_message_poly hα hU0 hU hk
  let c : Polynomial Sextic :=
    coreLocator * Q.comp ((Polynomial.X : Polynomial Sextic)^4096)
  refine ⟨c, hdegree, ?_⟩
  have hsupport : 1118207 ≤
      Fintype.card {j : Index // logicalSupport U j} :=
    logical_support_card_lower U hU
  let embed :
      {j : Index // logicalSupport U j} →
      {j : Index // lineAt alpha U0 (gamma alpha U0 U) j =
        c.eval (node6 j)} :=
    fun j => ⟨j.val, by
      change coreLocator.eval (node6 j.val) *
          (V y6 U0).eval ((node6 j.val)^4096) /
            ((node6 j.val)^4096 * ((node6 j.val)^4096 - alpha)) +
          gamma alpha U0 U *
            (-coreLocator.eval (node6 j.val) /
              ((node6 j.val)^4096 - alpha)) =
        (coreLocator * Q.comp ((Polynomial.X : Polynomial Sextic)^4096)).eval
          (node6 j.val)
      exact pencil_agrees_with_message_on_logical_support
        alpha U0 U Q hfactor havoid j.val j.property⟩
  have hinj : Function.Injective embed := by
    intro x y h
    apply Subtype.ext
    exact congrArg Subtype.val h
  exact hsupport.trans (Fintype.card_le_of_injective embed hinj)

#print axioms OrbitPencilLiftAgreementCount4096.exists_message_agreement_1118207

end OrbitPencilLiftAgreementCount4096
