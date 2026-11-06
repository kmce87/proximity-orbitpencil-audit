#!/usr/bin/env python3
"""N10: generate structured representatives rho = 1_{B+} - 1_P (mean 1/8) for n10_class.  Usage: n10_specs.py n outdir seed.
Names: fp<c>par  flat F (codim 3) + E - Q, E, Q parallel flats of codim c off F;  fp<c>skew  E, Q flats of codim c with different directions;
fp<c>rnd  E, Q random sets of density 2^-c off F;  fp<c>in  Q inside a sibling coset, E split;  rnd<c>  random B+ and P;
D<j>  type D: rho = 1_W - 1_T, W codim-2 flat, T of density 1/8 built from j flats (T not a flat, so no Boolean rep of this shape);
hyp  B+ and P in opposite hyperplanes; cut<c>  B+ = two half-flats of different directions + E."""
import random, sys

def flat(n, fixed):  # fixed: dict bit -> value
    return [x for x in range(1 << n) if all(((x >> b) & 1) == v for b, v in fixed.items())]

def rep(n, Bp, P):
    r = [0] * (1 << n)
    for x in Bp:
        r[x] += 1
    for x in P:
        r[x] -= 1
    assert sum(r) == (1 << n) // 8, (sum(r), (1 << n) // 8)
    return r

def specs(n, seed):
    rng = random.Random(seed)
    N = 1 << n
    t = [n - 1, n - 2, n - 3]
    F = flat(n, {t[0]: 0, t[1]: 0, t[2]: 0})
    out = {}
    for c in (4, 5, 6):
        if n - c < 1:
            continue
        low = list(range(c - 3))
        E = flat(n, {t[0]: 0, t[1]: 0, t[2]: 1, **{b: 0 for b in low}})
        Q = flat(n, {t[0]: 0, t[1]: 1, t[2]: 0, **{b: 0 for b in low}})
        out[f"fp{c}par"] = rep(n, F + E, Q)
        low2 = [b + 1 for b in low]
        Q2 = flat(n, {t[0]: 0, t[1]: 1, t[2]: 0, **{b: 0 for b in low2}})
        out[f"fp{c}skew"] = rep(n, F + E, Q2)
        Q3 = flat(n, {t[0]: 1, t[1]: 1, t[2]: 1, **{b: 0 for b in low}})
        out[f"fp{c}anti"] = rep(n, F + E, Q3)
        off = [x for x in range(N) if x not in set(F)]
        rng.shuffle(off)
        m = N >> c
        out[f"fp{c}rnd"] = rep(n, F + off[:m], off[m:2 * m])
        allp = list(range(N))
        rng.shuffle(allp)
        bs = N // 8 + m
        out[f"rnd{c}"] = rep(n, allp[:bs], allp[bs:bs + m])
    # type D: T built from flats, W = {x_top1 = x_top2 = 0}
    W = flat(n, {t[0]: 0, t[1]: 0})
    # T = two flats of codim 4, different directions, partly inside W
    T1 = flat(n, {t[0]: 1, t[1]: 0, t[2]: 0, 0: 0})
    T2 = flat(n, {t[0]: 0, t[1]: 1, t[2]: 0, 1: 0})
    # the two codim-4 flats are disjoint and of density 1/16 each
    out["D2out"] = rep(n, W, T1 + T2)
    T3 = flat(n, {t[0]: 0, t[1]: 0, t[2]: 0, 0: 0})
    out["D2half"] = rep(n, [x for x in W if x not in set(T3)], T1)
    T4 = flat(n, {t[0]: 1, t[2]: 0, 0: 0, 1: 0})
    T5 = flat(n, {t[0]: 1, t[2]: 1, 0: 0, 1: 1})
    TT = T4 + T5  # density 1/8: 2 flats of codim 4 inside the hyperplane x_top = 1
    out["Dhyp"] = rep(n, W, TT)
    A = [x for x in range(N) if not (x >> t[0] & 1)]  # hyperplane
    rng.shuffle(A)
    out["hyp"] = rep(n, W[:0] + F + [x for x in A if x not in set(F)][:N // 32], [x for x in range(N) if (x >> t[0] & 1)][:N // 32])
    # two half flats of different directions
    H1 = flat(n, {t[0]: 0, t[1]: 0, t[2]: 0, 0: 0})
    H2 = flat(n, {t[0]: 0, t[1]: 1, t[2]: 0, 1: 0})
    out["cut0"] = rep(n, H1 + H2, [])
    E = flat(n, {t[0]: 1, t[1]: 0, t[2]: 0, 0: 0, 1: 0})
    Q = flat(n, {t[0]: 1, t[1]: 1, t[2]: 0, 0: 1, 1: 1})
    out["cut5"] = rep(n, H1 + H2 + E, Q)
    return out

def extra_specs(n, seed):
    """Boolean comparators, small |P| on random and flat B+, and type D classes rho = 1_W - 1_T with T random."""
    rng = random.Random(seed + 1000)
    N = 1 << n
    t = [n - 1, n - 2, n - 3]
    F = flat(n, {t[0]: 0, t[1]: 0, t[2]: 0})
    out = {"flat": rep(n, F, [])}
    allp = list(range(N))
    rng.shuffle(allp)
    out["random"] = rep(n, allp[:N // 8], [])
    off = [x for x in allp if x not in set(F)]
    for e in (1, 2, 4, 8):
        if 2 * e >= N // 8:
            continue
        rng.shuffle(allp)
        out[f"rs{e}"] = rep(n, allp[:N // 8 + e], allp[N // 8 + e:N // 8 + 2 * e])
        rng.shuffle(off)
        out[f"fs{e}"] = rep(n, F + off[:e], off[e:2 * e])
    W = flat(n, {t[0]: 0, t[1]: 0})
    rng.shuffle(allp)
    out["Drnd"] = rep(n, W, allp[:N // 8])
    H = [x for x in range(N) if x >> t[0] & 1]
    rng.shuffle(H)
    out["Dh1"] = rep(n, W, H[:N // 8])
    # B+ = hyperplane-part structure: T in a hyperplane meeting W in half
    H2 = [x for x in range(N) if x >> t[1] & 1]
    rng.shuffle(H2)
    out["Dh1b"] = rep(n, W, H2[:N // 8])
    return out

def two_coset_specs(n):
    """flat F + E - P with P spread over several alternative cosets, so no alternative coset makes the representative Boolean."""
    N = 1 << n
    rng = random.Random(n * 7 + 1)
    out = {}
    F = [x for x in range(N) if x >> (n - 3) == 0]
    for e, cosets in ((2, (1, 2)), (4, (1, 2, 3, 4)), (8, (1, 2)), (16, (1, 2, 3, 4, 5, 6, 7))):
        if 2 * e >= N // 8:
            continue
        P = []
        for j in range(e):
            P.append(rng.choice([x for x in range(N) if x >> (n - 3) == cosets[j % len(cosets)] and x not in P]))
        off = [x for x in range(N) if x >> (n - 3) != 0 and x not in P]
        rng.shuffle(off)
        out[f"fsp{e}c{len(cosets)}"] = rep(n, F + off[:e], P)
    return out

if __name__ == "__main__":
    n = int(sys.argv[1])
    outdir = sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    for fam in (extra_specs(n, seed), specs(n, seed), two_coset_specs(n)):
        for name, r in fam.items():
            open(f"{outdir}/n{n}_{name}", "w").write(" ".join(map(str, r)))
            print(f"n{n}_{name}")
