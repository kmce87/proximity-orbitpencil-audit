#!/usr/bin/env python3
"""Fail-closed scope check for CAP25 v13.2 MCA definition (not a lift proof).
Replay: python3 mca/check_cap25_v132_scope.py
Requires public GitHub network access.
"""
import urllib.request

URL = "https://raw.githubusercontent.com/przchojecki/rs-mca/main/tex/cs25_cap_v13_2.tex"
req = urllib.request.Request(URL, headers={"User-Agent": "mca-cap25-scope-audit"})
with urllib.request.urlopen(req, timeout=30) as response:
    source = response.read().decode("utf-8")
start = source.index(r"\begin{definition}[mutual correlated agreement error")
end = source.index(r"\end{definition}", start)
definition = source[start:end]
assert r"\label{def:mca}" in definition
assert r"\gamma\leftarrow\F" in definition, "Not a uniform full-field challenge"
assert r"\max_{f_1,f_2\in\F^n}" in definition, "Fixed-line maximum missing"
assert r"\exists S\subseteq D" in definition, "Support-wise witness missing"
assert r"\distS" in definition, "Support-wise noncontainment missing"
assert r"\Gamma" not in definition, "Restricted challenge set detected"
print("PASS: CAP25 v13.2 def:mca quantifies uniform slopes over the full field.")
print("LIMIT: This does not establish that a different challenge statement uses this definition.")
print("LIMIT: No concrete 4096-fibre witness, degree bound, or Lean proof is checked.")
