// N6: exact count of the class per z-profile with orbit reduction on the first fibre.
// S in F_2^ny x F_2^4, |S| = 9*2^ny, 1_S = delta_q(z) + (1/8) Lambda; all w even (parity lemmas), so S_z has Fourier in (1/4)Z.
// u_eta = w_eta/2.  Lattice: u_eta mod 2 affine on Z; Walsh over any 3-flat = 0 mod 4; Walsh over Z = 0 mod 8.  At most 6 etas.
// build: g++ -O2 -std=c++17 n6_count.cpp -o n6_count; usage: n6_count ny n6_reps.txt [first_profile last_profile]
// optional sample dump for n6_verify.py: env DUMP=file DUMPN=count DUMPSKIP=stride
#include <cstdio>
#include <functional>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <map>
#include <array>
#include <algorithm>
#include <unordered_map>
using namespace std;
typedef long long ll;
int NY,NE;
struct Cand{ uint32_t mask; int d; int8_t u[16]; uint32_t pm, supp; };
vector<Cand> cand; vector<int> byD[9];
unordered_map<uint64_t,vector<int>> byDP;   // (d<<32 | pm) -> list
static inline int par(unsigned x){return __builtin_parity(x);}
int prof[16]; int sel[16]; uint32_t pmz[16];
map<int,ll> byRank; ll total, nodes, weight;
vector<array<int,8>> flats3; vector<int> flatLast[16];
int rankOf(uint32_t supp){ int basis[8]={0},rk=0; for(int e=1;e<NE;e++) if(supp>>e&1){int x=e; for(int i=NY-1;i>=0;i--){ if(!(x>>i&1))continue; if(!basis[i]){basis[i]=x;rk++;break;} x^=basis[i];}} return rk; }
inline bool checkFlat(const array<int,8>& F, uint32_t E){
  for(int eta=1;eta<NE;eta++){ if(!(E>>eta&1)) continue;
    int a[8]; bool nz=false; for(int t=0;t<8;t++){a[t]=cand[sel[F[t]]].u[eta]; if(a[t])nz=true;}
    if(!nz) continue;
    for(int m=0;m<8;m++){ int s=0; for(int t=0;t<8;t++) s+= par(m&t)?-a[t]:a[t]; if(s&3) return false; }
  }
  return true;
}
inline bool checkAll(uint32_t E){
  for(int eta=1;eta<NE;eta++){ if(!(E>>eta&1)) continue;
    int a[16]; for(int t=0;t<16;t++)a[t]=cand[sel[t]].u[eta];
    for(int m=0;m<16;m++){ int s=0; for(int t=0;t<16;t++) s+= par(m&t)?-a[t]:a[t]; if(s&7) return false; }
  }
  return true;
}
uint32_t usedE; int dumpLeft=0, dumpSeen=0, dumpSkip=1; FILE* dumpF=nullptr; int curLine=0;
void dfs(int z){
  nodes++;
  if(dumpLeft>0 && dumpSeen>=dumpLeft) return;
  if(z==16){ if(!checkAll(usedE)) return; total+=weight; byRank[rankOf(usedE)]+=weight;
    if(dumpF){ static long cnt=0; if(cnt++%dumpSkip==0){ fprintf(dumpF,"%d %d",curLine,rankOf(usedE)); for(int t=0;t<16;t++) fprintf(dumpF," %u",cand[sel[t]].mask); fprintf(dumpF,"\n"); dumpSeen++; } }
    return; }
  uint32_t keep=usedE;
  const vector<int>* L; 
  bool freeLevel=(z==0||z==1||z==2||z==4||z==8);
  uint32_t want=0;
  if(!freeLevel){ want=pmz[0]; for(int i=0;i<4;i++) if(z>>i&1) want^=pmz[0]^pmz[1<<i];
    auto it=byDP.find(((uint64_t)prof[z]<<32)|want); if(it==byDP.end()) return; L=&it->second; }
  else L=&byD[prof[z]];
  for(int a:*L){
    sel[z]=a; pmz[z]=cand[a].pm; uint32_t nu=keep|cand[a].supp;
    if(__builtin_popcount(nu)>6) continue;
    bool ok=true; for(int fi:flatLast[z]) if(!checkFlat(flats3[fi],nu)){ok=false;break;}
    if(!ok) continue;
    usedE=nu;
    dfs(z+1);
  }
  usedE=keep;
}
int main(int c,char**v){
  NY=atoi(v[1]);NE=1<<NY;
  uint64_t N=1ULL<<NE;
  unordered_map<uint32_t,int> idx;
  for(uint64_t A=0;A<N;A++){
    Cand C; C.mask=A; for(int i=0;i<16;i++)C.u[i]=0; bool ok=true; C.pm=0;C.supp=0;
    int wt=__builtin_popcountll(A); int dnum=8*wt; if(dnum%NE) continue; C.d=dnum/NE; if(C.d&1) continue;
    for(int eta=1;eta<NE&&ok;eta++){ int s=0; for(int y=0;y<NE;y++) if(A>>y&1) s+= par(eta&y)?-1:1;
      int num=8*s; if(num%NE||((num/NE)&1)){ok=false;break;} int uu=(num/NE)/2; C.u[eta]=uu; if(uu&1)C.pm|=1u<<eta; if(uu)C.supp|=1u<<eta; }
    if(ok){ idx[A]=cand.size(); byD[C.d].push_back(cand.size()); byDP[((uint64_t)C.d<<32)|C.pm].push_back(cand.size()); cand.push_back(C);}    
  }
  // orbits of AGL(ny) on candidates by union-find with generators
  vector<int> uf(cand.size()); for(size_t i=0;i<uf.size();i++)uf[i]=i;
  auto fnd=[&](int x){ while(uf[x]!=x){uf[x]=uf[uf[x]];x=uf[x];} return x; };
  auto applyGen=[&](uint32_t A,int kind,int i,int j){ uint32_t B=0; for(int y=0;y<NE;y++) if(A>>y&1){ int t=y; if(kind==0) t=y^(1<<i); else if(kind==1){ if(y>>j&1) t=y^(1<<i);} else { int bi=y>>i&1,bj=y>>j&1; t=y&~((1<<i)|(1<<j)); t|=bj<<i; t|=bi<<j; } B|=1u<<t; } return B; };
  for(size_t a=0;a<cand.size();a++){ 
    for(int i=0;i<NY;i++){ uint32_t B=applyGen(cand[a].mask,0,i,0); uf[fnd(a)]=fnd(idx.at(B)); }
    for(int i=0;i<NY;i++)for(int j=0;j<NY;j++) if(i!=j){ uint32_t B=applyGen(cand[a].mask,1,i,j); uf[fnd(a)]=fnd(idx.at(B)); B=applyGen(cand[a].mask,2,i,j); uf[fnd(a)]=fnd(idx.at(B)); }
  }
  map<int,int> osize; for(size_t a=0;a<cand.size();a++) osize[fnd(a)]++;
  printf("ny=%d candidates=%zu per d:",NY,cand.size()); for(int d=0;d<=8;d+=2)printf(" %d:%zu",d,byD[d].size()); printf(" orbits=%zu\n",osize.size());
  // 3-flats of F_2^4
  {
    vector<array<int,8>> tmp;
    for(int s=1;s<16;s++) for(int k=0;k<2;k++){ array<int,8> F; int n=0; for(int z=0;z<16;z++) if(par(s&z)==k) F[n++]=z; 
      // order so that index t -> affine coordinates: use basis of direction
      vector<int> basis; int base=F[0]; array<int,8> G; G[0]=base; int filled=1; for(int i=1;i<8&&filled<8;i++){ int x=F[i]^base; bool in=false; for(int t=0;t<filled;t++) if(G[t]==F[i]) in=true; if(in) continue; for(int t=0;t<filled;t++) G[filled+t]=G[t]^x; filled*=2; }
      tmp.push_back(G); }
    flats3=tmp; for(size_t i=0;i<flats3.size();i++){ int m=0; for(int z:flats3[i]) m=max(m,z); flatLast[m].push_back(i);}    
  }
  if(getenv("DUMP")){ dumpF=fopen(getenv("DUMP"),"w"); dumpLeft=atoi(getenv("DUMPN")); dumpSkip=atoi(getenv("DUMPSKIP")); }
  FILE*f=fopen(v[2],"r"); int line=0; int lo=c>3?atoi(v[3]):0, hi=c>4?atoi(v[4]):1000;
  long grand[8]={0};
  while(true){ long orb; if(fscanf(f,"%ld",&orb)!=1)break; int raw[16]; for(int i=0;i<16;i++) if(fscanf(f,"%d",&raw[i])!=1) return 1;
    if(line<lo||line>hi){line++;continue;}
    // translate z so that z=0 has d=4 if possible, else d=2/6, else as is
    int zs=-1; for(int i=0;i<16;i++) if(raw[i]==4){zs=i;break;} if(zs<0) for(int i=0;i<16;i++) if(raw[i]==2||raw[i]==6){zs=i;break;} if(zs<0) zs=0;
    for(int i=0;i<16;i++) prof[i]=raw[i^zs];
    total=0;byRank.clear();nodes=0;usedE=0;dumpSeen=0;curLine=line;
    // first level by orbits
    map<int,int> seen;
    for(int a:byD[prof[0]]){ int r=fnd(a); if(seen.count(r)) continue; seen[r]=1;
      weight=osize[r]; sel[0]=a; pmz[0]=cand[a].pm; usedE=cand[a].supp; dfs(1); }
    printf("profile#%d orbit %ld | members=%lld nodes=%lld ranks:",line,orb,total,nodes); for(auto&kv:byRank){printf(" %d:%lld",kv.first,kv.second);} puts(""); fflush(stdout); line++;
  }
}
