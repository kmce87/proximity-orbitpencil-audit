// N9 census: fixed B, |B| = N/8.  Count integer h, mean 1/2, Fourier in (1/4)Z, with phi = 1_B + h >= 0, by type, split by
// agreement |supp phi| > 9N/16 ("gt") and = 9N/16 ("eq", only for the types enumerated here: rank-7 m=8 alternatives are not listed).
// Types (see n9_types): T4 = 2-flat of characters (Boolean), T2 = hyperplane, 6a = (m=6,r=5,t=1), 6b = (m=6,r=4,t=1),
// 8a = (m=8,r=6,t=5), 8b = (m=8,r=5,t=3), 8c = (m=8,r=4,t=2), 8d = r=3, h=-1 on one coset.  Here t = number of W'-cosets with h = -1, W' = kernel.
// Usage: census n spec seed [extra]   spec = flat | random | halfflat | threeq | nearflat | frame | file
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <map>
#include <set>
#include <array>
#include <random>
#include <algorithm>
#include <string>
#include <ctime>
using namespace std;
static int n,N;
static vector<uint8_t> inB; static vector<int> Bl; static vector<int> rho; static vector<int> Pl; // rho = integer rep of mean 1/8; Bl = {rho>=1}, Pl = {rho=-1}
struct Pat{ int m,r,t; vector<array<int8_t,64>> h; };
static Pat P6a,P6b,P8a,P8b,P8c,P8d;
static int par(int x){return __builtin_parity(x);}
static int rankof(const vector<int>&a){ vector<int> b; for(int x:a){ for(int y:b) if((x^y)<x) x^=y; if(x){b.push_back(x);} } return b.size(); }
// brute pattern, E' (h=-1 set) must equal canon, canon contains 0
static void build(Pat&P,int m,int r,vector<int> canon){
    P.m=m;P.r=r;P.t=canon.size(); int R=1<<r; uint64_t cm=0; for(int c:canon) cm|=1ULL<<c;
    vector<int> a(m);
    // DFS over increasing chars
    struct S{ static void go(Pat&P,int m,int r,uint64_t cm,vector<int>&a,int k,int minv,int sum){
        int R=1<<r;
        if(k==m-1){ if(sum<minv||sum==0) return; a[m-1]=sum; if(rankof(a)!=r) return;
            // sign offsets: b with wt(b)=wt at point 0 equal to value giving h=-1:  m=6: wt 6, m=8: wt 7
            int want=(m==6)?6:7;
            for(int z=0;z<(want==m?1:m);z++){ int b=((1<<m)-1); if(want!=m) b^=(1<<z);
                array<int8_t,64> H; H.fill(0); uint64_t em=0; int y=0; bool ok=true;
                for(int v=0;v<R;v++){ int wt=0; for(int i=0;i<m;i++) wt+=par(a[i]&v)^((b>>i)&1); int num=2+m-2*wt; if(num%4){ok=false;break;} int hh=num/4; H[v]=hh; if(hh==-1) em|=1ULL<<v; if(hh==2) y++; if(hh>2||hh<-1) ok=false; }
                if(!ok) continue; if(em!=cm) continue; if(16*y>=R) continue;
                P.h.push_back(H);
            }
            return; }
        for(int x=minv;x<R;x++){ a[k]=x; go(P,m,r,cm,a,k+1,x+1,sum^x); }
    }};
    S::go(P,m,r,cm,a,0,1,0);
}
// explicit (m=8,r=6,t=5): canonical frame {0,e1,e2,e3,e4}
static void build8a(){
    Pat&P=P8a; P.m=8;P.r=6;P.t=5; int R=64;
    int pts[5]={0,1,2,4,8};
    for(int ext=0;ext<256;ext++){
        int a[8],b[8];
        int e[5]; int sum=0; for(int j=0;j<4;j++){ e[j]=(ext>>(2*j))&3; sum^=e[j]; } e[4]=sum;
        for(int j=0;j<5;j++){ b[j]=(j==0)?0:1; int aj=0; for(int k=1;k<=4;k++){ int val=(k==j)?0:1; if(((val^b[j])&1)) aj|=1<<(k-1);} aj|=e[j]<<4; a[j]=aj; }
        // triple
        a[5]=1<<4;a[6]=1<<5;a[7]=3<<4; b[5]=b[6]=b[7]=1;
        int s=0; for(int i=0;i<8;i++) s^=a[i]; if(s) continue; // sum of the first 4 coordinates is zero by construction, ext coordinates by choice of e[4]
        bool distinct=true; for(int i=0;i<8;i++){ if(a[i]==0) distinct=false; for(int k=0;k<i;k++) if(a[i]==a[k]) distinct=false; }
        if(!distinct) continue;
        vector<int> av(a,a+8); if(rankof(av)!=6) continue;
        array<int8_t,64> H; H.fill(0); int x=0,y=0; uint64_t em=0;
        for(int v=0;v<R;v++){ int wt=0; for(int i=0;i<8;i++) wt+=par(a[i]&v)^b[i]; int hh=(10-2*wt)/4; H[v]=hh; if(hh==-1){x++; em|=1ULL<<v;} if(hh==2) y++; }
        if(x!=5||y!=3) continue;
        bool cn=true; for(int q=0;q<5;q++) if(!(em>>pts[q]&1)) cn=false; if(!cn) continue;
        P.h.push_back(H);
    }
}
static void build8d(){ // all h on F_2^3, h(0)=-1, others in {0,1}, sum 4.  Fourier automatically in (1/4)Z.
    Pat&P=P8d; P.m=8;P.r=3;P.t=1;
    for(int mask=0;mask<128;mask++){ if(__builtin_popcount(mask)!=5) continue; array<int8_t,64> H; H.fill(0); H[0]=-1; for(int i=0;i<7;i++) H[i+1]=(mask>>i)&1; P.h.push_back(H);}
}
// counters
static long long gt[8],eq[8];
enum{T4=0,T2=1,T6A=2,T6B=3,T8A=4,T8B=5,T8C=6,T8D=7};
static const char*names[8]={"T4","T2","6a","6b","8a","8b","8c","8d"};
static void count_pat(const Pat&P,int ty,const vector<int>&cA,const vector<int>&cP,int d){
    // cA[x] = #{rho>=1} in the coset, cP[x] = #{rho=-1} in the coset
    int R=1<<P.r, sz=1<<d;
    for(const auto&H:P.h){ long long ag=0; bool pos=true; for(int x=0;x<R;x++){ int hh=H[x]; if(hh>=2) ag+=sz; else if(hh==1) ag+=sz-cP[x]; else if(hh==0){ if(cP[x]) {pos=false;break;} ag+=cA[x]; } else { if(cA[x]!=sz){pos=false;break;} } }
        if(!pos) continue;
        long long t=9LL*N/16; if(ag>t) gt[ty]++; else if(ag==t) eq[ty]++; }
}
// process direction W (RREF basis, dim d), full cosets known through recomputation
static void process(const vector<int>&W){
    int d=W.size(); int r=n-d; if(r<3||r>6) return; int R=1<<r;
    int pivmask=0; for(int w:W) pivmask|=1<<(31-__builtin_clz(w));
    vector<int> np; for(int i=0;i<n;i++) if(!(pivmask>>i&1)) np.push_back(i);
    auto red=[&](int v){ for(int w:W){ int p=31-__builtin_clz(w); if(v>>p&1) v^=w; } int u=0; for(int i=0;i<(int)np.size();i++) if(v>>np[i]&1) u|=1<<i; return u; };
    vector<int> cnt(R,0),cntP(R,0); for(int v:Bl) cnt[red(v)]++; for(int v:Pl) cntP[red(v)]++;
    vector<int> F; int sz=1<<d; for(int u=0;u<R;u++) if(cnt[u]==sz) F.push_back(u);
    if(F.empty()) return;
    auto runPat=[&](const Pat&P,int ty){ int t=P.t; if((int)F.size()<t) return;
        vector<int> idx(t); for(int i=0;i<t;i++) idx[i]=i;
        while(true){
            // affine map from canonical (0,e1..e_{t-1}) to the chosen cosets
            int p0=F[idx[0]]; vector<int> g; vector<int> ech; bool ok=true;
            for(int i=1;i<t;i++){ int x=F[idx[i]]^p0; g.push_back(x); int y=x; for(int z:ech) if((y^z)<y) y^=z; if(!y){ok=false;break;} ech.push_back(y); sort(ech.rbegin(),ech.rend()); }
            if(ok){ for(int b=0;b<r&&(int)g.size()<r;b++){ int x=1<<b,y=x; for(int z:ech) if((y^z)<y) y^=z; if(y){ g.push_back(x); ech.push_back(y); sort(ech.rbegin(),ech.rend()); } }
                vector<int> cA(R),cP(R); for(int x=0;x<R;x++){ int u=p0; for(int i=0;i<r;i++) if(x>>i&1) u^=g[i]; cA[x]=cnt[u]; cP[x]=cntP[u]; }
                count_pat(P,ty,cA,cP,d); }
            int i=t-1; while(i>=0&&idx[i]==(int)F.size()-t+i) i--; if(i<0) break; idx[i]++; for(int k=i+1;k<t;k++) idx[k]=idx[k-1]+1;
        }
    };
    if(r==6){ runPat(P8a,T8A); }
    if(r==5){ runPat(P6a,T6A); runPat(P8b,T8B); }
    if(r==4){ runPat(P6b,T6B); runPat(P8c,T8C); }
    if(r==3){ runPat(P8d,T8D); }
}
// RREF insert: returns new basis (sorted by decreasing pivot), u reduced nonzero
static vector<int> addvec(vector<int> W,int u){ for(int w:W){ int p=31-__builtin_clz(w); if(u>>p&1) u^=w; } int pu=31-__builtin_clz(u); for(int&w:W) if(w>>pu&1) w^=u; W.push_back(u); sort(W.rbegin(),W.rend()); return W; }
static void flats(){
    map<vector<int>,vector<int>> cur; // direction -> minimal reps of cosets inside B
    { vector<int> W; cur[W]=Bl; }
    for(int d=0;d<=n-3;d++){
        for(auto&kv:cur) process(kv.first);
        if(d==n-3) break;
        map<vector<int>,set<int>> nxt;
        for(auto&kv:cur){ const vector<int>&W=kv.first; const vector<int>&R=kv.second;
            auto red=[&](int v){ for(int w:W){ int p=31-__builtin_clz(w); if(v>>p&1) v^=w; } return v; };
            for(size_t i=0;i<R.size();i++) for(size_t j=i+1;j<R.size();j++){ int u=red(R[i]^R[j]); if(!u) continue; vector<int> W2=addvec(W,u);
                int v=R[i]; for(int w:W2){ int p=31-__builtin_clz(w); if(v>>p&1) v^=w; } nxt[W2].insert(v); }
        }
        cur.clear(); for(auto&kv:nxt) cur[kv.first]=vector<int>(kv.second.begin(),kv.second.end());
        if(cur.empty()) break;
    }
}
static vector<int> walsh_of(const vector<int>&L){ vector<int> W(N,0); for(int v:L) W[v]=1; for(int b=0;b<n;b++) for(int i=0;i<N;i++) if(i>>b&1){ int x=W[i^(1<<b)],y=W[i]; W[i^(1<<b)]=x+y; W[i]=x-y; } return W; }
static void quadrics(){
    // h = 1_C: phi = rho + 1_C >= 0 iff {rho=-1} is inside C; agreement = |C| - |P| + |B+| - |C cap B+|
    vector<int> W=walsh_of(Bl),WP=walsh_of(Pl); long long t=9LL*N/16; int bs=Bl.size(),ps=Pl.size();
    for(int a=1;a<N;a++) for(int s=-1;s<=1;s+=2){ long long tw=bs+s*W[a]; long long ov=tw/2; long long twp=ps+s*WP[a]; if(twp/2!=ps) continue; long long ag=bs+N/2-ov-ps; if(ag>t) gt[T2]++; else if(ag==t) eq[T2]++; }
    for(int pu=1;pu<n;pu++) for(int pw=0;pw<pu;pw++){
        for(int u=(1<<pu);u<(2<<pu);u++){ if(u>>pw&1) continue; for(int w=(1<<pw);w<(2<<pw);w++){
            for(int a=1;a<N;a++){ if(a&(1<<pu)) continue; if(a&(1<<pw)) continue;
                int A[4]={a,a^u,a^w,a^u^w}; int wa[4]={W[A[0]],W[A[1]],W[A[2]],W[A[3]]}; int wp[4]={WP[A[0]],WP[A[1]],WP[A[2]],WP[A[3]]};
                for(int sg=0;sg<16;sg++){ if(__builtin_popcount(sg)%2==0) continue; int sum=0,sump=0; for(int i=0;i<4;i++){ sum+=(sg>>i&1)?-wa[i]:wa[i]; sump+=(sg>>i&1)?-wp[i]:wp[i]; }
                    if(ps && (2LL*ps+sump)/4!=ps) continue;
                    long long fourov=2LL*bs+sum; if(fourov%4){ fprintf(stderr,"nonint\n"); exit(1);} long long ov=fourov/4; long long ag=bs+N/2-ov-ps; if(ag>t) gt[T4]++; else if(ag==t) eq[T4]++; }
            } } }
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); string spec=argv[2]; uint64_t seed=argc>3?atoll(argv[3]):1; int extra=argc>4?atoi(argv[4]):0; N=1<<n; mt19937_64 rng(seed); int bs=N/8;
    inB.assign(N,0); vector<int> perm(N); for(int i=0;i<N;i++) perm[i]=i;
    auto shuf=[&](vector<int>&v){ shuffle(v.begin(),v.end(),rng); };
    if(spec=="flat"){ for(int i=0;i<bs;i++) inB[i]=1; }
    else if(spec=="random"){ shuf(perm); for(int i=0;i<bs;i++) inB[perm[i]]=1; }
    else if(spec=="halfflat"){ vector<int> c; for(int i=0;i<N/4;i++) c.push_back(i); shuf(c); for(int i=0;i<bs;i++) inB[c[i]]=1; }
    else if(spec=="threeq"){ for(int i=0;i<bs;i++) if(i<3*bs/4) inB[i]=1; vector<int> c; for(int i=bs;i<N;i++) c.push_back(i); shuf(c); for(int i=0;i<bs/4;i++) inB[c[i]]=1; }
    else if(spec=="nearflat"){ for(int i=0;i<bs;i++) inB[i]=1; vector<int> a,b; for(int i=0;i<bs;i++) a.push_back(i); for(int i=bs;i<N;i++) b.push_back(i); shuf(a);shuf(b); for(int i=0;i<extra;i++){ inB[a[i]]=0; inB[b[i]]=1; } }
    else if(spec=="frame"){ // 5 affinely independent cosets of a codim-6 subspace + 3 random cosets
        int sz=N/64; int fr[5]={0,1,2,4,8}; for(int q=0;q<5;q++) for(int i=0;i<sz;i++) inB[(fr[q]<<(n-6))|i]=1; vector<int> c; for(int u=0;u<64;u++){ bool used=false; for(int q=0;q<5;q++) if(fr[q]==u) used=true; if(!used) c.push_back(u);} shuf(c); for(int q=0;q<3;q++) for(int i=0;i<sz;i++) inB[(c[q]<<(n-6))|i]=1; }
    else if(spec=="file"){ FILE*f=fopen(argv[4],"r"); int x; while(fscanf(f,"%d",&x)==1) inB[x]=1; fclose(f); }
    else if(spec=="signed"){ shuf(perm); for(int i=0;i<bs+extra;i++) inB[perm[i]]=1; for(int i=bs+extra;i<bs+2*extra;i++) Pl.push_back(perm[i]); }
    else if(spec=="signedflat"){ for(int i=0;i<bs;i++) inB[i]=1; vector<int> c; for(int i=bs;i<N;i++) c.push_back(i); shuf(c); for(int i=0;i<extra;i++) inB[c[i]]=1; for(int i=extra;i<2*extra;i++) Pl.push_back(c[i]); }
    else if(spec=="search"){ for(int i=0;i<bs;i++) inB[i]=1; }
    else if(spec=="double"){ shuf(perm); for(int i=0;i<bs-extra;i++) inB[perm[i]]=1; }
    else { fprintf(stderr,"bad spec\n"); return 1; }
    for(int i=0;i<N;i++) if(inB[i]) Bl.push_back(i);
    if(spec!="signed"&&spec!="signedflat"&&spec!="double"&&(int)Bl.size()!=bs){ fprintf(stderr,"|B| wrong %d\n",(int)Bl.size()); return 1; }
    build(P6a,6,5,{0}); build(P6b,6,4,{0}); build(P8b,8,5,{0,1,2}); build(P8c,8,4,{0,1}); build8a(); build8d();
    static bool once=false; if(!once){ fprintf(stderr,"configs per (W',E'): 6a=%zu 6b=%zu 8a=%zu 8b=%zu 8c=%zu 8d=%zu\n",P6a.h.size(),P6b.h.size(),P8a.h.size(),P8b.h.size(),P8c.h.size(),P8d.h.size()); once=true; }
    if(spec=="search"){ // argv: search seed objective(0=total_gt,1=nonBoolean only) seconds, start: random, then swaps; greedy with restarts
        int obj=extra; double limit=argc>5?atof(argv[5]):60; time_t t0=time(0); long long bestAll=-1; vector<uint8_t> bestB; int evals=0;
        auto eval=[&](const vector<uint8_t>&b)->long long{ inB=b; Bl.clear(); for(int i=0;i<N;i++) if(inB[i]) Bl.push_back(i); memset(gt,0,sizeof gt); memset(eq,0,sizeof eq); quadrics(); flats(); evals++; long long tg=0; for(int i=0;i<8;i++) if(!(obj==1&&(i==T4||i==T2))) tg+=gt[i]; return tg; };
        while(difftime(time(0),t0)<limit){
            vector<uint8_t> b(N,0); shuffle(perm.begin(),perm.end(),rng); for(int i=0;i<bs;i++) b[perm[i]]=1; long long cur=eval(b); int stall=0;
            while(stall<400&&difftime(time(0),t0)<limit){ vector<int> in,out; for(int i=0;i<N;i++) (b[i]?in:out).push_back(i); int p=in[rng()%in.size()],q=out[rng()%out.size()]; b[p]=0;b[q]=1; long long v=eval(b); if(v>=cur){ if(v>cur) stall=0; else stall++; cur=v; } else { b[p]=1;b[q]=0; stall++; } }
            if(cur>bestAll){ bestAll=cur; bestB=b; }
        }
        long long v=eval(bestB); printf("n=%d search obj=%d evals=%d best=%lld |",n,obj,evals,v); for(int i=0;i<8;i++) printf(" %s:%lld/%lld",names[i],gt[i],eq[i]); printf("\nB:"); for(int i=0;i<N;i++) if(bestB[i]) printf(" %d",i); printf("\n"); 
        // stabiliser dimension and rank of the affine span of B
        { int st=0; for(int t=1;t<N;t++){ bool ok=true; for(int v:Bl) if(!bestB[v^t]){ok=false;break;} if(ok) st++; } printf("stabiliser size %d\n",st+1); }
        return 0;
    }
    quadrics(); flats();
    long long tg=0; for(int i=0;i<8;i++) tg+=gt[i];
    unsigned long long g=((1ULL<<n)-1)*((1ULL<<(n-1))-1)/3; unsigned long long MC=8*g*((1ULL<<(n-2))-1);
    printf("n=%d %s seed=%llu extra=%d MC/2=%llu total_gt=%lld |",n,spec.c_str(),(unsigned long long)seed,extra,MC/2,tg);
    for(int i=0;i<8;i++) printf(" %s:%lld/%lld",names[i],gt[i],eq[i]); printf("\n");
    return 0;
}
