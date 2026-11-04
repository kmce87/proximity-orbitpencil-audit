# Lane A: subgroup admissibility against CAP25 v13.2 (2026-11-04 21:16 UTC)

## One falsifiable hypothesis
The published MCA model excludes the local evaluation subgroup because it requires a nontrivial coset alpha H with alpha != 1.

## Result: falsified by pinned manuscript source
Source: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex , section Preliminaries (paragraph Codes and distances). It explicitly states D=alpha H subset B^times, "The subgroup case is alpha=1", and allows B=F. Thus an embedded order-2^21 KoalaBear subgroup is an *admissible choice* of D, provided exact field embedding and order are proved. No need to match an independently fixed nontrivial alpha for this general statement.

This does NOT establish equality with any uniquely specified ABF26 deployed evaluation domain. It also does not show that the local fixed-line construction has >2^59 distinct bad slopes for the published RS[F,D,2^20].

The same pinned source, Definition def:mca, requires a common support S for agreement and simultaneous nonexplanation. It defines RS[F,D,k] with degree strictly less than k. Do not substitute auxiliary RS[F,D,k+1] witnesses.

## Replay
Fetch the pinned manuscript; search literal "The subgroup case is" and "def:mca". Fetch https://github.com/kmce87/proximity-orbitpencil-audit/blob/6cfc54d0dec9b6f6f1ed399111c7ea5df7bda23c/LeanPortSameKeyFamily.lean and inspect baseNttDomain21, omega21 and primitive.pow_inj. Next inspect CompPoly's primitive-domain source and kernel-check exact order 2^21, plus the sextic embedding.

## Evidence limits
Manuscript and local file independently source-inspected; no new Lean build or independent verifier acceptance. Literature novelty unresolved. Original OrbitPencil PR: https://github.com/proximity-prize/proximity-prize/pull/38 . Prize-qualifying result: NO.
