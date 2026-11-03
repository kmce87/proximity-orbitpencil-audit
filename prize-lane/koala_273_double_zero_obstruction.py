#!/usr/bin/env python3
"""Lane B: falsify automatic double root at zero from top/product keys.
Toy counterexample over F_97, NOT a KoalaBear-specific impossibility theorem.
Published construction and proof are the original authors' work.
"""
P=97
A=(2,3,4,5,8)
B=(1,2,3,7,9)
def polynomial(roots):
    c=[1]
    for r in roots:
        d=[0]*(len(c)+1)
        for i,v in enumerate(c):
            d[i]=(d[i]-r*v)%P
            d[i+1]=(d[i+1]+v)%P
        c=d
    return c
a,b=polynomial(A),polynomial(B)
assert a==[10,91,54,86,75,1]
assert b==[10,13,22,73,75,1]
assert (a[-2],a[0])==(b[-2],b[0])
d=[(x-y)%P for x,y in zip(a,b)]
assert d==[0,78,32,13,0,0]
# At alpha=1 the original pencil subtracts gamma*X,
# gamma = deltaV(alpha)/alpha; zero and alpha become roots.
alpha=1
gamma=sum(d)%P
q=d[:]
q[1]=(q[1]-gamma)%P
assert sum(q)%P==0 and q[0]==0
assert q[1]!=0 # derivative at zero, hence zero is SIMPLE
print('PASS: same leading subcoefficient and constant/product key')
print('deltaV:',d,'gamma:',gamma,'pencil:',q)
print('Pencil roots at 0 and 1, but derivative at 0 =',q[1], '!= 0')
print('No automatic third root from those two key equalities alone.')
print('This is a toy structural counterexample, NOT a Koala score improvement.')
