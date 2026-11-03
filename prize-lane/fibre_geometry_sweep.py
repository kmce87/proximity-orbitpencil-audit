#!/usr/bin/env python3
"""Necessary arithmetic gate for a generalized OrbitPencil template.
Not a Lean certificate or a general impossibility result.
"""
from math import comb, log2
P=2130706433
N=1<<18
K=1<<17
SLOPES=1<<59

def candidate(F,m):
    B=N//F
    # R degree B-1; Q degree <=m-t-3; c degree <=K-1
    t=max(0,m-3-(K-B)//B)
    if t>m-1:return None
    choices=comb(F-1,m)
    budget=P**t*F*SLOPES
    return {'F':F,'B':B,'m':m,'t':t,'agreement':(B-1)+B*m,
            'pass':choices>budget,'margin_bits':log2(choices)-log2(budget)}

if __name__=='__main__':
    best_all=None
    for F in [128,256,512,1024,2048,4096]:
        valid=[candidate(F,m) for m in range(1,F)]
        valid=[x for x in valid if x and x['pass']]
        best=max(valid,key=lambda x:x['agreement']) if valid else None
        if best and (best_all is None or best['agreement']>best_all['agreement']):best_all=best
        print('F=%d B=%d best=%s'%(F,N//F,best))
    assert best_all['F']==512 and best_all['m']==272 and best_all['agreement']==139775
    assert candidate(512,273)['pass'] is False
    print('PASS: no improvement in this six-geometry pigeonhole template sweep')
