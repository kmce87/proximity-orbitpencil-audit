#!/usr/bin/env python3
"""Necessary agreement-set turnover for a distinct Koala RS polynomial.
Combinatorial obstruction only; not an attack or Lean proof.
"""
N = 1 << 18
K = 1 << 17
OLD_UNSAFE = 122369
NEW_UNSAFE = 122362
old_agreements = N - OLD_UNSAFE
new_agreements = N - NEW_UNSAFE
max_common = K - 1
min_lost = old_agreements - max_common
min_gained = new_agreements - max_common
assert (old_agreements, new_agreements) == (139775, 139782)
assert (min_lost, min_gained) == (8704, 8711)
assert old_agreements - (min_lost - 1) == K
assert old_agreements - min_lost == K - 1
print(f'Koala n={N}, dimension={K}; old={old_agreements}, target={new_agreements}')
print(f'Distinct polynomial maximum shared old agreements: {max_common}')
print(f'Minimum old agreements sacrificed: {min_lost}')
print(f'Minimum new agreements outside old set: {min_gained}')
print('PASS: necessary conditions only; no existence or density claim')
