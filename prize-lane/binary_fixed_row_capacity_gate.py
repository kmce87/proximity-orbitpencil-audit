#!/usr/bin/env python3
"""Exact capacity gate for fixed-row leading-term cancellation.
Source: official SubmissionBinaryUpper/CorePencil.lean card_Param, NN, Sel_card;
LabelFamily.lean Gq_sub_natDegree and Cp_natDegree_le.
Not a Lean proof or an independently verified prize submission.
"""
from math import ceil
NN = 2**64 + 1
ROWS = 420
PER_ROW = 32 * 2047 * (1023*1022*1021) * 512 * 4
TOTAL = ROWS * PER_ROW
MIN_ROWS = (NN + PER_ROW - 1)//PER_ROW
assert TOTAL == 60144973141589360640
assert PER_ROW < NN
assert (MIN_ROWS-1)*PER_ROW < NN <= MIN_ROWS*PER_ROW
assert MIN_ROWS == 129
print('required distinct parameters:', NN)
print('maximum parameters from one row:', PER_ROW)
print('minimum rows even if every parameter is usable:', MIN_ROWS)
print('capacity hypothesis (one fixed row supplies 2^64+1): FALSE')
