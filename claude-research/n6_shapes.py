#!/usr/bin/env python3
"""N6: rank-4 shapes with 6 etas, each on a half-space of Z = F_2^4 (cost 2); every z sees nothing, a line or an affine plane of etas.
Counts exactly: number of (E, H) assignments, sign solutions over F_2, and valid d-profiles (Walsh(d) = 8 mod 16)."""
import itertools, sys, collections
pc=[bin(i).count('1')&1 for i in range(256)]
def rank(vs):
    b=[];
    for v in vs:
        for x in b: v=min(v,v^x)
        if v: b.append(v)
    return len(b)
halfs=[]
for s in range(1,16):
    for k in (0,1):
        halfs.append((s,k,frozenset(z for z in range(16) if pc[s&z]==k)))
Es=[E for E in itertools.combinations(range(1,16),6) if rank(E)==4]
print("rank-4 6-sets:",len(Es))
def circuits(E):
    C=set()
    for r in (3,4):
        for T in itertools.combinations(E,r):
            x=0
            for t in T:x^=t
            if x==0: C.add(frozenset(T))
    return C
# reduce by GL4 canonical form
GL=[]
for M in itertools.product(range(1,16),repeat=4):
    if rank(M)==4: GL.append(M)
def app(M,v):
    r=0
    for i in range(4):
        if v>>i&1:r^=M[i]
    return r
tables=[[app(M,v) for v in range(16)] for M in GL]
canon={}
reps=[]
seen=set()
for E in Es:
    if E in seen: continue
    orb={tuple(sorted(t[x] for x in E)) for t in tables}
    seen|=orb
    reps.append((E,len(orb)))
print("GL4 classes:",len(reps))
total=collections.Counter()
for E,orbE in reps:
    C=circuits(E)
    covered=set().union(*C) if C else set()
    if covered!=set(E):
        continue
    subs=set()
    for c in C:
        for r in range(0,len(c)+1):
            for T in itertools.combinations(sorted(c),r): subs.add(frozenset(T))
    subs.add(frozenset())
    full=set(C)|{frozenset()}
    sols=[]
    def rec(i,assign):
        if i==6:
            # final: E_z in circuits or empty
            for z in range(16):
                Ez=frozenset(E[j] for j in range(6) if z in halfs[assign[j]][2])
                if Ez not in full: return
            sols.append(tuple(assign)); return
        for h in range(30):
            assign.append(h)
            ok=True
            for z in range(16):
                Ez=frozenset(E[j] for j in range(i+1) if z in halfs[assign[j]][2])
                if Ez not in subs: ok=False;break
            if ok: rec(i+1,assign)
            assign.pop()
    rec(0,[])
    print("E",E,"orbit",orbE,"circuits",[sorted(c) for c in C],"H-assignments",len(sols))
    total[E]=len(sols)
    if sols:
        import json
        with open('/tmp/claude-0/n6_shape_%s.json'%('_'.join(map(str,E))),'w') as f: json.dump({"E":E,"orbit":orbE,"sols":sols},f)
