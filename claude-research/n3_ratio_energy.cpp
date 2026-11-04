// N3 side check: multiplicative structure of real label spaces.  Counts repeated ratios v/w among nonzero elements of an F_2-space A in BF64.
// A repeated ratio lam != 1 with multiplicity m means dim(A cap lam A) is large enough to hold m nonzero elements.
// Spaces: control D_<=12 (Krylov, f = 0) and A = L_Z(span(x^6..x^18)), a 13-dimensional part of the real f = 6 labels with Z = first 64 words.
// Build: g++ -O2 -mpclmul -msse4.1 -std=c++17 n3_ratio_energy.cpp -o n3_ratio_energy
#include <cstdint>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <immintrin.h>
typedef uint64_t u64;
static inline u64 gmul(u64 a, u64 b) {
  __m128i p = _mm_clmulepi64_si128(_mm_cvtsi64_si128((long long)a), _mm_cvtsi64_si128((long long)b), 0);
  u64 lo = (u64)_mm_cvtsi128_si64(p), hi = (u64)_mm_extract_epi64(p, 1);
  __m128i q = _mm_clmulepi64_si128(_mm_cvtsi64_si128((long long)hi), _mm_cvtsi64_si128(0x1B), 0);
  u64 l2 = (u64)_mm_cvtsi128_si64(q), h2 = (u64)_mm_extract_epi64(q, 1);
  __m128i r = _mm_clmulepi64_si128(_mm_cvtsi64_si128((long long)h2), _mm_cvtsi64_si128(0x1B), 0);
  return lo ^ l2 ^ (u64)_mm_cvtsi128_si64(r);
}
static u64 gpow(u64 a, unsigned __int128 e) { u64 r = 1; while (e) { if (e & 1) r = gmul(r, a); a = gmul(a, a); e >>= 1; } return r; }
static u64 ginv(u64 a) { return gpow(a, (((unsigned __int128)1 << 64) - 2)); }
typedef std::vector<u64> Lin;
static u64 linEval(const Lin& L, u64 x) { u64 r = 0, p = x; for (u64 c : L) { if (c) r ^= gmul(c, p); p = gmul(p, p); } return r; }
static Lin subspacePoly(const std::vector<u64>& basis) {
  Lin P{1};
  for (u64 u : basis) {
    u64 v = linEval(P, u);
    Lin Q(P.size() + 1, 0);
    for (size_t i = 0; i < P.size(); i++) { Q[i + 1] ^= gmul(P[i], P[i]); Q[i] ^= gmul(v, P[i]); }
    P = Q;
  }
  return P;
}
static void energy(const char* name, const std::vector<u64>& gens) {
  std::vector<u64> A{0};
  for (u64 g : gens) { size_t n = A.size(); for (size_t i = 0; i < n; i++) A.push_back(A[i] ^ g); }
  std::vector<u64> nz, inv;
  for (u64 a : A) if (a) { nz.push_back(a); inv.push_back(ginv(a)); }
  std::vector<u64> R; R.reserve(nz.size() * nz.size());
  for (size_t i = 0; i < nz.size(); i++) for (size_t j = 0; j < nz.size(); j++) if (i != j) R.push_back(gmul(nz[i], inv[j]));
  std::sort(R.begin(), R.end());
  size_t i = 0, distinct = 0, rep = 0, mx = 0; u64 best = 0;
  while (i < R.size()) {
    size_t j = i; while (j < R.size() && R[j] == R[i]) j++;
    size_t m = j - i; distinct++;
    if (m > 1) rep++;
    if (m > mx) { mx = m; best = R[i]; }
    i = j;
  }
  printf("%s: |A|=2^%zu pairs=%zu distinct ratios=%zu repeated=%zu max multiplicity=%zu (lam=%016llx)\n", name, gens.size(), R.size(), distinct, rep, mx, (unsigned long long)best);
}
int main() {
  std::vector<u64> ctrl; for (int i = 0; i <= 12; i++) ctrl.push_back(1ULL << i);
  energy("control D_<=12 (f=0)", ctrl);
  std::vector<u64> zb; for (int i = 0; i < 6; i++) zb.push_back(1ULL << i);
  Lin LZ = subspacePoly(zb);
  std::vector<u64> g6; for (int i = 6; i <= 18; i++) g6.push_back(linEval(LZ, 1ULL << i));
  energy("L_Z(span x^6..x^18) (f=6 labels)", g6);
  std::vector<u64> rnd; u64 s = 0x9E3779B97F4A7C15ULL;
  for (int i = 0; i < 13; i++) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; rnd.push_back(s); }
  energy("random 13-dim space (control)", rnd);
  return 0;
}
