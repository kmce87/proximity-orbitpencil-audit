import LeanPortSupport4096

/-!
# Abstract product elimination for the actual 4096-fibre support

Falsifiable hypothesis: eliminating *both* the image/union and product
memberships at polymorphic types, before specializing to the concrete
4096-row finite set, avoids Lean 4.34's maximum-recursion-depth failure.
Previous PR #21 failed on concrete Finset.mem_product.mp (line 35).

This bridge is a proof-engineering obligation only. It does not certify
an MCA bad slope, the received line, or the official ProtocolClaim.
Original OrbitPencil source: proximity-prize/proximity-prize PR #38,
including co-author erdkocak.
-/

namespace OrbitPencilLiftSupportBridge4096

open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

/-- Entire image-of-union-of-products decomposition, proved at abstract
finite-set types so the eliminators never inspect concrete 4096-row sets. -/
theorem mem_image_product_union_cases
    {α β γ : Type*}
    [DecidableEq α] [DecidableEq β] [DecidableEq γ]
    (R : Finset α) (Z U : Finset β) (f : α × β → γ) {j : γ}
    (hj : j ∈ ((R.product Z) ∪
        ((Finset.univ : Finset α).product U)).image f) :
    (∃ a : α, a ∈ R ∧ ∃ b : β, b ∈ Z ∧ f (a, b) = j) ∨
    (∃ a : α, ∃ b : β, b ∈ U ∧ f (a, b) = j) := by
  classical
  obtain ⟨⟨a, b⟩, hab, heq⟩ := Finset.mem_image.mp hj
  rcases Finset.mem_union.mp hab with hcore | hblock
  · have hp := Finset.mem_product.mp hcore
    exact Or.inl ⟨a, hp.1, b, hp.2, heq⟩
  · have hp := Finset.mem_product.mp hblock
    exact Or.inr ⟨a, b, hp.2, heq⟩

/-- Concrete support membership implies the logical root-support predicate.
The expensive product elimination has been compiled polymorphically. -/
theorem support_to_logical (U : Finset Small) (j : Index)
    (hj : j ∈ support U) : logicalSupport U j := by
  classical
  have hmem : j ∈ ((coreRows.product ({0} : Finset Column)) ∪
      ((Finset.univ : Finset Row).product U)).image encodePair := by
    change j ∈ (corePairs ∪ blockPairs U).image encodePair at hj
    change j ∈ ((coreRows.product ({0} : Finset Column)) ∪
      ((Finset.univ : Finset Row).product U)).image encodePair at hj
    exact hj
  rcases mem_image_product_union_cases coreRows ({0} : Finset Column)
      U encodePair hmem with
    ⟨a, ha, b, hb, heq⟩ | ⟨a, b, hb, heq⟩
  · have hz : b = (0 : Column) := Finset.mem_singleton.mp hb
    exact Or.inl ⟨a, ha, by simpa only [encodePair, hz] using heq⟩
  · exact Or.inr ⟨a, b, hb, heq⟩

#print axioms OrbitPencilLiftSupportBridge4096.mem_image_product_union_cases
#print axioms OrbitPencilLiftSupportBridge4096.support_to_logical

end OrbitPencilLiftSupportBridge4096
