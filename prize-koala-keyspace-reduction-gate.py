#!/usr/bin/env python3
"""Exact pigeonhole gate. Does NOT prove algebraic dependency or Lean soundness."""
from math import comb
q = 2**31 - 2**24 + 1
N = comb(511, 272)
target = 2**59 + 1
ceildiv = lambda a, b: (a + b - 1) // b
key15 = 512 * q**15
key14 = 512 * q**14
reduction = ceildiv(target * key15, N)
assert ceildiv(N, key15) < target <= ceildiv(N, key14)
assert (reduction - 1) * N < target * key15 <= reduction * N
assert reduction <= q
print("15-key guaranteed collision:", ceildiv(N, key15))
print("14-key guaranteed collision:", ceildiv(N, key14))
print("minimum keyspace reduction factor:", reduction)
print("field size:", q)
print("Conditional: fully redundant 15th key suffices; dependency NOT established.")
