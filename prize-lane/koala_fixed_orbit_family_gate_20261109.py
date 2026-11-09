#!/usr/bin/env python3
"""Source-grounded necessary-condition test for reusing the published OrbitPencil
116.13 upper attack at the proposed 116.12 index.

Source: zksecurity/proximity-prize-submissions-lean434,
submissions/reduction-upper/11613/{Solution,OrbitPencil}.lean.
Theorem T_card gives exactly 139775 agreements for every selected U;
winningSetDensity_gt_epsilon_window uses that exact size.
This checks only the existing fixed witness family, not all possible attacks.
"""
N = 262144
OLD_INDEX = 122369
NEW_INDEX = 122362
PUBLISHED_AGREEMENTS = 139775
assert N - OLD_INDEX == PUBLISHED_AGREEMENTS
assert N - NEW_INDEX == PUBLISHED_AGREEMENTS + 7
assert PUBLISHED_AGREEMENTS < N - NEW_INDEX
assert PUBLISHED_AGREEMENTS >= N - OLD_INDEX
# Source uses (1-delta)*N <= 139775, i.e. delta >= OLD_INDEX/N.
assert (N - NEW_INDEX) > PUBLISHED_AGREEMENTS
print('Existing OrbitPencil T_card:', PUBLISHED_AGREEMENTS)
print('Required agreements at 116.12 earliest index:', N - NEW_INDEX)
print('Shortfall of every published fixed T(U):', N - NEW_INDEX - PUBLISHED_AGREEMENTS)
print('Existing family cannot prove the new first radius via its T(U) witness.')
print('No statement about alternative witnesses, Lean kernel, or acceptance.')
