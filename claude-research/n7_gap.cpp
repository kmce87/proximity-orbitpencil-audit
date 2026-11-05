// N7 toy, general gap g: word <-> Lambda on polys of degree <= c+g-2 (c=N-D-g, D=N/2), T=complement of S (|T|=c).
// T in the list of the word iff Lambda(X^i L_T)=0 for i=0..g-2.
// Sample Lambda through m = floor((c+g-2)/(g-1)) random T's (plus, if the rows leave a larger null space, a random null vector) and count members.
// distinct polynomials = distinct error supports.  Same-top comparison printed from a direct hash of the top coefficients (largest classes).
// Args: n g seed tries [dump_threshold]
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <unordered_map>
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
static F inv(F a){ F r=1,b=a; uint32_t e=0xfffffffe; while(e){ if(e&1) r=mul(r,b); b=mul(b,b); e>>=1;} return r; }
int n,N,D,c,g,LEN;
vector<F> lab;
vector<uint32_t> Ts; vector<vector<F>> Lc;
static void locator(uint32_t mask, vector<F>&P){ P.assign(1,1); for(int i=0;i<N;i++) if(mask>>i&1){ P.push_back(0); for(int j=(int)P.size()-1;j>=1;j--) P[j]=P[j-1]^mul(P[j],lab[i]); P[0]=mul(P[0],lab[i]); } }
// right null space of the matrix M (rows), LEN columns
static vector<vector<F>> nullspace(vector<vector<F>> M){
    int R=M.size(),C=LEN; vector<int> piv; int r=0;
    for(int col=0;col<C&&r<R;col++){ int p=-1; for(int i=r;i<R;i++) if(M[i][col]){p=i;break;} if(p<0) continue; swap(M[r],M[p]); F iv=inv(M[r][col]); for(int j=0;j<C;j++) M[r][j]=mul(M[r][j],iv); for(int i=0;i<R;i++) if(i!=r&&M[i][col]){ F f=M[i][col]; for(int j=0;j<C;j++) M[i][j]^=mul(f,M[r][j]); } piv.push_back(col); r++; }
    vector<char> isp(C,0); for(int x:piv) isp[x]=1;
    vector<vector<F>> out;
    for(int f=0;f<C;f++) if(!isp[f]){ vector<F> v(C,0); v[f]=1; for(int i=0;i<(int)piv.size();i++) v[piv[i]]=M[i][f]; out.push_back(v); }
    return out;
}
static inline bool member(const vector<F>&lam,const vector<F>&L){
    for(int i=0;i<=g-2;i++){ F s=0; for(int j=0;j<=c;j++) s^=mul(lam[i+j],L[j]); if(s) return false; }
    return true;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); g=atoi(argv[2]); uint64_t seed=atoll(argv[3]); uint64_t tries=atoll(argv[4]); int dump=argc>5?atoi(argv[5]):1000000;
    N=1<<n; D=N/2; c=N-D-g; LEN=c+g-1;
    mt19937_64 rng(seed);
    vector<F> basis(n); for(int i=0;i<n;i++) basis[i]=(F)rng();
    lab.resize(N); for(int v=0;v<N;v++){F x=0; for(int i=0;i<n;i++) if(v>>i&1) x^=basis[i]; lab[v]=x;}
    // enumerate T's (Gosper)
    {
        uint64_t m=(1ULL<<c)-1, lim=1ULL<<N;
        while(m<lim){ Ts.push_back((uint32_t)m); uint64_t u=m&-m,v=m+u; m=v|(((v^m)/u)>>2); }
    }
    int M=Ts.size(); Lc.resize(M); for(int i=0;i<M;i++) locator(Ts[i],Lc[i]);
    // same-top classes: top g-1 coefficients below the leading one of L_T
    {
        map<vector<F>,int> cls; for(int i=0;i<M;i++){ vector<F> key; for(int j=0;j<g-1;j++) key.push_back(Lc[i][c-1-j]); cls[key]++; }
        int mx=0; map<int,int> h; for(auto&kv:cls){ mx=max(mx,kv.second); h[kv.second]++; }
        printf("n=%d g=%d N=%d D=%d c=%d T-sets=%d  same-top classes=%d  largest=%d\n",n,g,N,D,c,M,(int)cls.size(),mx);
        int shown=0; for(auto it=h.rbegin();it!=h.rend()&&shown<6;++it,++shown) printf("  same-top size %d : %d classes\n",it->first,it->second);
    }
    int mfree=(LEN-1)/(g-1);
    printf("LEN=%d mfree=%d\n",LEN,mfree);
    map<int,uint64_t> hist; int bestD=0; vector<F> P;
    for(uint64_t it=0;it<tries;it++){
        vector<vector<F>> rows;
        for(int k=0;k<mfree;k++){ int j=rng()%M; const vector<F>&L=Lc[j]; for(int i=0;i<=g-2;i++){ vector<F> r(LEN,0); for(int q=0;q<=c;q++) r[i+q]=L[q]; rows.push_back(r);} }
        auto ns=nullspace(rows);
        if(ns.empty()) continue;
        vector<F> lam(LEN,0);
        for(auto&v:ns){ F co=(F)rng(); for(int j=0;j<LEN;j++) lam[j]^=mul(co,v[j]); }
        vector<uint32_t> supps; int zeros=0;
        for(int i=0;i<M;i++){ if(!member(lam,Lc[i])) continue; zeros++;
            uint32_t sup=0; for(int t=0;t<N;t++) if(Ts[i]>>t&1){ locator(Ts[i]&~(1u<<t),P); F s=0; for(size_t j=0;j<P.size();j++) s^=mul(lam[j],P[j]); if(s) sup|=1u<<t; }
            supps.push_back(sup); }
        sort(supps.begin(),supps.end()); supps.erase(unique(supps.begin(),supps.end()),supps.end());
        int dist=supps.size();
        hist[dist]++;
        if(dist>bestD||dist>=dump){ if(dist>bestD) bestD=dist; printf("it=%llu distinct=%d zeros=%d lam:",(unsigned long long)it,dist,zeros); for(F x:lam) printf(" %08x",x); printf("\n"); fflush(stdout);}
    }
    for(auto&kv:hist) printf("distinct=%d : %llu\n",kv.first,(unsigned long long)kv.second);
}
