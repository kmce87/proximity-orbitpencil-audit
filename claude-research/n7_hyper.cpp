// N7 toy: list decoding of a word on V by polys of degree <= D, at S-size D+2 (one check).
// Dual form: word <-> functional Lambda on polys of degree <= c (c=N-D-2), T=V\S of size c, condition Lambda(L_T)=0.
// Each Lambda through c random independent T-locators is sampled; we count zeros and distinct polynomials (distinct error supports).
// The same-top class is the Lambda = e_1 + const, density 1/N of all T.
// Args: n seed tries [mode].  Field GF(2^32) (genericity), labels random independent.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <random>
#include <algorithm>
#include <wmmintrin.h>
#include <emmintrin.h>
using namespace std;
typedef uint32_t F;
static inline F mul(F a,F b){ // GF(2^32) mod x^32+x^22+x^2+x+1
    __m128i A=_mm_cvtsi32_si128((int)a),B=_mm_cvtsi32_si128((int)b);
    __m128i C=_mm_clmulepi64_si128(A,B,0);
    uint64_t r=_mm_cvtsi128_si64(C);
    // reduce: x^32 = x^22+x^2+x+1 (loop, since x^22 shifts can overflow again)
    while(r>>32){ uint64_t hi=r>>32; r=(r&0xffffffffULL)^hi^(hi<<1)^(hi<<2)^(hi<<22); }
    return (F)r;
}
static F inv(F a){ F r=1,b=a; uint32_t e=0xfffffffe; while(e){ if(e&1) r=mul(r,b); b=mul(b,b); e>>=1;} return r; }
int n,N,D,c;
vector<F> lab;
vector<uint32_t> Ts; vector<vector<F>> Lc;
static void locator(uint32_t mask, vector<F>&P){ P.assign(1,1); for(int i=0;i<N;i++) if(mask>>i&1){ P.push_back(0); for(int j=P.size()-1;j>=1;j--) P[j]=P[j-1]^mul(P[j],lab[i]); P[0]=mul(P[0],lab[i]); } }
// solve left-nullspace: given c rows of length c+1 return vector lam with lam.row=0
static bool nullvec(vector<vector<F>> M, vector<F>&lam){
    int R=M.size(),C=c+1; vector<int> piv; int r=0;
    for(int col=0;col<C&&r<R;col++){ int p=-1; for(int i=r;i<R;i++) if(M[i][col]){p=i;break;} if(p<0) continue; swap(M[r],M[p]); F iv=inv(M[r][col]); for(int j=0;j<C;j++) M[r][j]=mul(M[r][j],iv); for(int i=0;i<R;i++) if(i!=r&&M[i][col]){ F f=M[i][col]; for(int j=0;j<C;j++) M[i][j]^=mul(f,M[r][j]); } piv.push_back(col); r++; }
    if(r<R) return false;
    int fr=-1; for(int j=0;j<C;j++){ if(find(piv.begin(),piv.end(),j)==piv.end()){fr=j;break;} }
    lam.assign(C,0); lam[fr]=1; for(int i=0;i<R;i++) lam[piv[i]]=M[i][fr];
    return true;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); uint64_t seed=atoll(argv[2]); uint64_t tries=atoll(argv[3]); int mode=argc>4?atoi(argv[4]):0;
    N=1<<n; D=N/2; c=N-D-2;
    mt19937_64 rng(seed);
    vector<F> basis(n); for(int i=0;i<n;i++) basis[i]=(F)rng();
    lab.resize(N); for(int v=0;v<N;v++){F x=0; for(int i=0;i<n;i++) if(v>>i&1) x^=basis[i]; lab[v]=x;}
    // enumerate T's
    for(uint32_t m=0;m<(1u<<N);m++){ if(__builtin_popcount(m)==c) Ts.push_back(m); if(N>=32) break; }
    int M=Ts.size(); Lc.resize(M); for(int i=0;i<M;i++) locator(Ts[i],Lc[i]);
    printf("n=%d N=%d D=%d c=%d T-sets=%d same-top expected %d\n",n,N,D,c,M,M/N);
    // sampled Lambda through c random T's; early abort on a random sample of T's; full count of zeros and of distinct polynomials
    // (distinct polynomials <-> distinct error supports: E_T(t)=Lambda(L_{T-t})/L_T'(t), and two errors of support <= c with equal syndrome coincide)
    map<pair<int,int>,uint64_t> hist3; int dump=argc>6?atoi(argv[6]):1000000;
    const int SAMPLE=argc>7?atoi(argv[7]):300; int thresh=atoi(argc>5?argv[5]:"4");
    vector<int> samp(SAMPLE);
    uint64_t passed=0;
    for(uint64_t it=0;it<tries;it++){
        vector<vector<F>> rows; uint32_t andm=~0u;
        for(int k=0;k<c;k++){ int j=rng()%M; rows.push_back(Lc[j]); andm&=Ts[j]; }
        vector<F> lam; if(!nullvec(rows,lam)) continue;
        for(int k=0;k<SAMPLE;k++) samp[k]=rng()%M;
        int z=0; for(int k=0;k<SAMPLE;k++){ const vector<F>&L=Lc[samp[k]]; F s=0; for(int j=0;j<=c;j++) s^=mul(lam[j],L[j]); if(!s) z++; }
        if(z<thresh) continue;
        passed++;
        int zeros=0; vector<uint32_t> supps; vector<F> P;
        for(int i=0;i<M;i++){ F s=0; for(int j=0;j<=c;j++) s^=mul(lam[j],Lc[i][j]); if(s) continue; zeros++;
            uint32_t sup=0; for(int t=0;t<N;t++) if(Ts[i]>>t&1){ locator(Ts[i]&~(1u<<t),P); F v=0; for(size_t j=0;j<P.size();j++) v^=mul(lam[j],P[j]); if(v) sup|=1u<<t; }
            supps.push_back(sup); }
        sort(supps.begin(),supps.end()); supps.erase(unique(supps.begin(),supps.end()),supps.end());
        int dist=supps.size();
        // puncture rank: points lying in at least 90% of the distinct error supports
        vector<int> pd(N,0); for(uint32_t u:supps) for(int t=0;t<N;t++) if(u>>t&1) pd[t]++;
        int pr=0; for(int t=0;t<N;t++) if(10*pd[t]>=9*dist) pr++;
        // minimal support size, sums histogram mode
        map<uint32_t,int> sh; for(uint32_t u:supps){ uint32_t x=0; for(int t=0;t<N;t++) if(u>>t&1) x^=t; sh[x]++; }
        int mode=0; for(auto&kv:sh) mode=max(mode,kv.second);
        hist3[{pr,dist}]++;
        if(dist>=dump){ printf("CLASS it=%llu pr=%d distinct=%d zeros=%d sum-mode=%d lam:",(unsigned long long)it,pr,dist,zeros,mode); for(F x:lam) printf(" %08x",x); printf("\n"); fflush(stdout);}
    }
    printf("tries=%llu passed=%llu\n",(unsigned long long)tries,(unsigned long long)passed);
    for(auto&kv:hist3) printf("pr=%d distinct=%d : %llu\n",kv.first.first,kv.first.second,(unsigned long long)kv.second);
}
