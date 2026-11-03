# MCA semantic source audit — 2026-11-03 06:58 UTC

Base verified commit: c7a517c9fcb98d9e96c157d6240ea6e3d42a4eec
Hypothesis: the local domain-level WOnDomain predicate matches the finite-support MCA witness for the manuscript's **MCA route K=2^20+1**, hence gives a conditional counterexample to its adjacent safe row.

## Inspected primary sources
- Local LeanPortWaBridge4096.lean, LeanPortDomainTransport4096.lean, LeanPortMcaComposition4096.lean at the base commit.
- https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m2/m2_line_decoding_mca_bridge.md
- https://github.com/przchojecki/rs-mca/blob/main/experimental/grande_finale.tex
- https://github.com/przchojecki/rs-mca/blob/main/towards-prize.md
- Original construction: https://github.com/proximity-prize/proximity-prize/pull/38

## Source-to-source comparison
- The bridge defines a slope z as bad when there exists S subset D with |S| >= a, (f+zg)|S in C|S, and NOT both f|S and g|S in C|S. The local WOnDomain uses exactly this quantifier order and conjunction.
- Local D is the range of node6 with an injective index equivalence. The local theorem has a **fixed** f and g for all z, and Z is a Finset of sextic elements, so the counted slopes are distinct.
- Local WOnDomain requires polynomial natDegree <= 1048576. This is degree < K for K=1048577, exactly the manuscript's explicit MCA route K=2^20+1 (see the active frontier row and proof of the Q-packing proposition).
- The local stronger agreement support size >=1118207 implies the external proposed adjacent safe agreement 1116048. The local Z.card >274980728111395087.
- The ordinary list row uses K=2^20 and is not implicated.

## IMPORTANT manuscript ambiguity / falsification target
The same grande_finale.tex later calls the 'actual Reed--Solomon dimension on both active MCA rows' k=2^20=1048576, and sets R=n-k=1048576. This can be consistent if k is a base message dimension and K=k+1 is an MCA auxiliary code, but is not automatically identical to a statement about MCA of the actual deployed code RS[D,k]. The local theorem is a direct statement about RS[D,K] with K=1048577; **do not claim that it refutes an MCA bound for RS[D,k] unless the precise published target uses the augmented K code or a proved transfer lemma supplies the link.**

The local support-wise predicate is a sufficient bad-slope witness, not a kernel-checked import of the manuscript's definition. The external source is not a Lean theorem.

## Reproduction
Read the three local Lean files at the base commit; run:
```sh
git checkout c7a517c9fcb98d9e96c157d6240ea6e3d42a4eec
bash scripts/run_lean_434_gate.sh
```
Successful GitHub CI: https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41582700150 (93-declaration transitive axiom audit, only propext/Classical.choice/Quot.sound).

## Next decisive test
Locate the **definition** of epsilon_mca and the exact code C in the published conjecture, then show either:
1. C=RS[D,2^20+1] in the target claim; or
2. a formally proved reduction from the local K=2^20+1 bad slopes to the deployed RS[D,2^20] MCA game.
If neither is established, label the result a local K+1 support-wise counterexample only. Independent prize verifier acceptance: NO.
