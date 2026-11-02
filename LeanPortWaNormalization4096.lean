import LeanPortWaBridge4096

/-!
# Exact field-size normalization of the support-wise MCA witness

Falsifiable target: transfer the previously kernel-checked local W_a
counterexample to the integer inequality that is equivalent to an MCA
error strictly exceeding 2^(-128), assuming the published identity
eps_mca = LD_sw / |F| for the matching RS code and challenge field.

This is NOT an independent verifier acceptance or a Proximity Prize
ProtocolClaim. It uses the concrete KoalaBear.Ext6 cardinality, not
the base field's size. Original OrbitPencil 512-fibre source: official
proximity-prize/proximity-prize PR #38, including erdkocak.
-/

namespace OrbitPencilLiftWaNormalization4096

open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftWaBridge4096

/-- New normalization gate: the smallest cardinality above B* already
has normalized mass strictly greater than 2^(-128). -/
theorem budget_successor_exceeds_field :
    (2130706433 : ℕ)^6 <
      (2 : ℕ)^128 * 274980728111395088 := by
  norm_num

/-- One received affine line has a finite set of DISTINCT bad slopes
whose count, multiplied by 2^128, strictly exceeds the entire sextic
challenge-field cardinality. This is the exact cross-multiplied MCA
error threshold, with no floating-point rounding. -/
theorem exists_W_above_normalized_budget :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      Fintype.card Sextic < (2 : ℕ)^128 * Z.card ∧
      alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      ∀ z ∈ Z,
        BadSlope (receivedBase alpha U0) (receivedDirection alpha) z := by
  obtain ⟨alpha, U0, Z, hZ, halpha, havoid, hbad⟩ :=
    exists_many_W_bad_slopes
  have hmin : 274980728111395088 ≤ Z.card := by omega
  refine ⟨alpha, U0, Z, ?_, halpha, havoid, hbad⟩
  calc
    Fintype.card Sextic = (2130706433 : ℕ)^6 :=
      concrete_sextic_card
    _ < (2 : ℕ)^128 * 274980728111395088 :=
      budget_successor_exceeds_field
    _ ≤ (2 : ℕ)^128 * Z.card :=
      Nat.mul_le_mul_left _ hmin

#print axioms OrbitPencilLiftWaNormalization4096.budget_successor_exceeds_field
#print axioms OrbitPencilLiftWaNormalization4096.exists_W_above_normalized_budget

end OrbitPencilLiftWaNormalization4096
