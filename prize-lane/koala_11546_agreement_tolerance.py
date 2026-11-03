#!/usr/bin/env python3
"""Lane B: exact 115.46-bit agreement tolerance for hypothetical Koala upper.

Hypothesis: dropping six of the 140287 proposed agreement positions
still permits a 115.46-bit upper score. This is a necessary score gate only.
"""
N = 1 << 18
B = 11546

def passes(agreement: int) -> bool:
    assert 0 <= agreement <= N
    # i=N-agreement; 2^(-B/100) <= (agreement/N)^128.
    return N**12800 <= (1 << B) * agreement**12800

lo, hi = 1, N
while lo < hi:
    mid = (lo + hi) // 2
    if passes(mid):
        hi = mid
    else:
        lo = mid + 1
minimum_agreement = lo
assert minimum_agreement == 140282
assert not passes(140281)
assert passes(140282)
assert passes(140287)
assert not passes(140287 - 6)
assert passes(140287 - 5)
print('Minimum agreement for 115.46:', minimum_agreement)
print('Maximum unsafe index:', N - minimum_agreement)
print('Full proposed agreement:', 273*512+511)
print('Allowed lost positions:', 273*512+511-minimum_agreement)
print('Hypothesis (six losses permitted): FALSIFIED')
print('No actual construction, Lean kernel check, or verifier acceptance.')
