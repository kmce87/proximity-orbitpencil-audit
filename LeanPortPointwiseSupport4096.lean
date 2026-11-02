import LeanPortLineAgreement4096
import LeanPortSupport4096

/-!
# Pointwise agreement on the actual 2^21 KoalaBear domain

Adapted from the accepted OrbitPencil PR #38 (including erdkocak).
One falsifiable target: show that every index in the actual 1,118,207-point
4096-fibre support satisfies the rational received-line identity for any
same-key factorization certificate. This does not yet compose the existential
same-key family, prove support-wise MCA noncontainment, or satisfy the official
Proximity Prize ProtocolClaim.
-/

namespace OrbitPencilLiftPointwiseSupport4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftPencil4096
open OrbitPencilLiftLineAgreement4096

/-- A 4096th power of an actual NTT node depends only on its column. -/
theorem node6_pow_column (a : Row) (b : Column) :
    (node6 (idx a b)) ^ 4096 = y6 b := by
  have hw : omega21 ^ 2097152 = 1 := by
    have hlog : baseNttDomain21.logN = 21 := rfl
    simpa only [omega21, hlog, show (2 : ℕ)^21 = 2097152 by norm_num] using
      baseNttDomain21.primitive.pow_eq_one
  have h := OrbitPencilLiftGeometry.pow_block omega21 hw a b
  change (baseToSextic (omega21 ^ (a.val * 512 + b.val))) ^ 4096 =
    baseToSextic ((omega21 ^ b.val) ^ 4096)
  simpa only [map_pow] using congrArg baseToSextic h

theorem node6_pow_projected (j : Index) :
    (node6 j) ^ 4096 = y6 (column j) := by
  calc
    (node6 j) ^ 4096 =
        (node6 (idx (row j) (column j))) ^ 4096 := by rw [idx_row_column]
    _ = y6 (column j) := node6_pow_column _ _

theorem node6_pow_nonzero (j : Index) : (node6 j) ^ 4096 ≠ 0 := by
  have hw : omega21 ^ 2097152 = 1 := by
    have hlog : baseNttDomain21.logN = 21 := rfl
    simpa only [omega21, hlog, show (2 : ℕ)^21 = 2097152 by norm_num] using
      baseNttDomain21.primitive.pow_eq_one
  have homega : omega21 ≠ 0 := by
    intro hz
    rw [hz] at hw
    norm_num at hw
  have hj : node21 j ≠ 0 := by
    change omega21 ^ j.val ≠ 0
    exact pow_ne_zero _ homega
  have hnode : node6 j ≠ 0 := by
    intro hz
    have heq : baseToSextic (node21 j) = baseToSextic 0 := by
      simpa only [node6, map_zero] using hz
    exact hj (baseToSextic.injective heq)
  exact pow_ne_zero _ hnode

theorem node6_pow_ne_alpha (alpha : Sextic)
    (havoid : alpha ∉ projected6) (j : Index) :
    (node6 j) ^ 4096 ≠ alpha := by
  intro heq
  apply havoid
  apply Finset.mem_image.mpr
  exact ⟨column j, Finset.mem_univ _, (node6_pow_projected j).symm.trans heq⟩

theorem y6_injective : Function.Injective y6 := by
  exact mapped_nodes_injective baseToSextic projectedNode projectedNode_injective

/-- Every *logical* support witness is a core root or a selected-column root.
This avoids elaborating a huge concrete Finset union. A separate theorem
must still establish `j ∈ support U → logicalSupport U j`. -/
theorem logical_support_root_or (U : Finset Small) (j : Index)
    (hj : logicalSupport U j) :
    coreLocator.eval (node6 j) = 0 ∨
      (V y6 U).eval ((node6 j)^4096) = 0 := by
  rcases hj with ⟨a, ha, heq⟩ | ⟨a, b, hb, heq⟩
  · left
    rw [← heq]
    exact coreLocator_eval_core a ha
  · right
    rw [← heq, node6_pow_column]
    exact (V_eval_zero_iff_of_injective y6 y6_injective U b).mpr hb

/-- Conditional pointwise equality on the logical support predicate for KoalaBear
received line, conditional only on the factorization of the chosen pair.
The finite-support cardinality is proved separately; equivalence to this predicate is not yet proved. -/
theorem pencil_agrees_on_logical_support (alpha : Sextic)
    (U0 U : Finset Small) (Q : Polynomial Sextic)
    (hfactor : pencil alpha U0 U =
      (Polynomial.X : Polynomial Sextic) *
        (Polynomial.X - Polynomial.C alpha) * Q)
    (havoid : alpha ∉ projected6)
    (j : Index) (hj : logicalSupport U j) :
    coreLocator.eval (node6 j) *
        (V y6 U0).eval ((node6 j)^4096) /
        ((node6 j)^4096 * ((node6 j)^4096 - alpha)) +
      gamma alpha U0 U *
        (-coreLocator.eval (node6 j) / ((node6 j)^4096 - alpha)) =
      coreLocator.eval (node6 j) * Q.eval ((node6 j)^4096) := by
  have hroot := logical_support_root_or U j hj
  exact pencil_line_agrees_on_root alpha U0 U Q hfactor
    (coreLocator.eval (node6 j)) ((node6 j)^4096)
    (node6_pow_nonzero j) (node6_pow_ne_alpha alpha havoid j) hroot

/-- The right-hand side is exactly the evaluation of an admissible RS
message polynomial, rather than merely a scalar product. Degree admissibility
follows from exists_message_poly for any pair with the same key. -/
theorem pencil_agrees_with_message_on_logical_support (alpha : Sextic)
    (U0 U : Finset Small) (Q : Polynomial Sextic)
    (hfactor : pencil alpha U0 U =
      (Polynomial.X : Polynomial Sextic) *
        (Polynomial.X - Polynomial.C alpha) * Q)
    (havoid : alpha ∉ projected6)
    (j : Index) (hj : logicalSupport U j) :
    coreLocator.eval (node6 j) *
        (V y6 U0).eval ((node6 j)^4096) /
        ((node6 j)^4096 * ((node6 j)^4096 - alpha)) +
      gamma alpha U0 U *
        (-coreLocator.eval (node6 j) / ((node6 j)^4096 - alpha)) =
      (coreLocator * Q.comp ((Polynomial.X : Polynomial Sextic)^4096)).eval
        (node6 j) := by
  have h := pencil_agrees_on_logical_support alpha U0 U Q hfactor havoid j hj
  simpa only [Polynomial.eval_mul, Polynomial.eval_comp,
    Polynomial.eval_pow, Polynomial.eval_X] using h

end OrbitPencilLiftPointwiseSupport4096
