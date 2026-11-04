# Lane A: generator order versus external coset — 2026-11-04 20:17 UTC

## Falsifiable hypothesis
The local proof of the KoalaBear 2^21 domain's generator order is *missing entirely*, so its image may repeat before 2^21.

## Source inspection and result
**Hypothesis falsified at the source/conditional mathematical level.** At pinned parent 86da3582a55b1be76ed561bf736031f607be43b9, LeanPortSameKeyFamily.lean defines baseNttDomain21 via CompPoly.CPolynomial.NTT.KoalaBear.domainOfLogN 21 and omega21 as baseNttDomain21.omega. Its projectedNode_injective invokes baseNttDomain21.primitive.pow_inj for exponents below 2097152. LeanPortDomainTransport4096.lean proves node6_injective by node21_injective and RingHom.injective baseToSextic. LeanPortGeneratorPowerIdentity4096.lean proves node6 j = baseToSextic (omega21 ^ j.val) by rfl and D equality with these indexed powers.

Thus the **absence of a standalone exact-order lemma is not itself evidence of repeated nodes**: injectivity over all 2097152 exponents plus the NTT primitive-order contract supports exact order when the generator's 2097152-th power is one. The latter contract must be explicitly extracted from the CompPoly primitive-domain source before asserting a self-contained exact-order theorem. A distinct and larger gap remains: the manuscript permits a multiplicative coset alpha H in a subfield B, not necessarily the local subgroup D. Equality with a particular externally specified coset requires an explicit alpha and H, or a valid symmetry/isomorphism argument.

## Replay and falsification
1. Fetch pinned LeanPortSameKeyFamily.lean; locate baseNttDomain21, omega21, projectedNode_injective and primitive.pow_inj.
2. Fetch pinned LeanPortDomainTransport4096.lean and LeanPortGeneratorPowerIdentity4096.lean; locate node6_injective, node6_eq_embedded_omega_pow, D_eq_embedded_omega_powers.
3. Inspect the imported CompPoly.CPolynomial.NTT.KoalaBear.domainOfLogN and its primitive order theorem. Formally prove omega21 ^ 2097152 = 1 and omega21 ^ 1048576 != 1 (equivalently exact order 2097152 for a power-of-two order). Do not substitute a generic primitive root or unproved NTT assumption.
4. Independently compare the actual manuscript's D = alpha H and B with local D; distinguish existence of a permissible coset from equality to a uniquely prescribed coset.
5. Run Lean 4.34 and print axioms on any new theorem before certification.

## Evidence and limits
(i) Claimed: fixed received line, >2^59 slopes at 1118207.
(ii) Source-checked this run: concrete NTT primitive API is used, embedded-power identity and domain injectivity are present; exact order not freshly compiled.
(iii) Lean-kernel checked this run: none.
(iv) Independent verifier accepted: NO.
No external claim or upstream report. Original source: https://github.com/proximity-prize/proximity-prize/pull/38 ; pinned manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex . Novelty not determined. Ordinary LIST inequality at 1116047 unaffected.
