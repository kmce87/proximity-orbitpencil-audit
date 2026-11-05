// N7: exact checks of the "shortened quadric" family.
// mode A (n): exhaustive over all N/2-subsets C of V (n <= 5): which have deg(X^(N/2) - V_C) <= 3N/8 ?  Compare with the rank-2 quadric + hyperplane count.
// mode B (n, seed, nB): T = X^(N/2) V_B, B random of size N/8.  Enumerate all quadrics C, verify deg P <= N/2 and P=T on C u B by direct evaluation, histogram of |C u B|.
// Field GF(2^32), labels random independent; seed 0 selects the Krylov labels 1,x,...,x^(n-1) (exact for BF64 too at these small sizes, no wrap-around).
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <set>
#include <random>
#include <algorithm>
#include <wmmintrin.h>
#include <emmintrin.h>
using namespace std;
typedef uint32_t F;
static inline F mul(F a,F b){
    __m128i A=_mm_cvtsi32_si128((int)a),B=_mm_cvtsi32_si128((int)b);
    __m128i C=_mm_clmulepi64_si128(A,B,0);
    uint64_t r=_mm_cvtsi128_si64(C);
    while(r>>32){ uint64_t hi=r>>32; r=(r&0xffffffffULL)^hi^(hi<<1)^(hi<<2)^(hi<<22); }
    return (F)r;
}
int n,N;
vector<F> lab;
static vector<F> polymul(const vector<F>&a,const vector<F>&b){ vector<F> r(a.size()+b.size()-1,0); for(size_t i=0;i<a.size();i++) if(a[i]) for(size_t j=0;j<b.size();j++) r[i+j]^=mul(a[i],b[j]); return r; }
static vector<F> locator(const vector<int>&pts){ vector<F> P(1,1); for(int v:pts){ P.push_back(0); for(int j=(int)P.size()-1;j>=1;j--) P[j]=P[j-1]^mul(P[j],lab[v]); P[0]=mul(P[0],lab[v]); } return P; }
static F evalp(const vector<F>&P,F x){ F r=0; for(int j=(int)P.size()-1;j>=0;j--) r=mul(r,x)^P[j]; return r; }
static int degp(const vector<F>&P){ for(int j=(int)P.size()-1;j>=0;j--) if(P[j]) return j; return -1; }
// mode A: DFS with e1,e2,e3 (and e4..e_(N/8-1) when N/8 > 4), target all zero
static uint64_t foundA=0; static vector<uint32_t> setsA;
static int tA,kA; // choose kA points, coefficient positions 1..tA must vanish
static void dfsA(int start,int cnt,uint32_t mask,F* e){
    if(cnt==kA){ bool ok=true; for(int j=1;j<=tA;j++) if(e[j]) {ok=false;break;} if(ok){ foundA++; setsA.push_back(mask);} return; }
    if(N-start<kA-cnt) return;
    for(int v=start;v<N;v++){
        F f[10]; f[0]=1; F x=lab[v];
        for(int j=1;j<=tA;j++) f[j]=e[j]^mul(e[j-1],x);
        dfsA(v+1,cnt+1,mask|(1u<<v),f);
    }
}
static int walsh_is_plateau(uint32_t mask){ // returns 1 if all Walsh coefficients divisible by N/4 (so Fourier in (1/4)Z)
    for(int chi=1;chi<N;chi++){ int s=0; for(int v=0;v<N;v++) if(mask>>v&1) s+=__builtin_parity(v&chi)?-1:1; if(s%(N/4)) return 0; }
    return 1;
}
int main(int argc,char**argv){
    char mode=argv[1][0]; n=atoi(argv[2]); uint64_t seed=atoll(argv[3]);
    N=1<<n; mt19937_64 rng(seed);
    vector<F> basis(n); for(int i=0;i<n;i++) basis[i]=(F)rng();
    if(seed==0){ for(int i=0;i<n;i++) basis[i]=1u<<i; puts("Krylov labels 1,x,...,x^(n-1)"); }
    lab.resize(N); for(int v=0;v<N;v++){F x=0; for(int i=0;i<n;i++) if(v>>i&1) x^=basis[i]; lab[v]=x;}
    if(mode=='A'){
        kA=N/2; tA=N/8-1; if(tA>9){puts("too large");return 1;}
        F e[10]; e[0]=1; for(int j=1;j<10;j++) e[j]=0;
        dfsA(0,0,0,e);
        uint64_t plateau=0; for(uint32_t m:setsA) plateau+=walsh_is_plateau(m);
        // count of plateau Boolean functions of density 1/2: quadrics 8*[n,2]*(2^(n-2)-1) + hyperplane cosets 2(2^n-1)
        uint64_t g=((1ULL<<n)-1)*((1ULL<<(n-1))-1)/3;
        uint64_t pred=8*g*((1ULL<<(n-2))-1)+2*((1ULL<<n)-1);
        printf("n=%d N/2-subsets with deg(X^(N/2)-V_C)<=3N/8: %llu ; of those with Fourier in (1/4)Z: %llu ; predicted rank-2 quadrics+hyperplanes: %llu\n",n,(unsigned long long)foundA,(unsigned long long)plateau,(unsigned long long)pred);
        return 0;
    }
    // mode B
    int nB=N/8; vector<int> perm(N); for(int i=0;i<N;i++) perm[i]=i; shuffle(perm.begin(),perm.end(),rng);
    vector<int> B(perm.begin(),perm.begin()+nB); uint64_t Bmask[4]={0,0,0,0}; vector<char> inB(N,0); for(int v:B) inB[v]=1;
    vector<F> VB=locator(B);
    vector<F> X(N/2+1,0); X[N/2]=1;
    vector<F> T=polymul(X,VB);
    vector<F> Tvals(N); for(int v=0;v<N;v++) Tvals[v]=evalp(T,lab[v]);
    // enumerate all Boolean functions with Fourier support a 2-flat chi+L avoiding 0: F = (1/2) sum s_i chi_i with product of signs -1, C={F=-1}
    set<vector<F>> seen; map<int,uint64_t> hist; uint64_t cnt=0,bad=0;
    // alternating: choose independent a,b and chi not in <a,b>; the function value at v is 1 if chi(v)+a(v)b(v)+e1 a(v)+e2 b(v)+e0
    map<vector<uint32_t>,int> done;
    for(int a=1;a<N;a++) for(int b=a+1;b<N;b++){ int c=a^b; if(c<b) continue; // unordered 2-dim subspace {a,b,a^b}, with a<b<c
        for(int chi=1;chi<N;chi++){ if(chi==a||chi==b||chi==c) continue;
            // canonical coset representative: smallest of chi, chi^a, chi^b, chi^c
            int r=min(min(chi,chi^a),min(chi^b,chi^c)); if(r!=chi) continue;
            for(int e=0;e<8;e++){
                vector<int> C; for(int v=0;v<N;v++){ int f=__builtin_parity(v&chi)^(__builtin_parity(v&a)&__builtin_parity(v&b))^((e&1)?__builtin_parity(v&a):0)^((e&2)?__builtin_parity(v&b):0)^((e>>2)&1); if(f) C.push_back(v); }
                if((int)C.size()!=N/2){ bad++; continue; }
                vector<F> VC=locator(C);
                vector<F> W=VC; W[N/2]^=1; if(degp(W)>3*N/8) { printf("degree failure\n"); return 1; }
                vector<F> P=polymul(W,VB);
                if(degp(P)>N/2){ printf("deg P failure\n"); return 1; }
                int agr=0; for(int v=0;v<N;v++) if(evalp(P,lab[v])==Tvals[v]) agr++;
                int un=nB; for(int v:C) if(!inB[v]) un++;
                if(agr<un){ printf("agreement failure %d %d\n",agr,un); return 1; }
                hist[agr]++; cnt++;
            }
        }
    }
    uint64_t g=((1ULL<<n)-1)*((1ULL<<(n-1))-1)/3;
    printf("n=%d |B|=%d quadrics enumerated=%llu predicted=%llu density-fail=%llu\n",n,nB,(unsigned long long)cnt,(unsigned long long)(8*g*((1ULL<<(n-2))-1)),(unsigned long long)bad);
    uint64_t above=0; for(auto&kv:hist){ printf(" agreement %d (9/16 N=%d): %llu\n",kv.first,9*N/16,(unsigned long long)kv.second); if(kv.first>9*N/16) above+=kv.second; }
    printf(" members with agreement > 9N/16: %llu\n",(unsigned long long)above);
}
