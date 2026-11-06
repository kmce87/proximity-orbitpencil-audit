#!/usr/bin/env python3
"""N10: explicit upper bound on the members of ANY class of mass 5N/8 above 9N/16 with phi <= 2 (at most double roots), n = 21.  See LEDGER, Theory run 8.
All terms are upper bounds; floats are used only for bounds with a safety factor.  The identities used are checked exactly by n10_identities.py."""
from math import log, log2, exp

SAFE = 1.002

def gauss2(n, k):
    num = den = 1
    for i in range(k):
        num *= 2**(n - i) - 1
        den *= 2**(i + 1) - 1
    return num // den

def M_C(n):
    return 8 * gauss2(n, 2) * (2**(n - 2) - 1)

def Nplus(U, E0=7.0, cache={}):
    """sup #{Q subset T+ : sum_Q (1 - t) < U - 16 v} over v >= 0 and profiles with sum t^2 <= E0 + 64 v, t in [1/5, 1].
    Exponential moment: #Q <= exp(lam (U - 16 v)) prod (1 + exp(-lam (1 - t))), and prod <= exp(E max_t log(1 + exp(-lam(1-t)))/t^2)."""
    key = (round(U, 9), round(E0, 9))
    if key in cache:
        return cache[key]
    if U <= 0:
        return 1.0
    best = float("inf")
    tmin = max(0.2, 1 - U)
    for li in range(1, 400):
        lam = li * 0.05
        fmax = 0.0
        for k in range(0, 801):
            t = tmin + (1 - tmin) * k / 800
            fmax = max(fmax, log(1 + exp(-lam * (1 - t))) / (t * t))
        fmax *= 1.001  # grid margin
        # exponent is linear in v: lam (U - 16 v) + (E0 + 64 v) fmax; on 0 <= v <= U/16 take the larger end
        e0 = lam * U + E0 * fmax
        e1 = (E0 + 4 * U) * fmax  # v = U/16
        best = min(best, exp(max(e0, e1)))
    cache[key] = max(1.0, best * SAFE)
    return cache[key]

def abel_reps(Hbar, f, grid):
    """Upper bound of sum over reps of f(q(rep)), q in [grid[0], grid[-1]), when #reps with q < x is at most Hbar(x); f decreasing."""
    tot = Hbar(grid[-1]) * f(grid[-1])
    for a, b in zip(grid, grid[1:]):
        tot += Hbar(b) * (f(a) - f(b))
    return tot

def bound(n, verbose=True):
    N2 = 2.0 ** (2 * n)
    mc = M_C(n)
    terms = {}
    terms["main(<=8 reps)"] = 4.0 * mc  # 8 * M_C/2
    terms["main(1 rep)"] = mc / 2.0
    # j <= 2 small characters
    terms["j<=2"] = Nplus(4.0) + Nplus(3.2) * (2 + 2.0 ** (n + 1)) + Nplus(2.4) * 2.0 ** (n + 3)
    # j = 3: three odd (2/3) 2^(2n), or one even + two odd 2 * 2^(2n) with budget 2/5
    terms["j=3"] = Nplus(1.6) * (2.0 / 3) * N2 + Nplus(0.4) * 2 * N2
    # j = 4, zero sum, T_4 = 0 mod 4: both remaining products of the line are in T+
    Tplus = 1600 * (7 / 64 + 1 / 20)
    terms["K4a'"] = Nplus(0.8) * Tplus * Tplus / 2 * 2.0 ** (n + 2)
    # j = 4, zero sum, T_4 = 2 mod 4, reps with q >= 1/96: reps in a bin <= 1 + Nplus/3 (code of distance 4), 2-flats by Cauchy, 4 signs after the complement rule
    grid = [1 / 96]
    while grid[-1] < 1 / 40:
        grid.append(min(grid[-1] * 1.02, 1 / 40))
    Vmax = 7 / 64 + 2 / 40
    f = lambda q: Vmax / (q * q) * N2 / 6
    terms["K4a(ii)"] = abel_reps(lambda x: 1 + Nplus(32 * x) / 3, f, grid)
    # strict flat-like case: two reps with q < 2^-8; then 7 characters of rank 3 have t >= 7/8, so reps <= 8 * Nplus(U; E_rest), E_rest = 7 - 7 * 49/64
    Erest = 7 - 7 * 49 / 64
    K4a_S = abel_reps(lambda x: 8 * Nplus(32 * x, Erest), f, grid)
    # j = 4, xor nonzero (independent characters).  Every triple needs a product p with |hat(phi)(p)| >= (1/8 - s_triple)/4 >= 1/80, so p is in
    # R(s) = {|r| >= min(max((1/8 - s)/4, 1/80), 1/40)}, s = sum of the opposing |r_i|, budget for A+ below 8 s - 16 v.  Covers of the 4 triples up to S_4:
    # two disjoint edges (partition, sigma, sigma lambda' both in R: 2 free), triangle and edge + 2 marks (1 free, at most R^2 choices), path + mark, 4 marks (0 free).
    s0 = 1 / 40
    def Rsize(s, V):
        tau = min(max((1 / 8 - s) / 4, 1 / 80), 1 / 40)
        return V / (tau * tau)
    V0 = 7 / 64 + s0 / 2
    t_a0 = Nplus(8 * s0) * 3 * Rsize(s0, V0) * 2.0 ** (2 * n - 2) * 4  # 8 signs, each partition counted twice
    t_a1 = 0.0
    t_b = 0.0
    s = s0
    while s < 1 / 10:
        s2 = min(s * 1.05, 1 / 10)
        V = 7 / 64 + s2 / 2
        R = Rsize(s2, V)
        # two free parameters, but sum_4 r_i^2 >= s^2/4: at most V 2^n 4 / s^2 pairs of pairs per (partition, sigma) by Cauchy
        t_a1 += Nplus(8 * s2) * 3 * R * (V * 2.0 ** n * 4 / (s * s)) * 4
        s = s2
    Vm = 7 / 64 + 1 / 20
    Rm = Rsize(1 / 10, Vm)
    t_b = Nplus(0.8) * (2 * Rm * Rm * 2.0 ** n * 8 + 2 * Rm ** 3 * 8)
    # dependent: a line plus lambda'.  T_3 in {3,-1} is impossible (it needs sum_line eps r < -1/8), T_3 in {1,-3} forces two of the line characters into lambda' T+: 0 free.
    t_dep = Nplus(0.8) * Tplus * Tplus * 16
    terms["K4b"] = t_a0 + t_a1 + t_b + t_dep
    rest = sum(v for k, v in terms.items() if not k.startswith("main"))
    rest_S = rest - terms["K4a(ii)"] + K4a_S
    # general class: at most 1 rep with q < 2^-8, up to 7 more with q in [2^-8, 1/96), each with at most (V/q^2) 2^(2n)/6 quadrics
    main_G = mc / 2.0 + 7 * f(2.0**-8)
    if verbose:
        print(f"n={n} M_C/2 = 2^{log2(mc / 2):.3f}")
        for U in (0.2, 0.4, 0.5, 2 / 3, 0.8, 1.6, 2.4, 3.2, 4.0):
            print(f"   N+({U:.3f}) <= 2^{log2(Nplus(U)):.2f}")
        for k, v in terms.items():
            print(f"   {k:16s} 2^{log2(v):.3f}")
        print(f"   K4a(ii) strict flat-like 2^{log2(K4a_S):.3f}")
        print(f"   rest general     2^{log2(rest):.3f}, rest strict flat-like 2^{log2(rest_S):.3f}")
        print(f"   TOTAL strict flat-like class (8 reps): 2^{log2(4.0 * mc + rest_S):.3f}")
        print(f"   TOTAL every other class:               2^{log2(main_G + rest):.3f}")
    return max(4.0 * mc + rest_S, main_G + rest)

if __name__ == "__main__":
    for n in (21, 20):
        bound(n)
    assert bound(21, verbose=False) < 2.0**64
    print("bound(21) < 2^64: OK")
