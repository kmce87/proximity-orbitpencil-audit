#!/usr/bin/env python3
"""N6 step 1: all z-density profiles d(z) = 8*phi(z) on F_2^4 allowed by the Walsh lattice.
Constraint: 1_S = delta_q(z) + (1/8) sum b chi means d^(mu) = 8 mod 16 for every mu, Sum d = 72, 0 <= d <= 8.
y-budget: sum_{eta != 0} b^2 = (1/16) sum_z d(8-d).  Prints GL_4 + translation classes."""
import itertools, collections
pc=[bin(i).count('1')&1 for i in range(16)]
W3=[[1-2*pc[m&z] for z in range(8)] for m in range(8)]
halves=collections.defaultdict(list)
# DFS with Lambda_j pruning: restriction to subcube dim j has Walsh = 0 mod 2^j
def walsh(f,j):
    return [sum(f[z]*(1-2*pc[m&z]) for z in range(2**j)) for m in range(2**j)]
def rec(f):
    if len(f)==8:
        w=tuple(x%16 for x in walsh(f,3)); halves[w].append(tuple(f)); return
    for v in range(9):
        g=f+[v]
        L=len(g)
        if L in (2,4):
            j={2:1,4:2}[L]
            if any(x%(2**j) for x in walsh(g,j)): continue
        rec(g)
rec([])
print("half functions:",sum(len(v) for v in halves.values()),"residue classes:",len(halves))
profiles=[]
for w0,fs0 in halves.items():
    w1=tuple((x+8)%16 for x in w0)
    if w1 not in halves: continue
    # need d^ = D0 + D1 and D0 - D1 = 8 mod 16: D0 = 0 mod 8, D1 = D0 + 8 mod 16
    if any(x%8 for x in w0): continue
    for a in fs0:
        for b in halves[w1]:
            if sum(a)+sum(b)!=72: continue
            profiles.append(a+b)
print("profiles:",len(profiles))
# canonical form under AGL(4,2): generate group action on z
def mat_apply(M,z):
    r=0
    for i in range(4):
        if z>>i&1: r^=M[i]
    return r
GL=[]
for M in itertools.product(range(1,16),repeat=4):
    s={0}
    ok=True
    for c in M:
        if c in s: ok=False;break
        s|={x^c for x in s}
    if ok: GL.append(M)
print("|GL4|=",len(GL))
perms=[]
for M in GL:
    t=[mat_apply(M,z) for z in range(16)]
    for tr in range(16):
        perms.append(tuple(t[z]^tr for z in range(16)))
seen=set(); classes=[]
pset=set(profiles)
for p in sorted(profiles):
    if p in seen: continue
    orb={tuple(p[pp[z]] for z in range(16)) for pp in perms}
    seen|=orb
    classes.append((p,len(orb)))
print("classes:",len(classes))
# representatives of the even profiles, input of n6_count.cpp
even=sorted([c for c in classes if all(x%2==0 for x in c[0])],key=lambda t:-sum(x*(8-x) for x in t[0]))
with open('n6_reps.txt','w') as f:
    for p,o in even: f.write(str(o)+' '+' '.join(map(str,p))+'\n')
for p,o in sorted(classes,key=lambda t:-sum(x*(8-x) for x in t[0])):
    cnt=collections.Counter(p)
    budget=sum(x*(8-x) for x in p)/16
    wal=collections.Counter(abs(x)//8 for x in walsh(list(p),4)[1:])
    print(f"budget {budget:5.2f} orbit {o:7d} values {dict(sorted(cnt.items()))} |k_mu| {dict(sorted(wal.items()))}")
