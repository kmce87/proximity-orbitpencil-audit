import LeanPortDomainTransport4096

/-! Exact generator-power identity; separate from external manuscript field identification. -/
namespace OrbitPencilLiftDomainTransport4096

open OrbitPencilLiftGeometry OrbitPencilLiftSameKey OrbitPencilLiftSupport4096

theorem node6_eq_embedded_omega_pow (j : OrbitPencilLiftGeometry.Index) :
    node6 j = baseToSextic (omega21 ^ j.val) := by
  rfl

theorem D_eq_embedded_omega_powers :
    D = {x : Sextic | ∃ j : OrbitPencilLiftGeometry.Index,
      x = baseToSextic (omega21 ^ j.val)} := by
  ext x
  constructor
  · rintro ⟨j, rfl⟩
    exact ⟨j, node6_eq_embedded_omega_pow j⟩
  · rintro ⟨j, rfl⟩
    exact ⟨j, node6_eq_embedded_omega_pow j⟩

#print axioms OrbitPencilLiftDomainTransport4096.node6_eq_embedded_omega_pow
#print axioms OrbitPencilLiftDomainTransport4096.D_eq_embedded_omega_powers

end OrbitPencilLiftDomainTransport4096
