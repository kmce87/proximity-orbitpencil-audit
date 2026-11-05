# MCA definition equivalence audit — 2026-11-05 07:52 UTC

## Falsifiable hypothesis
The compiled local `DeployedBad` predicate is stronger than the support-wise MCA-bad event in the pinned CAP25 v13.2 manuscript, for the deployed RS[F,D,2^20] code, conditional on the concrete field/domain identifications.

## Inspected immutable sources
- Local source: https://raw.githubusercontent.com/kmce87/proximity-orbitpencil-audit/d6bbfd358d3ca06b170ccfbf946fa0b5907644dd/LeanPortDeployedDomainBridge4096.lean
- Manuscript: https://raw.githubusercontent.com/przchojecki/rs-mca/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
- Parent commit: https://github.com/kmce87/proximity-orbitpencil-audit/commit/d6bbfd358d3ca06b170ccfbf946fa0b5907644dd

## Definition comparison
CAP25 definition `def:mca` takes a MAX over one fixed pair f1,f2 in F^n, then probability over uniformly chosen gamma in F. The event is existence of a support S subset D with |S| >= (1-delta)n, the combination f1+gamma f2 agreeing on S with a codeword of C, and no pair of codewords simultaneously explaining f1,f2 on that SAME S.

Local `DeployedBad f g z` existentially provides S and polynomial c of natDegree <=1048575 with agreement >=1118207. It forbids simultaneous explanations by cf,cg even with natDegree <=1048576, a STRICTER noncontainment requirement than deployed degree <=1048575. The local theorem `exists_many_deployed_bad_slopes` existentially chooses alpha,U0,Z BEFORE universally quantifying z in Z. The same f,g are thus fixed across Z, and Z is a Finset (deduplicated slopes). The local theorem states |Z| > 2^59.

Conditional implication: IF `Sextic` is the intended field F_(p^6), `D` is exactly the manuscript's subgroup of F_p^× of size 2^21, and the evaluation map x.val is injective and identifies that subgroup, THEN every z in Z is MCA-bad at delta = 1 - 1118207/2097152 (and at all larger delta < 1/2 by support monotonicity). This would contradict a purported 2^-128 safe bound at agreement 1116048, because 1118207 >=1116048. This conditional statement does NOT address the ordinary LIST inequality at agreement 1116047.

## Important proof gaps
1. This audit is a source comparison, NOT a Lean proof of the equivalence to the manuscript's externally quantified MCA probability; no new Lean compile was performed.
2. Need kernel-level proof that `Sextic` has exactly p^6 elements with p=2130706433, and that `D` equals the deployed subgroup as an evaluated code, not just an abstract set of equal cardinality.
3. Need transitive `#print axioms` logs for both bridge theorems, including any nonstandard axioms or sorry-derived declarations in imports.
4. Need inspect the original accepted OrbitPencil PR and whether an equivalent n=2^21 result is already reported upstream. Do not claim novelty or external acceptance.
5. The manuscript's own KoalaBear-sextic corollary proves a weaker unsafe band, and describes some witnesses as nonconstructive; this audit does not establish a new published theorem or contradict that corollary.

## Replay
```sh
git fetch origin
git checkout d6bbfd358d3ca06b170ccfbf946fa0b5907644dd
sed -n '1,130p' LeanPortDeployedDomainBridge4096.lean
# Retrieve the pinned manuscript and inspect its definition labelled def:mca,
# and its corollary labelled cor:deployed.
lake env lean LeanPortDeployedDomainBridge4096.lean
```
No claim is made that the final command was executed this run.

Evidence: (i) full external counterexample claimed; (ii) local source/manuscript definition comparison independently checked; (iii) prior local CI reported successful, no fresh kernel run; (iv) independent verifier accepted NO.
Independently verified prize-qualifying result: NO.
