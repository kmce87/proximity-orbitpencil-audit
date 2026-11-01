import LeanPortGeometry
import LeanPortSameKeyFamily

/-!
# Exact support and 4095-point core for the n = 2^21 OrbitPencil lift

The original n = 2^18 construction is Proximity Prize OrbitPencil.lean,
accepted PR #38 (original contributors including erdkocak).

The theorem below is deliberately a *geometry and locator* certificate.
It does not claim that the support is an MCA witness or that any
line point is explained by a Reed–Solomon message.
-/

namespace OrbitPencilLiftSupport4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey

noncomputable def coreRows : Finset Row := Finset.univ.erase 0

theorem coreRows_card : coreRows.card = 4095 := by
  simp [coreRows]

noncomputable def corePairs : Finset (Row × Column) :=
  coreRows.product {0}

noncomputable def blockPairs (U : Finset Small) : Finset (Row × Column) :=
  Finset.univ.product U

noncomputable def pairSet (U : Finset Small) : Finset (Row × Column) :=
  corePairs ∪ blockPairs U

noncomputable def support (U : Finset Small) : Finset Index :=
  (pairSet U).image (fun ab => idx ab.1 ab.2)

/-- Candidate sets lie in {1,...,511}, so the core and full blocks
do not overlap. -/
theorem pair_disjoint {U : Finset Small} (hU : U ∈ Candidates) :
    Disjoint corePairs (blockPairs U) := by
  have hnot : (0 : Small) ∉ U := by
    intro h0
    have hout := (Finset.mem_powersetCard.mp hU).1 h0
    simpa [outer] using hout
  rw [Finset.disjoint_left]
  intro ab habc habb
  have hc := Finset.mem_product.mp
    (show ab ∈ coreRows.product ({0} : Finset Column) by
      simpa only [corePairs] using habc)
  have hb := Finset.mem_product.mp
    (show ab ∈ (Finset.univ : Finset Row).product U by
      simpa only [blockPairs] using habb)
  have hb0 : ab.2 = 0 := Finset.mem_singleton.mp hc.2
  rw [hb0] at hb
  exact hnot hb.2

/-- Exactly 272 complete 4096-point fibres and 4095 additional points
in column zero, with no multiplicity or support collisions. -/
theorem support_card {U : Finset Small} (hU : U ∈ Candidates) :
    (support U).card = 1118207 := by
  rw [support, Finset.card_image_of_injective _ idx_injective, pairSet,
    Finset.card_union_of_disjoint (pair_disjoint hU)]
  simp [corePairs, blockPairs, coreRows_card, candidate_card hU]

/-- Concrete n = 2^21 KoalaBear NTT node at an index. -/
noncomputable def node21 (j : Index) : _root_.KoalaBear.Field :=
  omega21 ^ j.val

theorem node21_injective : Function.Injective node21 := by
  intro i j h
  apply Fin.ext
  apply baseNttDomain21.primitive.pow_inj
  · change i.val < 2097152
    exact i.isLt
  · change j.val < 2097152
    exact j.isLt
  simpa only [node21, omega21] using h

noncomputable def node6 (j : Index) : Sextic :=
  baseToSextic (node21 j)

/-- The polynomial which vanishes on precisely the *chosen* core nodes,
with degree 4095, as required by the real lift. -/
noncomputable def coreLocator : Polynomial Sextic :=
  ∏ a ∈ coreRows, ((Polynomial.X : Polynomial Sextic) -
    Polynomial.C (node6 (idx a 0)))

theorem coreLocator_monic : coreLocator.Monic :=
  Polynomial.monic_prod_of_monic _ _ fun a _ =>
    Polynomial.monic_X_sub_C (node6 (idx a 0))

theorem coreLocator_natDegree : coreLocator.natDegree = 4095 := by
  rw [coreLocator, Polynomial.natDegree_prod_of_monic _ _
    (fun a (_ : a ∈ coreRows) =>
      Polynomial.monic_X_sub_C (node6 (idx a 0)))]
  simp [coreRows_card]

theorem coreLocator_ne_zero : coreLocator ≠ 0 :=
  coreLocator_monic.ne_zero

theorem coreLocator_eval_core (a : Row) (ha : a ∈ coreRows) :
    coreLocator.eval (node6 (idx a 0)) = 0 := by
  rw [coreLocator, Polynomial.eval_prod]
  refine Finset.prod_eq_zero ha ?_
  simp

end OrbitPencilLiftSupport4096
