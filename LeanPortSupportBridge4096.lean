import LeanPortSupport4096

/-!
Falsifiable 4096-fibre support bridge. The preceding CI run (PR #19)
failed at the concrete `Finset.mem_image.mp` elaboration with
"maximum recursion depth". Here the image/union elimination is performed
by the previously compiled polymorphic `mem_image_union_cases` lemma
rather than elaborating the eliminator at the expanded 4096-row support.

This is not yet a proof of an MCA bad-slope counterexample.
Original OrbitPencil rational-pencil source: Proximity Prize PR #38,
including co-author erdkocak.
-/

namespace OrbitPencilLiftSupportBridge4096

open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

theorem support_to_logical (U : Finset Small) (j : Index)
    (hj : j ∈ support U) : logicalSupport U j := by
  classical
  change j ∈ (corePairs ∪ blockPairs U).image encodePair at hj
  rcases mem_image_union_cases corePairs (blockPairs U) encodePair hj with
    ⟨ab, hc, heq⟩ | ⟨ab, hb, heq⟩
  · have hp : ab.1 ∈ coreRows ∧ ab.2 ∈ ({0} : Finset Column) :=
      Finset.mem_product.mp (show ab ∈ coreRows.product ({0} : Finset Column) from hc)
    have hz : ab.2 = (0 : Column) := Finset.mem_singleton.mp hp.2
    left
    refine ⟨ab.1, hp.1, ?_⟩
    simpa only [encodePair, hz] using heq
  · have hp : ab.1 ∈ (Finset.univ : Finset Row) ∧ ab.2 ∈ U :=
      Finset.mem_product.mp (show ab ∈ (Finset.univ : Finset Row).product U from hb)
    exact Or.inr ⟨ab.1, ab.2, hp.2, heq⟩

#print axioms OrbitPencilLiftSupportBridge4096.support_to_logical

end OrbitPencilLiftSupportBridge4096
