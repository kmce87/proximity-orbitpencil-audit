# DRAFT ONLY — request for independent review of a KoalaBear MCA counterexample

> **Not posted to `przchojecki/rs-mca`.** This note is a proposed issue for independent review, not a claimed external certification, publication, or Proximity Prize award.

## Proposed issue title

Potential counterexample to KoalaBear MCA first-safe agreement 1,116,048 via a 4,096-fibre OrbitPencil lift (Lean 4.34 checked locally)

## Suggested issue body

We would appreciate independent mathematical review of a possible counterexample to the *proposed* KoalaBear MCA bound

```text
B^MCA_C(1116048) <= floor((2130706433^6)/2^128)
                  = 274980728111395087.
```

This bound is stated as open in `agents.md` of this repository. We are **not** challenging the distinct ordinary LIST inequality at agreement 1,116,047.

### Provenance and attribution

The rational-pencil method is adapted from the previously accepted Proximity Prize **OrbitPencil.lean** construction at `n=2^18`, official PR https://github.com/proximity-prize/proximity-prize/pull/38 (submitted via Yukon; contributors include `erdkocak`). The possible new contribution here is a **larger-domain adaptation and an MCA application**, not invention of the original pencil. We have not established originality against all existing work.

### Source and reproducibility

Local audit repository: https://github.com/kmce87/proximity-orbitpencil-audit

Git commit **4224d4dca68eb4c111d272ecb3b35eee064a9ab5**, on branch `research/mca-deployed-degree-gate-20261103-0733`.

GitHub Actions result: https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41597057145

The repository's fail-closed Lean 4.34 candidate gate and transitive axiom audit reported **95/95 declarations passing**, with no extra axioms beyond `propext`, `Classical.choice`, `Quot.sound`. This is a *local kernel check*, not an independently accepted result in your repo or the official prize benchmark. Key final declarations:

- `OrbitPencilLiftDeployedTransfer4096.supportWiseBad_to_deployed`
- `OrbitPencilLiftDeployedTransfer4096.exists_many_deployed_bad_slopes`

Exact replay:

```bash
git clone https://github.com/kmce87/proximity-orbitpencil-audit.git
cd proximity-orbitpencil-audit
git checkout 4224d4dca68eb4c111d272ecb3b35eee064a9ab5
bash scripts/run_lean_434_gate.sh
```

### Proposed mathematical construction

Let `p=2130706433`, `F=GF(p^6)`, `n=2^21`, `k=2^20`, and let `D` be the `n` distinct points of the KoalaBear order-`n` NTT subgroup embedded from `GF(p)` into `F`. Write `x=ω^(512r+b)` with `0<=r<4096` and `0<=b<512`; then `x^4096=η^b` with `η=ω^4096`.

Choose `272`-element subsets `U` of `{1,...,511}` and set `V_U(T)=∏_(b in U)(T-η^b)`. Group them by (i) coefficients of degrees `271,...,258` in the base prime field and (ii) `Σ b mod 512`. The cardinal inequality

```text
binom(511,272) > (p^14*512)*2^59
```

gives a common-key family of at least `2^59+1` members. Same-key differences `V_U0-V_U` have degree at most `257` and vanish at `T=0`. An extension-field parameter `α` can be chosen outside the at most `513+(2^59+1)*2^59*257` forbidden points; the slopes

```text
γ_U = (V_U0(α)-V_U(α))/α
```

are distinct. Define `Q_U` by

```text
V_U0(T)-V_U(T)-γ_U*T = T*(T-α)*Q_U(T), deg Q_U<=255.
```

Let `R(X)=∏_(r=1..4095)(X-ω^(512r))` (degree `4095`) and `t=x^4096`. Define one fixed received pair

```text
f(x)=R(x)*V_U0(t)/(t*(t-α)),
g(x)=-R(x)/(t-α).
```

For each `U`, the line point `f+γ_U*g` agrees with the valid `RS[D,k]` polynomial `c_U(X)=R(X)*Q_U(X^4096)` of degree at most `4095+255*4096=1048575=k-1` on

```text
S_U = {(r,0):1<=r<=4095} union {(r,b):0<=r<=4095,b in U},
|S_U|=4095+272*4096=1118207.
```

On *any* support `S` of size at least `1116048`, the direction `g` cannot be represented by any polynomial of degree at most `1048576=k`. Otherwise `(X^4096-α)q(X)+R(X)` would have more roots than its degree `<= 1052672 < 1116048`, implying the impossible polynomial identity `(X^4096-α)q=-R` with nonzero `R` of smaller degree.

The Lean theorem `exists_many_deployed_bad_slopes` preserves **degree <=k-1** for each explaining polynomial and **noncontainment even for degree <=k** on the same support, with *one fixed received pair* `f,g` and **more than `2^59` distinct slopes**. It uses domain elements, not only index positions. Therefore the local support-wise numerator would exceed the conjectured budget already at the stronger `a=1118207`, hence at `a=1116048` by monotonicity.

### Independent verification requested

1. Verify the exact deployed code, field, evaluation subgroup, challenge field and line orientation against the *primary* MCA definition and the row in `agents.md`, not just this source-mirrored `WDeployed` predicate.
2. Check that the support-wise numerator really takes a maximum over one received pair and counts **distinct field slopes**, and that this theorem maps onto `LD_sw(C,a)` without omitted hypotheses.
3. Rerun/reformalize the proof using pinned Lean 4.34. Inspect the theorem statements and transitive dependencies independently; the existing audit is self-authored.
4. Identify any pre-existing report or stronger equivalent attack and correct the attribution.
5. If verified, determine the new unsafe endpoint; do not infer a new first-safe agreement without a separate upper bound.

No official `n=2^18` Proximity Prize `ProtocolClaim` score improvement is asserted here. The endpoint is the **separate, proposed, n=2^21 MCA safety bound**.

We welcome counterexamples to this report and will correct the claim if any model mismatch is found.
