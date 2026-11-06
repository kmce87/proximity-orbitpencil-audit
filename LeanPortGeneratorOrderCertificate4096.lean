import LeanPortDomainPowers4096
namespace OrbitPencilLiftDomainPowers4096
open OrbitPencilLiftGeometry
open OrbitPencilLiftDomainTransport4096
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096
private abbrev g : Sextic := baseToSextic omega21
theorem generator_pow_full : g ^ 2097152 = 1 := by
  have hlog : baseNttDomain21.logN = 21 := rfl
  have hw : omega21 ^ 2097152 = 1 := by
    simpa only [omega21, hlog, show (2 : ℕ) ^ 21 = 2097152 by norm_num] using
      baseNttDomain21.primitive.pow_eq_one
  change (baseToSextic omega21) ^ 2097152 = 1
  rw [← map_pow, hw, map_one]
theorem generator_no_short_period (t : ℕ) (ht : 0 < t) (hlt : t < 2097152) :
    g ^ t ≠ 1 := by
  intro hp
  have hzero : node6 (0 : Index) = g ^ 0 := node6_as_power 0
  have htval : node6 (⟨t, hlt⟩ : Index) = g ^ t := node6_as_power ⟨t, hlt⟩
  have heq : node6 (⟨t, hlt⟩ : Index) = node6 (0 : Index) := by
    rw [htval, hzero, hp, pow_zero]
  have hi := node6_injective heq
  have hv : t = 0 := congrArg Fin.val hi
  exact Nat.ne_of_gt ht hv
#print axioms OrbitPencilLiftDomainPowers4096.generator_pow_full
#print axioms OrbitPencilLiftDomainPowers4096.generator_no_short_period
end OrbitPencilLiftDomainPowers4096
