import LeanPortCAP25Budget4096

/-!
# Exact full-field MCA numerator/denominator bridge (local model)

Falsifiable target: the already kernel-checked fixed-pair finite bad-slope
witness implies a strict probability bound after normalizing by the
EXACT KoalaBear sextic field cardinality, rather than comparing to a
manually supplied budget. This is still a local CAP25-shaped predicate,
not a formal import of the external manuscript or independent acceptance.

CAP25 v13.2: przchojecki/rs-mca, tex/cs25_cap_v13_2.tex,
revision 4bea7abb2d9455583c8864b980e39d11d550f51d.
Original OrbitPencil prior art: proximity-prize/proximity-prize PR #38.
-/

namespace OrbitPencilCAP25Probability4096

open OrbitPencilLiftSameKey
open OrbitPencilLiftDomainTransport4096
open OrbitPencilCAP25Budget4096

/-- The exact finite set of bad slopes for a fixed received pair. -/
noncomputable def badSlopes (f g : D → Sextic) : Finset Sextic :=
  Finset.univ.filter (CAP25BadAtA0 f g)

/-- No loss of distinct slopes when passing from a witness set to the
full-field bad-slope numerator. -/
theorem witness_le_badSlopes (f g : D → Sextic)
    (Z : Finset Sextic)
    (h : ∀ z ∈ Z, CAP25BadAtA0 f g z) :
    Z.card ≤ (badSlopes f g).card := by
  classical
  apply Finset.card_le_card
  intro z hz
  simp only [badSlopes, Finset.mem_filter, Finset.mem_univ, true_and]
  exact h z hz

/-- A STRICT numerator bound in the full field, with the denominator
supplied by the concrete CompPoly KoalaBear sextic cardinality theorem.
The integer cross-product is exactly equivalent to
badSlopes.card / |Sextic| > 1 / 2^128 over rational numbers. -/
theorem exists_fixed_pair_probability_cross_product :
    ∃ f g : D → Sextic,
      Fintype.card Sextic <
        (2 : ℕ)^128 * (badSlopes f g).card := by
  classical
  obtain ⟨f, g, Z, hZ, hbad⟩ :=
    exists_many_CAP25_a0_above_budget
  have hsubset := witness_le_badSlopes f g Z hbad
  have hpositive :
      (2130706433 : ℕ)^6 <
        (2 : ℕ)^128 * (274980728111395087 + 1) := by
    norm_num
  have hmult :
      (2 : ℕ)^128 * (274980728111395087 + 1) ≤
        (2 : ℕ)^128 * (badSlopes f g).card := by
    exact Nat.mul_le_mul_left _ (by omega)
  refine ⟨f, g, ?_⟩
  rw [concrete_sextic_card]
  omega

#print axioms OrbitPencilCAP25Probability4096.witness_le_badSlopes
#print axioms OrbitPencilCAP25Probability4096.exists_fixed_pair_probability_cross_product

end OrbitPencilCAP25Probability4096
