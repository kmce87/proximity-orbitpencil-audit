#!/usr/bin/env python3
"""N6: exact total of the common-top class at each ny from the per-profile DFS logs (n6_count) and the rank-4 formula."""
import re,sys
from math import log2
def gauss(n,k):
    if k<0 or k>n: return 0
    a=b=1
    for i in range(k): a*=2**(n-i)-1; b*=2**(k-i)-1
    return a//b
Nr=dict.fromkeys(range(5),0)
for line in open(sys.argv[1]):
    m=re.match(r'profile#(\d+) orbit (\d+) \|.*ranks:(.*)',line)
    if not m: continue
    orb=int(m.group(2))
    for r,c in re.findall(r'(\d+):(\d+)',m.group(3)):
        r=int(r);c=int(c)
        # log is at ny=3: rank r members number [3,r]*N_r
        Nr[r]+=orb*c//gauss(3,r)
        assert orb*c%gauss(3,r)==0
Nr[4]=560*2520*2**17+560*3*840*2**15
print("N_rho:",Nr)
for ny in range(4,12):
    t=sum(gauss(ny,r)*Nr[r] for r in Nr)
    av=t*7//16
    a=9*2**ny+0
    print(f"ny={ny}: M_all=2^{log2(t):.3f}  rank4 share {gauss(ny,4)*Nr[4]/t:.3f}  with 0 not in S: 2^{log2(av):.3f}  need > 2^64 at ny=10 (f=7)")
t=sum(gauss(10,r)*Nr[r] for r in Nr)
print("exact M_all(10) =",t," M(0 not in S) =",t*7//16, " 2^64 =",2**64," ratio needed =",2**64/(t*7/16))
# cross-check: if a ny=4 log is given, its exact per-rank totals must match the formula
if len(sys.argv)>2:
    tot=dict.fromkeys(range(5),0)
    for line in open(sys.argv[2]):
        m=re.match(r'profile#(\d+) orbit (\d+) \|.*ranks:(.*)',line)
        if not m: continue
        for r,c in re.findall(r'(\d+):(\d+)',m.group(3)): tot[int(r)]+=int(m.group(2))*int(c)
    for r in tot: assert tot[r]==gauss(4,r)*Nr[r],(r,tot[r],gauss(4,r)*Nr[r])
    print("ny=4 logs match the formula at every rank:",tot)
