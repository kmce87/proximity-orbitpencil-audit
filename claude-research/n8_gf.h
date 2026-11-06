// N8 helpers: exact GF(2^m) arithmetic (m <= 64) with a sparse reduction polynomial x^m + r(x), deg r < 32; subspace polynomials.
#pragma once
#include <cstdint>
#include <vector>
#include <immintrin.h>
typedef uint64_t u64;
struct GF {
  int m; u64 r; u64 mask;  // field F_2[x]/(x^m + r)
  GF(int m_, u64 r_) : m(m_), r(r_), mask(m_ == 64 ? ~0ULL : ((1ULL << m_) - 1)) {}
  static inline void cl(u64 a, u64 b, u64& lo, u64& hi) {
    __m128i p = _mm_clmulepi64_si128(_mm_cvtsi64_si128((long long)a), _mm_cvtsi64_si128((long long)b), 0);
    lo = (u64)_mm_cvtsi128_si64(p); hi = (u64)_mm_extract_epi64(p, 1);
  }
  inline u64 mul(u64 a, u64 b) const {
    u64 lo, hi; cl(a, b, lo, hi);
    if (m == 64) {
      u64 l2, h2; cl(hi, r, l2, h2);
      u64 l3, h3; cl(h2, r, l3, h3);
      return lo ^ l2 ^ l3;
    }
    // split at bit m
    u64 top = (lo >> m) | (hi << (64 - m));
    u64 low = lo & mask;
    u64 l2, h2; cl(top, r, l2, h2);
    u64 t2 = (l2 >> m) | (h2 << (64 - m));
    u64 l3, h3; cl(t2, r, l3, h3);
    return low ^ (l2 & mask) ^ (l3 & mask);
  }
  inline u64 sq(u64 a) const { return mul(a, a); }
  u64 pow2k(u64 a, int k) const { for (int i = 0; i < k; i++) a = sq(a); return a; }
  // a^(2^m - 2) by square and multiply (Itoh-Tsujii is not needed at these sizes)
  u64 inv(u64 a) const { u64 r_ = 1, b = sq(a); for (int i = 1; i < m; i++) { r_ = mul(r_, b); b = sq(b); } return r_; }
  // subspace polynomial: c[i] = coefficient of X^(2^i)
  std::vector<u64> subspacePoly(const std::vector<u64>& basis) const {
    std::vector<u64> P{1};
    for (u64 u : basis) {
      u64 v = linEval(P, u);
      std::vector<u64> Q(P.size() + 1, 0);
      for (size_t i = 0; i < P.size(); i++) { Q[i + 1] ^= sq(P[i]); Q[i] ^= mul(v, P[i]); }
      P.swap(Q);
    }
    return P;
  }
  u64 linEval(const std::vector<u64>& L, u64 x) const { u64 s = 0, p = x; for (u64 c : L) { if (c) s ^= mul(c, p); p = sq(p); } return s; }
  // Rabin irreducibility test for x^m + r
  bool irreducible() const {
    // x^(2^m) == x, and gcd(x^(2^(m/p)) - x, f) = 1 is checked through: x^(2^d) != x for proper divisors d of m is necessary and,
    // with the first condition, sufficient when tested for all maximal proper divisors using polynomial gcd; here we test by order of x^(2^d) - x being invertible.
    u64 x = 2; if (m == 1) return true;
    u64 y = x; for (int i = 0; i < m; i++) y = sq(y);
    if (y != x) return false;
    for (int p = 2; p <= m; p++) {
      if (m % p) continue;
      bool prime = true; for (int q = 2; q * q <= p; q++) if (p % q == 0) prime = false;
      if (!prime) continue;
      u64 z = x; for (int i = 0; i < m / p; i++) z = sq(z);
      u64 w = z ^ x;
      if (w == 0) return false;
      // w must be a unit in the quotient ring: w^(2^m - 1) == 1 is implied by invertibility only in a field; test directly
      if (mul(w, inv(w)) != 1) return false;
    }
    return true;
  }
};
// All 2^k combinations of the generators, Gray-free (index bit i <-> gens[i]).
static inline std::vector<u64> spanOf(const std::vector<u64>& gens) {
  std::vector<u64> A{0};
  for (u64 g : gens) { size_t n = A.size(); for (size_t i = 0; i < n; i++) A.push_back(A[i] ^ g); }
  return A;
}
static inline int rankF2(std::vector<u64> v) {
  int r = 0;
  for (int b = 63; b >= 0; b--) {
    int p = -1;
    for (size_t i = r; i < v.size(); i++) if ((v[i] >> b) & 1) { p = (int)i; break; }
    if (p < 0) continue;
    std::swap(v[r], v[p]);
    for (size_t i = 0; i < v.size(); i++) if ((int)i != r && ((v[i] >> b) & 1)) v[i] ^= v[r];
    r++;
  }
  return r;
}
