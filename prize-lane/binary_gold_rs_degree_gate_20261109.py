#!/usr/bin/env python3
"""Lane B: falsify direct embedding of the 75%-zero Gold Boolean function
as a nonzero protected binary RS row codeword. Exact integer gate.

Assumption: protected binary RS row dimension k=2^20, with distinct
field evaluation points. A nonzero polynomial of degree < k has at
most k-1 distinct roots. Prior numerical witness: a=4 Gold Boolean
function has exactly 3*2^19 zero positions and 2^19 nonzero positions.
This does NOT rule out use as a received word or a different IRS attack.
"""
N = 1 << 21
K = 1 << 20
GOLD_ZEROS = 3 << 19
GOLD_NONZEROS = N - GOLD_ZEROS
MAX_NONZERO_CODEWORD_ZEROS = K - 1
CLAIM_UPPER_INDEX = 917378
assert GOLD_ZEROS == 1572864
assert GOLD_NONZEROS == 524288 > 0
assert GOLD_ZEROS > MAX_NONZERO_CODEWORD_ZEROS
assert N - CLAIM_UPPER_INDEX == 1179774
# Distances to zero row codeword; auxiliary, not a winning-set proof.
assert GOLD_NONZEROS < CLAIM_UPPER_INDEX
print('n', N, 'row dimension', K)
print('Gold zeros', GOLD_ZEROS, 'nonzeros', GOLD_NONZEROS)
print('maximum zeros for nonzero RS row codeword', MAX_NONZERO_CODEWORD_ZEROS)
print('excess roots', GOLD_ZEROS - MAX_NONZERO_CODEWORD_ZEROS)
print('direct RS-row embedding: IMPOSSIBLE by polynomial root bound')
print('received-word and full IRS winning-set constructions: UNRESOLVED')
