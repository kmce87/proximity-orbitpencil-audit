// N8: structure of a specific label space: for V = L_Y(D) with Y = q*P_f, D = P_(r+f) in BF64, list the largest multiplicities of ratios v/w^(2^i): dim(V cap lam V^(2^i)).
// Build: g++ -O2 -mpclmul -msse4.1 -std=c++17 n8_struct.cpp -o n8_struct ; Run: ./n8_struct qhex r f
#include "n8_gf.h"
#include <cstdio>
#include <cstdlib>
#include <algorithm>
int main(int argc,char**argv){
  u64 q=strtoull(argv[1],0,16);int r=atoi(argv[2]),f=atoi(argv[3]);GF F(64,0x1B);
  std::vector<u64> Y;for(int i=0;i<f;i++)Y.push_back(q<<i);
  auto L=F.subspacePoly(Y);
  // complement monomials by elimination
  std::vector<u64> ech=Y,gens;
  auto red=[&](u64 v){for(int b=63;b>=0;b--){if(!(v>>b&1))continue;bool hit=false;for(u64 e:ech)if(e>>b&1&&!(e>>(b+1))){v^=e;hit=true;break;}if(!hit){}}return v;};
  // simple rank based completion
  for(int i=0;i<r+f;i++){auto t=ech;t.push_back(1ULL<<i);if(rankF2(t)==(int)t.size()){ech=t;gens.push_back(F.linEval(L,1ULL<<i));}}
  printf("q=%llx r=%d f=%d labels=%zu rank=%d\n",(unsigned long long)q,r,f,gens.size(),rankF2(gens));
  auto A=spanOf(gens);std::vector<u64> nz(A.begin()+1,A.end()),inv(nz.size());
  for(size_t i=0;i<nz.size();i++)inv[i]=F.inv(nz[i]);
  std::vector<u64> R;R.reserve(nz.size()*nz.size());
  auto iw=inv;
  for(int i=0;i<64;i++){
    R.clear();
    for(size_t a=0;a<nz.size();a++)for(size_t b=0;b<nz.size();b++){u64 q2=F.mul(nz[a],iw[b]);if(i==0&&q2==1)continue;R.push_back(q2);}
    std::sort(R.begin(),R.end());
    size_t p=0,mx=0,nmx=0;u64 bl=0;
    while(p<R.size()){size_t e=p;while(e<R.size()&&R[e]==R[p])e++;if(e-p>mx){mx=e-p;bl=R[p];nmx=1;}else if(e-p==mx)nmx++;p=e;}
    if(mx>=3)printf(" frob %d: max mult %zu (t=%d) lam=%016llx ties=%zu\n",i,mx,(int)(__builtin_clzll(1)-__builtin_clzll(mx+1)),(unsigned long long)bl,nmx);
    for(auto&v:iw)v=F.sq(v);
  }
  return 0;
}
