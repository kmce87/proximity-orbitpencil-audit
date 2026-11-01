import Mathlib

/-!
  Independent Lean 4 / Mathlib adaptation candidate for the KoalaBear
  n = 2^21 fibre geometry used in an OrbitPencil MCA audit.

  STATUS: UNCOMPILED. No Lean executable or Mathlib build was available in
  this sandbox. This is a port candidate, NOT a Lean certificate.
  Credit for original 512-by-512 pattern: accepted OrbitPencil PR #38,
  proximity-prize/proximity-prize, including erdkocak.
-/

namespace OrbitPencilLiftGeometry

abbrev Row := Fin 4096
abbrev Column := Fin 512
abbrev Index := Fin 2097152

/-- Row-major index of a point in a 4096-by-512 grid. -/
def idx (a : Row) (b : Column) : Index :=
  ⟨a.val * 512 + b.val, by omega⟩

/-- Different row-column pairs encode different domain points. -/
theorem idx_injective :
    Function.Injective (fun ab : Row × Column => idx ab.1 ab.2) := by
  intro ab cd h
  apply Prod.ext
  · apply Fin.ext
    have hv := congrArg Fin.val h
    dsimp [idx] at hv
    omega
  · apply Fin.ext
    have hv := congrArg Fin.val h
    dsimp [idx] at hv
    omega

/-- Inverse coordinates of an index. -/
def row (j : Index) : Row := ⟨j.val / 512, by omega⟩
def column (j : Index) : Column := ⟨j.val % 512, Nat.mod_lt _ (by norm_num)⟩

theorem idx_row_column (j : Index) : idx (row j) (column j) = j := by
  apply Fin.ext
  simp only [idx, row, column]
  omega

/-- Every 4096-th power depends only on the projected column. -/
theorem pow_block {K : Type*} [CommMonoid K] (w : K)
    (hw : w ^ 2097152 = 1) (a : Row) (b : Column) :
    (w ^ (a.val * 512 + b.val)) ^ 4096 = (w ^ b.val) ^ 4096 := by
  rw [pow_add, mul_pow, ← pow_mul, ← pow_mul]
  rw [show (a.val * 512) * 4096 = a.val * 2097152 by ring]
  rw [show b.val * 4096 = 4096 * b.val by omega]
  rw [show a.val * 2097152 = 2097152 * a.val by omega, pow_mul]
  rw [hw, one_pow, one_mul]

end OrbitPencilLiftGeometry
