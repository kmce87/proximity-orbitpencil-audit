#!/usr/bin/env python3
"""Lane B: exact density threshold, correcting the prior 2^59 shortcut.

Hypothesis: 273-fibre candidate pigeonhole counting can afford >6
auxiliary classes while satisfying the exact strict density requirement.

This is CONDITIONAL arithmetic: the fibre construction, third-root key,
slope distinctness, and complete unsafe-suffix theorem are NOT proved.
"""
from math import comb

q = (1 << 31) - (1 << 24) + 1
field_size = q**6
candidate_count = comb(511, 273)
denominator = q**14 * 512

def exact_density_passes(classes: int) -> bool:
    # ceil(candidate_count/(classes*denominator)) guaranteed slopes.
    guaranteed = (candidate_count + classes*denominator - 1) // (classes*denominator)
    return guaranteed * (1 << 128) > field_size

def shortcut_passes(classes: int) -> bool:
    guaranteed = (candidate_count + classes*denominator - 1) // (classes*denominator)
    return guaranteed > (1 << 59)

assert shortcut_passes(6)
assert not shortcut_passes(7)
assert exact_density_passes(12)
assert not exact_density_passes(13)
assert all(exact_density_passes(k) for k in range(1, 13))
assert all(not exact_density_passes(k) for k in range(13, 20))
for classes in (6, 7, 8, 12, 13):
    guaranteed = (candidate_count + classes*denominator - 1) // (classes*denominator)
    print(f'classes={classes} guaranteed_slopes={guaranteed} '
          f'strict_density={exact_density_passes(classes)} '
          f'old_2^59_shortcut={shortcut_passes(classes)}')
print('MAX AUXILIARY CLASSES UNDER COUNTING ASSUMPTIONS: 12')
print('No actual Koala construction, Lean kernel proof or verifier acceptance.')
