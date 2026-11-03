#!/usr/bin/env python3
"""Prize Lane B: exact dyadic-fibre key-budget falsification sweep.

Scope: the *unmodified* OrbitPencil rational-pencil template on the official
n=2^18 KoalaBear domain, varying C=2^h projected columns and R=n/C rows.
It assumes a common fixed (R-1)-point core, m complete selected columns,
equality of t top coefficients, and equality of the product residue mod C.
It tests only this SUFFICIENT pigeonhole construction, not all attacks.
No Lean certificate or official score improvement is asserted.
"""

from math import comb, log2, ceil

P = 2130706433
Q = P**6
B = Q // (2**128)  # any guaranteed B+1 distinct slopes beats density target
N = 2**18
K = 2**17
CURRENT_AGREEMENT = 139775


def key_budget(columns: int, chosen: int) -> dict:
    assert columns > 1 and N % columns == 0 and columns & (columns - 1) == 0
    rows = N // columns
    # Equal monic degree-m polynomials and t top coefficients yield
    # deg(V_U - V_W) <= m-t-1. Two roots (0, alpha) give
    # deg Q_U <= m-t-3. For c_U=R_core*Q_U(X^rows),
    # deg c_U <= (rows-1) + rows*(m-t-3) <= K-1.
    t = max(0, chosen - (K // rows) - 2)
    assert chosen >= 3 and 0 <= t <= chosen - 3
    degree_bound = rows - 1 + rows * (chosen - t - 3)
    assert degree_bound <= K - 1
    candidate_sets = comb(columns - 1, chosen)
    key_count = P**t * columns
    guaranteed_fibre = candidate_sets // key_count
    agreement = rows * (chosen + 1) - 1
    return {
        'columns': columns, 'rows': rows, 'chosen': chosen, 'top_constraints': t,
        'degree_bound': degree_bound, 'agreement': agreement,
        'unsafe_index': N - agreement,
        'candidate_sets': candidate_sets, 'key_count': key_count,
        'guaranteed_fibre': guaranteed_fibre,
        'sufficient_pigeonhole_pass': candidate_sets > B * key_count,
        'pigeonhole_deficit_bits': log2(candidate_sets) - log2(B) - log2(key_count),
        # Diagnostic score, not proof of ProtocolClaimUpper.
        'indicative_centi_bits': ceil((-128*log2(agreement/N))*100 - 1e-10),
    }


def first_strictly_better(columns: int) -> dict:
    rows = N // columns
    # Agreement = rows*(m+1)-1 > CURRENT_AGREEMENT iff
    # m >= floor((CURRENT_AGREEMENT+1)/rows).
    m = (CURRENT_AGREEMENT + 1) // rows
    assert rows*(m+1)-1 > CURRENT_AGREEMENT
    assert m == 0 or rows*m-1 <= CURRENT_AGREEMENT
    assert 3 <= m < columns
    # At m >= columns/2, binomial(columns-1,m) is non-increasing,
    # while t=max(0,m-columns/2-2) is non-decreasing. Therefore, if
    # the first better case fails, all larger m fail for this template.
    assert m >= columns//2
    return key_budget(columns, m)


def main():
    assert B == 274980728111395087
    old = key_budget(512, 272)
    assert old['agreement'] == CURRENT_AGREEMENT
    assert old['sufficient_pigeonhole_pass']
    print('Official benchmark n=262144, k=131072; current attack agreement=139775')
    print('Exact sufficient bad-slope target: B+1=', B+1)
    print('columns  rows  m   t  agreement  centibits  budget-margin  pass')
    tested = []
    for h in range(3, 15):
        columns = 2**h
        r = first_strictly_better(columns)
        tested.append(r)
        print(f"{columns:7d} {r['rows']:5d} {r['chosen']:4d} {r['top_constraints']:3d} "
              f"{r['agreement']:10d} {r['indicative_centi_bits']:10d} "
              f"{r['pigeonhole_deficit_bits']:+13.4f} "
              f"{'YES' if r['sufficient_pigeonhole_pass'] else 'NO'}")
    assert all(not r['sufficient_pigeonhole_pass'] for r in tested)
    closest = max(tested, key=lambda r: r['pigeonhole_deficit_bits'])
    assert closest['columns'] == 256 and closest['chosen'] == 136
    assert closest['top_constraints'] == 6
    assert closest['agreement'] == 140287
    assert closest['indicative_centi_bits'] == 11546
    assert closest['guaranteed_fibre'] < B+1
    # A hypothetical effective product-residue key with <=63 values
    # would cross the cardinal threshold. Not proven to exist!
    max_residue_classes = (closest['candidate_sets'] - 1) // (P**6 * B)
    assert max_residue_classes == 63
    print('\nPASS (negative): no dyadic projection with 8..16384 columns beats '
          'current agreement using the unchanged exact-key pigeonhole test.')
    print('Closest failed improvement: 256 columns, 136 selected, '
          f"margin {closest['pigeonhole_deficit_bits']:+.6f} bits.")
    print('For this geometry an effective product-key with <=63 classes '
          'instead of 256 would meet the counting test. UNPROVED.')


if __name__ == '__main__':
    main()
