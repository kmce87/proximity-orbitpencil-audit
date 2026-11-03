# Lane A: pinned CAP25 v13.2 -> deployed 4096-fibre statement crosswalk

UTC 2026-11-03 21:46. Falsifiable hypothesis: the source-level predicates in the *kernel-checked local* deployed transfer match the support-wise MCA event in CAP25 v13.2 for the actual deployed RS[D,2^20], rather than merely the auxiliary RS[D,2^20+1].

## Sources inspected
- CAP25 v13.2, upstream file revision 4bea7abb2d9455583c8864b980e39d11d550f51d (July 19, 2026): tex/cs25_cap_v13_2.tex, definition def:mca and corollary cor:deployed.
- Local LeanPortDeployedTransfer4096.lean, LeanPortDomainTransport4096.lean, LeanPortMcaComposition4096.lean at parent c4efe7f2373ecadfdff28611c1ac8ebba92a01a2.
- Local kernel gate: GitHub Actions 41705984222 on 55c81d0b08b466d2b3b3294102390b0db9e9e267, successful; 95-declaration axiom audit previously reported. This audit does not recompile Lean.

## Logical crosswalk
CAP25 def:mca: max over fixed f1,f2 in F^n of the uniform gamma-in-F probability of existence of a single support S subset D, |S| >= (1-delta)n, where f1+gamma*f2 equals some RS[D,k] word on S, but f1 and f2 cannot both equal RS[D,k] words on S.

Local WDeployed(f,g,S,z): |S| >= 1118207; an explaining polynomial c with natDegree <= 1048575; and no pair (cf,cg) each of natDegree <= 1048576 simultaneously matches f,g on S. Since the deployed RS[D,k] consists of evaluations of polynomials of degree < k=1048576, the first clause is *exactly* deployed membership and the negative clause is *stronger* than the required noncontainment (which only excludes degrees <= 1048575). This direction is safe; the reverse equivalence is neither needed nor asserted.

Local D=range node6 is a subtype of Sextic; indexEquiv and node6_injective establish the 2^21 distinct positions. CAP25 cor:deployed uses the subgroup of order 2^21 in the KoalaBear prime field embedded in the sextic field. Matching the precise generator/domain equality, rather than only a same-sized subgroup, remains a source-to-source review item. In a finite field the subgroup of a given order is unique; the formal proof uses the CompPoly NTT generator, but this audit does not import the manuscript's D as a Lean object.

For a fixed f,g supplied by exists_many_deployed_bad_slopes and any delta satisfying ceil((1-delta)*2097152) <= 1118207, all z in Z meet the CAP25 support-wise event if the domain and code interpretations match. Distinctness follows from Z being a Finset Sextic and the prior image-injectivity proof. Consequently emca(C,delta) >= |Z|/|F| > 2^59/p^6, which is > 2^-128. In particular the candidate safe agreement 1116048 is within the range; this is NOT a refutation of the separate LIST inequality at 1116047.

## What this establishes and does not
- Source inspection: the event's quantifier order, full-field slope sampling, support-wise noncontainment, and degree conventions are compatible, with local noncontainment stronger than necessary.
- Lean kernel: the local deployed theorem is previously checked, but this manuscript crosswalk is not a new kernel theorem.
- Independent manuscript or prize verifier: none. The claimed safe edge in the manuscript is conjectural, not a proved upper bound; describe the result as counterevidence to a candidate safe edge, not a contradiction of an established theorem.
- No upstream issue/PR posted. Credit the original accepted OrbitPencil PR #38 and its contributors.

## Replay
Run `python3 mca/audit_cap25_deployed_crosswalk.py` from the repository root (network required). This checks pinned source phrases and local declarations and fails closed on changes. A manual source-to-statement review is still necessary; a textual audit is not a semantic proof.

## Next precise blocker
Add a Lean theorem stating a CAP25-shaped event with the exact deployed RS evaluation code and a finite-field probability numerator, deriving it from exists_many_deployed_bad_slopes. Have an independent reviewer verify that the CAP25 domain is the same subgroup and the normalization uses all p^6 slopes. Only then draft an author-crediting upstream report.
