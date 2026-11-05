#!/usr/bin/env python3
"""Exact degree-budget gate for common partial-fibre roots, Koala 116.12.
This checks the published worst-case degree bound, not actual Q degrees.
"""
ROW_MAX=131071
FIBRE=512
Q_BOUND=255
CORE=511
EXTRA=7
assert CORE+FIBRE*Q_BOUND==ROW_MAX
assert CORE+EXTRA+FIBRE*Q_BOUND==131078>ROW_MAX
assert (ROW_MAX-(CORE+EXTRA))//FIBRE==254
assert CORE+EXTRA+FIBRE*254==130566<=ROW_MAX
print('published degree upper bound:',CORE+FIBRE*Q_BOUND)
print('with 7 extra common RF roots:',CORE+EXTRA+FIBRE*Q_BOUND)
print('maximum certified Q degree after 7 extra roots:',(ROW_MAX-CORE-EXTRA)//FIBRE)
print('RESULT: existing Q<=255 guarantee cannot certify added roots; need Q<=254 or different architecture')
