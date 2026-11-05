// N9 validation, independent of n9_census: enumerate ALL zero-sum sets of distinct nonzero characters of size m and all signs
// (integrality fixes the parity of the sign vector), plus the (2,1^4) and (2) shapes, evaluate phi = 1_B + h with bit-sliced counters over N <= 64 points.
// Usage: brute n spec seed mmax   (spec = flat | random | file path)   Output: for each m, the number of h with phi >= 0 and agreement > 9N/16, = 9N/16.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <string>
#include <random>
#include <algorithm>
using namespace std;
static int n,N; static uint64_t Bm, Pm=0, ALL; static uint64_t X[64]; // X[a] = mask of v with a.v = 1
static long long gt[16],eq[16]; static int t916;
struct Cnt{ uint64_t b[4]; };
static inline Cnt add(Cnt c,uint64_t m){ for(int i=0;i<4;i++){ uint64_t carry=c.b[i]&m; c.b[i]^=m; m=carry; } return c; }
static inline uint64_t eqw(const Cnt&c,int w){ uint64_t r=ALL; for(int i=0;i<4;i++) r&=((w>>i)&1)?c.b[i]:~c.b[i]; return r&ALL; }
// h = (2 + m - 2 wt)/4
static inline void leaf(int m,const Cnt&c){
    uint64_t ge2=0,one=0,zero=0,minus1=0,minus2=0;
    for(int w=0;w<=m;w++){ uint64_t e=eqw(c,w); if(!e) continue; int num=2+m-2*w; if(num%4) return; int h=num/4; if(h>=2) ge2|=e; else if(h==1) one|=e; else if(h==0) zero|=e; else if(h==-1) minus1|=e; else minus2|=e; }
    if(minus2) return; if(minus1&~Bm) return; if((zero|minus1)&Pm) return;
    int ag=__builtin_popcountll(ge2|(one&~Pm)|(zero&Bm));
    if(ag>t916) gt[m]++; else if(ag==t916) eq[m]++;
}
static int M;
static void signs(const int*a,int k,Cnt c){ // assign sign to char k
    if(k==M){ leaf(M,c); return; }
    signs(a,k+1,add(c,X[a[k]])); signs(a,k+1,add(c,ALL&~X[a[k]]));
}
static void sets(int*a,int k,int minv,int sum){
    if(k==M-1){ if(sum<minv) return; a[k]=sum; Cnt c={{0,0,0,0}}; signs(a,0,c); return; }
    for(int x=minv;x<N;x++){ a[k]=x; sets(a,k+1,x+1,sum^x); }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); string spec=argv[2]; uint64_t seed=atoll(argv[3]); int mmax=atoi(argv[4]); N=1<<n; ALL=(N==64)?~0ULL:((1ULL<<N)-1); t916=9*N/16;
    for(int a=0;a<N;a++){ uint64_t m=0; for(int v=0;v<N;v++) if(__builtin_parity(a&v)) m|=1ULL<<v; X[a]=m; }
    mt19937_64 rng(seed); vector<int> p(N); for(int i=0;i<N;i++) p[i]=i; Bm=0;
    if(spec=="flat"){ for(int i=0;i<N/8;i++) Bm|=1ULL<<i; }
    else if(spec=="random"){ shuffle(p.begin(),p.end(),rng); for(int i=0;i<N/8;i++) Bm|=1ULL<<p[i]; }
    else { FILE*f=fopen(spec.c_str(),"r"); int x; while(fscanf(f,"%d",&x)==1){ if(x<0) Pm|=1ULL<<(-x-1); else Bm|=1ULL<<x; } fclose(f); } // negative entries -y-1 mark rho(y) = -1
    int a[16];
    for(M=4;M<=mmax;M+=2){ sets(a,0,1,0); printf("m=%d gt=%lld eq=%lld\n",M,gt[M],eq[M]); fflush(stdout); }
    // shape (2): hyperplanes, shape (2,1^4): h = 1_H + swap
    long long g2=0,e2=0,g3=0,e3=0;
    for(int b=1;b<N;b++) for(int s=0;s<2;s++){ uint64_t H=s?X[b]:(ALL&~X[b]); // h = 1_H
        if(!(Pm&~H)){ int ag=__builtin_popcountll((H&~Pm)|Bm); if(ag>t916) g2++; else if(ag==t916) e2++; }
        // add swap: 4 chars zero sum, sum of signs = 0 mod 4 => values in {-1,0,1}
        for(int a1=1;a1<N;a1++){ if(a1==b) continue; for(int a2=a1+1;a2<N;a2++){ if(a2==b) continue; for(int a3=a2+1;a3<N;a3++){ if(a3==b) continue; int a4=a1^a2^a3; if(a4<=a3||a4==b) continue;
            int A[4]={a1,a2,a3,a4};
            for(int sg=0;sg<16;sg++){ if(__builtin_popcount(sg)%2) continue; // sum of signs in {-4,0,4}
                Cnt c={{0,0,0,0}}; for(int i=0;i<4;i++) c=add(c,(sg>>i&1)?X[A[i]]:(ALL&~X[A[i]])); // l_i
                // wt 0 -> swap=+1, wt 4 -> swap=-1, wt 2 -> 0
                uint64_t Ep=eqw(c,0),Em=eqw(c,4);
                uint64_t two=Ep&H; uint64_t one=(H&~Em&~Ep)|(Ep&~H); uint64_t zero=(ALL&~H&~Ep&~Em)|(Em&H); uint64_t minus=Em&~H;
                if(minus&~Bm) continue; if((zero|minus)&Pm) continue; int ag2=__builtin_popcountll(two|(one&~Pm)|(zero&Bm)); if(ag2>t916) g3++; else if(ag2==t916) e3++;
            }
        } } }
    }
    printf("shape(2) gt=%lld eq=%lld ; shape(2,1^4) gt=%lld eq=%lld\n",g2,e2,g3,e3);
    return 0;
}
