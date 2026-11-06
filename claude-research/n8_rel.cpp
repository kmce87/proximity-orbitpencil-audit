// N8 (a): exhaustive over all f-dim Z in the Krylov domain D = F_2[x]_{<d} of GF(2^m):
// t(Z) = max over lam != 1 of dim(V cap lam V), V = L_Z(D), dim V = n = d - f. Optional semilinear version: V cap lam V^(2^i).
// Output: histogram of t, the examples at the maximum (Z basis, lam), written to stdout.
// Build: g++ -O2 -mpclmul -msse4.1 -std=c++17 n8_rel.cpp -o n8_rel
// Run: ./n8_rel m r d f [frob] [sampleStride]
#include "n8_gf.h"
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <map>
static int d, f;
int main(int argc, char** argv) {
  int m = atoi(argv[1]); u64 r = strtoull(argv[2], 0, 0); d = atoi(argv[3]); f = atoi(argv[4]);
  int frob = argc > 5 ? atoi(argv[5]) : 0; long stride = argc > 6 ? atol(argv[6]) : 1;
  GF F(m, r);
  if (!F.irreducible()) { printf("reducible\n"); return 1; }
  int n = d - f; int N = 1 << n;
  std::map<int, long> hist; int best = 0; std::vector<std::pair<std::vector<u64>, std::pair<u64,int>>> ex;
  long count = 0, used = 0;
  std::vector<u64> R; R.reserve((size_t)N * N);
  // pivots: combinations of f positions in [0,d)
  for (unsigned pm = 0; pm < (1u << d); pm++) {
    if (__builtin_popcount(pm) != f) continue;
    std::vector<int> piv; for (int i = 0; i < d; i++) if (pm >> i & 1) piv.push_back(i);
    // free entries: row j (pivot piv[j]) may have bits at non-pivot positions below piv[j]  (reduced echelon, leading = highest bit)
    std::vector<std::pair<int,int>> freeb;
    for (int j = 0; j < f; j++) for (int b = 0; b < piv[j]; b++) if (!(pm >> b & 1)) freeb.push_back({j, b});
    unsigned long total = 1UL << freeb.size();
    for (unsigned long fm = 0; fm < total; fm++) {
      count++;
      if (stride > 1 && (count % stride)) continue;
      used++;
      std::vector<u64> B(f);
      for (int j = 0; j < f; j++) B[j] = 1ULL << piv[j];
      for (size_t k = 0; k < freeb.size(); k++) if (fm >> k & 1) B[freeb[k].first] ^= 1ULL << freeb[k].second;
      auto L = F.subspacePoly(B);
      // images of the non-pivot monomials span V
      std::vector<u64> gens; for (int i = 0; i < d; i++) if (!(pm >> i & 1)) gens.push_back(F.linEval(L, 1ULL << i));
      auto A = spanOf(gens);
      std::vector<u64> nz(A.begin() + 1, A.end()), inv(nz.size());
      // batch inversion
      { u64 acc = 1; std::vector<u64> pre(nz.size());
        for (size_t i = 0; i < nz.size(); i++) { pre[i] = acc; acc = F.mul(acc, nz[i]); }
        u64 ia = F.inv(acc);
        for (long i = (long)nz.size() - 1; i >= 0; i--) { inv[i] = F.mul(ia, pre[i]); ia = F.mul(ia, nz[i]); } }
      int zt = 0; u64 zl = 0; int zi = 0;
      int imax = frob ? m : 1;
      std::vector<u64> iw = inv;
      for (int i = 0; i < imax; i++) {
        R.clear();
        for (size_t a = 0; a < nz.size(); a++) for (size_t b = 0; b < nz.size(); b++) {
          u64 q = F.mul(nz[a], iw[b]);
          if (i == 0 && q == 1) continue;
          R.push_back(q);
        }
        std::sort(R.begin(), R.end());
        size_t p = 0, mx = 0; u64 bl = 0;
        while (p < R.size()) { size_t q = p; while (q < R.size() && R[q] == R[p]) q++; if (q - p > mx) { mx = q - p; bl = R[p]; } p = q; }
        int t = 0; while ((1UL << (t + 1)) - 1 <= mx) t++;
        if (t > zt) { zt = t; zl = bl; zi = i; }
        for (auto& v : iw) v = F.sq(v);  // inverse of v^(2^(i+1))
      }
      hist[zt]++;
      if (zt > best) { best = zt; ex.clear(); }
      if (zt == best && ex.size() < 12) ex.push_back({B, {zl, zi}});
    }
  }
  printf("m=%d r=0x%llx d=%d f=%d n=%d frob=%d subspaces=%ld used=%ld\n", m, (unsigned long long)r, d, f, n, frob, count, used);
  for (auto& kv : hist) printf("  t=%d: %ld\n", kv.first, kv.second);
  for (auto& e : ex) { printf("  max t=%d Z=[", best); for (u64 b : e.first) printf("%llx ", (unsigned long long)b); printf("] lam=%llx frob=%d\n", (unsigned long long)e.second.first, e.second.second); }
  return 0;
}
