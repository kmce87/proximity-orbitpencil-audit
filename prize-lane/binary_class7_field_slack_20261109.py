#!/usr/bin/env python3
"""Falsify field-size bottleneck in published binary 64.00 class-7 proof.
Source: proximity-prize/proximity-prize/main/
ProximityPrize/SubmissionBinaryLower/P64C7High.lean
Only a necessary side condition; NOT a 64.01 proof or verifier submission.
"""
field_size = 2**192
max_nat_degree = 352552
max_weighted_degree = 369677849011
lhs = 2 * max_nat_degree * max_weighted_degree
assert lhs < field_size
assert field_size // lhs > 10**40
print('field_size =', field_size)
print('maximum side-condition LHS =', lhs)
print('integer slack factor =', field_size // lhs)
print('PASS: field-size inequality has > 10^40 slack; not a tight bottleneck.')
print('NO conclusion about extractor error or ProtocolClaim 6401.')
