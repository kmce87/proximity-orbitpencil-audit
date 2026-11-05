#!/usr/bin/env python3
"""Fail closed on missing/unexpected Lean #print axioms results.

Replay: python3 scripts/check_mca_axioms.py mca-axioms.log
Only standard Lean logical axioms are permitted; this is NOT a manuscript audit.
"""
import pathlib
import re
import sys

EXPECTED = (
    "OrbitPencilLiftSameKey.concrete_sextic_card",
    "OrbitPencilLiftDeployedDomain4096.supportWise_to_deployed",
    "OrbitPencilLiftDeployedDomain4096.exists_many_deployed_bad_slopes",
)
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
if len(sys.argv) != 2:
    sys.exit("usage: check_mca_axioms.py LOG")
log = pathlib.Path(sys.argv[1]).read_text()
# The baseline gate also prints axioms; audit only the dedicated stage.
marker = "STAGE: transitive axiom output"
end_marker = "STAGE: allowlist checker"
if log.count(marker) != 1 or log.count(end_marker) != 1:
    sys.exit("FAIL: missing or duplicate axiom audit stage markers")
audit = log.split(marker, 1)[1].split(end_marker, 1)[0]
if re.search(r"\bsorryAx\b|\berror:|unsolved goals", log, re.I):
    sys.exit("FAIL: Lean error or sorryAx in log")
# Lean prints: '<name> depends on axioms: [a, b, c]' (possibly line wrapped).
for name in EXPECTED:
    pattern = r"[\u0027\u0022]?" + re.escape(name) + r"[\u0027\u0022]?\s+depends on axioms:\s*\[([^\]]*)\]"
    matches = re.findall(pattern, audit, flags=re.S)
    if len(matches) != 1:
        sys.exit(f"FAIL: expected exactly one axiom report for {name}, found {len(matches)}")
    axioms = {a.strip() for a in matches[0].split(",") if a.strip()}
    unexpected = axioms - ALLOWED
    if unexpected:
        sys.exit(f"FAIL: {name} has nonstandard axioms: {sorted(unexpected)}")
    print(f"PASS {name}: {sorted(axioms)}")
print("PASS: all expected theorem axiom reports present and allowlisted")
