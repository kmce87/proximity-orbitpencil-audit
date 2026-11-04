#!/usr/bin/env python3
"""Exact 64.01-bit binary lower score gate; NOT an extractor-error proof."""
Q = 268435456
BASE = 78622925

def valid(bits, p):
    return (1 << bits) * (Q-p)**12800 <= Q**12800

def minimum(bits):
    lo, hi = 0, Q
    while lo < hi:
        mid = (lo+hi)//2
        if valid(bits, mid): hi = mid
        else: lo = mid+1
    assert valid(bits, lo) and not valid(bits, lo-1)
    return lo

if __name__ == "__main__":
    assert minimum(6400) == BASE
    p = minimum(6401)
    assert p == 78633204
    assert not valid(6401, BASE)
    print("64.01 minimum:", p, "/", Q)
    print("increment:", p-BASE)
