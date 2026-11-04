#!/usr/bin/env python3
"""Fail-closed audit of Lean #print axioms output for the two generator theorems.

Usage: python3 mca/check_generator_axioms.py /tmp/mca-generator.log
This checks logs only; it does NOT execute Lean or establish external MCA semantics.
"""
import pathlib
import re
import sys

NAMES = (
    "OrbitPencilLiftDomainTransport4096.node6_eq_embedded_omega_pow",
    "OrbitPencilLiftDomainTransport4096.D_eq_embedded_omega_powers",
)
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}

def check(log: str) -> None:
    if re.search(r"sorryAx|\berror:|unsolved goals|unknown constant", log):
        raise ValueError("Lean error, sorryAx or unresolved goal in output")
    for name in NAMES:
        # Lean prints: 'Name' depends on axioms: [ ... ]
        pattern = r"['‘]" + re.escape(name) + r"['’] depends on axioms:\s*\[([^\]]*)\]"
        matches = re.findall(pattern, log)
        no_axioms = re.search(r"['‘]" + re.escape(name) + r"['’] does not depend on any axioms", log)
        if len(matches) != 1 and not (len(matches) == 0 and no_axioms):
            raise ValueError(f"missing/ambiguous axiom declaration: {name}")
        if matches:
            actual = {x.strip() for x in matches[0].split(",") if x.strip()}
            if not actual <= ALLOWED:
                raise ValueError(f"disallowed axioms for {name}: {sorted(actual - ALLOWED)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: check_generator_axioms.py LEAN_LOG")
    try:
        check(pathlib.Path(sys.argv[1]).read_text())
    except (OSError, ValueError) as exc:
        sys.exit(f"FAIL: {exc}")
    print("PASS: generator theorem axiom output present and within whitelist (log-only)")
