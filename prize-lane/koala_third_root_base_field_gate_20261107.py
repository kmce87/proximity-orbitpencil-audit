#!/usr/bin/env python3
"""Lane B: cardinality obstruction to a uniform third Koala pencil root in K.

Official source: ProximityPrize/SubmissionUpper/OrbitPencil.lean.
K = KoalaBear.Field, |K| = 2^31 - 2^24 + 1.
Selected set Sel has NN = 2^59 + 1 members.
deltaV(U) is a polynomial over FF whose coefficients come from K.
gamma(U) = deltaV(U).eval(alpha)/alpha.
pencil(U) = deltaV(U) - C(gamma(U))*X.
Official lemma gamma_injective makes U -> gamma(U) injective on Sel.

Suppose beta in K is nonzero and pencil(U)(beta)=0 for every U in Sel.
Then gamma(U) = deltaV(U)(beta)/beta belongs to K, because deltaV(U)
has coefficients in K. By gamma_injective, |Sel| <= |K|, contradiction.
This is a mathematical deduction using the cited official lemmas,
not a new Lean kernel certificate. It does not exclude beta in FF\K.
"""
K = 2**31 - 2**24 + 1
NN = 2**59 + 1
assert K == 2130706433
assert NN == 576460752303423489
assert NN > K
print("K_card =", K)
print("Sel_card =", NN)
print("Uniform nonzero third root beta in K: IMPOSSIBLE for official injective gamma")
print("Uniform third root beta in FF outside K: UNRESOLVED")
