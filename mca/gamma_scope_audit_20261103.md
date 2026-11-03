# Lane A — upstream MCA slope-scope audit (2026-11-03 16:15 UTC)

**One falsifiable hypothesis.** Does the upstream Grande Finale source explicitly identify the KoalaBear adjacent MCA row as a *full-field* numerator, making the challenge-set membership obligation automatic?

**Outcome: NOT ESTABLISHED.** The source demonstrably contains both a challenge-restricted numerator and a full-field syndrome–secant compiler. The finite adjacent table does not itself bind its row to a particular challenge set. We cannot infer that an arbitrary constructed set of slopes belongs to the challenge set of the bound being challenged. This is a certification gap, not evidence of a counterexample failure.

## Source observations (current upstream main, fetched through connected GitHub)

- `experimental/grande_finale.tex`, line ~132: imports `B^{MCA}_{C,Gamma}(a)` from CAP25 foundation.
- Lines ~134–145: defines `B^{CA}_{C,Gamma}`, `sigma_{C,Gamma}` and the exact sparsification equation for *every nonempty Gamma*.
- Lines ~211–225: defines `Theta_t(y0,y1)` with `gamma in F` and states an unqualified `B_C^{MCA}(a) = max Theta_t`. This is a full-field compiler; it does not imply the restricted version for arbitrary Gamma.
- Lines ~4664–4679: finite KoalaBear MCA adjacent row `a+=1116048`, `B*=274980728111395087`, `K=2^20+1` on the MCA route. No Gamma appears in the row.
- Lines ~5075–5077: separately refers to `actual MCA code` with `R=n-k=1048576`. This underscores that `K` in the table and `k` in the actual-code discussion must not be silently equated. No inference of a formal mismatch is made without checking the foundation and precise convention.

## Replay

```bash
python3 mca/audit_gamma_scope.py
```

This is a fail-closed **textual source checker**, not a mathematical certificate. It fetches upstream main; if the text changes, review the source and update assertions. The script has been committed but not executed in a network-enabled shell in this run.

## Formal obligation to close

Find the precise statement whose proposed MCA upper bound is `B*`, and determine its quantification over `Gamma` (full field, a specified challenge set, or universally quantified). If the bound is stated for all nonempty `Gamma`, instantiate it with `Gamma=F` and show this is a legitimate instance; otherwise show that the concrete distinct slope set `Z` is contained in the relevant `Gamma`. Then prove `Z.card > B*` for one fixed received line in deployed `RS[D,2^20]`, with a witness polynomial of degree <2^20 and auxiliary noncontainment at degree <=2^20.

The previously reported `>2^59` slope construction is still a claim, not a Lean-kernel-checked or independently accepted concrete result. This audit does not touch LIST, the false adjacent first-safe conjecture, or the retired coset loop.

## Attribution / novelty

Source: [Przemek Chojecki's rs-mca repository](https://github.com/przchojecki/rs-mca/blob/main/experimental/grande_finale.tex), with the [M2 line-decoding bridge](https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m2/m2_line_decoding_mca_bridge.md). The original OrbitPencil construction is not claimed as ours; its original accepted-source author and any public reporting of the specific 4096-fibre lift remain to be independently checked. No external issue or PR was posted.

## Verification tiers

(i) Claimed: >2^59 distinct bad slopes at agreement 1118207.
(ii) Independently source-checked: restricted and full-field conventions coexist; finite row does not explicitly specify Gamma.
(iii) Lean-kernel checked: previously reported local 93-declaration gate only, not this audit or the concrete lift.
(iv) Independent verifier accepted: NO.

**Independently verified prize-qualifying result: NO.**
