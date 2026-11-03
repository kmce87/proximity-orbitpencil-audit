#!/usr/bin/env python3
"""Source-replayable audit of the rs-mca finite KoalaBear MCA row.
This is a *source consistency* test, NOT a Lean certificate or a proof
of any concrete slope witness. Requires network to retrieve upstream.
"""
import re
import urllib.request

URL = ("https://raw.githubusercontent.com/przchojecki/rs-mca/"
       "main/experimental/grande_finale.tex")
with urllib.request.urlopen(URL, timeout=30) as response:
    manuscript = response.read().decode("utf-8")
needle = "KoalaBear MCA & 1116047 & 1116048 & 67471 & 274980728111395087"
assert needle in manuscript, "The finite KoalaBear MCA row changed; audit manually."
pos = manuscript.index(needle)
near = manuscript[pos:pos+1300]
dimension = "Here $n=2^{21}$, $K=2^{20}+1$ on the MCA route, and $K=2^{20}$ on the list route."
assert dimension in near, "The finite-row dimension statement changed."
assert "KoalaBear list & 1116046 & 1116047" in near
# The row itself does not specify a challenge set Gamma.
row = manuscript[pos:manuscript.index("\\\\", pos)]
assert "Gamma" not in row and "\\Gamma" not in row
print("PASS: manuscript KoalaBear MCA row is at a0=1116047, a+=1116048.")
print("PASS: manuscript explicitly assigns K=2^20+1 to MCA and K=2^20 to LIST.")
print("PASS: finite MCA row itself does not specify Gamma.")
print("UNRESOLVED: authoritative challenge-set membership for constructed slopes.")
print("UNRESOLVED: deployed RS[D,2^20] degree<k witness for every slope.")
print("This test does not prove Gamma is proper, or that MCA uses deployed k.")
