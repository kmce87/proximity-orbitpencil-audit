// N8 (e): ker Phi_(r-4) on quotient labels L_Y(D), real BF64, real D = P_21, for structured and random Y of codim r (r = 6..10); excess over the forced kernel = gens - 64 j.
// Families: q*P_f for every q with deg q <= r-? (all q that fit), Y = random subspaces, random Y containing P_7, spans of arithmetic progressions of exponents.
// Build: g++ -O2 -mpclmul -msse4.1 -std=c++17 n8_phireal.cpp -o n8_phireal ; Run: ./n8_phireal r nrandom [d]
#include "n8_gf.h"
#include <array>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <random>
#include <algorithm>
static GF F(64, 0x1B);
static int D = 21;
static std::vector<std::vector<int>> Ts;
static int J;
static int kerDim(const std::vector<u64>& ell) {
  static std::vector<std::array<u64, 8>> rows; rows.resize(Ts.size());
  for (size_t k = 0; k < Ts.size(); k++) {
    auto& T = Ts[k]; int size = (int)T.size(), t = J - size;
    u64 u = ell[T[0]]; std::vector<u64> H; for (int i = 1; i < size; i++) H.push_back(u ^ ell[T[i]]);
    auto c = F.subspacePoly(H); u64 up = F.linEval(c, u);
    std::array<u64, 8> v{}; int len = (int)c.size();
    for (int s = 0; s < len; s++) v[s] = F.pow2k(F.mul(up, c[len - 1 - s]), t);
    rows[k] = v;
  }
  int rank = 0, nrows = (int)rows.size();
  for (int w = 0; w < J && rank < nrows; w++) for (int b = 63; b >= 0 && rank < nrows; b--) {
    int p = -1; for (int i = rank; i < nrows; i++) if ((rows[i][w] >> b) & 1) { p = i; break; }
    if (p < 0) continue;
    std::swap(rows[rank], rows[p]);
    for (int i = rank + 1; i < nrows; i++) if ((rows[i][w] >> b) & 1) for (int q = w; q < J; q++) rows[i][q] ^= rows[rank][q];
    rank++;
  }
  return nrows - rank;
}
// returns labels or empty if Y has wrong rank
static std::vector<u64> labelsOf(const std::vector<u64>& Y, int r) {
  if (rankF2(Y) != (int)Y.size() || (int)Y.size() != D - r) return {};
  auto L = F.subspacePoly(Y);
  std::vector<u64> ech = Y, ell;
  for (int i = 0; i < D && (int)ell.size() < r; i++) { auto t = ech; t.push_back(1ULL << i); if (rankF2(t) == (int)t.size()) { ech = t; ell.push_back(F.linEval(L, 1ULL << i)); } }
  return ell;
}
int main(int argc, char** argv) {
  int r = atoi(argv[1]); long nrand = atol(argv[2]); if (argc > 3) D = atoi(argv[3]);
  J = r - 4; int f = D - r;
  for (unsigned T = 1; T < (1u << r); T++) { int s = __builtin_popcount(T); if (s <= J) { std::vector<int> v; for (int i = 0; i < r; i++) if (T >> i & 1) v.push_back(i); Ts.push_back(v); } }
  int forced = std::max(0, (int)Ts.size() - 64 * J);
  printf("r=%d f'=%d j=%d gens=%zu forced=%d\n", r, f, J, Ts.size(), forced); fflush(stdout);
  // family 1: q * P_f
  { std::map<int, int> hist; for (u64 q = 1; q < (1ULL << (D - f + 1)); q++) { int dq = 63 - __builtin_clzll(q); if (dq + f - 1 > D - 1) continue;
      std::vector<u64> Y; for (int i = 0; i < f; i++) Y.push_back(q << i);
      auto ell = labelsOf(Y, r); if (ell.empty()) continue; int k = kerDim(ell); hist[k]++;
      if (k > forced) { printf("  q*P_f excess: q=%llx ker=%d\n", (unsigned long long)q, k); fflush(stdout); } }
    printf(" family q*P_f:"); for (auto& kv : hist) printf(" ker%d=%d", kv.first, kv.second); printf("\n"); fflush(stdout); }
  // family 2: arithmetic progressions of exponents and shifts: Y = span(x^(a + s i)) (needs enough room)
  { std::map<int, int> hist; for (int s = 1; s <= 4; s++) for (int a = 0; a + s * (f - 1) < D; a++) { std::vector<u64> Y; for (int i = 0; i < f; i++) Y.push_back(1ULL << (a + s * i));
      auto ell = labelsOf(Y, r); if (ell.empty()) continue; int k = kerDim(ell); hist[k]++; if (k > forced) { printf("  progression excess a=%d s=%d ker=%d\n", a, s, k); fflush(stdout); } }
    printf(" family progressions:"); for (auto& kv : hist) printf(" ker%d=%d", kv.first, kv.second); printf("\n"); fflush(stdout); }
  // family 3: random Y; family 4: random Y containing P_7 (the first 128 words), when f >= 7
  std::mt19937_64 rng(20261106);
  for (int fam = 0; fam < 2; fam++) {
    std::map<int, long> hist;
    for (long n = 0; n < nrand; n++) {
      std::vector<u64> Y; if (fam == 1) { if (f < 7) break; for (int i = 0; i < 7; i++) Y.push_back(1ULL << i); }
      while ((int)Y.size() < f) { u64 c = rng() & ((1ULL << D) - 1); auto t = Y; t.push_back(c); if (rankF2(t) == (int)t.size()) Y = t; }
      auto ell = labelsOf(Y, r); int k = kerDim(ell); hist[k]++;
      if (k > forced) { printf("  random excess fam=%d ker=%d Y0=%llx\n", fam, k, (unsigned long long)Y[0]); fflush(stdout); }
    }
    printf(" family random%s:", fam ? " containing P_7" : ""); for (auto& kv : hist) printf(" ker%d=%ld", kv.first, kv.second); printf("\n"); fflush(stdout);
  }
  return 0;
}
