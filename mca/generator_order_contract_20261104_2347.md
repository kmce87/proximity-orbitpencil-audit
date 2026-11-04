# Lane A — primitive-domain exact-order contract (2026-11-04 23:47 UTC)

## One falsifiable hypothesis
The existing source provides **both** the exponent-2^21 identity and injectivity of all 2^21 powers of `omega21`, through CompPoly's primitive-domain API, even though no explicit `orderOf` declaration was located in the two inspected files.

**Result: supported by source inspection**, not a new kernel check. At parent commit `c8328cb6f6418dcf1e41d05bdaec762259ec8cb9`, `LeanPortSameKeyFamily.lean` uses `baseNttDomain21.primitive.pow_inj` to prove projected-node injectivity. Its `eta6_pow` proof explicitly invokes `baseNttDomain21.primitive.pow_eq_one` to derive `omega21 ^ 2097152 = 1`. Thus the previous source-coverage report correctly found no named exact-order theorem, but the mathematical ingredients are already referenced by compiled-looking source. No inspection of the CompPoly implementation or fresh compilation was performed.

## Precise next Lean certificate (unexecuted template)
```lean
import LeanPortSameKeyFamily

namespace OrbitPencilLiftSameKey

theorem omega21_pow_full : omega21 ^ 2097152 = 1 := by
  have hlog : baseNttDomain21.logN = 21 := rfl
  simpa only [omega21, hlog, show (2 : ℕ) ^ 21 = 2097152 by norm_num] using
    baseNttDomain21.primitive.pow_eq_one

theorem omega21_powers_injective
    {i j : ℕ} (hi : i < 2097152) (hj : j < 2097152)
    (h : omega21 ^ i = omega21 ^ j) : i = j := by
  exact baseNttDomain21.primitive.pow_inj hi hj h

end OrbitPencilLiftSameKey
```
The exact Lean syntax of the second theorem is to be checked against the CompPoly API. The first theorem is a direct extraction of an already present proof. A subsequent theorem should show `orderOf omega21 = 2097152`, and then preserve order under `baseToSextic` by injectivity. **Do not treat this template as compiled.**

## Replay
```sh
git checkout mca-generator-order-contract-20261104-2347
grep -nE 'primitive.pow_eq_one|primitive.pow_inj|omega21|eta6_pow' LeanPortSameKeyFamily.lean
lake env lean LeanPortSameKeyFamily.lean
```

## Limits
This does not certify the manuscript's external field/domain identity, deployed RS[D,2^20] polynomial witness, or >2^59 distinct MCA bad slopes. Original attack: https://github.com/proximity-prize/proximity-prize/pull/38 ; pinned manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex . No independent originality review or upstream publication was completed. LIST at a=1116047 is not refuted. Independently verified prize-qualifying result: NO.
