#!/usr/bin/env python3
"""Fail-closed provenance check for the ORIGINAL 512-fibre OrbitPencil submission.
This does not verify the proposed 4096-fibre MCA lift.
Requires network access to api.github.com; run with Python 3.
"""
import json
import urllib.request

URL = "https://api.github.com/repos/proximity-prize/proximity-prize/pulls/38"
req = urllib.request.Request(URL, headers={"Accept": "application/vnd.github+json", "User-Agent": "mca-provenance-audit"})
with urllib.request.urlopen(req, timeout=20) as response:
    pr = json.load(response)
assert pr["number"] == 38
assert pr["merged_at"] is not None, "Original PR is not merged"
body = pr.get("body") or ""
assert "512-fibre rational pencil" in body, "Expected original construction not identified"
assert "131071" in body and "131072" in body, "Expected deployed row-degree argument absent"
assert "2^59" in body, "Expected distinct challenge count absent"
print("Original PR #38 merged:", pr["merged_at"])
print("PR opener:", pr["user"]["login"])
print("Source describes 512-fibre construction and deployed degree bound.")
print("IMPORTANT: bot PR opener is NOT sufficient to identify human mathematical authorship.")
print("IMPORTANT: PR merge is NOT verification of a 4096-fibre MCA lift.")
