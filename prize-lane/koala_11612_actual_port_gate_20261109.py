#!/usr/bin/env python3
"""Exact score feasibility of changing the published Lean-4.34 Koala upper
ProtocolClaimUpper 11613 122369 to 11612 at its existing index.

Source: https://github.com/zksecurity/proximity-prize-submissions-lean434
No claim about unsafeAbove, Lean compilation, or verifier acceptance.
"""
N = 1 << 18
T = 128 * 100
EXISTING_INDEX = 122369

def passes(centibits, index):
    assert 0 < index < N // 2
    return (1 << centibits) * pow(N-index, T) >= pow(N, T)

def max_feasible_index(centibits):
    low, high = 1, N // 2 - 1
    while low < high:
        mid = (low + high + 1) // 2
        if passes(centibits, mid):
            low = mid
        else:
            high = mid - 1
    return low

if __name__ == '__main__':
    assert passes(11613, EXISTING_INDEX)
    assert not passes(11612, EXISTING_INDEX)
    cutoff = max_feasible_index(11612)
    assert cutoff == 122362
    assert passes(11612, cutoff) and not passes(11612, cutoff+1)
    assert EXISTING_INDEX - cutoff == 7
    print('Published Lean 4.34 port: ProtocolClaimUpper 11613 122369')
    print('116.13 score at actual index: PASS')
    print('116.12 score at actual index: FAIL')
    print('116.12 score maximum index:', cutoff)
    print('Necessary expansion of unsafe suffix:', EXISTING_INDEX-cutoff, 'grid points')
    print('First newly required radius:', f'{cutoff}/{N}')
    print('No winning-set proof or independently accepted improvement')
