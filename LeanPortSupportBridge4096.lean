import LeanPortSupport4096

/-!
Falsifiable 4096-fibre support bridge: prove that actual finite support
membership yields a logical row/column witness. The earlier variant used
`rw [support]` plus a large concrete iff term and failed in elaboration.
This variant keeps the finite-image expression opaque until the membership
eliminator runs. It does not establish the MCA counterexample.
Original rational-pencil construction: Proximity Prize PR #38 (erdkocak).
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
  change j ∈ (pairSet U).image encodePair at hj
  obtain ⟨ab, hab, heq⟩ := Finset.mem_image.mp hj
  change ab ∈ corePairs ∪ blockPairs U at hab
  rcases Finset.mem_union.mp hab with hc | hb
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
