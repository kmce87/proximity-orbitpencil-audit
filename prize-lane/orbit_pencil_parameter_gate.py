#!/usr/bin/env python3
"""Fail-fast arithmetic gate for the accepted OrbitPencil parameter family.

This is NOT a proof of any Proximity Prize ProtocolClaimUpper.
The gate tests the sufficient same-key pigeonhole condition of the
original 512-fibre construction, not all possible refinements.
"""
from math import comb, log2, ceil

P = 2130706433
N = 262144
ROW_DIM = 131072
FIBRE = 512
CORE = 511
OUTER = 511
SLOPES = 1 << 59


def row(m: int) -> dict:
    # Degree(V_U - V_W) <= m - t - 1 after equating t top
    # coefficients below the common monic term. Removing roots 0 and
    # alpha gives degree(Q_U) <= m - t - 3.
    top_constraints = max(0, m - 258)
    assert CORE + FIBRE * (m - top_constraints - 3) <= ROW_DIM - 1
    available_sets = comb(OUTER, m)
    key_count = P**top_constraints * FIBRE
    required = key_count * SLOPES
    agreement = CORE + FIBRE*m
    unsafe_index = N - agreement
    exact_pass = available_sets > required
    margin_bits = log2(available_sets) - log2(required)
    theoretical_bits = -128 * log2(agreement / N)
    return dict(m=m, top_constraints=top_constraints,
                agreement=agreement, unsafe_index=unsafe_index,
                keys=key_count, candidates=available_sets,
                exact_pigeonhole_pass=exact_pass,
                margin_bits=margin_bits,
                indicative_bits=theoretical_bits,
                indicative_centiBits=ceil(theoretical_bits*100 - 1e-10))


if __name__ == '__main__':
    for m in range(270, 275):
        d=row(m)
        print('m={m} t={top_constraints} a={agreement} unsafe_index={unsafe_index} '
              'pigeonhole={exact_pigeonhole_pass} margin_bits={margin_bits:+.6f} '
              'indicative_score={indicative_centiBits}/100'.format(**d))
    assert row(272)['exact_pigeonhole_pass'] is True
    assert row(273)['exact_pigeonhole_pass'] is False
    assert row(273)['indicative_centiBits'] == 11546
    print('PASS: 273-column naive extension fails exact same-key pigeonhole budget; no new proof')
