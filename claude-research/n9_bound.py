#!/usr/bin/env python3
"""N9: exact integer upper bound on the members above 9N/16 of a mass-5N/8 class with a non-negative representative.

phi = 1_B + h, |B| = N/8, h integer, mean 1/2, Fourier in (1/4)Z, phi >= 0, |supp phi| > 9N/16.
Types (n9_types.cpp lists all abstract patterns; shapes with a coefficient +-2 are worked out in the ledger):
  T4 + T2  Boolean h: at most one of C, complement of C (their overlaps with B sum to N/8).
  6a, 6b, 8a, 8b, 8c, 8d: h = -1 exactly on t cosets of the kernel W' (codim r), all inside B.  c = number of h per (W', E').
Tuple bound: (basis of the first coset, one point of each other coset) is a tuple of d + t points of B that determines (W', E'),
and each (W', E') has t! * bases(d) * 2^((t-1) d) such tuples, so #(W', E') <= |B|^(d+t) / (t! bases(d) 2^((t-1)d)).
"""
from fractions import Fraction
from math import log2, factorial

def gl(d):
    r = 1
    for i in range(d):
        r *= (2**d - 2**i)
    return r

def bases(d):
    return 2**d * gl(d)

def gauss2(n, k):
    num = den = 1
    for i in range(k):
        num *= 2**(n - i) - 1
        den *= 2**(i + 1) - 1
    return num // den

def M_C(n):
    return 8 * gauss2(n, 2) * (2**(n - 2) - 1)

TYPES = [  # name, c, r, t
    ("6a", 13888, 5, 1),
    ("6b", 280, 4, 1),
    ("8a", 256, 6, 5),
    ("8b", 1344, 5, 3),
    ("8c", 56, 4, 2),
    ("8d", 21, 3, 1),
]

def bound(n, Bsize=None):
    B = Bsize if Bsize is not None else 2**(n - 3)
    out = {}
    tot = M_C(n) // 2 + (2**n - 1)
    out["T4+T2"] = tot
    for name, c, r, t in TYPES:
        d = n - r
        if d < 0:
            continue
        num = B**(d + t)
        den = factorial(t) * bases(d) * 2**((t - 1) * d)
        e = num // den
        out[name] = c * e
        tot += c * e
    out["total"] = tot
    return out

if __name__ == "__main__":
    assert M_C(21) == 3074447083519519400
    assert gl(5) // factorial(6) == 13888
    for n in (21, 20, 19, 18):
        b = bound(n)
        print("n=%d" % n, " ".join("%s=2^%.3f" % (k, log2(v)) for k, v in b.items()))
    b = bound(21)
    print("n=21 total =", b["total"], " 2^64 =", 2**64, " total < 2^64:", b["total"] < 2**64)
    print("margin factor 2^64/total = %.3f" % (2**64 / b["total"]))
    # what the T4 part alone misses by
    print("2^64/(M_C(21)/2) = %.3f" % (2**64 / (M_C(21) // 2)))
    # flat B, exact values (census formula, checked at n = 5..9): 6a gt = 1792 per E', 8b = 1344 per E', 4 [n-3,2] flats E' of each kind
    g = gauss2(18, 2)
    print("flat B at n=21: 6a gt = 2^%.2f, 8b gt = 2^%.2f" % (log2(4 * g * 1792), log2(4 * g * 1344)))
