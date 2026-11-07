// Lane B: exact BF64 cancellation search in one entire official parameter slice.
// Compile: g++ -O3 -std=c++17 -Wall -Wextra -o /tmp/prize_coeff prize-lane/binary_bf64_exact_slice_20261107.cpp
// Run: /tmp/prize_coeff
//
// Official source geometry: SubmissionBinaryUpper/{LabelFamily,LabelTable,LabelSpace,
// FlatPoly,SubspacePoly,CorePencil}.lean at proximity-prize/proximity-prize
// BF64 modulus: CompPoly BF64/Basic.lean, x^64+x^4+x^3+x+1.
// FIXED row=0: Q={1,2,4}, s=(8,15,7); r=1; vary jr in Fin8 and ee in GF2.
// Exhaustively considers all injective nonzero mr : Fin 3 -> NZ10 and all
// jn : Fin 3 -> Fin 8 by meet-in-the-middle, not by iterating all ~5e11 tuples.
// aa,e0,e1 do not enter phi's *direction* and therefore do not change
// the coefficient. They multiply the proven slice coverage by 8.
// This experiment is numerical and does not establish a new Lean claim.
#include <array>
#include <string>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <unordered_map>
#include <vector>
using U=uint64_t; using W=unsigned __int128;
constexpr U TAIL=0x1b;
constexpr W MOD=(W(1)<<64)|TAIL;

static inline U gf(U a,U b){
  W p=0, x=a;
  while(b){if(b&1)p^=x; x<<=1; b>>=1;}
  for(int k=127;k>=64;--k) if((p>>k)&1) p^=(MOD<<(k-64));
  return (U)p;
}
static inline int parity(unsigned x){return __builtin_parity(x);}
static std::vector<U> makepoly(const std::vector<U>& nodes){
  std::vector<U> coeff{1};
  for(auto u:nodes){
    U v=0,x=u;
    for(auto c:coeff){v^=gf(c,x);x=gf(x,x);}
    std::vector<U> out(coeff.size()+1,0);
    for(size_t i=0;i<coeff.size();i++){out[i]^=gf(v,coeff[i]);out[i+1]^=gf(coeff[i],coeff[i]);}
    coeff=std::move(out);
  }
  if(coeff.back()!=1){std::cerr<<"bad monic\n";exit(4);}
  return coeff;
}
static U eval(const std::vector<U>& coeff,U x){
  U v=0;for(auto c:coeff){v^=gf(c,x);x=gf(x,x);} return v;
}
static std::array<U,15> ELL;
static std::vector<U> LW;
static void initialize(){
  std::vector<U> basis;for(int i=0;i<6;i++)basis.push_back(U(1)<<i);
  auto ys=makepoly(basis);
  for(int i=0;i<15;i++)ELL[i]=eval(ys,U(1)<<(6+i));
  basis.clear();for(int i=0;i<11;i++)basis.push_back(ELL[i]);
  LW=makepoly(basis);
  if(ELL[0]!=0x796adf34d64462c2ULL || ELL[1]!=0x3438da15cd9684cdULL)
    {std::cerr<<"basis mismatch with Python\n";exit(5);}
}
static inline U lab(unsigned b){U o=0;while(b){int i=__builtin_ctz(b);b&=b-1;o^=ELL[i];}return o;}
static inline int beta(int s,int j){int i=__builtin_ctz((unsigned)s);return (j% (1<<i)) + (1<<(i+1))*(j/(1<<i));}
static std::array<unsigned,12> kernel(unsigned a,unsigned b,unsigned c){
  unsigned forms[3]={a,b,c}; int pivot[3];int n=0;
  for(int col=0;col<15&&n<3;col++){
    int hit=-1;for(int r=n;r<3;r++)if(forms[r]&(1u<<col)){hit=r;break;}
    if(hit<0)continue;
    std::swap(forms[n],forms[hit]);
    for(int r=0;r<3;r++)if(r!=n && (forms[r]&(1u<<col)))forms[r]^=forms[n];
    pivot[n++]=col;
  }
  if(n!=3){std::cerr<<"rank failure\n";exit(6);}
  std::array<unsigned,12> out{};int ct=0;
  for(int j=0;j<15;j++){
    bool isPivot=false;for(int p:pivot)if(p==j)isPivot=true;
    if(isPivot)continue;
    unsigned v=1u<<j;
    for(int r=0;r<3;r++)if(parity(forms[r]&v))v^=1u<<pivot[r];
    if(parity(a&v)||parity(b&v)||parity(c&v)){std::cerr<<"kernel check failed\n";exit(7);}
    out[ct++]=v;
  }
  if(ct!=12){std::cerr<<"dim failure\n";exit(8);}
  return out;
}
static U sublead(const std::array<unsigned,12>& basis){
  std::vector<U> z;z.reserve(12);
  for(auto x:basis)z.push_back(lab(x));
  auto coeff=makepoly(z);
  return coeff[11]; // [X^2048] in degree-4096 additive polynomial
}
struct Opt{U a;unsigned m;unsigned j;};
static const int S[3]={8,15,7};
static unsigned JR=0, EE=0;
static U flatcoeff(int t,unsigned m,unsigned j){
  unsigned sig=(unsigned)S[t]<<11;
  unsigned rho = (unsigned)(beta(S[0],JR) ^ ((t==0)?0:((t==1)?EE:(EE^1))*S[0]))<<11;
  unsigned rr=1u;
  unsigned nu=(unsigned)beta(S[t],j)<<11;
  return sublead(kernel(sig,rr^rho,(m<<1)^nu));
}
int main(int argc,char**argv){
  if(argc!=3){std::cerr<<"usage: program JR(0..7) EE(0..1)\n";return 9;}
  JR=std::stoul(argv[1]); EE=std::stoul(argv[2]);
  if(JR>=8||EE>=2)return 10;
  initialize();
  U target=eval(LW,lab(1<<11))^eval(LW,lab(2<<11))^eval(LW,lab(4<<11));
  if(target!=0x17c6dbd8e3893ddcULL){std::cerr<<"wrong reserved sum\n";return 1;}
  std::array<std::vector<Opt>,3> sets;
  for(int t=0;t<3;t++){
    for(unsigned m=1;m<=1023;m++)for(unsigned j=0;j<8;j++)sets[t].push_back({flatcoeff(t,m,j),m,j});
  }
  // Independent reference checksum: m=(1,2,4), j=(0,0,0)
  U check=flatcoeff(0,1,0)^flatcoeff(1,2,0)^flatcoeff(2,4,0);
  if(JR==0 && EE==0 && check!=0x199f1d4b6282354eULL){std::cerr<<"Python cross-check mismatch\n";return 2;}
  std::unordered_multimap<U,Opt> candidates;
  candidates.reserve(sets[2].size()*2);
  for(auto opt:sets[2])candidates.emplace(opt.a,opt);
  uint64_t visits=0, raw_hits=0, valid_hits=0;
  bool reported=false;
  for(auto x:sets[0])for(auto y:sets[1]){
    ++visits;
    if(x.m==y.m)continue;
    const auto range=candidates.equal_range(target^x.a^y.a);
    for(auto z=range.first;z!=range.second;++z){
      ++raw_hits;
      if(z->second.m!=x.m && z->second.m!=y.m){
        ++valid_hits;
        if(!reported){std::cout<<"WITNESS m=("<<x.m<<","<<y.m<<","<<z->second.m
                               <<") j=("<<x.j<<","<<y.j<<","<<z->second.j<<")\n";reported=true;}
      }
    }
  }
  const uint64_t distinctm=1023ULL*1022ULL*1021ULL;
  const uint64_t candidates_total=distinctm*512ULL;
  std::cout<<"PINNED_ROW=(q1,q2,q3,s0,s1,s2)=(1,2,4,8,15,7)\n"
           <<"FIXED_r=1; variable jr,ee,m_t (injective),jn_t\n"
           <<"BF64_MOD=x^64+x^4+x^3+x+1\n"
           <<"rhs=0x"<<std::hex<<std::setfill('0')<<std::setw(16)<<target<<std::dec<<"\n"
           <<"jr="<<JR<<" ee="<<EE<<"\n"
           <<"sample_checksum=0x"<<std::hex<<check<<std::dec<<"\n"
           <<"options_per_flat="<<sets[0].size()<<"\n"
           <<"pair_lookup_count="<<visits<<"\n"
           <<"complete_admissible_direction_jn_tuples="<<candidates_total<<"\n"
           <<"coefficient_matches_before_m_filter="<<raw_hits<<"\n"
           <<"coefficient_zero_full_matches="<<valid_hits<<"\n"
           <<"coverage_including_aa_e0_e1="<<candidates_total*8ULL<<"\n";
  return 0;
}
