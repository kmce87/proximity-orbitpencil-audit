// Run 17: real-field meaning of ChatGPT lane B's two binary gates of 2026-11-10 (read only).
// BF64 = GF(2)[x]/(x^64+x^4+x^3+x+1), labels and LabelFamily member construction reused verbatim
// from n2_kappa.cpp (credit: the family is BitWonka's, PR #592).
//  A (61bdc80, reserved-coset XOR): the reserved block prod_{z in Q} (L_W + c_z) has second coefficient
//    c_Q = c_{q0} + c_{q1} + c_{q2} = L_W(ell(xor Q)); check c is F_2-linear and injective on F_2^4, so c_Q
//    takes exactly 15 nonzero values (28 rows each, by r17_laneb_check.py), and compare with the
//    direct locator of the 3 * 2^11 reserved points.
//  B (4b399f5, affine constants): (aa, e0, e1) only move the constants of the three flat locators
//    L_U(X) + L_U(c), so every coefficient of V_S above |S| - 2^12 = 14336 (kappa at 16384 included)
//    is the same for the 8 members; direct locators at the real size, |S| = 18432.
// Build: g++ -O2 -mpclmul -msse4.1 -std=c++17 r17_laneb_real.cpp -o r17_laneb_real
// Run:   ./r17_laneb_real qrows.txt [nparams]
#define main n2_main
#include "n2_kappa.cpp"
#undef main

static Poly directLocator(const std::vector<unsigned>& S) {
  Poly V = {1}; V.reserve(S.size() + 1);
  for (unsigned v : S) { u64 c = lab(v); V.push_back(0); for (int i = V.size() - 1; i > 0; i--) V[i] = V[i - 1] ^ gmul(V[i], c); V[0] = gmul(V[0], c); }
  return V;
}

int main(int argc, char** argv) {
  loadRows(argv[1]);
  int nParams = (argc > 2) ? atoi(argv[2]) : 3;
  std::vector<u64> low; for (int i = 0; i < 6; i++) low.push_back(1ULL << i);
  Lin Ys = subspacePoly(low);
  for (int i = 0; i < 15; i++) ell[i] = linEval(Ys, 1ULL << (6 + i));
  std::vector<u64> lowLabs(ell, ell + 11); LW = subspacePoly(lowLabs);
  for (int q = 0; q < 16; q++) cq[q] = linEval(LW, lab((unsigned)q << 11));
  if (rows.size() != 420 || LW.size() != 12 || LW[11] != 1) { puts("setup FAIL"); return 1; }

  // A1: c is additive and injective on F_2^4.
  bool lin = cq[0] == 0, inj = true;
  for (int a = 0; a < 16; a++) for (int b = 0; b < 16; b++) if (cq[a ^ b] != (cq[a] ^ cq[b])) lin = false;
  for (int a = 1; a < 16; a++) for (int b = 0; b < a; b++) if (cq[a] == cq[b]) inj = false;
  // A2: every row's reserved second coefficient is c_{xor Q} != 0.
  std::unordered_map<u64,int> vals; bool rowsOk = true;
  for (auto& R : rows) { u64 s = cq[R.q[0]] ^ cq[R.q[1]] ^ cq[R.q[2]]; if (!s || s != cq[R.q[0] ^ R.q[1] ^ R.q[2]]) rowsOk = false; vals[s]++; }
  bool counts = vals.size() == 15; for (auto& kv : vals) if (kv.second != 28) counts = false;
  printf("A: c_z additive %d, injective %d; reserved coefficient = c_{xor Q} != 0 on all 420 rows %d; %zu distinct values, 28 rows each %d\n",
    lin, inj, rowsOk, vals.size(), counts);
  // A3: direct locator of the reserved block for 3 rows vs (L_W + c0)(L_W + c1)(L_W + c2).
  bool directOk = true;
  for (int ri : {0, 211, 419}) {
    const Row& R = rows[ri];
    std::vector<unsigned> P; for (int k = 0; k < 3; k++) for (unsigned y = 0; y < 2048; y++) P.push_back(y | ((unsigned)R.q[k] << 11));
    Poly V = directLocator(P);
    Poly T = {1}; for (int k = 0; k < 3; k++) T = pmulSparse(T, sparseOfLin(LW, cq[R.q[k]]));
    if (V != T) directOk = false;
    Poly T3 = {1}; for (int k = 0; k < 3; k++) T3 = pmulSparse(T3, sparseOfLin(LW, 0));   // L_W^3
    Poly Dif = V; for (size_t i = 0; i < T3.size(); i++) Dif[i] ^= T3[i];
    if (degOf(V) != 6144 || degOf(Dif) != 4096 || Dif[4096] != cq[R.q[0] ^ R.q[1] ^ R.q[2]]) directOk = false;
  }
  printf("A: direct reserved locators (rows 0, 211, 419) = product formula; V - L_W^3 has degree exactly 4096 = 6144 - 2^11 with top c_{xor Q}: %d\n", directOk);

  // B: (aa, e0, e1) invariance at the real size.
  std::mt19937_64 g(20261111);
  bool allInv = true, allKap = true, allDistinct = true; int minTop = 1 << 30, maxTop = -1;
  for (int it = 0; it < nParams; it++) {
    Param p = randomParam(g);
    std::vector<Poly> Vs; std::vector<std::vector<unsigned>> Ss;
    for (int c = 0; c < 8; c++) {
      Param q = p; q.aa = c & 1; q.e0 = (c >> 1) & 1; q.e1 = (c >> 2) & 1;
      auto S = memberSet(q);
      if (S.size() != 18432) { puts("size FAIL"); return 1; }
      Poly V = directLocator(S);
      Poly T = {1}; auto sW = sparseOfLin(LW, 0); for (int k = 0; k < 3; k++) T = pmulSparse(T, sW);
      u64 kap = V[16384] ^ T[16384 - 12288];
      if (kap != kappaFormula(q)) allKap = false;
      Ss.push_back(S); Vs.push_back(V);
    }
    for (int a = 0; a < 8; a++) for (int b = 0; b < a; b++) if (Ss[a] == Ss[b]) allDistinct = false;
    int top = -1;                                   // highest degree where two of the 8 locators differ
    for (int d = 18432; d >= 0 && top < 0; d--) for (int c = 1; c < 8; c++) if (Vs[c][d] != Vs[0][d]) { top = d; break; }
    if (top > 14336) allInv = false;
    minTop = std::min(minTop, top); maxTop = std::max(maxTop, top);
    printf("B: params %d (row %d): 8 distinct members %d, highest differing degree %d, kappa = formula %d\n", it, p.row, allDistinct, top, allKap);
  }
  printf("B: over %d parameter sets, coefficients above 14336 invariant %d (highest differing degree %d..%d), kappa equal and = formula %d\n",
    nParams, allInv, minTop, maxTop, allKap);
  bool pass = lin && inj && rowsOk && counts && directOk && allInv && allKap && allDistinct && maxTop == 14336;
  puts(pass ? "PASS: both lane B gates hold in BF64 at the real size; neutral for the record (N2's factor-8 invariance, reserved gap 2^11)" : "FAIL");
  return pass ? 0 : 1;
}
