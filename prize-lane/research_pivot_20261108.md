# Lane B: independent research pivot — 2026-11-08 UTC

**Status:** Research review and exact score gates only; NO improved Lean proof; NO independently accepted result. This replaces default OrbitPencil/CorePencil parameter tweaking as the next-research programme. Lane A untouched.

## Official frozen instance and source facts

Official main: `proximity-prize/proximity-prize@eb82d3bf04a9c876c7ef9c3e6de4640fb85062f2`. Koala `n=2^18`: public leaderboard attack 116.13, soundness 68.15; source `ProtocolClaimUpper 11613 122369` and `ProtocolClaim 6815 331366399 1073741824`. Binary `n=2^21`, rate 1/2, challenge field GF(2^192): source `ProtocolClaimUpper 10624 917441` and `ProtocolClaim 6400 78622925 268435456`. **Binary independently accepted submissions NOT confirmed**; source config v3 is not the service registration.

Pins: Lean 4.34.0; Mathlib `5ed2965256430c3649e86755f9576b54eca72435`; ArkLib `34a834c61c859cc04205f5f43fd237cda8fb0da4`; CompPoly `411708c17175ab5ecaf035036608c206c4ee0878`. The upper contract proves strict `winningSetDensity > 2^-128` for *every* radius in the unsafe suffix plus the score; lower contract proves `certifiedGammaError <= 2^-128` at the claimed safe radius plus the score. No source theorem is automatically independently accepted.

## Actual research alternatives and exit gates

**Priority 1: Koala lower — second-order hidden-derivative / full support MCA.** Dao–Kominers–Thaler (2026) proves quantitative list/MCA results with formal ArkLib components. However paper itself reports a 66.15-bit Proximity Prize specialisation and a later 68.11 submission, below current 68.15: simply importing first-order results is not new. At rate 1/2, its first-order agreement threshold is `a1=(3rho+2sqrt(rho(5-rho)(2-rho)))/(8-rho)=0.6898979485566...`. An explicit genuinely beyond-first-order target is Koala **69.00 bits**, requiring a score-certified radius `334773390/1073741824` and agreement `0.6882179845...`, *below* a1. First gate: check formal second-derivative condition `Gamma(rho,a,d=2)>1`, characteristic cap at p=2^31-2^24+1, and explicit bad-set count below `|F|/2^128`; abort if finite constants cannot meet the security budget. DKT's Nov 2 proof revision in quangvdao/ArkLib is not automatically compatible with official pinned September ArkLib/Lean4.34.

**Park pending a new extension-field lifting lemma: Koala upper — root-of-unity additive combinatorics.** Krachun–Kazanin–Haböck (ePrint 2026/782) constructs prime-field affine-line counterexamples via sums of roots of unity, genuinely distinct from OrbitPencil. But a single affine line with parameters in the KoalaBear *base field* has at most q=2,130,706,433 distinct values, versus **274,980,728,111,395,088** required bad challenges over the *sextic challenge field*. This is an immediate direct-port obstruction, over eight orders of magnitude, even before checking >=139782 agreements or the full unsafe suffix. Proceed only if a demonstrably new extension-field lift supplies the missing challenge cardinality; the paper's `2^{Omega(1/eta)}` asymptotic does not.

**Priority 3: Binary upper — Gold-moment / quadratic-rank methods on *sparse* GF(2) additive domain.** Dao–Kominers–Thaler–Zheng (ECCC TR26-237; Nov3 revision) proves binary counterexamples. Decision-tree height 3 yields `9/16` agreement; published binary source already has `9n/16+63=1179711`; height 4 yields lower agreement and worse upper score. Their Gold theorem assumes a **dense** additive domain, whereas protected n=2^21 is a `2^-43` fraction of BF64. Only a new rank count for the exact 21-dimensional basis could help. Hard gate: >=1179774 agreements and >=2^64+1 bad challenges, source-compatible correction polynomial, whole unsafe suffix.

**Priority 4: Binary lower — exact domain-specific beyond-Johnson bound.** Source 64.00 radius `78622925/268435456` is within 1e-9 of the rate-1/2 Johnson radius `1-sqrt(1/2)`. To beat it, 64.01 bits needs `78633204/268435456` and certified extractor error <=2^-128. The binary counterexample paper makes a uniform beyond-Johnson theorem implausible, but does not refute this exact finite claim. Existing source contains 81 specialised lower Lean modules; do not repeat baseline list-size sweeps.

**Park:** OrbitPencil 272/273 fibres, core root changes, product-key pigeonhole, third-field roots; binary 9/16 relabelling; random puncturing / designed subspace evaluation sets (change protected domain); naive prime-field list bounds (do not automatically apply to extension-field received words).

## Anti-loop protocol

- One falsifiable lemma and exact centibit/index/radius target per run; read existing `prize-` branches before repeating. Existing `prize-binary-lower-johnson-6401-20261103` already tests the binary numerical boundary. No new sequential experiment ledgers. Commit SHA is experiment ID.
- Prove applicability -> exact finite count -> explicit new inequality/construction -> pinned Lean 4.34 kernel -> axiom audit -> independent verifier proof acceptance for exact slug/version/commit. Never conflate stages.
- Do not modify or import work from the independent MCA Lane A unless a genuinely certified transferable lemma directly helps.
- No accepted improvement exists as of this review. Deadline 2027-12-31; any monetary award is discretionary.

## Primary sources

- https://github.com/proximity-prize/proximity-prize
- https://better.codes/
- https://eprint.iacr.org/2026/2056 (Dao–Kominers–Thaler; formally verified derivative analysis)
- https://eccc.weizmann.ac.il/report/2026/237/ (Dao–Kominers–Thaler–Zheng; binary counterexamples)
- https://eprint.iacr.org/2026/782 (Krachun–Kazanin–Haböck; roots-of-unity construction)
- https://eccc.weizmann.ac.il/report/2026/169/ (Jeronimo; prime-field list/MCA)
- https://eccc.weizmann.ac.il/report/2026/262/ (Alrabiah–Goyal–Guruswami; designed evaluation domains)
