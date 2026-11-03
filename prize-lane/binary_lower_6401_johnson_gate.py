#!/usr/bin/env python3
"""Exact arithmetic, not a Lean proof: binary lower 64.01 and Johnson barrier.
Sources: official BinaryTargetLower, P64List, P64Final at proximity-prize/proximity-prize.
"""
from fractions import Fraction
from math import isqrt

N,K=2**21,2**20
D=K-1 # official Johnson helper uses 1_048_575
OLD_RADIUS=Fraction(78622925,2**28)

def score_ok(a,b):
    """Exact test for ((a/N)^128 <= 2^(-b/100))."""
    return a.numerator**12800 * 2**b <= (a.denominator*N)**12800

def ceil_fraction(a):
    return (a.numerator+a.denominator-1)//a.denominator

def johnson_denom(a):
    return a*a-N*D

def main():
    old_a=(1-OLD_RADIUS)*N
    assert old_a==Fraction(189812531,128)
    old_t=ceil_fraction(old_a)
    assert old_t==1482911 and score_ok(old_a,6400) and not score_ok(old_a,6401)
    grid_a=1482830
    assert score_ok(Fraction(grid_a),6401)
    assert not score_ok(Fraction(grid_a+1),6401)
    # Rational radii are allowed; gain one agreement point over grid ceiling.
    new_a=Fraction(16*grid_a+1,16)
    new_radius=1-new_a/N
    assert new_radius==Fraction(9829151,33554432)
    assert score_ok(new_a,6401)
    assert not score_ok(Fraction(16*grid_a+2,16),6401)
    new_t=ceil_fraction(new_a)
    assert new_t==1482831 and old_t-new_t==80
    johnson_min=isqrt(N*D)+1
    assert johnson_min==1482910
    assert johnson_denom(johnson_min)>0
    assert johnson_denom(johnson_min-1)<=0
    assert johnson_denom(old_t)==3875521
    assert johnson_denom(new_t)==-233383839
    assert N*(old_t-D)//johnson_denom(old_t)==235031
    assert N*(johnson_min-D)//johnson_denom(johnson_min)==1001282
    print(f'Old radius {OLD_RADIUS}: agreement >= {old_t}, Johnson denominator {johnson_denom(old_t)}')
    print(f'64.01 radius {new_radius}: agreement >= {new_t}, Johnson denominator {johnson_denom(new_t)}')
    print(f'Integer/grid-aligned 64.01 maximum agreement: {grid_a}')
    print(f'Minimum agreement for positive Johnson denominator: {johnson_min}')
    print('PASS: exact arithmetic; 80-position gap.')
    print('NEGATIVE: existing Johnson list theorem not reusable at 64.01; new beyond-Johnson argument needed.')
    print('Prize-qualifying Lean certificate: NO')

if __name__=='__main__': main()
