#!/usr/bin/env python3
"""Lane B: exact necessary cardinality gate for a Koala 116.12-bit candidate.

Hypothesis: injectivity alone rules out selecting >2^59 distinct gamma_U
inside the quadratic subfield F_(q^2), q = 2^31-2^24+1.
Result: falsified. There is room even for the earlier 273-fibre
14-key counting lower bound, though existence is NOT established.

This is arithmetic only, not Lean, a construction, or a prize submission.
Official source: ProximityPrize/SubmissionUpper/OrbitPencil.lean,
ProximityPrize/Benchmark/TargetUpper.lean at official main
 eb82d3bf04a9c876c7ef9c3e6de4640fb85062f2.
"""
q = 2**31 - 2**24 + 1
needed = 2**59 + 1
# Prior lane B 273-fibre 14-key class size (exact counting lower bound).
family_lower_bound = 3_509_925_131_112_143_307
assert q < needed
assert needed < family_lower_bound
assert family_lower_bound < q**2
assert q**2 < q**6
# A purely injective map from a set of this size into F_(q^2) is
# cardinally possible; no claim is made that actual gamma_U does so.
print('q=',q)
print('required=',needed)
print('273_fibre_14_key_lower_bound=',family_lower_bound)
print('q_squared=',q**2)
print('capacity_slack=',q**2-family_lower_bound)
print('cardinality_only_obstruction_to_q2=NO')
print('third_root_constructed=NO')
print('lean_kernel_checked=NO')
print('independent_acceptance=NO')
