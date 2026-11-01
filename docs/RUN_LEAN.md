# How to run the three Lean proof candidates

The private GitHub repo runs the `Lean 4.34 candidate kernel gate` automatically on pushes to `main`. Open **Actions** for the compiler output. The workflow can also be started manually from the Actions tab.

The versions are pinned in `lean-toolchain` (4.34.0) and `lakefile.toml` (ArkLib revision `34a834c61c859cc04205f5f43fd237cda8fb0da4`).

If GitHub Actions fails at install/dependencies, that is NOT evidence that the theorem fails. A red step containing `LeanPortIndexedNoncontainment.lean:<line>:<column>` is a genuine first compiler diagnostic.

The modules are **conditional lemmas**, not the full `2^58` distinct-slope theorem, not a claim of refuting the MCA safe row, and not an official Proximity Prize submission.

Attribution: accepted [OrbitPencil PR #38](https://github.com/proximity-prize/proximity-prize/pull/38), contributors including `erdkocak`.

Complete historical Git research archive, numerical code, and large certificates are preserved in the latest downloaded ZIP; this initial remote upload only contains proof candidates, project configuration, and the CI workflow.
