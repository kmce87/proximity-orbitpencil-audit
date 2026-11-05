#!/usr/bin/env python3
"""Black-box regression tests for the MCA Lean axiom log checker.

Replay from repository root:
    python3 -m unittest discover -s tests -p 'test_mca_axiom_parser.py' -v
These tests do not certify the mathematical construction or manuscript equivalence.
"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_mca_axioms.py"
NAMES = (
    "OrbitPencilLiftSameKey.concrete_sextic_card",
    "OrbitPencilLiftDeployedDomain4096.supportWise_to_deployed",
    "OrbitPencilLiftDeployedDomain4096.exists_many_deployed_bad_slopes",
)
STANDARD = "propext, Classical.choice, Quot.sound"


def make_log(axioms=STANDARD, omit=None, duplicate=False, missing_end=False):
    reports = [
        f"'{name}' depends on axioms:\n[{axioms}]"
        for name in NAMES if name != omit
    ]
    if duplicate:
        reports.append(reports[0])
    return (
        "STAGE: baseline gate\n"
        "STAGE: transitive axiom output\n"
        + "\n".join(reports)
        + ("\n" if missing_end else "\nSTAGE: allowlist checker\n")
    )


class ParserRegression(unittest.TestCase):
    def check(self, log, should_pass):
        with tempfile.TemporaryDirectory() as d:
            path = pathlib.Path(d) / "audit.log"
            path.write_text(log)
            result = subprocess.run(
                [sys.executable, str(CHECKER), str(path)],
                capture_output=True, text=True, cwd=ROOT
            )
        self.assertEqual(result.returncode == 0, should_pass,
                         result.stdout + result.stderr)

    def test_quoted_multiline_standard_axioms_pass(self):
        self.check(make_log(), True)

    def test_unexpected_axiom_rejected(self):
        self.check(make_log(axioms=STANDARD + ", Lean.ofReduceBool"), False)

    def test_missing_report_rejected(self):
        self.check(make_log(omit=NAMES[1]), False)

    def test_duplicate_report_rejected(self):
        self.check(make_log(duplicate=True), False)

    def test_missing_stage_marker_rejected(self):
        self.check(make_log(missing_end=True), False)

    def test_sorry_rejected(self):
        self.check(make_log() + "sorryAx\n", False)


if __name__ == "__main__":
    unittest.main()
