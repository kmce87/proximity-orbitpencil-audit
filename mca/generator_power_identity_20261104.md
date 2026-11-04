# Generator-power identity: source-level certification gate (2026-11-04 07:49 UTC)

## Single falsifiable hypothesis
For every `j : Index`, `node6 j = baseToSextic (omega21 ^ j.val)`. If this is false, the claimed published-subgroup identification fails.

## Inspected exact definitions
At parent commit `93cf43a5bbf31067ead65f133ecdd2d329a4b4be`:
- `LeanPortSameKeyFamily.lean`: `omega21 := baseNttDomain21.omega`, `baseNttDomain21 := ...domainOfLogN 21`, `baseToSextic := algebraMap KoalaBear.Field Sextic`.
- `LeanPortSupport4096.lean`: `node21 j := omega21 ^ j.val`, `node6 j := baseToSextic (node21 j)`.
- `LeanPortDomainTransport4096.lean`: `D := Set.range node6`; `indexEquiv : Index ≃ D`.

The hypothesis follows by unfolding definitions, *without* any cardinality argument. This establishes the literal power-image identity, not yet the external manuscript's domain identity.

## Proposed Lean theorem (NOT kernel-tested in this run)
```lean
import LeanPortDomainTransport4096
namespace OrbitPencilLiftDomainTransport4096
open OrbitPencilLiftSameKey OrbitPencilLiftSupport4096

theorem node6_eq_embedded_omega_pow (j : Index) :
    node6 j = baseToSextic (omega21 ^ j.val) := by
  rfl

theorem D_eq_embedded_omega_powers :
    D = {x : Sextic | ∃ j : Index, x = baseToSextic (omega21 ^ j.val)} := by
  ext x
  simp only [D, Set.mem_range, Set.mem_setOf_eq]
  constructor
  · rintro ⟨j, rfl⟩
    exact ⟨j, (node6_eq_embedded_omega_pow j).symm⟩
  · rintro ⟨j, rfl⟩
    exact ⟨j, (node6_eq_embedded_omega_pow j).symm⟩
end OrbitPencilLiftDomainTransport4096
```

The first theorem is definitional; the second is a proposed proof and must be compiled before counting as verified. The published subgroup identification additionally needs primitive order 2^21 in the sextic field, subgroup uniqueness, and exact field representation/isomorphism. Injectivity of the embedding and base primitive-order result are present in source but the combined subgroup equality has not been kernel-checked.

## Replay
```bash
git fetch origin
git checkout mca-generator-power-bridge-20261104-0749
bash scripts/run_lean_434_gate.sh
# Put the proposed theorem in a new Lean file and compile with lake env lean.
```

## Falsification and status
Failure modes: wrong index exponent orientation, baseToSextic not the claimed embedding, nonprimitive omega21, manuscript uses a different field representation without a transport theorem. No external reviewer acceptance, no prize-qualifying claim, no changes to old archives. The ordinary LIST bound at agreement 1116047 is unaffected.

Prior art: https://github.com/proximity-prize/proximity-prize/pull/38
Manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
