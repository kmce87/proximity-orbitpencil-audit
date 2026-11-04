#!/usr/bin/env python3
"""Fail-closed integer-radius and quantifier-order audit for Lane A.
Run from repository root: python3 mca/check_cap25_radius_quantifiers.py
No external dependencies. This is a source audit, NOT a Lean proof.
"""
from pathlib import Path

n = 2**21
k = 2**20
a0 = 1116048
a1 = 1118207
assert 0 < k < a0 < a1 <= n
assert n - a0 == 981104
assert n - a1 == 978945
# At delta=(n-a0)/n, ceil((1-delta)*n)=a0 exactly.
from fractions import Fraction
delta = Fraction(n-a0,n)
assert (1-delta)*n == a0
assert delta < Fraction(n-k,n)
# At the same delta, every support with >=a1 points qualifies.
assert a1 >= a0

event = Path("LeanPortCAP25Event4096.lean").read_text()
budget = Path("LeanPortCAP25Budget4096.lean").read_text()
prob = Path("LeanPortCAP25Probability4096.lean").read_text()
checks = {
 "degree strict deployed": "c.natDegree < 1048576" in event,
 "support at a1": "1118207 ≤ S.card" in event,
 "support at a0": "1116048 ≤ S.card" in budget,
 "fixed received pair outside slope": "∃ (f g : D → Sextic) (Z : Finset Sextic)" in event,
 "slope witnesses support existential": "∃ S : Finset D" in event,
 "same-support noncontainment": "¬ (Explains f S ∧ Explains g S)" in event and "¬ (Explains f S ∧ Explains g S)" in budget,
 "full-field slope filter": "Finset.univ.filter (CAP25BadAtA0 f g)" in prob,
 "fixed pair probability theorem": "exists_fixed_pair_probability_cross_product" in prob,
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
assert all(checks.values()), "Source mismatch; reject audit"
print("PASS: integer-ball threshold at a0, monotonic transfer from a1")
print("LIMIT: string matching does not certify semantic equivalence to CAP25 or Lean compilation")
