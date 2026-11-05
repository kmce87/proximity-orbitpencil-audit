// N7 small exact checks, field GF(2^32), labels random independent (mode k: Krylov labels 1,x,x^2,... with x=2).
// mobius n seed : m* = largest number of disjoint pairs {a,b} of V swapped by one non-translation Moebius involution (a+l)(b+l)=mu.
// sametop n s seed : largest same-top class (top s-D-1 coefficients below the leading one) among s-subsets, gap g=s-D, exhaustive DFS, for n=5.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
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
int n,N; vector<F> lab;
static unordered_map<uint64_t,uint32_t> cls;
static int K_,tA;
static inline uint64_t mix(F a,F b,F c){ uint64_t h=a; h=h*0x9E3779B97F4A7C15ULL^b; h=h*0xBF58476D1CE4E5B9ULL^c; h^=h>>29; return h; }
static void dfs(int start,int cnt,F e1,F e2,F e3){
    if(cnt==K_){ cls[mix(e1,e2,e3)]++; return; }
    if(N-start<K_-cnt) return;
    for(int v=start;v<N;v++){ F x=lab[v]; dfs(v+1,cnt+1,e1^x,e2^mul(e1,x),e3^mul(e2,x)); }
}
int main(int argc,char**argv){
    string mode=argv[1]; n=atoi(argv[2]); N=1<<n;
    uint64_t seed=atoll(argv[argc-1]); mt19937_64 rng(seed);
    vector<F> basis(n); for(int i=0;i<n;i++) basis[i]=(F)rng();
    lab.resize(N); for(int v=0;v<N;v++){F x=0; for(int i=0;i<n;i++) if(v>>i&1) x^=basis[i]; lab[v]=x;}
    if(mode=="mobius"){
        // all pairs of disjoint pairs define (l,mu); hash and count
        map<pair<F,F>,vector<pair<int,int>>> inv_;
        vector<pair<int,int>> pr; for(int a=0;a<N;a++) for(int b=a+1;b<N;b++) pr.push_back({a,b});
        int mstar=0; map<int,long> h;
        for(size_t i=0;i<pr.size();i++) for(size_t j=i+1;j<pr.size();j++){
            int a=pr[i].first,b=pr[i].second,c=pr[j].first,d=pr[j].second; if(a==c||a==d||b==c||b==d) continue;
            F den=lab[a]^lab[b]^lab[c]^lab[d]; if(!den) continue; // translation type
            F l=mul(mul(lab[a],lab[b])^mul(lab[c],lab[d]),inv(den));
            F mu=mul(lab[a]^l,lab[b]^l);
            if(!mu) continue; // star, collapse case
            inv_[{l,mu}].push_back({(int)i,(int)j});
        }
        for(auto&kv:inv_){ // number of pairs swapped: incident pair indices
            vector<int> s; for(auto&p:kv.second){ s.push_back(p.first); s.push_back(p.second);} sort(s.begin(),s.end()); s.erase(unique(s.begin(),s.end()),s.end());
            int m=s.size(); h[m]++; mstar=max(mstar,m);
        }
        printf("n=%d seed=%llu m*=%d histogram:",n,(unsigned long long)seed,mstar); for(auto&kv:h) printf(" %d:%ld",kv.first,kv.second); printf("\n");
    } else if(mode=="sametop"){
        int s=atoi(argv[3]); K_=s;
        cls.reserve(1<<22);
        dfs(0,0,0,0,0);
        uint32_t mx=0; for(auto&kv:cls) mx=max(mx,kv.second);
        map<uint32_t,long> h; for(auto&kv:cls) h[kv.second]++;
        printf("n=%d |S|=%d classes(e1,e2,e3)=%zu largest=%u ; top:",n,s,cls.size(),mx); int shown=0; for(auto it=h.rbegin();it!=h.rend()&&shown<5;++it,++shown) printf(" %u:%ld",it->first,it->second); printf("\n");
    }
}
