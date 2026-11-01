#!/usr/bin/env bash
# Fail-closed transitive axiom audit of the seven currently compiled Lean lemmas.
set -euo pipefail
cd "$(dirname "$0")/.."
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/targets.txt" <<'TARGETS'
LeanPortIndexedNoncontainment.lean OrbitPencilLiftIndexedNoncontainment.no_large_support OrbitPencilLiftIndexedNoncontainment.no_large_support_on_indices OrbitPencilLiftIndexedNoncontainment.quotient_direction_not_codeword_on_indices
LeanPortNoncontainment.lean OrbitPencilLiftNoncontainment.no_large_support
LeanPortGeometry.lean OrbitPencilLiftGeometry.idx_injective OrbitPencilLiftGeometry.idx_row_column OrbitPencilLiftGeometry.pow_block
TARGETS
while read -r file names; do
  out="$tmp/$(basename "$file").out"
  source="$tmp/$(basename "$file")"
  cat "$file" > "$source"
  for name in $names; do printf '\n#print axioms %s\n' "$name" >> "$source"; done
  lake env lean "$source" > "$out" 2>&1 || { cat "$out"; exit 1; }
  cat "$out"
  python3 - "$out" $names <<'PY'
import re, sys
from pathlib import Path
log = Path(sys.argv[1]).read_text()
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
for name in sys.argv[2:]:
    # Lean prints the qualified declaration in single quotes; the axiom list
    # can wrap across multiple lines. Match the exact name (not its prefix).
    pattern = (r"(?m)^'" + re.escape(name) +
               r"' (does not depend on any axioms|depends on axioms: \[([\s\S]*?)\])")
    m = re.search(pattern, log)
    if not m:
        raise SystemExit(f'FAIL: missing/unparseable #print axioms result for {name}')
    if m.group(1) == 'does not depend on any axioms':
        print(f'AXIOM PASS: {name}: none')
        continue
    found = {x.strip() for x in m.group(2).split(',') if x.strip()}
    unexpected = found - allowed
    if unexpected:
        raise SystemExit(f'FAIL: {name} depends on non-whitelisted axioms: {sorted(unexpected)}')
    print(f'AXIOM PASS: {name}: {sorted(found)}')
PY
done < "$tmp/targets.txt"
echo "TRANSITIVE AXIOM AUDIT PASS: seven lemmas; only allowed axioms"
