#!/usr/bin/env python3
"""Lane B: test whether 129 rows can share the same reserved cq triple.

Pinned official source at 2026-11-06.  Pure source-table audit, NOT Lean proof.
"""
import re
import urllib.request
from collections import Counter

URL = ("https://raw.githubusercontent.com/proximity-prize/proximity-prize/"
       "eb82d3bf04a9c876c7ef9c3e6de4640fb85062f2/"
       "ProximityPrize/SubmissionBinaryUpper/LabelTable.lean")

def run(source):
    rows = [tuple(map(int, m)) for m in re.findall(
        r"⟨(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)⟩", source)]
    assert len(rows) == 420, len(rows)
    triples = Counter(tuple(sorted(row[:3])) for row in rows)
    assert len(triples) == 420, len(triples)
    assert max(triples.values()) == 1
    # Fixed cq triple = fixed reserved Q; no two official rows share Q.
    print("420 rows, 420 distinct reserved triples; maximum multiplicity 1.")
    print("129-row fixed-Q strategy: FALSIFIED.")
    print("This does NOT rule out common leading coefficients for distinct Q.")

if __name__ == "__main__":
    with urllib.request.urlopen(URL, timeout=20) as response:
        run(response.read().decode("utf-8"))
