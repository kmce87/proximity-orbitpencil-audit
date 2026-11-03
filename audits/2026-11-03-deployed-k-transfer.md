# MCA deployed-code transfer: dimension monotonicity audit (2026-11-03 07:05 UTC)

## One falsifiable hypothesis
The locally kernel-checked witness for the augmented RS[D,K] code, K=2^20+1, also witnesses support-wise MCA badness for the deployed RS[D,k] code, k=2^20, without changing the received line, slope set, or support.

## Source evidence
- rs-mca/experimental/grande_finale.tex lines 4672-4679: adjacent KoalaBear MCA row uses K=2^20+1, while list uses K=2^20.
- Same manuscript lines 5707-5710: *actual Reed--Solomon dimension* on active MCA rows is k=2^20.
- rs-mca/experimental/notes/m2/m2_line_decoding_mca_bridge.md lines 12-36 defines LD_sw(C,a) by existence of one support S of size >=a explaining f+zg, but no simultaneous explanations of f and g on that same S.
- Local PR #39 diff: SupportWiseBad has an explaining polynomial c with natDegree <=1048575, and excludes direction polynomial q with natDegree <=1048576. WOnDomain uses <=1048576 for both explaining and excluded polynomials. CI run 41582700150 passed 93-declaration transitive axiom audit.

## Elementary transfer lemma (mathematical, NOT newly Lean checked)
Let C_small=RS[D,k] and C_large=RS[D,k+1]. Then C_small subset C_large.
For fixed f,g,z,S:
1. If (f+zg)|S is explained by c in C_small, it is explained for C_small.
2. If there are NO cf,cg in C_large simultaneously explaining f,g on S, then there are NO cf,cg in C_small, since C_small subset C_large.
Therefore a witness with small-code explanation and large-code noncontainment is MCA-bad for the deployed small code.
The PR #39 SupportWiseBad predicate has exactly these asymmetric degree cutoffs (c <=k-1, q <=k), and the final WOnDomain proof uses a c inherited from that stronger SupportWiseBad witness. This suggests the k/K discrepancy is resolvable by an explicit lemma, not an assumption of equality between codes.

## Remaining exact proof obligations
- Write a Lean theorem using the ACTUAL domain-level witness showing the existential c can be chosen with natDegree <=1048575, not just the weaker WOnDomain cutoff <=1048576. This may require exposing the stronger witness through the domain transport instead of relying on WOnDomain alone.
- Confirm the full field and evaluation-domain equivalence with the manuscript's exact RS[D,k] definition.
- Connect the >2^59 distinct slopes to the external full-field B^MCA_C(a) numerator at a=1116048 via monotonicity.
- Independently review the witness and its original OrbitPencil attribution before posting a public refutation.

## Verification status
Mathematical inclusion argument: independently reasoned from the inspected source.
New Lean transfer theorem: NOT WRITTEN / NOT CHECKED.
Official prize-verifier acceptance: NO.
Original attack credited to proximity-prize/proximity-prize PR #38; no new benchmark score asserted.
