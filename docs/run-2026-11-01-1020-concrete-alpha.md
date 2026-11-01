# Concrete same-key family → separating alpha composition

## Falsifiable hypothesis
The actual KoalaBear.Ext6 same-key family and the abstract separating-alpha
lemma compose into one Lean 4.34 theorem asserting existence of a **single**
alpha with `2^59+1` pairwise distinct gamma labels. No abstract cardinality,
nonzero-difference, degree, or large-family assumptions remain.

## Replay
```bash
bash scripts/run_lean_434_gate.sh
```

The GitHub Actions result on this branch is the compilation and axiom
certificate. Do not mark this theorem kernel-checked unless CI passes.

## What is NOT proved
The gamma labels are **not yet proved to be MCA-bad slopes**. In particular
there is no construction of the received affine line, no support proof for
1,118,207 agreement positions, and no bridge to the exact RS-MCA predicate.
The official Koala protected benchmark uses n=2^18, not this n=2^21 lift.

Attribution: accepted Proximity Prize OrbitPencil PR #38, including original
co-author erdkocak.
