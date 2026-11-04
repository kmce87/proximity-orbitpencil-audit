#!/usr/bin/env python3
"""Exact score-only boundary; source 64.00 candidate is NOT verified acceptance."""
N=1073741824
P=314458111
T=6400
rhs=N**12800
def valid(p):
    return (1 << T)*pow(N-p,12800) <= rhs
lo,hi=0,N
while lo+1<hi:
    mid=(lo+hi)//2
    if valid(mid): hi=mid
    else: lo=mid
assert valid(hi) and not valid(hi-1)
assert hi>P
print('source_candidate_bits=63.99')
print('source_candidate_radius=',P,'/',N,sep='')
print('64.00_min_numerator=',hi,sep='')
print('extra_numerator_units=',hi-P,sep='')
print('source_radius_passes_64.00=',valid(P),sep='')
SOURCE_P=78622925
SOURCE_Q=268435456
assert SOURCE_P*4==hi and SOURCE_Q*4==N
print('current_source_candidate_bits=64.00')
print('current_source_radius=',SOURCE_P,'/',SOURCE_Q,sep='')
print('source_matches_exact_minimum=True')
