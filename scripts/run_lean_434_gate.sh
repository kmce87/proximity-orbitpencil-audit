#!/usr/bin/env bash
# Strict proof gate: exit 77 when Lean 4.34 is unavailable; never report success.
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v lake >/dev/null 2>&1 || ! command -v lean >/dev/null 2>&1; then
  echo 'BLOCKED: Lean and/or Lake unavailable. No kernel check performed.' >&2
  exit 77
fi
if ! lean --version | grep -Fq 'Lean (version 4.34.0'; then
  echo "BLOCKED: wrong Lean version: $(lean --version)" >&2
  exit 77
fi
lake update
lake exe cache get
# CompPoly is a source dependency, not part of Mathlib's prebuilt cache.
lake build CompPoly.Univariate.NTT.KoalaBear
mkdir -p .lake/build/lib/lean
lake env lean -o .lake/build/lib/lean/LeanPortSameKeyFamily.olean LeanPortSameKeyFamily.lean
lake env lean -o .lake/build/lib/lean/LeanPortSeparatingAlpha.olean LeanPortSeparatingAlpha.lean
lake env lean -o .lake/build/lib/lean/LeanPortConcreteSlopes.olean LeanPortConcreteSlopes.lean
lake env lean -o .lake/build/lib/lean/LeanPortIndexedNoncontainment.olean LeanPortIndexedNoncontainment.lean
lake env lean LeanPortNoncontainment.lean
lake env lean -o .lake/build/lib/lean/LeanPortGeometry.olean LeanPortGeometry.lean
# Diagnostic gate: distinguish large Fin types from concrete support expansion.
lake env lean LeanPortFiniteImageProbe.lean
# The earlier failing predicate/finite-image diagnostics remain in the repository
# but are not prerequisites for this *different* logical-support hypothesis.
lake env lean -o .lake/build/lib/lean/LeanPortSupport4096.olean LeanPortSupport4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortPencil4096.olean LeanPortPencil4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortLineAgreement4096.olean LeanPortLineAgreement4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortPointwiseSupport4096.olean LeanPortPointwiseSupport4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortTypedSupport4096.olean LeanPortTypedSupport4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortAgreementCount4096.olean LeanPortAgreementCount4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortSelectedAgreement4096.olean LeanPortSelectedAgreement4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortDirectionNoncode4096.olean LeanPortDirectionNoncode4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortMcaComposition4096.olean LeanPortMcaComposition4096.lean
lake env lean -o .lake/build/lib/lean/LeanPortWaBridge4096.olean LeanPortWaBridge4096.lean
lake env lean LeanPortWaNormalization4096.lean
bash scripts/audit_axioms_434.sh
echo 'LOCAL LEAN COMPILATION + AXIOM AUDIT PASS (NOT independent prize-verifier acceptance)'
