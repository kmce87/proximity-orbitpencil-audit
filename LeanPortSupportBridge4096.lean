import LeanPortSupport4096

/-!
One falsifiable Lean 4.34 elaboration experiment: abstract the *actual*
finite-set arguments before applying the already-compiled polymorphic
image-of-union eliminator.  The preceding PR #20 specialized the lemma to
corePairs and blockPairs U, triggering maximum recursion depth.

This proof, if accepted, bridges membership in the concrete 1118207-point
support to logicalSupport. It does NOT prove any MCA bad-slope theorem.
Original rational-pencil source: Proximity Prize PR #38, co-author erdkocak.
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
  -- The eliminator must see local Finsets A and B, not the expanded
  -- 4096-row / 272-column concrete expressions.
  generalize hcore : corePairs = A at hj
  generalize hblock : blockPairs U = B at hj
  rcases mem_image_union_cases A B encodePair hj with
    ⟨ab, hc, heq⟩ | ⟨ab, hb, heq⟩
  · have hc' : ab ∈ corePairs := by simpa only [hcore] using hc
    have hp : ab.1 ∈ coreRows ∧ ab.2 ∈ ({0} : Finset Column) :=
      Finset.mem_product.mp (show ab ∈ coreRows.product ({0} : Finset Column) from hc')
    have hz : ab.2 = (0 : Column) := Finset.mem_singleton.mp hp.2
    left
    refine ⟨ab.1, hp.1, ?_⟩
    simpa only [encodePair, hz] using heq
  · have hb' : ab ∈ blockPairs U := by simpa only [hblock] using hb
    have hp : ab.1 ∈ (Finset.univ : Finset Row) ∧ ab.2 ∈ U :=
      Finset.mem_product.mp (show ab ∈ (Finset.univ : Finset Row).product U from hb')
    exact Or.inr ⟨ab.1, ab.2, hp.2, heq⟩

#print axioms OrbitPencilLiftSupportBridge4096.support_to_logical

end OrbitPencilLiftSupportBridge4096
