#!/usr/bin/env python3
"""N9 toy replay: for each type of n9_types, build h from characters, take B containing {h = -1}, and check in GF(2^16) with random
F_2-linear labels that V_phi = prod (X - ell(v))^phi(v) has the same coefficients as X^(N/2) V_B above degree N/2 (phi = 1_B + h).
Negative control: moving one root must break it.  Also checks the integrality rule and the moment identity m/16 = 1/2 + 2 w' - mu_B/4."""
import random, sys
from fractions import Fraction as Fr

POLY = 0x1100B
EXP = [0] * 131072
LOG = [0] * 65536
x = 1
for i in range(65535):
    EXP[i] = x
    LOG[x] = i
    x <<= 1
    if x >> 16:
        x ^= POLY
for i in range(65535, 131072):
    EXP[i] = EXP[i - 65535]

def mul(a, b):
    return 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]

def polyfromroots(roots):
    P = [1]
    for r in roots:
        Q = [0] * (len(P) + 1)
        for i, c in enumerate(P):
            Q[i + 1] ^= c
            Q[i] ^= mul(c, r)
        P = Q
    return P

def polymul(A, B):
    R = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a:
            for j, b in enumerate(B):
                R[i + j] ^= mul(a, b)
    return R

def par(x):
    return bin(x).count("1") & 1

def rank(vs):
    b = []
    for v in vs:
        for u in b:
            v = min(v, v ^ u)
        if v:
            b.append(v)
    return len(b)

def h_from(chars, signs, N):
    """h(v) = 1/2 + (1/4) sum sign_i chi_{a_i}(v); returns None unless integer valued."""
    m = len(chars)
    h = []
    for v in range(N):
        s = 2
        for a, b in zip(chars, signs):
            s += 1 - 2 * (par(a & v) ^ b)
        if s % 4:
            return None
        h.append(s // 4)
    return h

def random_chars(n, m, r, rng):
    """m distinct nonzero characters of rank r with zero sum."""
    N = 1 << n
    for _ in range(100000):
        basis = []
        while rank(basis) < r:
            basis = [rng.randrange(1, N) for _ in range(r)]
        span = [0]
        for b in basis:
            span += [s ^ b for s in span]
        span = [s for s in span if s]
        if len(span) < m:
            continue
        c = rng.sample(span, m - 1)
        last = 0
        for a in c:
            last ^= a
        if last == 0 or last in c:
            continue
        c.append(last)
        if rank(c) == r:
            return c
    raise RuntimeError

def test_type(n, m, r, want_x, rng, trials=20):
    N = 1 << n
    D = N // 2
    done = 0
    tries = 0
    while done < trials and tries < 2000000:
        tries += 1
        chars = random_chars(n, m, r, rng)
        signs = [rng.randrange(2) for _ in chars]
        h = h_from(chars, signs, N)
        if h is None or min(h) < -1:
            continue
        E = [v for v in range(N) if h[v] == -1]
        if len(E) * (1 << r) != want_x * N:
            continue
        if len(E) > N // 8:
            continue
        rest = [v for v in range(N) if h[v] != -1]
        B = E + rng.sample(rest, N // 8 - len(E))
        basis = [rng.randrange(1, 65536) for _ in range(n)]
        while rank(basis) < n:
            basis = [rng.randrange(1, 65536) for _ in range(n)]
        lab = [0] * N
        for v in range(N):
            for i in range(n):
                if v >> i & 1:
                    lab[v] ^= basis[i]
        inB = [0] * N
        for v in B:
            inB[v] = 1
        phi = [h[v] + inB[v] for v in range(N)]
        assert min(phi) >= 0 and sum(phi) == 5 * N // 8
        roots = [lab[v] for v in range(N) for _ in range(phi[v])]
        Vphi = polyfromroots(roots)
        T = polymul([0] * D + [1], polyfromroots([lab[v] for v in B]))
        assert len(Vphi) == len(T), (len(Vphi), len(T))
        ok = all(Vphi[i] == T[i] for i in range(D + 1, len(T)))
        if not ok:
            print("FAIL polynomial top", n, m, r)
            sys.exit(1)
        # negative control: replace one root
        rr = list(roots)
        rr[0] = lab[N - 1] if rr[0] != lab[N - 1] else lab[N - 2]
        Vbad = polyfromroots(rr)
        assert any(Vbad[i] != T[i] for i in range(D + 1, len(T)))
        # moment identity
        w = sum(Fr(p * (p - 1), 2) for p in phi) / N
        muB = Fr(sum(phi[v] for v in B), len(B))
        assert Fr(m, 16) == Fr(1, 2) + 2 * w - muB / 4
        done += 1
    return done, tries

def main():
    rng = random.Random(20261105)
    for (n, m, r, x) in [(7, 4, 3, 0), (7, 6, 5, 1), (7, 6, 4, 1), (7, 8, 5, 3), (7, 8, 4, 2), (7, 8, 6, 5), (8, 6, 5, 1), (8, 8, 6, 5)]:
        d, t = test_type(n, m, r, x, rng, trials=6 if n == 8 else 12)
        print("n=%d m=%d r=%d t=%d: %d polynomial checks passed (%d candidates drawn)" % (n, m, r, x, d, t))

if __name__ == "__main__":
    main()
