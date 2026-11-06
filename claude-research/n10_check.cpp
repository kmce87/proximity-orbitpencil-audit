// N10 check build: same DFS as n10_class, and at each member with phi <= 2 above 9N/16 tests the statements of Theory run 8 exactly.
// N10: unbiased exact census of ONE class (coset of L = {d: V->Z, mean 0, Fourier in (1/4)Z}), any integer representative.
// Input: n, file with N integers rho(x) (mean 1/8, any sign), Phi (cap on phi_max used only for the budget), optional k cap.
// g = 1/2 + rho, reduced to the minimal residue g_min (all |r| <= 1/8), member = g_min + (1/4) sum a_chi chi, a integer.
// Budget (exact identity): sum (a^2 + 8 r a) = 16 (var phi - var g_min), var phi = 15/64 + 2 O', O' = E[C(phi,2)] <= (Phi/2) O < Phi/32 when phi <= Phi.
// DFS over characters sorted by minimal cost, integer arithmetic (costs scaled by N).  Every a-vector is visited once; each gives one phi.
// Output: members with |supp| > 9N/16 and = 9N/16, split by number of nonzero a, by phi_max.  Usage: n10_class n file Phi [quiet]
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <algorithm>
#include <map>
using namespace std;
static int n,N; static vector<int> G; // 4 g_min(x)
static vector<vector<int8_t>> chi; static vector<long long> Wm; static vector<int> order_, pos;
static int lam, sumtarget; static long long ucap; static long long leaves=0;
static long long gt[32],eqc[32],gtphi[32]; static int t916; static int8_t Tbuf[64][4096];
static map<vector<pair<int,int>>,int> dummy;
static inline long long costf(int c,int a){ return (long long)N*a*a+2*a*Wm[c]; }
static int stC[64],stA[64]; static long long Qglob; static long long viol[8],tested[8]; static vector<int> aOf;
static void checks(const int8_t*T,int k,int sup){
    // A+ and A-
    vector<int> Am,Ap; for(int i=0;i<k;i++){ int c=stC[i],a=stA[i]; bool opp=(a*Wm[c]<0)||Wm[c]==0; if(abs(a)==1&&opp&&10*llabs(Wm[c])>=N) Ap.push_back(i); else Am.push_back(i); }
    long long Ocount=0,C2=0; for(int x=0;x<N;x++){ int p=(G[x]+T[x])/4; if(p>=2) Ocount+=p-1; C2+=p*(p-1)/2; }
    // units identity
    long long U=0; for(int i=0;i<k;i++) U+=costf(stC[i],stA[i]); tested[0]++; if(U!=10LL*N+32*C2-Qglob) viol[0]++;
    tested[1]++; if(Am.size()>4) viol[1]++;
    for(size_t i=0;i<Am.size();i++) if(abs(stA[Am[i]])>=2 && Am.size()>3) viol[1]++;
    if(Am.size()!=4) return;
    int xr=0,all1=1; for(int i:Am){ if(abs(stA[i])!=1) all1=0; xr^=stC[i]; }
    if(!all1) return;
    int ch[4],ep[4]; for(int j=0;j<4;j++){ ch[j]=stC[Am[j]]; ep[j]=stA[Am[j]]; }
    fill(aOf.begin(),aOf.end(),0); for(int i=0;i<k;i++) aOf[stC[i]]=stA[i];
    auto hatN=[&](int c){ return Wm[c]+(long long)aOf[c]*N; }; // 4N * hat(phi)(c)
    if(xr==0){
        int s4=ep[0]+ep[1]+ep[2]+ep[3];
        if(((s4%4)+4)%4==2){ // Boolean C: 1_C = 1/2 + T4/4
            long long pp=0,d2=0; long long sumEW=0; for(int j=0;j<4;j++) sumEW+=ep[j]*Wm[ch[j]];
            bool bad=false; for(int x=0;x<N;x++){ int t4=0; for(int j=0;j<4;j++) t4+=ep[j]*chi[ch[j]][x]; int inC=(2+t4)/4; if(t4!=2&&t4!=-2) bad=true; int p=(G[x]+T[x])/4; int rho=p-inC; if(rho==-1) pp++; if(rho==2) d2++; }
            tested[2]++; if(bad) viol[2]++; if(16*Ocount!=N+sumEW+16*(pp+d2)) viol[2]++;
            // q < -kappa
            tested[3]++; if(!(16*(pp+d2) < -sumEW)) viol[3]++;
        } else { // T4 = 0 mod 4: at least two of the three remaining products of the 2-flat have |r| >= 1/40 (10*|Wm| >= N)
            int prod[3]={ch[0]^ch[1],ch[0]^ch[2],ch[0]^ch[3]}; int big=0; for(int j=0;j<3;j++) if(10*llabs(Wm[prod[j]])>=N) big++;
            tested[4]++; if(big<2) viol[4]++;
        }
    } else {
        // independent? then every triple has a product with |hat| > (1/8 - s_triple)/4
        int idx[4][3]={{0,1,2},{0,1,3},{0,2,3},{1,2,3}};
        bool indep=true; { int b[4]; int rk=0; for(int j=0;j<4;j++){ int v=ch[j]; for(int q=0;q<rk;q++) if((v^b[q])<v) v^=b[q]; if(v) b[rk++]=v; } if(rk<4) indep=false; }
        if(indep) for(auto&tr:idx){ int c1=ch[tr[0]],c2=ch[tr[1]],c3=ch[tr[2]]; long long s=0; for(int q=0;q<3;q++){ int j=tr[q]; if(ep[j]*Wm[ch[j]]<0) s+=llabs(Wm[ch[j]]); }
            int pr[4]={c1^c2,c1^c3,c2^c3,c1^c2^c3}; long long tot=0; for(int q=0;q<4;q++) tot+=llabs(hatN(pr[q])); // sum |hat(p)| * 4N
            // need sum_p |hat(p)| >= 1/8 - s_triple, in units 4N: N/2 - s
            tested[5]++; if(tot<N/2-s) viol[5]++; }
    }
}
static inline void leaf(const int8_t*T,int k){
    leaves++;
    int sup=0,mx=0; for(int x=0;x<N;x++){ int p=G[x]+T[x]; if(p<0) return; if(p>0) sup++; if(p>mx) mx=p; }
    if(sup>t916){ gt[k]++; gtphi[mx/4]++; if(mx<=8) checks(T,k,sup); } else if(sup==t916) eqc[k]++;
}
static void push(int d,int c,int a){ const int8_t*s=Tbuf[d]; int8_t*t=Tbuf[d+1]; const int8_t*h=chi[c].data(); for(int x=0;x<N;x++) t[x]=s[x]+a*h[x]; }
static void dfs(int d,int idx,long long used,int xr,int sumA,int k){
    if(xr==lam && ((sumA-sumtarget)&3)==0) leaf(Tbuf[d],k);
    int M=order_.size(); if(idx>=M) return;
    long long rem=ucap-used; long long cnext=N-2*llabs(Wm[order_[idx]]);
    if(cnext>rem) return;
    if(2*cnext>rem){ // at most one more character can be afforded
        if(xr!=lam){ int c=xr^lam; if(pos[c]>=idx) for(int a:{1,-1,3,-3}){ long long cc=costf(c,a); if(cc<=rem && (((sumA+a)-sumtarget)&3)==0){ push(d,c,a); stC[k]=c; stA[k]=a; leaf(Tbuf[d+1],k+1);} } }
        else if(rem>=2LL*N){ for(int i=idx;i<M;i++){ int c=order_[i]; for(int a:{2,-2}){ long long cc=costf(c,a); if(cc<=rem && (((sumA+a)-sumtarget)&3)==0){ push(d,c,a); leaf(Tbuf[d+1],k+1);} } } }
        return;
    }
    for(int i=idx;i<M;i++){ int c=order_[i]; long long cm=N-2*llabs(Wm[c]); if(cm>rem) break;
        for(int a:{1,-1,2,-2,3,-3}){ long long cc=costf(c,a); if(cc>rem) continue; push(d,c,a); stC[k]=c; stA[k]=a; dfs(d+1,i+1,used+cc,(a&1)?(xr^c):xr,sumA+a,k+1); }
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); N=1<<n; int Phi=atoi(argv[3]); bool quiet=argc>4; t916=9*N/16;
    vector<int> rho(N); FILE*f=fopen(argv[2],"r"); for(int i=0;i<N;i++) if(fscanf(f,"%d",&rho[i])!=1){ fprintf(stderr,"short file\n"); return 1; } fclose(f);
    long long s=0; for(int x:rho) s+=x; if(s!=N/8){ fprintf(stderr,"mass %lld != N/8\n",s); return 1; }
    chi.assign(N,vector<int8_t>(N)); for(int c=0;c<N;c++) for(int x=0;x<N;x++) chi[c][x]=__builtin_parity(c&x)?-1:1;
    G.resize(N); for(int x=0;x<N;x++) G[x]=2+4*rho[x];
    // Walsh of 4g
    auto walsh=[&](vector<long long> v){ for(int b=0;b<n;b++) for(int i=0;i<N;i++) if(i>>b&1){ long long p=v[i^(1<<b)],q=v[i]; v[i^(1<<b)]=p+q; v[i]=p-q; } return v; };
    vector<long long> Wv(N); for(int i=0;i<N;i++) Wv[i]=G[i]; Wv=walsh(Wv);
    // minimal residue: hat = W/(4N); a0 = nearest integer of W/N (W/(4N) = a0/4 + r, |r| <= 1/8 <=> |W - a0 N| <= N/2)
    vector<int> T0(N,0); for(int c=1;c<N;c++){ long long w=Wv[c]; long long a0=(w>=0)?((2*w+N)/(2*N)):-((-2*w+N)/(2*N)); if(a0) for(int x=0;x<N;x++) T0[x]+=a0*chi[c][x]; }
    for(int x=0;x<N;x++){ if((T0[x]&0)!=0) {} G[x]-=T0[x]; }
    vector<long long> Gv(N); for(int i=0;i<N;i++) Gv[i]=G[i]; Wm=walsh(Gv);
    long long Q=0; for(int x=0;x<N;x++) Q+=(long long)G[x]*G[x];
    for(int c=1;c<N;c++) if(llabs(Wm[c])*2>N){ fprintf(stderr,"residue not minimal\n"); return 1; }
    ucap=(10+Phi)*(long long)N-Q; Qglob=Q; aOf.assign(N,0); // scaled by N
    // integrality data
    if(((G[0]%2)+2)%2 != ((G[1]%2)+2)%2) { fprintf(stderr,"parity\n"); return 1; }
    lam=0; for(int b=0;b<n;b++){ int dd=G[1<<b]-G[0]; if(dd%2){ fprintf(stderr,"odd difference\n"); return 1; } if(((dd/2)%2+2)%2) lam|=1<<b; }
    sumtarget=((-G[0])%4+4)%4;
    order_.clear(); for(int c=1;c<N;c++) order_.push_back(c);
    sort(order_.begin(),order_.end(),[&](int a,int b){ long long ca=N-2*llabs(Wm[a]),cb=N-2*llabs(Wm[b]); if(ca!=cb) return ca<cb; return a<b; });
    pos.assign(N,0); for(size_t i=0;i<order_.size();i++) pos[order_[i]]=i;
    memset(Tbuf,0,sizeof Tbuf);
    int nt=0,nb=0; for(int c:order_){ if(2*llabs(Wm[c])==N) nt++; if(56*llabs(Wm[c])>=4*N) nb++; }
    dfs(0,0,0,0,0,0);
    long long tg=0,te=0; for(int i=0;i<32;i++){ tg+=gt[i]; te+=eqc[i]; }
    unsigned long long g2=((1ULL<<n)-1)*((1ULL<<(n-1))-1)/3; unsigned long long MC=8*g2*((1ULL<<(n-2))-1);
    printf("n=%d file=%s Phi=%d var*64=%.3f lambda=%d ties=%d big=%d ucap/N=%.3f MC/2=%llu | gt=%lld eq=%lld frac=%.4f | by k:",n,argv[2],Phi,((double)Q/N/16-25.0/64)*64,lam,nt,nb,(double)ucap/N,MC/2,tg,te,(double)tg/(MC/2));
    for(int i=0;i<32;i++) if(gt[i]||eqc[i]) printf(" %d:%lld/%lld",i,gt[i],eqc[i]);
    printf(" | phimax:"); for(int i=0;i<32;i++) if(gtphi[i]) printf(" %d:%lld",i,gtphi[i]);
    printf(" | leaves=%lld\n",leaves); const char*nm[6]={"units","j<=4","(*)","q<-kappa","T4=0mod4","triple"}; printf("  checks:"); for(int i=0;i<6;i++) printf(" %s %lld/%lld",nm[i],viol[i],tested[i]); printf("\n");
    return 0;
}
