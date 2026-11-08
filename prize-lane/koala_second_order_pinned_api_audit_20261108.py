#!/usr/bin/env python3
"""Reproduce the pinned ArkLib 4.34 second-order entrypoint audit.
Network access to GitHub REST API is required; no login for public repo.
The audit establishes file-level availability, not theorem-level impossibility.
"""
import json
from urllib.request import urlopen
REV = "34a834c61c859cc04205f5f43fd237cda8fb0da4"
URL = f"https://api.github.com/repos/Verified-zkEVM/ArkLib/git/trees/{REV}?recursive=1"
with urlopen(URL, timeout=30) as response:
    tree = json.load(response)
assert not tree["truncated"], "Tree truncated; negative result inconclusive"
paths = {entry["path"] for entry in tree["tree"] if entry["type"] == "blob"}
root = "ArkLib/Data/CodingTheory/HiddenDerivative/"
expected = [
    root + "Parameters/Basic.lean",
    root + "Parameters/FreeOrder.lean",
    root + "Interpolation/Counting.lean",
    root + "Parameters/FirstOrder/RateBound.lean",
]
assert all(p in paths for p in expected)
parameters = sorted(p for p in paths if p.startswith(root + "Parameters/") and p.endswith(".lean"))
named_second = [p for p in parameters if "SecondOrder" in p or "SecondDerivative" in p]
print("Pinned ArkLib", REV)
print("Existing general and first-order entrypoints:", *expected, sep="\n")
print("Named second-order parameter files:", named_second)
print("Parameter Lean file count:", len(parameters))
print("No named second-order parameter file; this does NOT establish theorem absence.")
