#!/usr/bin/env python3
"""
Independent toy-field replay for N2 (no shared code with n2_kappa.cpp).

Toy model of BitWonka's family (PR #592): K = GF(2^16), label space of dim n = 8
(y = 4 bits, z = 4 bits), W = {z = 0}, D = 2^(n-1) = 128, |S| = 9/16 * 2^n = 144, f = 2,
toy domain of dim 10, k = 2^9.  Checks:
 (a) C_S = V_S - L_W^3 X^96 has degree <= 128, top coefficient = kappa formula, next degree 120
 (b) a(Y + <w>) = a(Y)^2 + L_Y(w)
 (c) a_top is injective on the hyperplanes of a fixed W_t, and a^2 = A(W_t) + c_U
 (d) two members with equal kappa plus a fixed label set T of size 2^(n-5) keep a common top
 (e) a member with two flats over one half-space + one flat over a plane (shape "AAB") has the same top
 (f) end-to-end pencil replay: f1 + C_S(alpha) f2 agrees with a degree < k polynomial on
     exactly (2^f - 1) + 2^f |S| domain points, for both shapes
"""
import itertools, random

POLY, MB = 0x1002B, 16
EXP, LOG = [0] * (2 * (2**MB)), [0] * (2**MB)
def rawmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        b >>= 1; a <<= 1
        if a >> MB: a ^= POLY
    return r
def rawpow(a, e):
    r = 1
    while e:
        if e & 1: r = rawmul(r, a)
        a = rawmul(a, a); e >>= 1
    return r
GEN = next(g for g in range(2, 2**MB) if all(rawpow(g, (2**MB - 1) // p) != 1 for p in (3, 5, 17, 257)))
x = 1
for i in range(2**MB - 1):
    EXP[i] = x; LOG[x] = i
    x = rawmul(x, GEN)
assert x == 1 and len(set(EXP[:2**MB - 1])) == 2**MB - 1
for i in range(2**MB - 1, 2 * (2**MB)): EXP[i] = EXP[i - (2**MB - 1)]
def mul(a, b): return 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]
def inv(a): return EXP[(2**MB - 1) - LOG[a]]
def pmul(A, B):
    R = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a:
            la = LOG[a]
            for j, b in enumerate(B):
                if b: R[i + j] ^= EXP[la + LOG[b]]
    return R
def padd(A, B):
    R = [0] * max(len(A), len(B))
    for i, a in enumerate(A): R[i] ^= a
    for i, b in enumerate(B): R[i] ^= b
    return R
def deg(P):
    d = len(P) - 1
    while d >= 0 and P[d] == 0: d -= 1
    return d
def peval(P, v):
    r = 0
    for c in reversed(P): r = mul(r, v) ^ c
    return r
def locator(pts):
    P = [1]
    for v in pts:
        Q = [0] * (len(P) + 1)
        for i, c in enumerate(P):
            Q[i + 1] ^= c; Q[i] ^= mul(c, v)
        P = Q
    return P
def span(B):
    S = [0]
    for b in B: S += [s ^ b for s in S]
    return S
def subspace_poly(B):
    pts = span(B); assert len(set(pts)) == len(pts)
    return locator(pts)

rng = random.Random(20261103)
while True:
    dom_basis = rng.sample(range(1, 2**MB), 10)
    if len(set(span(dom_basis))) == 2**10: break
Zb, rest = dom_basis[:2], dom_basis[2:]
LZ = subspace_poly(Zb)
ell = [peval(LZ, b) for b in rest]                 # 8 label basis vectors (y0..y3, z0..z3)
assert len(set(span(ell))) == 2**8
n, ny, D = 8, 4, 128
def lab(v):
    r = 0
    for i in range(n):
        if v >> i & 1: r ^= ell[i]
    return r
def par(x): return bin(x).count('1') & 1
LW = subspace_poly(ell[:ny])
def top():                                          # L_W^3 X^96
    T = pmul(pmul(LW, LW), LW)
    return [0] * 96 + T
TOP = top()
ZM = lambda s: s << ny                               # z-functional as a mask on v
def make_flat(eqs):                                  # eqs = list of (mask, value)
    return {v for v in range(2**n) if all(par(v & m) == b for m, b in eqs)}
def direction_coeff(F):                              # coefficient of X^(|F|/2) in the locator of a flat
    L = locator(sorted(lab(v) for v in F))
    return L[len(F) // 2], L

# ------------------------------------ an AAA member (row: s0 + s1 + s2 = 0, kappa = (1, 0, 0))
s0, s1, s2 = 8, 15, 7                                # first row of BitWonka's table: Q = {1, 2, 4}, v3 = 7
Q = [1, 2, 4]
def aaa_member(r, m, beta, a, e, nus, bs):
    coefL, rhoC = [0, e, e ^ 1], [a, a ^ 1 ^ e, a ^ e]
    ss, kap = [s0, s1, s2], [1, 0, 0]
    flats = []
    for t in range(3):
        rho_mask = r | ZM(beta ^ (s0 if coefL[t] else 0))
        flats.append(make_flat([(ZM(ss[t]), kap[t]), (rho_mask, rhoC[t]), (m[t] | ZM(nus[t]), bs[t])]))
    return flats
def as_member(flats, Qz):
    S = set()
    for z in Qz: S |= {y | z << ny for y in range(2**ny)}
    tot = len(S)
    for F in flats:
        assert not (S & F), "overlap"
        S |= F; tot += len(F)
    assert len(S) == tot == 144
    return S
flatsA = aaa_member(r=0b0001, m=[0b0010, 0b0100, 0b1000], beta=0b0010, a=0, e=0, nus=[0, 0, 0], bs=[0, 0, 1])
SA = as_member(flatsA, Q)
VA = locator([lab(v) for v in sorted(SA)])
CA = padd(VA, TOP)
LWz = lambda z: peval(LW, lab(z << ny))
kap_formula = LWz(Q[0]) ^ LWz(Q[1]) ^ LWz(Q[2])
for F in flatsA: kap_formula ^= direction_coeff(F)[0]
d0 = deg(CA); CA2 = CA[:]; CA2[d0] = 0
print(f"(a) deg C_S = {d0} (D = {D}), kappa direct = {CA[D]}, formula = {kap_formula}, next degree = {deg(CA2)}")
assert d0 == D and CA[D] == kap_formula and deg(CA2) == D - 2**(n - 5)

# ------------------------------------ (b) a(Y + <w>) = a(Y)^2 + L_Y(w)
okb = True
for _ in range(50):
    k = rng.randint(2, 5)
    B = rng.sample([lab(v) for v in range(1, 2**n)], k + 1)
    if len(set(span(B))) != 2**(k + 1): continue
    LY, LU = subspace_poly(B[:k]), subspace_poly(B)
    okb &= LU[2**k] == (mul(LY[2**(k - 1)], LY[2**(k - 1)]) ^ peval(LY, B[k]))
print("(b) a(Y+<w>) = a(Y)^2 + L_Y(w):", okb); assert okb

# ------------------------------------ (c) hyperplanes of a fixed W_t
Wt = make_flat([(ZM(s0), 0), (0b0001 | ZM(0b0010), 0)])
Wtb = []
for v in sorted(Wt):
    if v and v not in set(sum([[u ^ w for u in [0]] for w in []], [])):
        if lab(v) not in span([lab(b) for b in Wtb]): Wtb.append(v)
assert len(Wtb) == 6
LWt = subspace_poly([lab(b) for b in Wtb])
vals, okc = {}, True
for code in range(1, 2**6):
    piv = next(i for i in range(6) if code >> i & 1)
    ker = [Wtb[i] ^ (Wtb[piv] if code >> i & 1 else 0) for i in range(6) if i != piv]
    LU = subspace_poly([lab(b) for b in ker])
    a, c = LU[16], peval(LU, lab(Wtb[piv]))
    okc &= mul(a, a) == (LWt[32] ^ c)
    vals[a] = vals.get(a, 0) + 1
print(f"(c) hyperplanes of W_t: 63, distinct a = {len(vals)}, identity ok = {okc}"); assert okc and len(vals) == 63

# ------------------------------------ (d) equal kappa + fixed T keeps a common top (toy K has only 16 bits)
hole = 7                                             # v3: no member of this row touches z = 7
T = [lab(y | hole << ny) for y in range(2**(n - 5))]
VT = locator(T)
seen, pair = {}, None
for trial in range(400000):
    r = rng.randrange(1, 16); pv = (r & -r)
    ms = [rng.randrange(1, 16) for _ in range(3)]
    ms = [(mm & ~pv) for mm in ms]
    if 0 in ms or len({ms[0], ms[1], ms[2]}) < 3: continue
    a, e, beta = rng.randrange(2), rng.randrange(2), rng.randrange(16)
    nus = [rng.randrange(16) for _ in range(3)]; bs = [rng.randrange(2) for _ in range(3)]
    fl = aaa_member(r, ms, beta, a, e, nus, bs)
    if any(len(F) != 32 for F in fl) or fl[0] & fl[1] or fl[0] & fl[2] or fl[1] & fl[2]: continue
    k = kap_formula_val = LWz(Q[0]) ^ LWz(Q[1]) ^ LWz(Q[2])
    key = tuple(sorted(tuple(direction_coeff(F)[1][1:]) for F in fl))   # directions only: pairs differing by a translation do not count
    for F in fl: k ^= direction_coeff(F)[0]
    if k in seen and seen[k][0] != key: pair = (seen[k][1], fl, k); break
    seen.setdefault(k, (key, fl))
assert pair, "no kappa collision found in the toy"
S1, S2 = as_member(pair[0], Q), as_member(pair[1], Q)
V1, V2 = locator([lab(v) for v in sorted(S1)]), locator([lab(v) for v in sorted(S2)])
dd = deg(padd(pmul(V1, VT), pmul(V2, VT)))
print(f"(d) equal kappa = {pair[2]} after {len(seen)} distinct kappas: deg(V1 V_T - V2 V_T) = {dd} <= {D}, |S|+|T| = {144 + len(T)}")
assert dd <= D

# ------------------------------------ (e) shape AAB: F0, F1 over one half-space, B-flat over a plane in the complement
H = (8, 1)                                           # half-space s.z = 1 with s = 8: z in {8..15}; the complement is z in {0..7}
PlaneB = [(ZM(1), 0), (ZM(2), 0)]                    # z in {0, 4} + ... plane inside z3 = 0 below
def aab_member(r, m0, m1, beta, c0, nu0, nu1, b0, b1, g, nu2, b2):
    F0 = make_flat([(ZM(8), 1), (r | ZM(beta), c0), (m0 | ZM(nu0), b0)])
    F1 = make_flat([(ZM(8), 1), (r | ZM(beta), c0 ^ 1), (m1 | ZM(nu1), b1)])
    F2 = make_flat([(ZM(8), 0), (ZM(1), 1), (g | ZM(nu2), b2)])          # plane z3 = 0, z0 = 1: z in {1, 3, 5, 7}
    return [F0, F1, F2]
QB = [2, 4, 6]                                        # in the complement {0,...,7} minus the plane {1,3,5,7}; hole z = 0
flatsB = aab_member(0b0001, 0b0010, 0b0100, 0b0010, 0, 0b0001, 0b0010, 1, 0, 0b1001, 0b0010, 1)
SB = as_member(flatsB, QB)
VB = locator([lab(v) for v in sorted(SB)])
CB = padd(VB, TOP)
print(f"(e) AAB member: |S| = {len(SB)}, deg(V_S - L_W^3 X^96) = {deg(CB)} <= {D}; same top as AAA: deg(VA - VB) = {deg(padd(VA, VB))}")
assert deg(CB) <= D and deg(padd(VA, VB)) <= D

# ------------------------------------ (f) end-to-end pencil replay on the toy domain
dom = span(dom_basis)
def replay(S, name):
    ynodes = {x: peval(LZ, x) for x in dom}
    labels = set(ynodes.values())
    alpha = next(a for a in range(1, 2**MB) if a not in labels)
    assert lab(0) == 0 and 0 not in S
    R = locator([z for z in span(Zb) if z != 0])    # 3-point core: the fibre of label 0 without the word 0
    Rt = TOP
    C = padd(locator([lab(v) for v in sorted(S)]), Rt)
    gamma = peval(C, alpha)
    agree = []
    # Q_S = (C_S - gamma) / (Y - alpha) by synthetic division over K
    N = [c for c in C]; N[0] ^= gamma
    Qs = [0] * deg(N); carry = 0
    for i in range(deg(N), 0, -1):
        carry = N[i] ^ mul(carry, alpha); Qs[i - 1] = carry
    assert (N[0] ^ mul(carry, alpha)) == 0
    for x_ in dom:
        y = ynodes[x_]; den = inv(y ^ alpha); rv = peval(R, x_)
        f2 = mul(rv, den); f1 = mul(mul(rv, peval(Rt, y)), den)
        lhs = f1 ^ mul(gamma, f2)
        rhs = mul(rv, peval(Qs, y))                  # the degree < 2^9 codeword R(x) Q_S(Y(x)) (sign is trivial in char 2)
        if lhs == rhs: agree.append(x_)
    deg_code = 3 + 4 * (len(Qs) - 1)
    print(f"(f) {name}: agreement = {len(agree)} = 3 + 4*|S| = {3 + 4 * len(S)}?, codeword degree <= {deg_code} < 512")
    assert len(agree) == 3 + 4 * len(S) and deg_code < 512
replay(SA, "AAA"); replay(SB, "AAB")
print("all toy checks passed")
