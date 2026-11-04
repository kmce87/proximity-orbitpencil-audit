# KoalaBear sextic NTT-domain identity: falsification-first source audit (2026-11-04 UTC)

## Hypothesis
The local domain `D := Set.range node6` is exactly the order-2^21 subgroup of the published KoalaBear sextic challenge field, not merely a 2^21-element set.

## Pinned sources
- `LeanPortSameKeyFamily.lean`: `baseNttDomain21 := CompPoly.CPolynomial.NTT.KoalaBear.domainOfLogN 21`; `omega21 := baseNttDomain21.omega`; `projectedNode b := (omega21 ^ b.val)^4096`; `baseNttDomain21.primitive.pow_inj`.
- `LeanPortDomainTransport4096.lean`: `D := Set.range node6`, `node6_injective`, `indexEquiv : Index ≃ D`, `W_to_domain`.
- `LeanPortDeployedTransfer4096.lean`: deployed explaining degree <= 1048575, noncontainment even at <=1048576.
- `LeanPortCAP25Event4096.lean`: `Explains` degree < 1048576; same fixed received pair, slope-dependent support.
- CAP25 manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
- Original accepted prior art: https://github.com/proximity-prize/proximity-prize/pull/38

## Source-checked result and precise gap
The concrete NTT generator is sourced from CompPoly's KoalaBear domain of log-size 21, rather than chosen as an arbitrary primitive root. The `Index ≃ D` equivalence and `node6_injective` establish distinctness of the 2^21 evaluation points. However, cardinality and injectivity alone do **not** establish equality to the published subgroup: a set of 2^21 arbitrary field elements could also satisfy both.

To close the remaining gap in Lean, prove:
1. `∀ j : Index, node6 j = baseToSextic (omega21 ^ j.val)` (or the exact orientation used by the underlying definition);
2. `(baseToSextic omega21) ^ 2097152 = 1`, and no smaller positive exponent divides its order (from `baseNttDomain21.primitive`);
3. `D = Subgroup.closure {baseToSextic omega21}` as a set, and identify it with the manuscript's order-2^21 subgroup.
4. Verify the manuscript uses the same sextic extension field up to an explicit field isomorphism; finite-field isomorphism by cardinality alone is not definitional identity. If it uses another representation, transport received words, polynomials, evaluation and slope sampling through the isomorphism.

## Reproduction (clean checkout with Lean 4.34 and dependencies)
```bash
git checkout fee0051256585c590bae034a1158909900ce26c8
bash scripts/run_lean_434_gate.sh
lake env lean -o .lake/build/lib/lean/LeanPortDomainTransport4096.olean LeanPortDomainTransport4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortDeployedTransfer4096.olean LeanPortDeployedTransfer4096.lean
lake env lean LeanPortCAP25Event4096.lean
```

This is a source audit, not a new compiled theorem. No external acceptance or originality conclusion. Ordinary LIST at agreement 1116047 remains separate.
