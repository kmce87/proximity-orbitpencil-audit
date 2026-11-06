// N10: unbiased exact census of ONE class (coset of L = {d: V->Z, mean 0, Fourier in (1/4)Z}), any integer representative.
// Input: n, file with N integers rho(x) (mean 1/8, any sign), Phi (cap on phi_max used only for the budget), optional k cap.
// g = 1/2 + rho, reduced to the minimal residue g_min (all |r| <= 1/8), member = g_min + (1/4) sum a_chi chi, a integer.
// Budget (exact identity): sum (a^2 + 8 r a) = 16 (var phi - var g_min), var phi = 15/64 + 2 O', O' = E[C(phi,2)] <= (Phi/2) O < Phi/32 when phi <= Phi.
// DFS over characters sorted by minimal cost, integer arithmetic (costs scaled by N).  Every a-vector is visited once; each gives one phi.
// (n10_search: hill climbing over classes without a Boolean representative, same DFS as n10_class.)
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
static inline void leaf(const int8_t*T,int k){
    leaves++;
    int sup=0,mx=0; for(int x=0;x<N;x++){ int p=G[x]+T[x]; if(p<0) return; if(p>0) sup++; if(p>mx) mx=p; }
    if(sup>t916){ gt[k]++; gtphi[mx/4]++; } else if(sup==t916) eqc[k]++;
}
static inline long long costf(int c,int a){ return (long long)N*a*a+2*a*Wm[c]; }
static void push(int d,int c,int a){ const int8_t*s=Tbuf[d]; int8_t*t=Tbuf[d+1]; const int8_t*h=chi[c].data(); for(int x=0;x<N;x++) t[x]=s[x]+a*h[x]; }
static void dfs(int d,int idx,long long used,int xr,int sumA,int k){
    if(xr==lam && ((sumA-sumtarget)&3)==0) leaf(Tbuf[d],k);
    int M=order_.size(); if(idx>=M) return;
    long long rem=ucap-used; long long cnext=N-2*llabs(Wm[order_[idx]]);
    if(cnext>rem) return;
    if(2*cnext>rem){ // at most one more character can be afforded
        if(xr!=lam){ int c=xr^lam; if(pos[c]>=idx) for(int a:{1,-1,3,-3}){ long long cc=costf(c,a); if(cc<=rem && (((sumA+a)-sumtarget)&3)==0){ push(d,c,a); leaf(Tbuf[d+1],k+1);} } }
        else if(rem>=2LL*N){ for(int i=idx;i<M;i++){ int c=order_[i]; for(int a:{2,-2}){ long long cc=costf(c,a); if(cc<=rem && (((sumA+a)-sumtarget)&3)==0){ push(d,c,a); leaf(Tbuf[d+1],k+1);} } } }
        return;
    }
    for(int i=idx;i<M;i++){ int c=order_[i]; long long cm=N-2*llabs(Wm[c]); if(cm>rem) break;
        for(int a:{1,-1,2,-2,3,-3}){ long long cc=costf(c,a); if(cc>rem) continue; push(d,c,a); dfs(d+1,i+1,used+cc,(a&1)?(xr^c):xr,sumA+a,k+1); }
    }
}

static vector<long long> walsh(vector<long long> v){ for(int b=0;b<n;b++) for(int i=0;i<N;i++) if(i>>b&1){ long long p=v[i^(1<<b)],q=v[i]; v[i^(1<<b)]=p+q; v[i]=p-q; } return v; }
struct Res{ long long gt,eq,Q; bool boolrep; };
// returns members above 9N/16 for the class of rho
static Res evalClass(const vector<int>&rho,int Phi,bool wantCount){
    G.assign(N,0); for(int x=0;x<N;x++) G[x]=2+4*rho[x];
    vector<long long> Wv(N); for(int i=0;i<N;i++) Wv[i]=G[i]; Wv=walsh(Wv);
    vector<int> T0(N,0); for(int c=1;c<N;c++){ long long w=Wv[c]; long long a0=(w>=0)?((2*w+N)/(2*N)):-((-2*w+N)/(2*N)); if(a0) for(int x=0;x<N;x++) T0[x]+=a0*chi[c][x]; }
    for(int x=0;x<N;x++) G[x]-=T0[x];
    vector<long long> Gv(N); for(int i=0;i<N;i++) Gv[i]=G[i]; Wm=walsh(Gv);
    long long Q=0; for(int x=0;x<N;x++) Q+=(long long)G[x]*G[x];
    Res R; R.Q=Q; R.gt=R.eq=0;
    // Boolean representative? it differs from g_min only by flips on exact ties
    vector<int> ties; for(int c=1;c<N;c++) if(2*llabs(Wm[c])==N) ties.push_back(c);
    R.boolrep=false;
    if(Q==8LL*N && ties.size()<=16){ for(int m=0;m<(1<<ties.size())&&!R.boolrep;m++){ bool ok=true; for(int x=0;x<N&&ok;x++){ int v=G[x]; for(size_t i=0;i<ties.size();i++) if(m>>i&1){ int c=ties[i]; int a=(Wm[c]>0)?-1:1; v+=a*chi[c][x]; } if(v!=2&&v!=6) ok=false; } if(ok) R.boolrep=true; } }
    if(!wantCount) return R;
    ucap=(10+Phi)*(long long)N-Q;
    lam=0; for(int b=0;b<n;b++){ int dd=G[1<<b]-G[0]; if(((dd/2)%2+2)%2) lam|=1<<b; }
    sumtarget=((-G[0])%4+4)%4;
    order_.clear(); for(int c=1;c<N;c++) order_.push_back(c);
    sort(order_.begin(),order_.end(),[&](int a,int b){ long long ca=N-2*llabs(Wm[a]),cb=N-2*llabs(Wm[b]); if(ca!=cb) return ca<cb; return a<b; });
    pos.assign(N,0); for(size_t i=0;i<order_.size();i++) pos[order_[i]]=i;
    memset(Tbuf,0,sizeof Tbuf); memset(gt,0,sizeof gt); memset(eqc,0,sizeof eqc); memset(gtphi,0,sizeof gtphi); leaves=0;
    dfs(0,0,0,0,0,0);
    for(int i=0;i<32;i++){ R.gt+=gt[i]; R.eq+=eqc[i]; }
    return R;
}
#include <random>
#include <ctime>
int main(int argc,char**argv){ // n10_search n startfile Phi seconds seed
    n=atoi(argv[1]); N=1<<n; int Phi=atoi(argv[3]); double limit=atof(argv[4]); mt19937_64 rng(atoll(argv[5])); t916=9*N/16;
    chi.assign(N,vector<int8_t>(N)); for(int c=0;c<N;c++) for(int x=0;x<N;x++) chi[c][x]=__builtin_parity(c&x)?-1:1;
    vector<int> rho(N); FILE*f=fopen(argv[2],"r"); for(int i=0;i<N;i++) if(fscanf(f,"%d",&rho[i])!=1) return 1; fclose(f);
    Res cur=evalClass(rho,Phi,true); long long best=-1; vector<int> bestrho=rho; if(!cur.boolrep) best=cur.gt;
    printf("start gt=%lld Q/N=%.3f boolrep=%d\n",cur.gt,(double)cur.Q/N,(int)cur.boolrep); fflush(stdout);
    time_t t0=time(0); long long evals=1,acc=0;
    while(difftime(time(0),t0)<limit){
        int k=1+(rng()%2); vector<pair<int,int>> mv; vector<int> r2=rho; bool ok=true;
        for(int i=0;i<k;i++){ int a=rng()%N,b=rng()%N; if(a==b||r2[a]<=-1||r2[b]>=2){ok=false;break;} r2[a]--; r2[b]++; }
        if(!ok) continue;
        Res q=evalClass(r2,Phi,false); if(q.boolrep) continue; // stay outside the Boolean classes
        Res r=evalClass(r2,Phi,true); evals++;
        if(r.gt>=cur.gt||cur.boolrep){ if(r.gt>cur.gt) acc++; rho=r2; cur=r; if(r.gt>best){ best=r.gt; bestrho=r2; printf("t=%.0f evals=%lld gt=%lld eq=%lld Q/N=%.3f\n",difftime(time(0),t0),evals,r.gt,r.eq,(double)r.Q/N); fflush(stdout);} }
    }
    unsigned long long g2=((1ULL<<n)-1)*((1ULL<<(n-1))-1)/3; unsigned long long MC=8*g2*((1ULL<<(n-2))-1);
    printf("END n=%d start=%s evals=%lld best=%lld frac=%.4f\nrep:",n,argv[2],evals,best,(double)best/(MC/2));
    for(int x=0;x<N;x++) if(bestrho[x]) printf(" %d:%d",x,bestrho[x]); printf("\n");
    return 0;
}
