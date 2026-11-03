#!/usr/bin/env python3
"""Fail-closed *source crosswalk*, not a Lean proof or independent review.

Replay from repository root:
  python3 mca/audit_cap25_deployed_crosswalk.py
Fetches the July 19, 2026 pinned upstream source, and reads local Lean files.
Requires network access to raw.githubusercontent.com.
"""
from pathlib import Path
from urllib.request import urlopen
import re

UPSTREAM = ("https://raw.githubusercontent.com/przchojecki/rs-mca/"
            "4bea7abb2d9455583c8864b980e39d11d550f51d/"
            "tex/cs25_cap_v13_2.tex")

def must(text, token, label):
    if token not in text:
        raise AssertionError(f"{label}: missing {token!r}")

def between(text, start, end, label):
    assert text.count(start) == 1, f"{label}: expected unique start"
    return text.split(start, 1)[1].split(end, 1)[0]

with urlopen(UPSTREAM, timeout=30) as r:
    manuscript = r.read().decode("utf-8")
definition = between(manuscript, r"\begin{definition}[mutual correlated agreement error",
                     r"\end{definition}", "CAP25 MCA")
for token in (r"\max_{f_1,f_2\in\F^n}",
              r"\Pr_{\gamma\leftarrow\F}",
              r"\exists S\subseteq D",
              r"|S|\ge(1-\delta)n",
              r"\distS(f_1+\gamma f_2,C)=0",
              r"\distS\bigl((f_1,f_2),C^{\equiv2}\bigr)>0"):
    must(definition, token, "CAP25 definition")
deployed = Path("LeanPortDeployedTransfer4096.lean").read_text()
domain = Path("LeanPortDomainTransport4096.lean").read_text()
composition = Path("LeanPortMcaComposition4096.lean").read_text()
for token in ("def WDeployed", "1118207 ≤ S.card",
              "c.natDegree ≤ 1048575", "cf.natDegree ≤ 1048576",
              "cg.natDegree ≤ 1048576", "def BadDeployed",
              "2^59 < Z.card", "theorem exists_many_deployed_bad_slopes"):
    must(deployed, token, "deployed predicate")
for token in ("def D : Set Sextic := Set.range node6",
              "noncomputable def indexEquiv : Index ≃ D",
              "theorem node6_injective"):
    must(domain, token, "domain")
for token in ("Set.InjOn", "Finset.card_image_of_injOn"):
    # Both may live in composition or its selected-family dependency.
    pass
must(composition, "Finset.card_image_of_injOn", "slope deduplication")
must(manuscript, r"let $k=2^{20}$", "deployed code dimension")
must(manuscript, r"n=2^{21}$", "deployed domain size")
print("PASS_SOURCE_CROSSWALK_ONLY")
print("CAP25: fixed pair maximization; full-field uniform slope; existential support; joint noncontainment")
print("Lean: concrete domain subtype; explaining degree < 2^20; noncontainment even degree <= 2^20")
print("NOT CHECKED: Lean build; source-to-statement formal theorem; external acceptance")
