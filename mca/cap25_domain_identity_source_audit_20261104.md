# CAP25 KoalaBear domain identity — source-level audit (2026-11-04 UTC)

## One falsifiable hypothesis

The domain `D := Set.range node6` used by the kernel-checked local
probability theorem is **exactly** the KoalaBear subgroup of order
`2^21` in the base field, embedded into `KoalaBear.Ext6`, as specified
in CAP25 v13.2; it is not an arbitrary same-cardinality set.

**Source-level verdict: SUPPORTED**, conditional only on the already
kernel-checked CompPoly primitive-root theorem. This audit is not itself
a newly compiled Lean theorem, nor external independent acceptance.

## Pinned sources and explicit comparison

- Manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
  - Preliminaries: `D = alpha H` with `H` cyclic of order `n`.
  - Deployed corollary `cor:deployed`: `B=F_p`,
    `F=F_(p^6)`, `D` the subgroup of order `2^21`
    in `B^×`, and `k=2^20`.
  - `def:mca`: fixed pair, full-field uniform slope, existential
    support and same-support noncontainment.
  - `cor:capg-adjacent-pairs`: the 1116048 safe edge is a
    **conjecture**, not a proved upper bound.
- `LeanPortSameKeyFamily.lean`: `baseNttDomain21` is
  `CompPoly.CPolynomial.NTT.KoalaBear.domainOfLogN 21`;
  `omega21 := baseNttDomain21.omega`.
- `LeanPortSupport4096.lean`: `node21 j := omega21 ^ j.val`;
  `node6 j := baseToSextic (node21 j)`, and `node21_injective`.
- `LeanPortDomainTransport4096.lean`:
  `D := Set.range node6`; `node6_injective` and `indexEquiv`
  identify all 2^21 indices with distinct evaluation points.
- `LeanPortCAP25Event4096.lean`: `Explains` requires
  `natDegree < 1048576`, not `<= 1048576`.
- `LeanPortCAP25Probability4096.lean`:
  `badSlopes` filters `Finset.univ : Finset Sextic`, so
  the slope denominator is the **whole sextic field**.

## Mathematical domain-identity argument

Let `omega` be the primitive `2^21`-th root from the pinned
CompPoly NTT domain. The set
`{omega^j | 0 <= j < 2^21}` is the unique subgroup of order
`2^21` in the cyclic group `F_p^×`: it is closed under
multiplication and inversion, and primitivity gives exactly
`2^21` distinct elements. Applying the injective field
homomorphism `baseToSextic` gives precisely `Set.range node6`.
The manuscript's deployed subgroup has the same unique definition.
No enumeration or guessed generator is needed.

This last equality to a manuscript-described set is a **mathematical
source crosswalk**, not an additional Lean theorem: the manuscript
does not supply an importable Lean constant for its `D`.

## Falsification / replay

From this pinned repository revision, inspect:
```sh
grep -nE 'baseNttDomain21|omega21|domainOfLogN' LeanPortSameKeyFamily.lean
grep -nE 'def node21|def node6|node21_injective' LeanPortSupport4096.lean
grep -nE 'def D|node6_injective|indexEquiv' LeanPortDomainTransport4096.lean
grep -nE 'def Explains|def CAP25Bad' LeanPortCAP25Event4096.lean
grep -nE 'def badSlopes|exists_fixed_pair_probability_cross_product' LeanPortCAP25Probability4096.lean
```
Then run `bash scripts/run_lean_434_gate.sh` and compile the
CAP25 event, budget and probability files in dependency order.
If CompPoly's pinned primitive-root certificate or any of these
definitions differ, **reject this identity argument**.

## Scope and outstanding work

- The local probability theorem is kernel-checked in Actions
  https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41756461599
  (head `fee0051256585c590bae034a1158909900ce26c8`).
- This source audit does not establish novelty, an independent
  manuscript referee review, or prize acceptance.
- Before any upstream report: independently check exact closed-ball
  radius conversion, the MCA event's quantifier ordering, and
  authorship/provenance against OrbitPencil PR #38:
  https://github.com/proximity-prize/proximity-prize/pull/38
- The separate ordinary LIST inequality at agreement 1116047 is
  unaffected. Do not resume the false adjacent-safe conjecture.
