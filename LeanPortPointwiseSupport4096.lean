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

/-- Every support index is either a core root or a complete selected-column
root, with no assumption about the message polynomial or received line. -/
theorem support_root_or (U : Finset Small) (j : Index)
    (hj : j ∈ support U) :
    coreLocator.eval (node6 j) = 0 ∨
      (V y6 U).eval ((node6 j)^4096) = 0 := by
  classical
  -- Expose only the outer image/union constructors. Do not simplify
  -- the concrete Finset universes: they have 4096 rows.
  change j ∈ (pairSet U).image (fun ab : Row × Column => idx ab.1 ab.2) at hj
  rw [Finset.mem_image] at hj
  obtain ⟨⟨a, b⟩, hp, heq⟩ := hj
  change (a, b) ∈ corePairs ∪ blockPairs U at hp
  rcases Finset.mem_union.mp hp with hc | hb
  · have ha : a ∈ coreRows := (Finset.mem_product.mp hc).1
    have hb0 : b = 0 := Finset.mem_singleton.mp (Finset.mem_product.mp hc).2
    left
    rw [← heq, hb0]
    exact coreLocator_eval_core a ha
  · have hU : b ∈ U := (Finset.mem_product.mp hb).2
    right
    rw [← heq, node6_pow_column]
    exact (V_eval_zero_iff_of_injective y6 y6_injective U b).mpr hU

/-- Actual support-wise pointwise equality for the concrete KoalaBear
received line, conditional only on the factorization of the chosen pair.
The exact support cardinality is separately proved by support_card. -/
theorem pencil_agrees_on_support (alpha : Sextic)
    (U0 U : Finset Small) (Q : Polynomial Sextic)
    (hfactor : pencil alpha U0 U =
      (Polynomial.X : Polynomial Sextic) *
        (Polynomial.X - Polynomial.C alpha) * Q)
    (havoid : alpha ∉ projected6)
    (j : Index) (hj : j ∈ support U) :
    coreLocator.eval (node6 j) *
        (V y6 U0).eval ((node6 j)^4096) /
        ((node6 j)^4096 * ((node6 j)^4096 - alpha)) +
      gamma alpha U0 U *
        (-coreLocator.eval (node6 j) / ((node6 j)^4096 - alpha)) =
      coreLocator.eval (node6 j) * Q.eval ((node6 j)^4096) := by
  have hroot := support_root_or U j hj
  exact pencil_line_agrees_on_root alpha U0 U Q hfactor
    (coreLocator.eval (node6 j)) ((node6 j)^4096)
    (node6_pow_nonzero j) (node6_pow_ne_alpha alpha havoid j) hroot

/-- The right-hand side is exactly the evaluation of an admissible RS
message polynomial, rather than merely a scalar product. Degree admissibility
follows from exists_message_poly for any pair with the same key. -/
theorem pencil_agrees_with_message_on_support (alpha : Sextic)
    (U0 U : Finset Small) (Q : Polynomial Sextic)
    (hfactor : pencil alpha U0 U =
      (Polynomial.X : Polynomial Sextic) *
        (Polynomial.X - Polynomial.C alpha) * Q)
    (havoid : alpha ∉ projected6)
    (j : Index) (hj : j ∈ support U) :
    coreLocator.eval (node6 j) *
        (V y6 U0).eval ((node6 j)^4096) /
        ((node6 j)^4096 * ((node6 j)^4096 - alpha)) +
      gamma alpha U0 U *
        (-coreLocator.eval (node6 j) / ((node6 j)^4096 - alpha)) =
      (coreLocator * Q.comp ((Polynomial.X : Polynomial Sextic)^4096)).eval
        (node6 j) := by
  have h := pencil_agrees_on_support alpha U0 U Q hfactor havoid j hj
  simpa only [Polynomial.eval_mul, Polynomial.eval_comp,
    Polynomial.eval_pow, Polynomial.eval_X] using h

end OrbitPencilLiftPointwiseSupport4096
