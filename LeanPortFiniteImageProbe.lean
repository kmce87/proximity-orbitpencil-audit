import LeanPortGeometry

/-!
# Minimal Finset image-membership elaboration probe

One falsifiable diagnostic: is the large concrete index TYPE (Fin 2097152)
alone responsible for the recursion error in support_cases?  This file
deliberately leaves the input Finsets as opaque parameters.  No proof of
the MCA bound, no claim about the official Proximity Prize verifier.
-/

namespace OrbitPencilLiftFiniteImageProbe

open OrbitPencilLiftGeometry

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

def encodePair (ab : Row × Column) : Index := idx ab.1 ab.2

/-- The exact large concrete row/column/index types, but no unfolded
    Finset.univ/product/image support definitions. -/
theorem concrete_type_image_union_cases
    (A B : Finset (Row × Column)) (j : Index)
    (hj : j ∈ (A ∪ B).image encodePair) :
    (∃ ab, ab ∈ A ∧ encodePair ab = j) ∨
      (∃ ab, ab ∈ B ∧ encodePair ab = j) := by
  classical
  obtain ⟨ab, hab, hencode⟩ := Finset.mem_image.mp hj
  rcases Finset.mem_union.mp hab with ha | hb
  · exact Or.inl ⟨ab, ha, hencode⟩
  · exact Or.inr ⟨ab, hb, hencode⟩

#print axioms OrbitPencilLiftFiniteImageProbe.concrete_type_image_union_cases

end OrbitPencilLiftFiniteImageProbe
