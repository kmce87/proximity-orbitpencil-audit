// N8 (b): exact size of the label-level class at n = 6 for ARBITRARY F_2-linear labels: all 36-subsets S of the 64 labels with
// V_S = X^36 + a X^34 + b X^33 + O(X^32), where L_W = X^4 + a X^2 + b X (W of dim 2).  Meet in the middle over the 2^60 subsets:
// S = S_A u S_B over a hyperplane H and its coset.  e1(S) = 0 forces even sizes and equal sums s on the two sides, so each side runs over a
// coset of RM(3,5) = [32,26,4] (2^26 words per s).  With e1 = 0: e3(S) = p3(S), e2(S) = e2A + e2B + s^2.  Weight-4 generators have zero sum, so
// e2 changes by a table lookup and p3 by xor.  Keys are 64-bit mixes (false match rate about 2^-7 per run; they can only add to a count).
// For generic labels T2-T4 predict exactly M_all(2) = 12032931760 members.
// Build: g++ -O2 -mpclmul -msse4.1 -mbmi2 -std=c++17 n8_class6.cpp -o n8_class6
// Run: ./n8_class6 m r l0 l1 l2 l3 l4 l5 w1 w2   (labels hex; w1, w2 = indices in F_2^6 spanning W; l5 is the coset direction)
#include "n8_gf.h"
#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <thread>
#define SHIFT_BITS 8
#define SEL 512
static GF* F;
static u64 lab[64];
struct Gen { uint32_t mask; u64 t[2][16]; u64 p3[2]; };
static std::vector<Gen> gens;
static inline u64 mix(u64 size, u64 e2, u64 p3) {
  u64 h = e2 * 0x9E3779B97F4A7C15ULL; h ^= h >> 29;
  h += p3 * 0xC2B2AE3D27D4EB4FULL; h ^= h >> 31;
  h *= 0x165667B19E3779F9ULL; h ^= h >> 32;
  return h + size * 0x27D4EB2F165667C5ULL;
}
static void buildGens() {
  // pick 26 independent 2-flats of F_2^5
  std::vector<uint32_t> ech; std::vector<uint32_t> chosen;
  for (int t = 0; t < 32 && chosen.size() < 26; t++) for (int a = 1; a < 32 && chosen.size() < 26; a++) for (int b = a + 1; b < 32 && chosen.size() < 26; b++) {
    if ((a ^ b) < b) continue;  // canonical-ish filter, keeps enough flats
    uint32_t m = (1u << t) | (1u << (t ^ a)) | (1u << (t ^ b)) | (1u << (t ^ a ^ b));
    uint32_t v = m;
    for (uint32_t e : ech) if ((v ^ e) < v) v ^= e;
    if (v) { ech.push_back(v); std::sort(ech.rbegin(), ech.rend()); chosen.push_back(m); }
  }
  if (chosen.size() != 26) { printf("generator failure %zu\n", chosen.size()); exit(1); }
  gens.resize(26);
  for (int k = 0; k < 26; k++) {
    Gen& G = gens[k]; G.mask = chosen[k];
    int pts[4], c = 0; for (int i = 0; i < 32; i++) if (chosen[k] >> i & 1) pts[c++] = i;
    for (int side = 0; side < 2; side++) {
      u64 off = side ? lab[32] : 0, y[4], cube = 0;
      for (int j = 0; j < 4; j++) { y[j] = lab[pts[j]] ^ off; cube ^= F->mul(y[j], F->sq(y[j])); }
      G.p3[side] = cube;
      for (int I = 0; I < 16; I++) {
        u64 e = 0;
        for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) if (((I >> p) & 1) == ((I >> q) & 1)) e ^= F->mul(y[p], y[q]);
        G.t[side][I] = e;  // e2(I) + e2(Y \ I)
      }
    }
  }
}
// walk the coset r_s + RM(3,5), storing mixes.  shiftE2, shiftP3 and sizeTarget implement the query transform for side B.
struct KM{u64 k; uint32_t m;};
static const u64 SAMPLE=(1ULL<<SHIFT_BITS)-1;
static void walk(int side, int s, u64 shiftE2, u64 shiftP3, std::vector<KM>& out) {
  uint32_t S = (s == 0) ? 0 : ((1u << 0) | (1u << s));
  u64 off = side ? lab[32] : 0;
  int size = __builtin_popcount(S);
  u64 e2 = 0, p3 = 0;
  { std::vector<u64> pts; for (int i = 0; i < 32; i++) if (S >> i & 1) pts.push_back(lab[i] ^ off);
    for (size_t i = 0; i < pts.size(); i++) { p3 ^= F->mul(pts[i], F->sq(pts[i])); for (size_t j = i + 1; j < pts.size(); j++) e2 ^= F->mul(pts[i], pts[j]); } }
  size_t total = 1UL << 26;
  out.clear();
  for (size_t idx = 0; idx < total; idx++) {
    { u64 kk = mix(side ? (u64)(36 - size) : (u64)size, e2 ^ shiftE2, p3 ^ shiftP3); if ((kk & SAMPLE) == 0) out.push_back({kk, S}); }
    if (idx + 1 == total) break;
    int k = __builtin_ctzl(idx + 1);
    const Gen& G = gens[k];
    unsigned I = _pext_u32(S, G.mask);
    e2 ^= G.t[side][I];
    p3 ^= G.p3[side];
    size += 4 - 2 * __builtin_popcount(I);
    S ^= G.mask;
  }
}
int main(int argc, char** argv) {
  if (argc < 11) { printf("usage\n"); return 1; }
  int m = atoi(argv[1]); u64 r = strtoull(argv[2], 0, 0);
  static GF field(m, r); F = &field;
  if (!F->irreducible()) { printf("reducible\n"); return 1; }
  u64 ell[6]; for (int i = 0; i < 6; i++) ell[i] = strtoull(argv[3 + i], 0, 16);
  { std::vector<u64> tmp(ell, ell + 6); if (rankF2(tmp) != 6) { printf("labels dependent\n"); return 1; } }
  for (int v = 0; v < 64; v++) { u64 x = 0; for (int i = 0; i < 6; i++) if (v >> i & 1) x ^= ell[i]; lab[v] = x; }
  int w1 = atoi(argv[9]), w2 = atoi(argv[10]);
  auto L = F->subspacePoly({lab[w1], lab[w2]});  // X^4 + a X^2 + b X
  u64 a = L[1], b = L[0];
  buildGens();
  int sv = atoi(argv[11]); size_t maxout = strtoul(argv[12], 0, 10);
  std::vector<KM> A, B;
  u64 ss = F->sq(lab[sv]);
  std::thread th1([&] { walk(0, sv, 0, 0, A); });
  std::thread th2([&] { walk(1, sv, a ^ ss, b, B); });
  th1.join(); th2.join();
  auto cmp = [](const KM& x, const KM& y) { return x.k < y.k; };
  std::sort(A.begin(), A.end(), cmp); std::sort(B.begin(), B.end(), cmp);
  size_t i = 0, j = 0, found = 0, printed = 0; u64 st = 88172645463325252ULL;
  while (i < A.size() && j < B.size()) {
    if (A[i].k < B[j].k) i++;
    else if (A[i].k > B[j].k) j++;
    else { u64 v = A[i].k; size_t i2 = i; while (i2 < A.size() && A[i2].k == v) i2++; size_t j2 = j; while (j2 < B.size() && B[j2].k == v) j2++;
      for (size_t p = i; p < i2; p++) for (size_t q = j; q < j2; q++) { found++; st ^= st << 13; st ^= st >> 7; st ^= st << 17;
        if ((st % SEL) == 0 && printed < maxout) { printed++; printf("%016llx\n", (unsigned long long)(((u64)B[q].m << 32) | A[p].m)); } }
      i = i2; j = j2; }
  }
  fprintf(stderr, "sampled matches %zu printed %zu\n", found, printed);
  return 0;
}
