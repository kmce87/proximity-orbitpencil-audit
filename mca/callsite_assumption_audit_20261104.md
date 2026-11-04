# Lane A — concrete indexed noncontainment call-site audit (2026-11-04 18:11 UTC)

## Single falsifiable hypothesis
At parent commit a0e9313b91e2e8fae2c91430dcfda87fb6631907, the call from `received_direction_not_rs_on_support` to `quotient_direction_not_codeword_on_indices` explicitly supplies the indexed-domain injectivity, denominator nonvanishing, and quotient identity assumptions, without assuming the desired noncontainment conclusion.

## Inspected source
- `LeanPortIndexedNoncontainment.lean` (blob dd2bd9cd69d4c40813631f8a26a84efc9d0dabd0)
- `LeanPortDirectionNoncode4096.lean` (blob 58b971f7e8e60efb5918256e63a92de24f3e85e0)
- `LeanPortMcaComposition4096.lean` (blob bbdd21145974a5a4c91219a9234736a36380f78f)

## Source-level result: supported, NOT independently kernel-checked this run
1. `node6_injective` is proved by applying `node21_injective` to the injectivity of `baseToSextic`; this depends on the imported concrete geometry proofs, not an axiom inserted at this call site.
2. `hdenom` uses `node6_pow_ne_alpha alpha havoid j` to show `(node6 j)^4096 - alpha ≠ 0`, then rewrites the polynomial evaluation identity.
3. `hquot` rewrites `A.eval (node6 j)` into `(node6 j)^4096-alpha` and applies the hypothesized RS explanation `hmatch j hjS`.
4. `hScard` is an explicit hypothesis of `received_direction_not_rs_on_support`; `exists_many_supportwise_bad_slopes` constructs S from the subtype of agreement positions, proves its cardinality at least 1,118,207, then supplies the 1,116,048 threshold by `omega`.
5. The direction noncontainment excludes polynomials of degree ≤ 1,048,576. The explaining polynomial supplied by `hagree` has degree ≤ 1,048,575. These bounds are deliberately different and no inference from auxiliary RS[D,k+1] to RS[D,k] is made.

## Limits / falsification conditions
This is source inspection, not a fresh Lean execution. It does not independently verify imported `node21_injective`, `baseToSextic.injective`, `node6_pow_ne_alpha`, or `hagree`; nor does it identify the published sextic field/domain, the exact external MCA event, or an independent prize verifier. A mismatch in any imported assumption, or a compiler failure, would invalidate stronger certification claims. The local predicate is not automatically the manuscript predicate.

## Reproduce
```sh
git checkout a0e9313b91e2e8fae2c91430dcfda87fb6631907
grep -n -E 'theorem node6_injective|theorem received_direction_not_rs_on_support|have hdenom|have hquot|quotient_direction_not_codeword_on_indices' LeanPortDirectionNoncode4096.lean
grep -n -E 'def SupportWiseBad|theorem exists_many_supportwise_bad_slopes|hScard|received_direction_not_rs_on_support' LeanPortMcaComposition4096.lean
bash scripts/run_lean_434_gate.sh
lake env lean LeanPortIndexedNoncontainment.lean
lake env lean LeanPortDirectionNoncode4096.lean
lake env lean LeanPortMcaComposition4096.lean
```
The compilation commands are required future tests, not executions claimed here.

## Next precise blocker
Kernel-check this exact dependency chain and compare the fixed-line support-wise event against the rs-mca manuscript's quantifier order and deployed RS[D,2^20] definition. Then establish the concrete sextic field/domain equivalence. Original OrbitPencil source: https://github.com/proximity-prize/proximity-prize/pull/38 ; external manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex . No new novelty or upstream-report status was established.
