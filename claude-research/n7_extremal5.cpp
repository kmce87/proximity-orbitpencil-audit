// N7: exhaustive extremal test at n=5.  All real-root members at agreement >=19 (of 32), degree bound D=16:
// phi = 1_S (|S|=20) or phi = 1_S + delta_y (|S|=19, y in S).  mass 20, gap 4, so the class of the word is (e1,e2,e3)(phi).
// Output: largest number of distinct polynomials per class, i.e. the largest real-root list at agreement >=19.
// Also the same with mass-only (no doubles), to compare with the plain same-top list.
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
static inline F mul(F a,F b){
    __m128i A=_mm_cvtsi32_si128((int)a),B=_mm_cvtsi32_si128((int)b);
    __m128i C=_mm_clmulepi64_si128(A,B,0);
    uint64_t r=_mm_cvtsi128_si64(C);
    while(r>>32){ uint64_t hi=r>>32; r=(r&0xffffffffULL)^hi^(hi<<1)^(hi<<2)^(hi<<22); }
    return (F)r;
}
static const int N=32;
static F lab[N];
struct Ent{F a,b,c; uint32_t bool20,dbl;};
static vector<Ent> tab; static uint64_t MASK; static uint64_t used=0;
static inline void add(F e1,F e2,F e3,int isbool){
    uint64_t h=e1; h=h*0x9E3779B97F4A7C15ULL^e2; h=h*0xBF58476D1CE4E5B9ULL^e3; h^=h>>29; h*=0x94D049BB133111EBULL; h^=h>>31;
    uint64_t i=h&MASK;
    while(true){ Ent&t=tab[i]; if(t.bool20==0&&t.dbl==0){ t.a=e1;t.b=e2;t.c=e3; used++; if(isbool)t.bool20=1; else t.dbl=1; return; } if(t.a==e1&&t.b==e2&&t.c==e3){ if(isbool)t.bool20++; else t.dbl++; return; } i=(i+1)&MASK; }
}
static int want; static int stk[32];
static void dfs(int start,int cnt,F e1,F e2,F e3){
    if(cnt==want){
        if(want==20){ add(e1,e2,e3,1); return; }
        for(int k=0;k<cnt;k++){ F y=lab[stk[k]]; add(e1^y,e2^mul(e1,y),e3^mul(e2,y),0); }
        return;
    }
    if(N-start<want-cnt) return;
    for(int v=start;v<N;v++){ F x=lab[v]; stk[cnt]=v; dfs(v+1,cnt+1,e1^x,e2^mul(e1,x),e3^mul(e2,x)); }
}
int main(int argc,char**argv){
    uint64_t seed=atoll(argv[1]); mt19937_64 rng(seed);
    F basis[5]; for(int i=0;i<5;i++) basis[i]=(F)rng();
    if(seed==0) for(int i=0;i<5;i++) basis[i]=1u<<i;
    for(int v=0;v<N;v++){F x=0; for(int i=0;i<5;i++) if(v>>i&1) x^=basis[i]; lab[v]=x;}
    int bits=26; MASK=(1ULL<<bits)-1; tab.assign(1ULL<<bits,Ent{0,0,0,0,0});
    want=20; dfs(0,0,0,0,0); printf("boolean done, classes=%llu\n",(unsigned long long)used); fflush(stdout);
    want=19; dfs(0,0,0,0,0); printf("doubles done, classes=%llu\n",(unsigned long long)used); fflush(stdout);
    map<uint32_t,long> h; uint32_t mx=0,mxb=0; Ent best{0,0,0,0,0};
    for(auto&t:tab){ uint32_t s=t.bool20+t.dbl; if(!s) continue; h[s]++; if(s>mx){mx=s;best=t;} mxb=max(mxb,t.bool20); }
    printf("largest real-root list at agreement>=19: %u (of which boolean 20-sets %u, doubles %u); largest purely boolean list: %u\n",mx,best.bool20,best.dbl,mxb);
    printf("key %08x %08x %08x\n",best.a,best.b,best.c);
    int shown=0; for(auto it=h.rbegin();it!=h.rend()&&shown<12;++it,++shown) printf(" size %u : %ld classes\n",it->first,it->second);
}
