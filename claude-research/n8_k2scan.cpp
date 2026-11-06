// N8 (c): exhaustive scan of the merge kernel at quotient level r = 6.  For every subspace Y of codim 6 in D = F_2[x]_{<d} of GF(2^m), take the 6 labels
// L_Y(non-pivot monomials) and compute dim ker Phi_2, Phi_2: F_2^21 -> K^2 (see n8_k2.py).  ker Phi_2 != 0 means two Walsh classes of the quotient labels share a top,
// and by the composition rule this lifts to every finer level (n8 theory).  Stride > 1 samples every stride-th subspace.
// Build: g++ -O2 -mpclmul -msse4.1 -std=c++17 n8_k2scan.cpp -o n8_k2scan
// Run: ./n8_k2scan m r d [stride]
#include "n8_gf.h"
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <map>
struct V128 { u64 a, b; };
static int kerDim(const GF& F, const u64* ell) {
  V128 piv[128]; bool has[128]; for (int i = 0; i < 128; i++) has[i] = false;
  int rank = 0, cnt = 0;
  auto ins = [&](u64 a, u64 b) {
    cnt++;
    for (int h = 127; h >= 0; h--) {
      int bit = h >= 64 ? (a >> (h - 64)) & 1 : (b >> h) & 1;
      if (!bit) continue;
      if (has[h]) { a ^= piv[h].a; b ^= piv[h].b; }
      else { has[h] = true; piv[h] = {a, b}; rank++; return; }
    }
  };
  u64 sq[6]; for (int i = 0; i < 6; i++) { sq[i] = F.sq(ell[i]); ins(sq[i], 0); }
  for (int i = 0; i < 6; i++) for (int j = i + 1; j < 6; j++) ins(F.mul(ell[i], ell[j]), F.mul(sq[i], ell[j]) ^ F.mul(ell[i], sq[j]));
  return cnt - rank;
}
int main(int argc, char** argv) {
  int m = atoi(argv[1]); u64 r = strtoull(argv[2], 0, 0); int d = atoi(argv[3]); long stride = argc > 4 ? atol(argv[4]) : 1;
  GF F(m, r);
  if (!F.irreducible()) { printf("reducible\n"); return 1; }
  int f = d - 6;
  std::map<int, long> hist; long count = 0, used = 0; int printed = 0;
  for (unsigned pm = 0; pm < (1u << d); pm++) {
    if (__builtin_popcount(pm) != f) continue;
    std::vector<int> piv; for (int i = 0; i < d; i++) if (pm >> i & 1) piv.push_back(i);
    std::vector<std::pair<int,int>> freeb;
    for (int j = 0; j < f; j++) for (int b = 0; b < piv[j]; b++) if (!(pm >> b & 1)) freeb.push_back({j, b});
    int fb = (int)freeb.size();
    if (fb > 62) { printf("too many\n"); return 1; }
    unsigned long total = 1UL << fb;
    for (unsigned long fm = 0; fm < total; fm++) {
      count++;
      if (stride > 1 && (count % stride)) continue;
      used++;
      std::vector<u64> B(f);
      for (int j = 0; j < f; j++) B[j] = 1ULL << piv[j];
      for (int k = 0; k < fb; k++) if (fm >> k & 1) B[freeb[k].first] ^= 1ULL << freeb[k].second;
      auto L = F.subspacePoly(B);
      u64 ell[6]; int c = 0; for (int i = 0; i < d; i++) if (!(pm >> i & 1)) ell[c++] = F.linEval(L, 1ULL << i);
      int kd = kerDim(F, ell);
      hist[kd]++;
      if (kd > 0 && printed < 40) { printed++; printf("  ker=%d Y=[", kd); for (u64 b : B) printf("%llx ", (unsigned long long)b); printf("]\n"); }
    }
  }
  printf("m=%d r=0x%llx d=%d codim 6: subspaces=%ld used=%ld hist:", m, (unsigned long long)r, d, count, used);
  for (auto& kv : hist) printf(" ker%d=%ld", kv.first, kv.second);
  printf("\n");
  return 0;
}
