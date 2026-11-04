# MCA generator identity: falsification gate (2026-11-04 08:34 UTC)

Pinned parent: `6ed09ffb0409641be7bc622d61e4c34c07048f3d`.
Hypothesis: `LeanPortGeneratorPowerIdentity4096.lean` compiles on Lean 4.34 with no `sorryAx`, and its domain equality really identifies the indexed domain with the set of embedded NTT powers.

## Direct source inspection

* `LeanPortSupport4096.lean`: `node21 j := omega21 ^ j.val` and `node6 j := baseToSextic (node21 j)`.
* `LeanPortDomainTransport4096.lean`: `D := Set.range node6`; `node6_injective` uses injectivity of the prime-to-sextic field homomorphism.
* `LeanPortSameKeyFamily.lean`: `omega21` comes from `CompPoly.CPolynomial.NTT.KoalaBear.domainOfLogN 21`, and `node21_injective` uses `baseNttDomain21.primitive.pow_inj`.
* `LeanPortGeneratorPowerIdentity4096.lean`: proposed `node6_eq_embedded_omega_pow` and `D_eq_embedded_omega_powers`.

These sources support a **definitional** equality between the local indexed domain and embedded NTT powers. They do not alone establish an independently defined external sextic field model or identify the external author's domain choice.

## Replay (fail closed)

```sh
git checkout 6ed09ffb0409641be7bc622d61e4c34c07048f3d
bash scripts/run_lean_434_gate.sh
lake env lean LeanPortGeneratorPowerIdentity4096.lean 2>&1 | tee /tmp/mca-generator-identity.log
test ${PIPESTATUS[0]} -eq 0
! grep -E 'sorryAx|error:|unsolved goals' /tmp/mca-generator-identity.log
grep 'node6_eq_embedded_omega_pow' /tmp/mca-generator-identity.log
grep 'D_eq_embedded_omega_powers' /tmp/mca-generator-identity.log
```

The command above is a **requested replay**, not evidence of execution. The shell requires Bash for PIPESTATUS. If the module import cannot be resolved, compile the imported dependencies to `.olean` in their repository-defined dependency order first. Audit the `#print axioms` lines; expected kernel axioms are `propext`, `Classical.choice`, `Quot.sound` only.

## Additional obligations before external certification

1. Prove `omega21` has **exact** multiplicative order 2^21 in the prime field, and its embedded image has the same order. Existing `primitive.pow_inj` suggests this but is not an explicit exported theorem in this candidate.
2. Establish equality with the unique subgroup of order 2^21 in the sextic field; an indexed set equality is not by itself a comparison to the manuscript's subgroup definition.
3. Identify the manuscript's field `F_(p^6)` and the concrete CompPoly `KoalaBear.Ext6` by an explicit field isomorphism (or prove representation-independence of MCA/RS).
4. Re-check the **deployed** RS degree < 2^20 witness and noncontainment, distinct slope count, and one fixed received line; do not substitute the auxiliary dimension 2^20+1.
5. Review original OrbitPencil PR #38 for credit and independently search upstream rs-mca for prior reports before posting.

Source: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
Prior art: https://github.com/proximity-prize/proximity-prize/pull/38

No independent verifier acceptance; no prize-qualifying result. LIST inequality at a=1116047 unaffected.
