#!/usr/bin/env python3
"""Fail-closed independent parser for pinned Lean 4.34 GitHub Actions job log.

Replay:
  gh api repos/kmce87/proximity-orbitpencil-audit/actions/jobs/126333616273/logs > /tmp/mca-job.log
  python3 mca/check_probability_kernel_log.py /tmp/mca-job.log

GitHub's endpoint may redirect and gh may follow it. This parser does not
download or authenticate. The source theorem and job commit must be checked
separately: this verifies what the log reports, not the external manuscript.
"""
from pathlib import Path
import re
import sys

EXPECTED = (
    "OrbitPencilCAP25Probability4096.witness_le_badSlopes",
    "OrbitPencilCAP25Probability4096.exists_fixed_pair_probability_cross_product",
)
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
if len(sys.argv) != 2:
    raise SystemExit("usage: check_probability_kernel_log.py <downloaded-actions-job-log>")
log = Path(sys.argv[1]).read_text(errors="replace")
for name in EXPECTED:
    pattern = r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]+)\]"
    hits = re.findall(pattern, log)
    if not hits:
        raise SystemExit(f"FAIL missing axiom report: {name}")
    for hit in hits:
        found = {a.strip() for a in hit.split(",")}
        if found - ALLOWED:
            raise SystemExit(f"FAIL unexpected axioms for {name}: {found - ALLOWED}")
    print(f"PASS {name}: {sorted({a.strip() for a in hits[-1].split(',')})}")
if "TRANSITIVE AXIOM AUDIT PASS: 95 declarations; only allowed axioms" not in log:
    raise SystemExit("FAIL base audit success marker missing")
if "LOCAL LEAN COMPILATION + AXIOM AUDIT PASS" not in log:
    raise SystemExit("FAIL base compilation success marker missing")
if re.search(r"(?m)^.*(?:error:|sorryAx).*", log):
    raise SystemExit("FAIL log contains error or sorryAx")
print("PASS log evidence: base 95-declaration audit and probability theorem axiom reports")
