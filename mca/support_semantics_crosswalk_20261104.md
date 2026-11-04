# MCA support semantics — falsification-first audit (2026-11-04 05:38 UTC)

## Single hypothesis
The local predicate `CAP25Bad` is a sufficient instance of the published support-wise MCA event at the deployed KoalaBear code, **provided** the independently proved domain identity and concrete field interpretation hold.

## Source pins
- External: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex (definition `def:mca`).
- Local base: https://github.com/kmce87/proximity-orbitpencil-audit/blob/fee0051256585c590bae034a1158909900ce26c8/LeanPortCAP25Event4096.lean
- Domain: same commit, `LeanPortDomainTransport4096.lean`.
- Deployed transfer: same commit, `LeanPortDeployedTransfer4096.lean`.
- Original 512-fibre prior art: https://github.com/proximity-prize/proximity-prize/pull/38

## Predicate-by-predicate crosswalk
External: `max_(f1,f2 in F^n) Pr_(gamma uniform F) [exists S subset D, |S| >= (1-delta)n, dist_S(f1+gamma f2,C)=0 and dist_S((f1,f2),C^2)>0]`.

Local: `exists f g : D -> Sextic, exists Z : Finset Sextic, ... forall z in Z, exists S : Finset D, |S|>=1118207, Explains (f+z*g) S and not (Explains f S and Explains g S)`.

* The order `exists f,g; forall z in Z; exists S` preserves one received pair and permits slope-dependent supports. It is sufficient for the external max, not an equality of predicates.
* `Explains h S` means there is ONE global polynomial `c` with `natDegree c < 1048576` whose evaluations agree on S; it is not arbitrary interpolation with an S-dependent degree cutoff.
* `not (Explains f S and Explains g S)` is exactly failure of simultaneous agreement by a pair of deployed codewords on the SAME support. Stronger local `BadDeployed` excludes degree <= 1048576 for both received words.
* `Finset Sextic` enforces distinct slopes, and `Finset D` distinct evaluation points; `indexEquiv` maps indices bijectively to the domain subtype.
* The external normalized distance on S equals zero iff all points of S agree; `S` is nonempty by the cardinality threshold.
* For delta = 981104/2097152, `ceil((1-delta)n)=1116048`. Agreement 1118207 implies the published event at that radius.
* The full-field uniform probability is at least `|Z|/|Sextic|`; local cross-product theorem proves it exceeds 2^-128, conditional on the semantic correspondence.

## Remaining falsifiers / independent reviewer checklist
1. Confirm `node6` is an order-2^21 primitive subgroup generator in the EXACT concrete KoalaBear extension and that its field embedding is injective. Matching cardinality alone is insufficient.
2. Confirm `Sextic` is genuinely a field of order `2130706433^6`, not just a ring or synthetic type with a cardinality theorem.
3. Re-run the entire Lean dependency chain from a clean checkout at pinned commit, not merely trust the historical Actions success badge. Inspect all transitive axioms and reject `sorryAx`.
4. Verify manuscript `distS` and `RS[F,D,k]` conventions against the degree < k evaluator used here. Check no puncturing/extension or affine coordinate convention changes the code.
5. Confirm the alleged adjacent safe bound is a conjecture/proposal rather than a proven theorem, and check newer upstream versions/issues before claiming novelty.
6. Credit original OrbitPencil contributors. No independent external review or upstream issue is claimed.

## Reproduction
```sh
git checkout fee0051256585c590bae034a1158909900ce26c8
bash scripts/run_lean_434_gate.sh
lake env lean -o .lake/build/lib/lean/LeanPortDeployedTransfer4096.olean LeanPortDeployedTransfer4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortCAP25Event4096.olean LeanPortCAP25Event4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortCAP25Budget4096.olean LeanPortCAP25Budget4096.lean
lake env lean LeanPortCAP25Probability4096.lean
```
This is a source audit, not a new theorem or a fresh Lean run. No mathematical files or historical archives changed.
