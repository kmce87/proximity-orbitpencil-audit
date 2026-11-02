import LeanPortPredicateSupportProbe

/-!
Concrete finite-image bridge for the 4096 × 512 KoalaBear support.
A deliberately separate compile gate: if this fails but the predicate probe
passes, the image-membership bridge, not the large index type or the
witness-level support decomposition, is the remaining elaboration blocker.
No MCA counterexample or prize verification is claimed.
-/

namespace OrbitPencilLiftConcreteSupportProbe
open OrbitPencilLiftGeometry
open OrbitPencilLiftPredicateSupportProbe
set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

noncomputable def support (U : Finset Column) : Finset Index :=
  (pairSet U).image encodePair

theorem concrete_support_to_witness (U : Finset Column) (j : Index)
    (hj : j ∈ support U) :
    supportWitness U j := by
  classical
  change j ∈ (pairSet U).image encodePair at hj
  exact Finset.mem_image.mp hj

theorem concrete_support_cases (U : Finset Column) (j : Index)
    (hj : j ∈ support U) :
    (∃ ab, ab ∈ corePairs ∧ encodePair ab = j) ∨
      (∃ ab, ab ∈ blockPairs U ∧ encodePair ab = j) :=
  predicate_support_cases U j (concrete_support_to_witness U j hj)

#print axioms OrbitPencilLiftConcreteSupportProbe.concrete_support_cases
end OrbitPencilLiftConcreteSupportProbe
