# Lane A checkpoint — 2026-11-03 13:43 UTC

## Single falsifiable hypothesis

The previous `mca/BridgeQuantifiers.lean` can define `LocalNumerator` using `Finset.univ.filter (fun z => LocalBadSlope ...)` without explicitly providing a decision procedure for `LocalBadSlope`.

**Source-level result: rejected as an unjustified elaboration assumption.** The predicate contains existential witnesses over arbitrary sets and functions, and no constructive `DecidablePred` is supplied. The original definition did not enter `classical` or declare itself noncomputable. The updated file uses `noncomputable def ... := by classical; exact ...`, and `classical` in the theorem proof. This is a **candidate elaboration repair**, not a successfully compiled file.

## Reproduce

```sh
git checkout mca-numerator-decidability-20261103
lake env lean mca/BridgeQuantifiers.lean
```

No Lean/lake binary was available in this run; the compile outcome is unknown. If Lean rejects the file, record the exact compiler output and fix it rather than asserting kernel success. A CI workflow should run Lean 4.34 and print `#print axioms McaBridgeQuantifiers.numerator_gt_two_pow_59`.

## Upstream semantic comparison

[rs-mca M2 bridge](https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m2/m2_line_decoding_mca_bridge.md) defines
`LD_sw(C,a) = max_{f,g in F^D} #{z : exists S subset D, |S| >= a, f+zg|S in C|S, and not both f|S,g|S in C|S}`.
Our `LocalNumerator C D a f g` counts slopes for a **single fixed** `f,g`, and is only a lower-bound candidate for that maximum when `C` is identified with the appropriate deployed RS code on D. This file neither formalizes the maximum nor establishes equality with `eps_mca`.

The upstream bridge also states `eps_mca(C,delta) = LD_sw(C,ceil((1-delta)n))/|F|`. Its exact-support reduction requires `a >= k+1`. The deployed target `k=2^20, a=1118207` satisfies that inequality, but a concrete support family, injective slope set, and the code/domain equivalence are not supplied by the present abstract theorem.

[Grande Finale v4 manuscript](https://github.com/przchojecki/rs-mca/blob/main/experimental/grande_finale.tex) by Przemek Chojecki, dated July 2026, is background; it does not independently certify our proposed lift.

## Cumulative inspected history

This run fetched `mca/BridgeQuantifiers.lean` at `22d44b6ce6200e538542d2f9ab4e88ccef94017d`, `mca/SelfContainedFiniteCertificate.lean` at `8728d329020ca4736e965883706832119ad75d82`, and `mca/DomainPolynomialTransfer.lean` at `ee32bd8363841392020b93bc985fe5428efbcbb0`. The latter imports only Mathlib while referring to `McaDeployedTransfer` declarations defined in another file; it is not a self-contained compile target. The previous 93-declaration local gate at `c7a517c` was reported earlier, not re-executed. No historical archives were modified.

## Verification status

(i) Claimed: fixed-line KoalaBear lift with >2^59 distinct bad slopes, a=1118207, 4096-point fibres.
(ii) Independently source-checked: upstream M2 definition and local missing explicit decidability.
(iii) Lean-kernel checked this run: NO. Previously reported local 93-declaration gate is distinct.
(iv) Independently accepted: NO. Prize-qualifying result: NO.

## Next precise blocker

Run Lean 4.34 on the repaired numerator theorem and capture compiler/axiom output. Then define the **deployed** RS[D,2^20] over the exact KoalaBear F_(p^6) domain and instantiate fixed-line supports, degree <k witnesses, auxiliary noncontainment, and an injective slope set with >2^59 elements. The ordinary LIST bound at a=1116047 is untouched. No external rs-mca issue or PR was posted.
