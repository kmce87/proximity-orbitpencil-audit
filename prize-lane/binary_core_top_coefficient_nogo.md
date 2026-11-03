# Lane B: a structural no-go for one binary CorePencil score shortcut

**Status:** original mathematical argument + exact arithmetic and finite-sample tests; **NOT Lean kernel checked, independently reviewed, or an accepted prize improvement**. The original CorePencil/LabelFamily construction belongs to the contributors of [proximity-prize/proximity-prize](https://github.com/proximity-prize/proximity-prize). No originality claim for their construction is made here.

## Falsifiable hypothesis

The binary upper proof [CorePencil.lean](https://github.com/proximity-prize/proximity-prize/blob/main/ProximityPrize/SubmissionBinaryUpper/CorePencil.lean) has `C_p(X)=V_p(X)-Rtop(X)` of degree at most 16384. One idea for reducing it to degree <=16383 is to restrict to a sufficiently large subfamily sharing the coefficient of `X^16384`, so that one **fixed** leading correction could be incorporated into `Rtop`.

**Result:** Within the published `LabelFamily.Param` and fixed `Rtop`-plus-one-common-coefficient design, a single-coefficient fibre has **strictly fewer than `2^64+1` parameters**. This is insufficient for the published binary challenge's `2^-128` winning-set target over `GF(2^192)`. It excludes this particular shortcut, not every better attack.

## Exact arithmetic

From the [official Lean cardinality lemma](https://github.com/proximity-prize/proximity-prize/blob/main/ProximityPrize/SubmissionBinaryUpper/CorePencil.lean):

```
|Param| = 420 * 32 * 2047 * (1023 * 1022 * 1021) * 512 * 4
        = 60144973141589360640.
|Param|/8 = 7518121642698670080
        < 18446744073709551617 = 2^64+1.
```

The binary challenge field has cardinality `2^192`, so more than `2^64` distinct slopes suffice to exceed `2^-128` winning-set density. Even in the best case of one distinct slope per parameter, one coefficient class cannot meet that target.

## The abstract polynomial lemma

Let `F` have characteristic 2, let `K` be a finite-dimensional `F_2`-linear subspace of `F` of dimension `d>=2`, and let `H_1,H_2` be **distinct hyperplanes of K**. Let

```
P_H(X) = product_{h in H} (X-h).
```

Write `T=H_1 intersection H_2`. Then `dim(T)=d-2`. Choose `a_i in H_i\T`. Each `H_i=T union (a_i+T)` (disjoint), and the finite-subspace polynomial `P_T` is additive. Hence

```
P_Hi(X) = P_T(X) * (P_T(X) + P_T(a_i))
        = P_T(X)^2 + P_T(a_i)*P_T(X).
```

As `a_1+a_2 notin T`, the values `P_T(a_1)` and `P_T(a_2)` are unequal. Therefore

```
P_H1(X)-P_H2(X) =
    (P_T(a_1)-P_T(a_2))*P_T(X)
```

has **exact degree `2^(d-2)`**, since `P_T` is monic of that degree. In particular, the coefficient at `X^(2^(d-2))` differs between the two monic degree-`2^(d-1)` subspace polynomials. This is a general identity, independently of the field presentation.

For `d=13`, the distinct 12-dimensional hyperplanes thus have different coefficients at `X^2048`.

## Applying the lemma to the published parameter `jn 0`

For a fixed published `Param` except `jn 0 : Fin 8`, the direction subspace of flat `F_0` is the kernel of three binary linear functionals on `V=F_2^11 x F_2^4`:

```
s0·z=0,
r·y + beta(s0,jr)·z=0,
m0·y + beta(s0,jn0)·z=0.
```

The first two equations have common kernel `K` of dimension 13 because `s0 != 0` and `r != 0`. The third equation cuts `K` down to a 12-dimensional hyperplane: by construction `m0 != 0` and its coordinate at the pivot of `r` is zero, hence it is linearly independent of `r`.

The canonical `beta(s0,j)` for the eight values of `j` enumerates distinct linear functionals modulo the span of `s0`; its coefficient at the least set bit of `s0` is always zero. Therefore distinct `jn0` produce distinct hyperplanes of the **same K**. (If their restrictions to K agreed, the difference of two `beta` forms would vanish on all `z` with `s0·z=0`, so it would lie in the span of `s0`, impossible.)

By the abstract lemma, the eight direction-locator polynomials of `F_0` have eight distinct coefficients at degree 2048. Affine translation of a flat changes only the **constant term** of its locator, not its positive-degree coefficients.

The published locators have degrees `4096` and subleading degrees at most `2048`. In `V_p=Gq * F_0 * F_1 * F_2`, the coefficient of `X^16384` depends on `jn0` **only through the `X^2048` coefficient of `F_0`**. The other terms (`Gq`, `F_1`, `F_2`, `Rtop`) stay fixed. Hence the coefficient of `X^16384` in `C_p=V_p-Rtop` takes **eight distinct values** as `jn0` varies.

Partition `Param` into blocks of eight with all other coordinates fixed. Each block contributes at most one parameter to a fixed-`C_p[X^16384]` family. Therefore every such family has size at most `|Param|/8`, strictly below `2^64+1` as calculated above.

## What this does and does not establish

- The algebraic argument is general, not an extrapolation from eight observed BF64 coefficients. The numerical script checks arithmetic and samples; it does not exhaust billions of parameter blocks.
- The bound is for this **particular** published parameter family and a **single shared leading-correction coefficient**, not a global lower bound on Proximity Prize scores.
- Lower correction degree would create **degree slack**, not automatically new agreement points. An independent construction of 64 additional agreement points would also be required for a genuine 106.23-bit upper attack.
- `ProtocolClaimUpper 10623 ...` has **not** been proved, compiled, or accepted.
- The source is a mathematical argument awaiting independent review/formalisation; it is not labelled Lean-verified.

## Replay

```bash
git checkout prize-binary-coeff-injection-20261103
python3 prize-lane/binary_core_top_coefficient_nogo.py
```

For the underlying official definitions, inspect `LabelFamily.lean`, `LabelSpace.lean`, `FlatPoly.lean`, `LabelTable.lean`, and `CorePencil.lean` in the public prize repository. Do not use the separate n=2^21 KoalaBear Lane A construction as an official binary result.

## Next falsifiable idea

Seek a new binary label family with **at least `2^64+1` distinct members**, agreement strictly above `1179711`, and a **fixed common top polynomial** that makes the explaining polynomial degree <=`2^20-1`. Quantify candidate count and algebraic degree first, before writing Lean; a score-only calculation is not a result.
