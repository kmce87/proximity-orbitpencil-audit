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

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

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

/-- A product with a zero-only second coordinate is disjoint from
a product whose second coordinate excludes zero. This general lemma avoids
reducing the concrete 4096-element row universe during elaboration. -/
theorem disjoint_zero_column_product
    (T : Finset Row) (U : Finset Column)
    (hzero : (0 : Column) ∉ U) :
    Disjoint (T.product ({0} : Finset Column))
      ((Finset.univ : Finset Row).product U) := by
  rw [Finset.disjoint_left]
  intro ab hcore hblock
  have hc := Finset.mem_product.mp hcore
  have hb := Finset.mem_product.mp hblock
  have hz : ab.2 = (0 : Column) := Finset.mem_singleton.mp hc.2
  exact hzero (hz ▸ hb.2)

/-- Candidate sets lie in {1,...,511}, so the core and full blocks
do not overlap. -/
theorem pair_disjoint {U : Finset Small} (hU : U ∈ Candidates) :
    Disjoint corePairs (blockPairs U) := by
  have hnot : (0 : Small) ∉ U := by
    intro h0
    have hout := (Finset.mem_powersetCard.mp hU).1 h0
    simpa [outer] using hout
  exact disjoint_zero_column_product coreRows U hnot

/-- Exactly 272 complete 4096-point fibres and 4095 additional points
in column zero, with no multiplicity or support collisions. -/
theorem support_card {U : Finset Small} (hU : U ∈ Candidates) :
    (support U).card = 1118207 := by
  have hcore : corePairs.card = 4095 := by
    simp [corePairs, coreRows_card]
  have hblock : (blockPairs U).card = 4096 * 272 := by
    simp [blockPairs, candidate_card hU]
  calc
    (support U).card = (pairSet U).card := by
      exact Finset.card_image_of_injective _ idx_injective
    _ = corePairs.card + (blockPairs U).card := by
      exact Finset.card_union_of_disjoint (pair_disjoint hU)
    _ = 1118207 := by norm_num [hcore, hblock]

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


/-- A polymorphic image-of-union eliminator.  Its proof is elaborated without
    specializing to the 4096-row KoalaBear Finset. -/
theorem mem_image_union_cases
    {α β : Type*} [DecidableEq α] [DecidableEq β]
    (A B : Finset α) (f : α → β) {z : β}
    (hz : z ∈ (A ∪ B).image f) :
    (∃ x, x ∈ A ∧ f x = z) ∨ (∃ x, x ∈ B ∧ f x = z) := by
  obtain ⟨x, hx, hfx⟩ := Finset.mem_image.mp hz
  rcases Finset.mem_union.mp hx with ha | hb
  · exact Or.inl ⟨x, ha, hfx⟩
  · exact Or.inr ⟨x, hb, hfx⟩

/-- Keep the concrete 2^21 support opaque for downstream pointwise proofs. -/
theorem support_cases (U : Finset Small) (j : Index)
    (hj : j ∈ support U) :
    (∃ ab, ab ∈ corePairs ∧ idx ab.1 ab.2 = j) ∨
      (∃ ab, ab ∈ blockPairs U ∧ idx ab.1 ab.2 = j) := by
  classical
  rw [support, pairSet] at hj
  exact mem_image_union_cases corePairs (blockPairs U)
    (fun ab : Row × Column => idx ab.1 ab.2) hj

end OrbitPencilLiftSupport4096
