import Mathlib

/-!
Candidate lemma for the n = 2^21 KoalaBear OrbitPencil lift.

STATUS: NOT COMPILED. Requires Lean 4.34/Mathlib, and the entire bridge
from the formal RS code to its received-line direction is still unproved.

The original root-counting approach is credited to the accepted OrbitPencil
Lean proof, proximity-prize/proximity-prize PR #38 (incl. erdkocak).

Assumptions are explicit: A is the degree-4096 denominator polynomial,
R is the degree-at-most-4095 nonzero core polynomial, q is a degree-<2^20
codeword polynomial, and P = A*q+R vanishes on a support S.
-/

namespace OrbitPencilLiftNoncontainment

open Polynomial

/-- A nonzero at-most-4095-degree core cannot cancel a 4096-degree factor times
    a degree-<1048576 RS polynomial on 1116048 different field points.
    The support is a Finset of *field elements*: injectivity of the original
    index-domain map must be established separately before applying this. -/
theorem no_large_support {F : Type*} [Field F]
    (A R q : Polynomial F) (S : Finset F)
    (hAne : A ≠ 0) (hAdeg : A.natDegree = 4096)
    (hRne : R ≠ 0) (hRdeg : R.natDegree ≤ 4095)
    (hqdeg : q.natDegree ≤ 1048575)
    (hScard : 1116048 ≤ S.card)
    (heval : ∀ x ∈ S, (A * q + R).eval x = 0) : False := by
  let P : Polynomial F := A * q + R
  have hPdeg : P.natDegree ≤ 1052671 := by
    dsimp [P]
    calc
      (A * q + R).natDegree ≤ max (A * q).natDegree R.natDegree :=
        Polynomial.natDegree_add_le _ _
      _ ≤ max (A.natDegree + q.natDegree) R.natDegree :=
        max_le_max (Polynomial.natDegree_mul_le) le_rfl
      _ ≤ 1052671 := by omega
  have hPzero : P = 0 := by
    apply Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero' P S
    · exact heval
    · omega
  have hEq : A * q = -R := by
    have hzero : A * q + R = 0 := hPzero
    exact add_eq_zero_iff_eq_neg.mp hzero
  by_cases hq : q = 0
  · subst q
    have hRzero : R = 0 := by
      simpa only [mul_zero, neg_eq_zero] using hEq.symm
    exact hRne hRzero
  · have hDegEq : A.natDegree + q.natDegree = R.natDegree := by
      calc
        A.natDegree + q.natDegree = (A * q).natDegree := by
          rw [Polynomial.natDegree_mul hAne hq]
        _ = R.natDegree := by rw [hEq, Polynomial.natDegree_neg]
    omega

end OrbitPencilLiftNoncontainment
