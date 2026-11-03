#!/usr/bin/env python3
"""Exact Koala score gate for HYPOTHETICAL 273-fibre agreement.

This is NOT an attack, unsafe-suffix proof, Lean certificate or accepted score.
"""
N = 1 << 18
AGREEMENT = 273 * 512 + 511
INDEX = N - AGREEMENT

def score_gate(B: int, index: int = INDEX) -> bool:
    """Exact: 2^(-B/100) <= (1-index/N)^128."""
    assert 0 < index <= N
    return N**12800 <= (N-index)**12800 * (1 << B)

assert AGREEMENT == 140287
assert INDEX == 121857
assert not score_gate(11545)
assert score_gate(11546)
assert score_gate(11612)
assert not score_gate(11612, 122369)
assert score_gate(11613, 122369)
print(f"hypothetical agreement={AGREEMENT}, unsafe index={INDEX}")
print("115.45 fails; 115.46 passes; 116.12 passes")
print("Historical index 122369: 116.12 fails, 116.13 passes")
print("Numerical gate ONLY: no construction, Lean proof or acceptance.")
