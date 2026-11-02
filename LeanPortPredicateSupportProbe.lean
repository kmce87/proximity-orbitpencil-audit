import LeanPortGeometry

/-!
Minimal diagnostic for the actual 4096 × 512 support, independent of KoalaBear
field imports. This is NOT a proof that the large-n MCA claim holds.
The predicate is an explicit existential witness; its connection to the
finite image support is tested separately in LeanPortConcreteSupportProbe.
Original OrbitPencil idea: proximity-prize PR #38, including erdkocak.
-/

namespace OrbitPencilLiftPredicateSupportProbe
open OrbitPencilLiftGeometry
set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

noncomputable def coreRows : Finset Row := Finset.univ.erase 0
noncomputable def corePairs : Finset (Row × Column) :=
  coreRows.product {0}
noncomputable def blockPairs (U : Finset Column) : Finset (Row × Column) :=
  Finset.univ.product U
noncomputable def pairSet (U : Finset Column) : Finset (Row × Column) :=
  corePairs ∪ blockPairs U
def encodePair (ab : Row × Column) : Index := idx ab.1 ab.2

/-- Witness-level support, deliberately not a Finset.image membership. -/
def supportWitness (U : Finset Column) (j : Index) : Prop :=
  ∃ ab : Row × Column, ab ∈ pairSet U ∧ encodePair ab = j

theorem predicate_support_cases (U : Finset Column) (j : Index)
    (hj : supportWitness U j) :
    (∃ ab, ab ∈ corePairs ∧ encodePair ab = j) ∨
      (∃ ab, ab ∈ blockPairs U ∧ encodePair ab = j) := by
  rcases hj with ⟨ab, hab, heq⟩
  change ab ∈ corePairs ∪ blockPairs U at hab
  rcases Finset.mem_union.mp hab with hc | hb
  · exact Or.inl ⟨ab, hc, heq⟩
  · exact Or.inr ⟨ab, hb, heq⟩

#print axioms OrbitPencilLiftPredicateSupportProbe.predicate_support_cases
end OrbitPencilLiftPredicateSupportProbe
