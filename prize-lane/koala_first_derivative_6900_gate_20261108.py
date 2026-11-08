#!/usr/bin/env python3
"""Necessary-domain gate, NOT a proof of Koala soundness or higher derivatives.

Checks whether the DKT first-order theorem a > a1(rho) can be applied
at the proposed 69.00-bit Koala lower radius.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
getcontext().prec = 80
rho = Decimal(1)/2
n = 262144
p = 2130706433
challenge_cardinality = p**6
numerator, denominator = 334773390, 1073741824
radius = Fraction(numerator, denominator)
agreement = 1 - radius
first_order = (3*rho + 2*(rho*(5-rho)*(2-rho)).sqrt())/(8-rho)
agreement_decimal = Decimal(agreement.numerator)/Decimal(agreement.denominator)
eta = agreement_decimal-first_order
assert eta < 0, 'First-order curve unexpectedly applicable; revisit analysis'
assert radius < Fraction(131073,262144), 'Radius inadmissible'
print('koala n:',n,'base characteristic:',p,'challenge cardinality:',challenge_cardinality)
print('candidate ProtocolClaim:',6900,numerator,denominator)
print('candidate agreement:',agreement_decimal)
print('first-order agreement threshold:',first_order)
print('eta = agreement - a1:',eta)
print('first-order DKT theorem at 69.00 bits: NOT APPLICABLE (eta <= 0)')
print('Higher derivative finite bound: NOT TESTED / NOT PROVED')
