import LeanPortDeployedStrongDomain4096

/-!
Lane A: concrete evaluation-domain powers bridge.
Falsifiable target: D is exactly the powers of the embedded KoalaBear
omega21 with exponents in Fin 2097152, not merely an arbitrary image.
This is a source candidate until a pinned Lean 4.34 job checks it.
No claim of external rs-mca domain equality is made.
-/

namespace OrbitPencilLiftDomainPowers4096
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096
open OrbitPencilLiftDomainTransport4096

theorem node6_as_power (j : Index) :
    node6 j = (baseToSextic omega21) ^ j.val := by
  simp only [node6, node21, map_pow]

theorem domain_eq_bounded_powers :
    D = {x : Sextic | ∃ j : Index,
      (baseToSextic omega21) ^ j.val = x} := by
  ext x
  simp only [D, Set.mem_range, Set.mem_setOf_eq]
  constructor
  · rintro ⟨j, rfl⟩
    exact ⟨j, (node6_as_power j).symm⟩
  · rintro ⟨j, hj⟩
    exact ⟨j, (node6_as_power j).trans hj⟩

#print axioms OrbitPencilLiftDomainPowers4096.node6_as_power
#print axioms OrbitPencilLiftDomainPowers4096.domain_eq_bounded_powers
end OrbitPencilLiftDomainPowers4096
