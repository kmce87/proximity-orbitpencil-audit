// N8 (d): exhaustive/sampled scan of ker Phi_(r-4) at quotient level r: labels L_Y(non-pivot monomials), Y of codim r in D = F_2[x]_{<d} of GF(2^m). See n8_phi.py for Phi.
// Build: g++ -O2 -mpclmul -msse4.1 -std=c++17 n8_phiscan.cpp -o n8_phiscan
// Run: ./n8_phiscan m r_poly d codim [stride]
#include "n8_gf.h"
#include <cstdio>
#include <cstdlib>
#include <map>
#include <array>
#include <algorithm>
#include <cstring>
static int J;
#include <array>
int main(int argc, char** argv) {
  int m = atoi(argv[1]); u64 rp = strtoull(argv[2], 0, 0); int d = atoi(argv[3]); int r = atoi(argv[4]); long stride = argc > 5 ? atol(argv[5]) : 1;
  GF F(m, rp); if (!F.irreducible()) { printf("reducible\n"); return 1; }
  int f = d - r; int j = r - 4; J = j;
  std::map<int, long> hist; long count = 0, used = 0; int printed = 0;
  std::vector<std::vector<int>> Ts;
  for (unsigned T = 1; T < (1u << r); T++) { int s = __builtin_popcount(T); if (s <= j) { std::vector<int> v; for (int i = 0; i < r; i++) if (T >> i & 1) v.push_back(i); Ts.push_back(v); } }
  std::vector<std::array<u64, 8>> vecs(Ts.size());
  for (unsigned pm = 0; pm < (1u << d); pm++) {
    if (__builtin_popcount(pm) != f) continue;
    std::vector<int> piv; for (int i = 0; i < d; i++) if (pm >> i & 1) piv.push_back(i);
    std::vector<std::pair<int,int>> freeb;
    for (int q = 0; q < f; q++) for (int b = 0; b < piv[q]; b++) if (!(pm >> b & 1)) freeb.push_back({q, b});
    int fb = (int)freeb.size(); unsigned long total = 1UL << fb;
    for (unsigned long fm = 0; fm < total; fm++) {
      count++;
      if (stride > 1 && (count % stride)) continue;
      used++;
      std::vector<u64> B(f);
      for (int q = 0; q < f; q++) B[q] = 1ULL << piv[q];
      for (int k = 0; k < fb; k++) if (fm >> k & 1) B[freeb[k].first] ^= 1ULL << freeb[k].second;
      auto L = F.subspacePoly(B);
      std::vector<u64> ell; for (int i = 0; i < d; i++) if (!(pm >> i & 1)) ell.push_back(F.linEval(L, 1ULL << i));
      // vectors
      for (size_t k = 0; k < Ts.size(); k++) {
        auto& T = Ts[k]; int size = (int)T.size(); int t = j - size;
        u64 u = ell[T[0]]; std::vector<u64> H; for (int i = 1; i < size; i++) H.push_back(u ^ ell[T[i]]);
        auto c = F.subspacePoly(H); u64 up = F.linEval(c, u);
        std::array<u64, 8> v{}; int len = (int)c.size();
        for (int s = 0; s < len; s++) v[s] = F.pow2k(F.mul(up, c[len - 1 - s]), t);
        vecs[k] = v;
      }
      // rank over F_2 (row reduction on j words of width m bits, stored as 64-bit words)
      int rank = 0; std::vector<std::array<u64, 8>> rows = vecs;
      int nrows = (int)rows.size();
      for (int w = 0; w < j && rank < nrows; w++) for (int b = 63; b >= 0 && rank < nrows; b--) {
        int p = -1; for (int i = rank; i < nrows; i++) if ((rows[i][w] >> b) & 1) { p = i; break; }
        if (p < 0) continue;
        std::swap(rows[rank], rows[p]);
        for (int i = rank + 1; i < nrows; i++) if ((rows[i][w] >> b) & 1) for (int q = w; q < j; q++) rows[i][q] ^= rows[rank][q];
        rank++;
      }
      int kd = nrows - rank; hist[kd]++;
      if (kd > 0 && printed < 30) { printed++; printf("  ker=%d Y=[", kd); for (u64 b : B) printf("%llx ", (unsigned long long)b); printf("]\n"); fflush(stdout); }
    }
  }
  printf("m=%d r=0x%llx d=%d codim=%d j=%d gens=%zu: subspaces=%ld used=%ld hist:", m, (unsigned long long)rp, d, r, j, Ts.size(), count, used);
  for (auto& kv : hist) printf(" ker%d=%ld", kv.first, kv.second);
  printf("\n");
  return 0;
}
