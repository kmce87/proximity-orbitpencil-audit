# Lane A — exact generator order: falsification gate (2026-11-04 22:15 UTC)

## Single hypothesis
The existing local source `LeanPortSameKeyFamily.lean` and `LeanPortGeneratorPowerIdentity4096.lean` already contain a standalone theorem asserting `orderOf omega21 = 2097152`.

**Result: NOT ESTABLISHED by the inspected source.** The former invokes `baseNttDomain21.primitive.pow_inj` to prove projected-node injectivity, while the latter proves `node6 j = baseToSextic (omega21 ^ j.val)` and identifies `D` as a set of embedded powers. Neither inspected file declares an exact-order theorem. This is a *source-coverage finding*, not a counterexample to exact order. The primitive-domain API may imply it, but its implementation was not inspected in this run.

## Required mathematical bridge
For an element `omega` of a field, establish:
1. `omega ^ 2097152 = 1`;
2. `forall i j, i < 2097152 -> j < 2097152 -> omega ^ i = omega ^ j -> i = j`.
Then the powers 0..2097151 are distinct, so the multiplicative order is exactly 2097152. Under an injective field homomorphism `phi`, `phi omega` has the same order: equality of mapped powers reflects equality of base powers, and the n-th power maps to one. The image of those powers is therefore a subgroup of size n. This still requires checking whether the external MCA statement accepts this subgroup and the precise RS evaluation convention.

## Replay / source checks
```sh
git checkout mca-generator-order-obligation-20261104-2215
grep -nE 'baseNttDomain21|omega21|primitive.pow_inj|orderOf|node6_eq_embedded_omega_pow|D_eq_embedded_omega_powers' LeanPortSameKeyFamily.lean LeanPortGeneratorPowerIdentity4096.lean
lake env lean LeanPortGeneratorPowerIdentity4096.lean
```
The Lean command is a proposed replay, **not executed this run**. The next proof must import the CompPoly primitive-domain implementation and formally derive `orderOf omega21 = 2097152`, then `orderOf (baseToSextic omega21) = 2097152`. Do not treat the existing generator-power identity as that proof.

## External checks and limits
Original attack: https://github.com/proximity-prize/proximity-prize/pull/38
MCA manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
No fresh originality search or upstream report was completed. The deployed degree <= k-1 explaining witness and degree <= k noncontainment must remain separate. LIST at a=1116047 is not refuted. No independently verified prize-qualifying result exists.
