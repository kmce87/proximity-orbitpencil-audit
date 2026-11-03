#!/usr/bin/env python3
"""Lane B, 2026-11-03: one exact falsifiable numerical gate.

Hypothesis: a six-valued derivative key is still affordable for a 273-fibre
Koala upper construction, with STRICT >2^59 slopes after pigeonholing,
so its winning-set density exceeds 2^-128 in the official GF(q^6) field.

This is CONDITIONAL arithmetic, not an actual derivative key, attack, Lean
proof, or independent verifier acceptance. Historical upper 116.13 belongs
to the original published contributors.
"""
from math import comb

q = (1 << 31) - (1 << 24) + 1
f = comb(511, 273)
den = q**14 * 512
required_slopes = 1 << 59
six_bucket_min = (f + 6*den - 1) // (6*den)
seven_bucket_min = (f + 7*den - 1) // (7*den)

assert f > 6*den*required_slopes, "Six classes cannot guarantee >2^59"
assert f <= 7*den*required_slopes, "Seven classes unexpectedly affordable"
assert six_bucket_min > required_slopes
assert seven_bucket_min <= required_slopes

# The official challenge field is KoalaBear.Ext6, cardinality q^6.
assert required_slopes * (1 << 128) > q**6
assert 273*512 + 511 == 140287
assert 262144 - 140287 == 121857
# The score gate requires unsafeIndex <=122362; 121857 is numerically
# stronger if a genuine construction and unsafe suffix proof existed.
assert 121857 <= 122362

print("PASS: six-value key STRICTLY preserves >2^59 slope guarantee")
print("PASS: seven-value key does NOT guarantee >2^59")
print("PASS: 2^59 / q^6 > 2^-128")
print("Hypothetical agreement count:", 140287)
print("Hypothetical unsafe index:", 121857)
print("Numerical score gate 116.12: conditional, not certified")
print("BLOCKER: actual <=6-valued third-root derivative invariant in the")
print("published Koala fibre family, plus distinctness and Lean unsafeAbove")
print("NEW independently verifier-accepted result: NO")
