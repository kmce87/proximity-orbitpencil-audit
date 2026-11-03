#!/usr/bin/env python3
"""Lane A: fail-closed source scope check, NOT a proof of the MCA lift.
Reads upstream main intentionally: future upstream edits require renewed audit.
Run: python3 mca/audit_gamma_scope.py
"""
from urllib.request import urlopen
URL = "https://raw.githubusercontent.com/przchojecki/rs-mca/main/experimental/grande_finale.tex"
with urlopen(URL, timeout=30) as response:
    s = response.read().decode("utf-8")
checks = {
 "restricted foundation": r"B^{\rm MCA}_{C,\Gamma}(a)" in s,
 "full-field compiler": r"\gamma\in\F:\exists E\subseteq D" in s,
 "unqualified full-field equality": r"B_C^{\rm MCA}(a)=\max_{y_0,y_1\in\F^{n-k}}" in s,
 "finite KoalaBear row": "KoalaBear MCA & 1116047 & 1116048 & 67471 & 274980728111395087" in s,
 "auxiliary K statement": "K=2^{20}+1$ on the MCA route" in s,
 "actual MCA code dimension": "For the actual MCA code, $R=n-k=1048576$" in s,
}
for k,v in checks.items():
    print(("PASS" if v else "FAIL") + ": " + k)
assert all(checks.values()), "Upstream text changed or assertion incorrect; manually review."
print("PASS: the source uses both restricted and full-field conventions.")
print("NOT PROVED: which convention controls the specific proposed adjacent row.")
print("NOT PROVED: membership of the constructed slopes in Gamma.")
