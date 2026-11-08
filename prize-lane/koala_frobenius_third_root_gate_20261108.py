#!/usr/bin/env python3
"""Lane B: exact cardinality gate for a Frobenius-conjugate third pencil root.

Source: proximity-prize/proximity-prize,
ProximityPrize/SubmissionUpper/OrbitPencil.lean (main at
eb82d3bf04a9c876c7ef9c3e6de4640fb85062f2), lines 367-370, 382-383,
448-453; 162 and 235 give |Sel| = 2^59+1.

HYPOTHESIS (falsified mathematically):
  beta = alpha^q, q = |KoalaBear.Field|, can be a third common root of
  pencil(U) = deltaV(U) - gamma(U)*X for every U in Sel.

Proof, conditional on the source declarations:
  deltaV(U) = VF(U0)-VF(U) is the image of a polynomial over K=GF(q).
  Therefore deltaV(U)(alpha^q) = deltaV(U)(alpha)^q.
  gamma(U) = deltaV(U)(alpha)/alpha, alpha != 0, so
    pencil(U)(alpha^q)
      = (gamma(U)*alpha)^q - gamma(U)*alpha^q
      = (gamma(U)^q - gamma(U))*alpha^q.
  Since alpha^q != 0, the root condition is gamma(U)^q = gamma(U).
  In FF=GF(q^6), the q-Frobenius fixed field is exactly K, with q elements.
  Since gamma is injective on Sel, at most q members can have that root.
  Since |Sel| = 2^59+1 > q, beta cannot be a common root.

Moreover alpha^q != alpha: if alpha in K, then gamma(U) is in K for
all U in Sel, contradicting injectivity and |Sel|>q.
Thus beta is a distinct third-root candidate, but cannot work uniformly.

This script checks only the exact integer/cardinality consequences; the
field-theoretic proof above is a paper argument, NOT a Lean certificate.
"""
from math import gcd

q = 2**31 - 2**24 + 1
selected = 2**59 + 1
assert q == 2_130_706_433
assert selected == 576_460_752_303_423_489
assert q < selected
assert gcd(1, 6) == 1
assert 273 * 512 + 511 == 140_287
assert 140_287 >= 139_782
assert 511 + 512 * 255 == 131_071
print("PASS: KoalaBear base-field cardinality =", q)
print("PASS: selected family size =", selected)
print("PASS: at most", q, "selected gamma-values can satisfy gamma^q=gamma")
print("PASS: fixed beta=alpha^q cannot be a uniform third root")
print("STATUS: mathematical obstruction; Lean kernel and verifier not run")
