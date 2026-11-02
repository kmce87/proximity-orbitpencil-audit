# KoalaBear 4096-fibre W_a normalization: bounded source audit (2026-11-02 UTC)

**One falsifiable target for this run:** verify that the new exact-integer normalization certificate in PR #33 refers to the **same sextic field** and the **distinct support-wise bad-slope numerator** used by the preceding 83-declaration local theorem. This is a source review, NOT a new kernel proof.

## Sources inspected at `c8445fcf6933898a96c9aa55d3a8612c745c2524`

- `LeanPortSameKeyFamily.lean`: `Sextic := KoalaBear.Ext6`; `concrete_sextic_card` proves `Fintype.card Sextic = (2130706433 : Nat)^6` using `KoalaBear.card_ext6`.
- `LeanPortWaBridge4096.lean`: `BadSlope f g z` projects an explicit finite support `S`, `W f g S z` requires `|S| >= 1116048`, RS explanation of `f + z*g` on `S`, and excludes a simultaneous RS explanation of both generators. `exists_many_W_bad_slopes` supplies a *Finset Sextic* `Z` with `274980728111395087 < Z.card` for one `receivedBase, receivedDirection` pair.
- `LeanPortWaNormalization4096.lean`: `budget_successor_exceeds_field` states `p^6 < 2^128*(274980728111395088)`; `exists_W_above_normalized_budget` composes that with the existing distinct-slope count via `Nat.mul_le_mul_left`.
- Published `rs-mca` M2 bridge: https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m2/m2_line_decoding_mca_bridge.md states `eps_mca(C,delta)=LD_sw(C,ceil((1-delta)n))/|F|` and defines the per-support witness.
- Published target workboard: https://github.com/przchojecki/rs-mca/blob/main/agents.md states the KoalaBear candidate first-safe agreement `1116048` and integer cap `274980728111395087`.

## Source-level verdict

**PASS, limited to compatibility of the stated algebraic definitions:** the `Z.card` in the normalization theorem is a count of distinct field-valued slopes, rather than an enumeration of support witnesses; its denominator is the sextic field's cardinality, not the base prime-field size. The arithmetic comparison is strict and cross-multiplied, avoiding floating-point rounding. The support-wise predicate is modeled locally; the external `rs-mca` model is not formally imported.

## Missing independent checks (do not silently promote)

1. **Lean 4.34 kernel and transitive-axiom gate for these two new declarations:** no successful PR #33 CI receipt was located at the time of this audit. The prior 83-declaration receipt is GitHub Actions run 41540671381, commit `8a96a891a3b7ddb4e03bae2d34122fe02ca946f8`.
2. Fresh clean-room replay of the full dependencies, exact `KoalaBear.Ext6` field instance and evaluation-domain/index equivalence.
3. Exact source-to-source match of the code `C`, challenge distribution over `F_(p^6)`, agreement endpoint, and the original paper's `B^MCA_C(a)` definition. A matching prose note alone is not a formally imported equivalence.
4. Independent review, and any external author-crediting report, must preserve credit for original 512-fibre `OrbitPencil.lean` (proximity-prize/proximity-prize PR #38, including `erdkocak`). Do not present this lift as an accepted Proximity Prize `ProtocolClaim`.
5. The ordinary LIST bound at agreement `1116047` remains separate and is **not** refuted here.

## Exact replay

```sh
git clone https://github.com/kmce87/proximity-orbitpencil-audit.git
cd proximity-orbitpencil-audit
git checkout c8445fcf6933898a96c9aa55d3a8612c745c2524
bash scripts/run_lean_434_gate.sh
```

**Status at creation: SOURCE-AUDITED, NEW LEAN GATE UNVERIFIED, INDEPENDENT PRIZE ACCEPTANCE: NO.** No historical experiment ledger was changed.
