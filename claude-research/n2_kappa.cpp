// N2: the degree-2^14 coefficient kappa_S of C_S in BitWonka's real family (BF64, f = 6).
// Exact arithmetic in GF(2)[x]/(x^64+x^4+x^3+x+1) (CompPoly BF64), labels and family as in
// ProximityPrize/SubmissionBinaryUpper (credit: BitWonka, PR #592).
// Build: g++ -O2 -mpclmul -std=c++17 n2_kappa.cpp -o n2_kappa; run: ./n2_kappa qrows.txt
#include <cstdint>
#include <cstdio>
#include <vector>
#include <array>
#include <random>
#include <algorithm>
#include <unordered_map>
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
static inline u64 gsqr(u64 a) { return gmul(a, a); }
static u64 gpow(u64 a, unsigned __int128 e) { u64 r = 1; while (e) { if (e & 1) r = gmul(r, a); a = gsqr(a); e >>= 1; } return r; }
static u64 ginv(u64 a) { return gpow(a, (((unsigned __int128)1 << 64) - 2)); }
static u64 gsqrt(u64 a) { for (int i = 0; i < 63; i++) a = gsqr(a); return a; }
// Linearized polynomial: c[i] = coefficient of X^(2^i).
typedef std::vector<u64> Lin;
static u64 linEval(const Lin& L, u64 x) { u64 r = 0, p = x; for (u64 c : L) { if (c) r ^= gmul(c, p); p = gsqr(p); } return r; }
// P_{k+1} = P_k * (P_k - P_k(u)) = P_k^2 + P_k(u) P_k  (char 2).
static Lin subspacePoly(const std::vector<u64>& basis) {
  Lin P = {1};
  for (u64 u : basis) {
    u64 c = linEval(P, u);
    Lin Q(P.size() + 1, 0);
    for (size_t i = 0; i < P.size(); i++) { Q[i + 1] ^= gsqr(P[i]); Q[i] ^= gmul(c, P[i]); }
    P = Q;
  }
  return P;
}
static inline int parity(u64 x) { return __builtin_parityll(x); }
static inline int bit(u64 x, int i) { return (x >> i) & 1; }
// Label space: v = y | (z << 11), y 11 bits, z 4 bits. lab(v) = xor of ell[i].
static u64 ell[15];
static u64 lab(unsigned v) { u64 r = 0; for (int i = 0; i < 15; i++) if (bit(v, i)) r ^= ell[i]; return r; }
struct Row { int q[3]; int s[3]; };
static std::vector<Row> rows;
static int lowbit4(int s) { return (s & 1) ? 0 : (s & 2) ? 1 : (s & 4) ? 2 : 3; }
static int betaOf(int s, int j) { int l = lowbit4(s); return j % (1 << l) + (1 << (l + 1)) * (j / (1 << l)); }
static unsigned insertZero(unsigned m, int pos) { return (m & ((1u << pos) - 1)) | ((m >> pos) << (pos + 1)); }
struct Param { int row, jr, aa, ee; unsigned r; unsigned m[3]; int jn[3]; int e0, e1; };
// Functionals on V: y-part mask and z-part mask combined into a 15-bit mask.
static inline int dotv(unsigned f, unsigned v) { return parity(f & v); }
struct Flat { unsigned f[3]; int t[3]; };          // f[i].v = t[i]
static Flat flatOf(const Param& p, int k) {
  const Row& R = rows[p.row];
  int kap = (k == 0) ? 1 : 0;
  int beta = betaOf(R.s[0], p.jr);
  int coefL = (k == 0) ? 0 : (k == 1 ? p.ee : (p.ee ^ 1));
  int rhoC = (k == 0) ? p.aa : (k == 1 ? (p.aa ^ 1 ^ p.ee) : (p.aa ^ p.ee));
  int bC = (k == 0) ? p.e0 : (k == 1 ? ((p.aa ^ p.ee) ? 1 : p.e1) : ((p.aa ^ p.ee) ? p.e1 : 1));
  int rhoLinMask = beta ^ (coefL ? R.s[0] : 0);
  int pv = __builtin_ctz(p.r);                     // a pivot of r (the Lean uses Classical.choose)
  unsigned mm = insertZero(p.m[k], pv);
  int nuS = betaOf(R.s[k], p.jn[k]);
  Flat F;
  F.f[0] = (unsigned)R.s[k] << 11; F.t[0] = kap;
  F.f[1] = p.r | ((unsigned)rhoLinMask << 11); F.t[1] = rhoC;
  F.f[2] = mm | ((unsigned)nuS << 11); F.t[2] = bC;
  return F;
}
// Basis of the direction of a flat (kernel of three independent functionals on F_2^15), and one point.
static void flatDirection(const Flat& F, std::vector<unsigned>& basis, unsigned& pt) {
  // Row reduce the 3x15 system.
  std::array<unsigned,3> a = {F.f[0], F.f[1], F.f[2]}; std::array<int,3> b = {F.t[0], F.t[1], F.t[2]};
  int piv[3], rk = 0;
  for (int col = 0; col < 15 && rk < 3; col++) {
    int sel = -1; for (int i = rk; i < 3; i++) if (bit(a[i], col)) { sel = i; break; }
    if (sel < 0) continue;
    std::swap(a[sel], a[rk]); std::swap(b[sel], b[rk]);
    for (int i = 0; i < 3; i++) if (i != rk && bit(a[i], col)) { a[i] ^= a[rk]; b[i] ^= b[rk]; }
    piv[rk++] = col;
  }
  if (rk != 3) { fprintf(stderr, "rank %d\n", rk); exit(1); }
  pt = 0; for (int i = 0; i < 3; i++) if (b[i]) pt |= 1u << piv[i];
  basis.clear();
  for (int col = 0; col < 15; col++) {
    if (col == piv[0] || col == piv[1] || col == piv[2]) continue;
    unsigned w = 1u << col;
    for (int i = 0; i < 3; i++) if (bit(a[i], col)) w |= 1u << piv[i];
    basis.push_back(w);
  }
}
static std::vector<u64> labs(const std::vector<unsigned>& B) { std::vector<u64> o; for (unsigned w : B) o.push_back(lab(w)); return o; }
static std::vector<unsigned> memberSet(const Param& p) {
  const Row& R = rows[p.row];
  Flat Fs[3]; for (int k = 0; k < 3; k++) Fs[k] = flatOf(p, k);
  std::vector<unsigned> S;
  for (unsigned v = 0; v < (1u << 15); v++) {
    int z = v >> 11;
    bool in = (z == R.q[0] || z == R.q[1] || z == R.q[2]);
    for (int k = 0; k < 3 && !in; k++)
      in = dotv(Fs[k].f[0], v) == Fs[k].t[0] && dotv(Fs[k].f[1], v) == Fs[k].t[1] && dotv(Fs[k].f[2], v) == Fs[k].t[2];
    if (in) S.push_back(v);
  }
  return S;
}
static Lin LW; static u64 cq[16];
static Param randomParam(std::mt19937_64& g) {
  Param p; p.row = g() % rows.size(); p.jr = g() % 8; p.aa = g() % 2; p.ee = g() % 2;
  do { p.r = g() % 2048; } while (!p.r);
  do { for (int k = 0; k < 3; k++) { do { p.m[k] = g() % 1024; } while (!p.m[k]); } } while (p.m[0]==p.m[1] || p.m[0]==p.m[2] || p.m[1]==p.m[2]);
  for (int k = 0; k < 3; k++) p.jn[k] = g() % 8;
  p.e0 = g() % 2; p.e1 = g() % 2;
  return p;
}
static u64 a11OfFlat(const Param& p, int k) {
  std::vector<unsigned> B; unsigned pt; flatDirection(flatOf(p, k), B, pt);
  Lin L = subspacePoly(labs(B));           // degree 2^12: L[12] = 1, L[11] = a_11
  if (L.size() != 13 || L[12] != 1) { fprintf(stderr, "bad L\n"); exit(1); }
  return L[11];
}
static u64 kappaFormula(const Param& p) {
  const Row& R = rows[p.row];
  u64 k = cq[R.q[0]] ^ cq[R.q[1]] ^ cq[R.q[2]];
  for (int t = 0; t < 3; t++) k ^= a11OfFlat(p, t);
  return k;
}
// ---------- dense polynomial helpers (index = degree) ----------
typedef std::vector<u64> Poly;
static Poly pmulSparse(const Poly& A, const std::vector<std::pair<int,u64>>& B) {
  int da = A.size() - 1, db = 0; for (auto& t : B) db = std::max(db, t.first);
  Poly R(da + db + 1, 0);
  for (auto& t : B) for (int i = 0; i <= da; i++) if (A[i]) R[i + t.first] ^= gmul(A[i], t.second);
  return R;
}
static std::vector<std::pair<int,u64>> sparseOfLin(const Lin& L, u64 c0) {
  std::vector<std::pair<int,u64>> s; if (c0) s.push_back({0, c0});
  for (size_t i = 0; i < L.size(); i++) if (L[i]) s.push_back({1 << i, L[i]});
  return s;
}
static int degOf(const Poly& P) { int d = P.size() - 1; while (d >= 0 && !P[d]) d--; return d; }
static void loadRows(const char* path) {
  FILE* f = fopen(path, "r"); if (!f) { perror("qrows"); exit(1); }
  Row R; while (fscanf(f, "%d %d %d %d %d %d", &R.q[0], &R.q[1], &R.q[2], &R.s[0], &R.s[1], &R.s[2]) == 6) rows.push_back(R);
  fclose(f);
}
int main(int argc, char** argv) {
  loadRows(argv[1]);
  std::mt19937_64 g(20261103);
  // T0 field sanity
  if (gmul(1ULL << 63, 2) != 0x1B) { puts("field FAIL"); return 1; }
  u64 t0 = 0x123456789ABCDEFULL; if (gmul(t0, ginv(t0)) != 1 || gsqr(gsqrt(t0)) != t0) { puts("inv/sqrt FAIL"); return 1; }
  // T1 labels
  std::vector<u64> low; for (int i = 0; i < 6; i++) low.push_back(1ULL << i);
  Lin Ys = subspacePoly(low);
  for (u64 l = 0; l < 64; l++) if (linEval(Ys, l)) { puts("Ys FAIL"); return 1; }
  for (int i = 0; i < 15; i++) ell[i] = linEval(Ys, 1ULL << (6 + i));
  // T2 L_W and c_q
  std::vector<u64> lowLabs(ell, ell + 11); LW = subspacePoly(lowLabs);
  for (int q = 0; q < 16; q++) cq[q] = linEval(LW, lab((unsigned)q << 11));
  printf("field ok; ell[0]=%016llx LW has %zu terms; rows=%zu\n", (unsigned long long)ell[0], LW.size(), rows.size());
  // T3 direct locators
  int nDirect = (argc > 2) ? atoi(argv[2]) : 3;
  for (int it = 0; it < nDirect; it++) {
    Param p = randomParam(g);
    auto S = memberSet(p);
    Poly V = {1}; V.reserve(S.size() + 1);
    for (unsigned v : S) { u64 c = lab(v); V.push_back(0); for (int i = V.size() - 1; i > 0; i--) V[i] = V[i - 1] ^ gmul(V[i], c); V[0] = gmul(V[0], c); }
    // Rtop = L_W^3 X^12288
    Poly T = {1}; auto sW = sparseOfLin(LW, 0);
    for (int k = 0; k < 3; k++) T = pmulSparse(T, sW);
    Poly C = V; for (size_t i = 0; i < T.size(); i++) C[i + 12288] ^= T[i];
    int d = degOf(C); u64 kap = C[16384];
    Poly C2 = C; C2[16384] = 0; int d2 = degOf(C2);
    Poly C3 = C2; if (d2 >= 0) C3[d2] = 0; int d3 = degOf(C3);
    printf("member %d: |S|=%zu has0=%d degV=%d deg(C)=%d kappa_direct=%016llx kappa_formula=%016llx match=%d next degrees: %d %d\n",
      it, S.size(), (int)std::count(S.begin(), S.end(), 0u), degOf(V), d, (unsigned long long)kap, (unsigned long long)kappaFormula(p), kap == kappaFormula(p), d2, d3);
  }
  // T4/T5 hyperplane structure of one W_t, exhaustive over (m, jn)
  int injective_all = 1, identity_all = 1, additive_all = 1;
  for (int trial = 0; trial < 6; trial++) {
    Param p = randomParam(g); int t = trial % 3;
    Flat F0 = flatOf(p, t);
    // W_t = kernel of the first two functionals. Build a basis by extending direction of U.
    std::vector<unsigned> UB; unsigned pt; flatDirection(F0, UB, pt);
    unsigned wx = 0; for (unsigned v = 1; v < (1u << 15); v++) if (dotv(F0.f[0], v) == 0 && dotv(F0.f[1], v) == 0 && dotv(F0.f[2], v) == 1) { wx = v; break; }
    auto WB = UB; WB.push_back(wx);
    Lin LWt = subspacePoly(labs(WB));
    if (LWt.size() != 14) { puts("W FAIL"); return 1; }
    u64 A12 = LWt[12];
    std::unordered_map<u64,int> seen; seen.reserve(20000);
    for (int m = 1; m < 1024; m++) for (int j = 0; j < 8; j++) {
      Param q = p; q.m[t] = m; q.jn[t] = j;
      Flat Fq = flatOf(q, t); std::vector<unsigned> B; unsigned pq; flatDirection(Fq, B, pq);
      Lin L = subspacePoly(labs(B)); u64 a = L[11];
      unsigned w = 0; for (unsigned x : WB) if (dotv(Fq.f[2], x) == 1) { w = x; break; }
      u64 c = linEval(L, lab(w));
      if (gsqr(a) != (A12 ^ c)) identity_all = 0;
      if (seen.count(a)) injective_all = 0;
      seen[a] = 1;
    }
    if (seen.size() != 1023u * 8u) injective_all = 0;
    // additivity of U -> 1/c_U^2 in the functional, on all hyperplanes of W_t (random triples)
    std::vector<u64> xi(1u << 13, 0);
    for (unsigned code = 1; code < (1u << 13); code++) {
      // functional on W_t with coordinates code in the basis WB
      std::vector<unsigned> ker; int pivot = __builtin_ctz(code);
      for (int i = 0; i < 13; i++) if (i != pivot) ker.push_back(WB[i] ^ (bit(code, i) ? WB[pivot] : 0));
      Lin L = subspacePoly(labs(ker)); u64 c = linEval(L, lab(WB[pivot]));
      xi[code] = ginv(gsqr(c));
    }
    for (unsigned a = 1; a < (1u << 13); a++) for (int b = 0; b < 13; b++) { unsigned e = 1u << b; if ((a ^ e) && xi[a ^ e] != (xi[a] ^ xi[e])) additive_all = 0; }
  }
  printf("a_11 injective on (m,jn), identity a^2=A12+c, additivity of 1/c^2: %d %d %d\n", injective_all, identity_all, additive_all);

  // T6 fibres of kappa on one slice (row, rho, r fixed; (m_t, jn_t) free, m's not forced distinct: an upper bound).
  {
    Param p = randomParam(g);
    std::vector<u64> A[3];
    for (int t = 0; t < 3; t++) { A[t].reserve(8184);
      for (int m = 1; m < 1024; m++) for (int j = 0; j < 8; j++) { Param q = p; q.m[t] = m; q.jn[t] = j; A[t].push_back(a11OfFlat(q, t)); } }
    std::vector<u64> P; P.reserve(A[0].size() * A[1].size());
    for (u64 a : A[0]) for (u64 b : A[1]) P.push_back(a ^ b);
    std::sort(P.begin(), P.end());
    size_t dup = 0; for (size_t i = 1; i < P.size(); i++) if (P[i] == P[i-1]) dup++;
    long long maxFib = 0, totFib = 0; int samples = 4000;
    for (int it = 0; it < samples; it++) {
      u64 kap = A[0][g() % 8184] ^ A[1][g() % 8184] ^ A[2][g() % 8184];
      long long fib = 0;
      for (u64 c : A[2]) { auto r = std::equal_range(P.begin(), P.end(), kap ^ c); fib += r.second - r.first; }
      maxFib = std::max(maxFib, fib); totFib += fib;
    }
    printf("slice: |A0+A1 pairs|=%zu duplicate pair-sums=%zu; sampled kappa fibres on 8184^3 triples: mean=%.4f max=%lld (samples=%d)\n",
      P.size(), dup, (double)totFib / samples, maxFib, samples);
  }
  // T7 kappa over the whole family: random members, count repeated values.
  {
    size_t N = 3000000; std::vector<u64> K_; K_.reserve(N);
    for (size_t i = 0; i < N; i++) K_.push_back(kappaFormula(randomParam(g)));
    std::sort(K_.begin(), K_.end());
    size_t distinct = std::unique(K_.begin(), K_.end()) - K_.begin();
    printf("whole family: %zu random members, %zu distinct kappa values\n", N, distinct);
    // invariance under the translation-only parameters (aa, e0, e1)
    int inv = 1; for (int it = 0; it < 2000; it++) { Param p = randomParam(g); u64 k0 = kappaFormula(p); Param q = p; q.aa ^= 1; q.e0 ^= 1; q.e1 ^= 1; if (kappaFormula(q) != k0) inv = 0; }
    printf("kappa invariant under (aa,e0,e1): %d\n", inv);
  }
  return 0;
}
