# Concrete KoalaBear sextic instantiation — 2026-11-01

## One falsifiable hypothesis
The 272-of-511 same-key polynomial family built over the **actual** pinned
KoalaBear 2^21 NTT projected nodes survives the concrete CompPoly
`KoalaBear.Ext6` embedding with (i) sextic cardinality p^6, (ii) equal
constant coefficients, (iii) nonzero pairwise differences and (iv) degree
less than 258. Failure of any statement blocks the lifted rational pencil.

## Source and authorship
Adapted from the accepted OrbitPencil PR #38, original contributors
including `erdkocak`, with the sextic implementation from CompPoly
(`CompPoly/Fields/KoalaBear/Ext6.lean`, author Derek Sorensen).
No claim of original attack authorship.

## Replay
```bash
bash scripts/run_lean_434_gate.sh
```

The strict gate compiles the proof files with Lean 4.34.0 and checks the
transitive axiom closure against the benchmark whitelist. The GitHub Actions
run is the actual verification record; do not mark the lemmas verified until
the run completes successfully.

## Boundary
This is a concrete field/polynomial bridge, **not** the complete received
line, the agreement support, the >2^59 distinct bad slopes on that line,
or an independent verifier-accepted Proximity Prize result. The official
Koala profile has n=2^18, not n=2^21.
