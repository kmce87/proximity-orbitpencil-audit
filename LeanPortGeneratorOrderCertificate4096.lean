import LeanPortSameKeyFamily

/-!
# Explicit exact-order obligations for the KoalaBear 2^21 NTT generator

This file deliberately separates full-power identity and absence of
premature identity powers. It does not claim an external MCA certificate.
-/

namespace OrbitPencilLiftSameKey

theorem omega21_pow_full_cert : omega21 ^ 2097152 = 1 := by
  have hlog : baseNttDomain21.logN = 21 := rfl
  simpa only [omega21, hlog, show (2 : ℕ) ^ 21 = 2097152 by norm_num] using
    baseNttDomain21.primitive.pow_eq_one

theorem omega21_no_early_identity_cert
    {i : ℕ} (hi : 0 < i) (hbound : i < 2097152) :
    omega21 ^ i ≠ 1 := by
  intro h
  have heq : omega21 ^ i = omega21 ^ 0 := by simpa using h
  have hi0 : i = 0 := by
    apply baseNttDomain21.primitive.pow_inj
    · exact hbound
    · norm_num
    · simpa only [omega21] using heq
  omega

theorem sextic_omega21_pow_full_cert :
    (baseToSextic omega21) ^ 2097152 = 1 := by
  rw [← map_pow, omega21_pow_full_cert, map_one]

theorem sextic_omega21_no_early_identity_cert
    {i : ℕ} (hi : 0 < i) (hbound : i < 2097152) :
    (baseToSextic omega21) ^ i ≠ 1 := by
  intro h
  have hbase : omega21 ^ i = 1 := by
    apply baseToSextic.injective
    simpa only [map_pow, map_one] using h
  exact omega21_no_early_identity_cert hi hbound hbase

#print axioms omega21_pow_full_cert
#print axioms omega21_no_early_identity_cert
#print axioms sextic_omega21_pow_full_cert
#print axioms sextic_omega21_no_early_identity_cert

end OrbitPencilLiftSameKey
