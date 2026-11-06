#!/usr/bin/env python3
"""N10 Lemma check.  Pure local-mean classification on F_2^r: T = sum a_chi chi, |a| <= 3, sum a^2 <= mmax, chars of full rank r (up to GL_r the
standard basis is among the chars and, by translation, its signs are +).  y = 5/8 + xi + T/4 with |xi| <= tol.  Necessary for any member whose
residues on the span have sup norm <= tol: y >= 0 and E[(y-1)^+] < 1/16.  Prints every feasible T.  Exact rational arithmetic."""
from fractions import Fraction as Fr
from itertools import combinations, product
import sys

def par(x):
    return bin(x).count("1") & 1

def feasible(R, chars, a, tol):
    T = [sum(ai * (-1) ** par(c & x) for c, ai in zip(chars, a)) for x in range(R)]
    exc = Fr(0)
    for t in T:
        y = Fr(5, 8) + Fr(t, 4)
        if y + tol < 0:
            return None
        exc += max(Fr(0), y - tol - 1)
    return T if exc / R < Fr(1, 16) else None

def run(r, tol, mmax):
    R = 1 << r
    basis = [1 << i for i in range(r)]
    others = [c for c in range(1, R) if c not in basis]
    seen = {}
    for extra in range(0, mmax - r + 1):
        for ex in combinations(others, extra):
            chars = basis + list(ex)
            k = len(chars)
            for abs_a in product((1, 2, 3), repeat=k):
                m = sum(x * x for x in abs_a)
                if m > mmax:
                    continue
                for sg in product((1, -1), repeat=extra):
                    a = list(abs_a[:r]) + [x * s for x, s in zip(abs_a[r:], sg)]
                    T = feasible(R, chars, a, tol)
                    if T is None:
                        continue
                    key = (k, tuple(sorted(abs_a)), tuple(sorted(T)))
                    if key not in seen:
                        seen[key] = (chars, a)
    return seen

if __name__ == "__main__":
    # rank >= 5 follows from rank 4: a local mean on the span of 4 independent characters of T is again of this form (m <= 9 by the L2 bound)
    for r, mmax in ((1, 9), (2, 9), (3, 9), (4, 9)):
        for tol in (Fr(1, 16),):
            s = run(r, tol, mmax)
            print(f"r={r} tol={tol} mmax={mmax}: {len(s)} patterns", flush=True)
            for (k, aa, T), (chars, a) in sorted(s.items()):
                hist = {}
                for t in T:
                    hist[t] = hist.get(t, 0) + 1
                print(f"   k={k} |a|={aa} T-hist={sorted(hist.items())} e.g. chars={chars} a={a}", flush=True)
