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
lake env lean LeanPortIndexedNoncontainment.lean
lake env lean LeanPortNoncontainment.lean
lake env lean LeanPortGeometry.lean
lake env lean LeanPortSeparatingAlpha.lean
bash scripts/audit_axioms_434.sh
echo 'LOCAL LEAN COMPILATION + AXIOM AUDIT PASS (NOT independent prize-verifier acceptance)'
