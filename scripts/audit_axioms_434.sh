#!/usr/bin/env bash
# Fail-closed transitive axiom audit of the seventy-five targeted Lean lemmas.
set -euo pipefail
cd "$(dirname "$0")/.."
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/targets.txt" <<'TARGETS'
LeanPortIndexedNoncontainment.lean OrbitPencilLiftIndexedNoncontainment.no_large_support OrbitPencilLiftIndexedNoncontainment.no_large_support_on_indices OrbitPencilLiftIndexedNoncontainment.quotient_direction_not_codeword_on_indices
LeanPortNoncontainment.lean OrbitPencilLiftNoncontainment.no_large_support
LeanPortGeometry.lean OrbitPencilLiftGeometry.idx_injective OrbitPencilLiftGeometry.idx_row_column OrbitPencilLiftGeometry.pow_block
LeanPortSameKeyFamily.lean OrbitPencilLiftSameKey.outer_card OrbitPencilLiftSameKey.candidates_card OrbitPencilLiftSameKey.card_keys OrbitPencilLiftSameKey.pigeonhole OrbitPencilLiftSameKey.orbit_count OrbitPencilLiftSameKey.exists_big_same_key_family OrbitPencilLiftSameKey.V_monic OrbitPencilLiftSameKey.V_natDegree OrbitPencilLiftSameKey.candidate_card OrbitPencilLiftSameKey.V_coeff_top OrbitPencilLiftSameKey.V_coeff_gt OrbitPencilLiftSameKey.top_coeff_eq_of_key OrbitPencilLiftSameKey.V_sub_degree_lt_of_key OrbitPencilLiftSameKey.V_eval_zero_pow OrbitPencilLiftSameKey.V_eval_zero_eq_of_key OrbitPencilLiftSameKey.projectedNode_injective OrbitPencilLiftSameKey.V_eval_zero_iff_of_injective OrbitPencilLiftSameKey.V_injective_of_y_injective OrbitPencilLiftSameKey.concrete_V_injective OrbitPencilLiftSameKey.concrete_V_sub_ne_zero OrbitPencilLiftSameKey.mapped_nodes_injective OrbitPencilLiftSameKey.V_map OrbitPencilLiftSameKey.mapped_V_injective OrbitPencilLiftSameKey.mapped_V_sub_ne_zero OrbitPencilLiftSameKey.mapped_V_sub_natDegree_lt_of_key OrbitPencilLiftSameKey.concrete_prime_card OrbitPencilLiftSameKey.concrete_sextic_card OrbitPencilLiftSameKey.eta6_pow OrbitPencilLiftSameKey.eta6_node OrbitPencilLiftSameKey.concrete_sextic_constant_eq_of_key OrbitPencilLiftSameKey.concrete_same_key_family OrbitPencilLiftSameKey.concrete_sextic_degree_lt_of_key OrbitPencilLiftSameKey.concrete_sextic_sub_ne_zero
LeanPortSeparatingAlpha.lean OrbitPencilLiftSeparatingAlpha.bad_card_le OrbitPencilLiftSeparatingAlpha.alpha_arithmetic OrbitPencilLiftSeparatingAlpha.exists_alpha_gamma_injective
LeanPortConcreteSlopes.lean OrbitPencilLiftConcreteSlopes.exists_concrete_alpha_distinct_slopes
LeanPortSupport4096.lean OrbitPencilLiftSupport4096.coreRows_card OrbitPencilLiftSupport4096.pair_disjoint OrbitPencilLiftSupport4096.support_card OrbitPencilLiftSupport4096.node21_injective OrbitPencilLiftSupport4096.coreLocator_monic OrbitPencilLiftSupport4096.coreLocator_natDegree OrbitPencilLiftSupport4096.coreLocator_ne_zero OrbitPencilLiftSupport4096.coreLocator_eval_core
LeanPortPencil4096.lean OrbitPencilLiftPencil4096.delta_eval_zero OrbitPencilLiftPencil4096.pencil_eval_zero OrbitPencilLiftPencil4096.pencil_eval_alpha OrbitPencilLiftPencil4096.pencil_degree_lt OrbitPencilLiftPencil4096.exists_quotient OrbitPencilLiftPencil4096.abstract_message_degree_le OrbitPencilLiftPencil4096.exists_message_poly
LeanPortLineAgreement4096.lean OrbitPencilLiftLineAgreement4096.rational_line_identity OrbitPencilLiftLineAgreement4096.pencil_line_identity OrbitPencilLiftLineAgreement4096.pencil_line_agrees_on_root
LeanPortPointwiseSupport4096.lean OrbitPencilLiftPointwiseSupport4096.node6_pow_column OrbitPencilLiftPointwiseSupport4096.node6_pow_projected OrbitPencilLiftPointwiseSupport4096.node6_pow_nonzero OrbitPencilLiftPointwiseSupport4096.node6_pow_ne_alpha OrbitPencilLiftPointwiseSupport4096.y6_injective OrbitPencilLiftPointwiseSupport4096.logical_support_root_or OrbitPencilLiftPointwiseSupport4096.pencil_agrees_on_logical_support OrbitPencilLiftPointwiseSupport4096.pencil_agrees_with_message_on_logical_support
LeanPortTypedSupport4096.lean OrbitPencilLiftTypedSupport4096.point_logical OrbitPencilLiftTypedSupport4096.pointIndex_injective OrbitPencilLiftTypedSupport4096.selected_card OrbitPencilLiftTypedSupport4096.logical_support_card_lower
LeanPortAgreementCount4096.lean OrbitPencilLiftAgreementCount4096.exists_message_agreement_1118207
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
echo "TRANSITIVE AXIOM AUDIT PASS: seventy-five lemmas; only allowed axioms"
