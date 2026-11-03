import LeanPortPointwiseSupport4096

/-!
# Typed support: count actual agreement witnesses without finite-image elimination

Hypothesis: a tagged sum of *coordinate subtypes* avoids reduction of the
concrete 2^21-point Finset image, and proves a 1,118,207 lower bound on the
number of indices satisfying logicalSupport. This does not yet assemble an
MCA-bad-slope witness or an official ProtocolClaim.

The 4096-fibre rational-pencil adaptation builds on the accepted 512-fibre
OrbitPencil submission, proximity-prize/proximity-prize PR #38 (including
co-author erdkocak). No originality or prize acceptance is claimed.
-/

namespace OrbitPencilLiftTypedSupport4096

open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

/-- Core points and selected-column points carry their membership *in their
type*, so no proof ever has to eliminate membership in a huge finite image. -/
abbrev SelectedPoint (U : Finset Small) : Type :=
  (↑coreRows : Type) ⊕ (Row × (↑U : Type))

def pointIndex (U : Finset Small) : SelectedPoint U → Index
  | .inl a => idx a.val 0
  | .inr ab => idx ab.1 ab.2.val

theorem point_logical (U : Finset Small) (x : SelectedPoint U) :
    logicalSupport U (pointIndex U x) := by
  cases x with
  | inl a =>
      exact Or.inl ⟨a.val, a.property, rfl⟩
  | inr ab =>
      exact Or.inr ⟨ab.1, ab.2.val, ab.2.property, rfl⟩

/-- The core column is zero, whereas all selected columns are nonzero.
This makes the two tags disjoint and prevents any index deduplication. -/
theorem pointIndex_injective (U : Finset Small)
    (hzero : (0 : Column) ∉ U) :
    Function.Injective (pointIndex U) := by
  intro x y h
  cases x with
  | inl a =>
    cases y with
    | inl b =>
        have hp : (a.val, (0 : Column)) = (b.val, (0 : Column)) :=
          idx_injective (by simpa only [pointIndex] using h)
        have he : a.val = b.val := congrArg Prod.fst hp
        exact congrArg Sum.inl (Subtype.ext he)
    | inr ab =>
        have hp : (a.val, (0 : Column)) = (ab.1, ab.2.val) :=
          idx_injective (by simpa only [pointIndex] using h)
        have hz : (0 : Column) = ab.2.val := congrArg Prod.snd hp
        exact False.elim (hzero (hz.symm ▸ ab.2.property))
  | inr ab =>
    cases y with
    | inl b =>
        have hp : (ab.1, ab.2.val) = (b.val, (0 : Column)) :=
          idx_injective (by simpa only [pointIndex] using h)
        have hz : ab.2.val = (0 : Column) := congrArg Prod.snd hp
        exact False.elim (hzero (hz ▸ ab.2.property))
    | inr cd =>
        have hp : (ab.1, ab.2.val) = (cd.1, cd.2.val) :=
          idx_injective (by simpa only [pointIndex] using h)
        have ha : ab.1 = cd.1 := congrArg (fun q : Row × Column => q.1) hp
        have hb : ab.2.val = cd.2.val := congrArg (fun q : Row × Column => q.2) hp
        exact congrArg Sum.inr (Prod.ext ha (Subtype.ext hb))

theorem selected_card (U : Finset Small) (hU : U ∈ Candidates) :
    Fintype.card (SelectedPoint U) = 1118207 := by
  classical
  simp only [SelectedPoint, Fintype.card_sum, Fintype.card_prod,
    Fintype.card_coe, Row, Fintype.card_fin, coreRows_card, candidate_card hU]

/-- A proof of >= 1,118,207 distinct logical-support indices, requiring no
membership-elimination lemma for the giant concrete finite support. -/
theorem logical_support_card_lower (U : Finset Small) (hU : U ∈ Candidates)
    [DecidablePred (logicalSupport U)] :
    1118207 ≤ Fintype.card {j : Index // logicalSupport U j} := by
  classical
  have hzero : (0 : Column) ∉ U := by
    intro h0
    have hout := (Finset.mem_powersetCard.mp hU).1 h0
    simpa [outer] using hout
  let f : SelectedPoint U → {j : Index // logicalSupport U j} :=
    fun x => ⟨pointIndex U x, point_logical U x⟩
  have hinj : Function.Injective f := by
    intro x y h
    apply pointIndex_injective U hzero
    exact congrArg Subtype.val h
  have hcard := Fintype.card_le_of_injective f hinj
  rw [selected_card U hU] at hcard
  exact hcard

#print axioms OrbitPencilLiftTypedSupport4096.point_logical
#print axioms OrbitPencilLiftTypedSupport4096.pointIndex_injective
#print axioms OrbitPencilLiftTypedSupport4096.selected_card
#print axioms OrbitPencilLiftTypedSupport4096.logical_support_card_lower

end OrbitPencilLiftTypedSupport4096
