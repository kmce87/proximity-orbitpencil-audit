// Lane B 2026-11-07: exact BF64 test of the conjectured rr-image invariance.
// Build: g++ -O3 -std=c++17 -Wall -Wextra prize-lane/binary_rr_image_invariance_20261107.cpp -o /tmp/prize_rr_image
// Replay: /tmp/prize_rr_image
// Test whether sorted coefficient multisets per flat stay identical for rr=1 and
// rr in {3,5,7,9,15}, with the same pivot, fixed row 0, JR=EE=0.
// This deliberately tests image invariance, NOT cancellation or 106.23 certification.
#define main old_rr_main
#include "binary_rr_slice_20261107.cpp"
#undef main
#include <algorithm>
#include <cstdio>
int main(){
 initialize();
 std::array<std::vector<U>,3> base;
 RR=1;JR=0;EE=0;
 for(int t=0;t<3;t++)for(unsigned m=1;m<=1023;m++)for(unsigned j=0;j<8;j++)base[t].push_back(flatcoeff(t,m,j));
 for(auto &a:base)std::sort(a.begin(),a.end());
 for(unsigned rr : {3u,5u,7u,9u,15u}){
  RR=rr;
  for(int t=0;t<3;t++){
   std::vector<U> test;
   for(unsigned m=1;m<=1023;m++)for(unsigned j=0;j<8;j++)test.push_back(flatcoeff(t,m,j));
   std::sort(test.begin(),test.end());
   unsigned changed=0;for(size_t k=0;k<test.size();k++)changed+=(test[k]!=base[t][k]);
   printf("rr=%u flat=%d sorted_coefficient_differences=%u / %zu\n",rr,t,changed,test.size());
   if(changed==0)return 2; // Falsification must be witnessed for every tested rr/flat.
  }
 }
}
