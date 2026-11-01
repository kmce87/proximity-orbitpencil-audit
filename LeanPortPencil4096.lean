import LeanPortConcreteSlopes
import LeanPortSupport4096

/-!
# 4096-fibre OrbitPencil polynomial factorisation and message degree

Proof adapted from the accepted Proximity Prize OrbitPencil.lean (PR #38,
original contributors including erdkocak). The n=2^21 lift uses the
concrete KoalaBear.Ext6 field, a 4095-point core and z = x^4096.

This module establishes the crucial RS message-degree upper bound
1048575 = 2^20 - 1 for any two selections sharing a candidate key and
any nonzero separating alpha. It does NOT yet show that the received affine
line agrees on the support or that the slopes satisfy MCA.
-/

namespace OrbitPencilLiftPencil4096

open Polynomial
open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

noncomputable def deltaV (U0 U : Finset Small) : Polynomial Sextic :=
  V y6 U0 - V y6 U

noncomputable def gamma (alpha : Sextic) (U0 U : Finset Small) : Sextic :=
  (deltaV U0 U).eval alpha / alpha

noncomputable def pencil (alpha : Sextic) (U0 U : Finset Small) : Polynomial Sextic :=
  deltaV U0 U - Polynomial.C (gamma alpha U0 U) * Polynomial.X

theorem delta_eval_zero {U0 U : Finset Small}
    (hU0 : U0 ∈ Candidates) (hU : U ∈ Candidates)
    (hk : key projectedNode U0 = key projectedNode U) :
    (deltaV U0 U).eval 0 = 0 := by
  have hconst := concrete_sextic_constant_eq_of_key hU0 hU hk
  change (V y6 U0).eval 0 = (V y6 U).eval 0 at hconst
  rw [deltaV, Polynomial.eval_sub, hconst, sub_self]

theorem pencil_eval_zero {alpha : Sextic} {U0 U : Finset Small}
    (hU0 : U0 ∈ Candidates) (hU : U ∈ Candidates)
    (hk : key projectedNode U0 = key projectedNode U) :
    (pencil alpha U0 U).eval 0 = 0 := by
  simp [pencil, delta_eval_zero hU0 hU hk]

theorem pencil_eval_alpha (alpha : Sextic) (hα : alpha ≠ 0)
    (U0 U : Finset Small) :
    (pencil alpha U0 U).eval alpha = 0 := by
  rw [pencil, Polynomial.eval_sub, Polynomial.eval_mul,
    Polynomial.eval_C, Polynomial.eval_X, gamma,
    div_mul_cancel₀ _ hα, sub_self]

theorem pencil_degree_lt {alpha : Sextic} {U0 U : Finset Small}
    (hU0 : U0 ∈ Candidates) (hU : U ∈ Candidates)
    (hk : key projectedNode U0 = key projectedNode U) :
    (pencil alpha U0 U).degree < (258 : ℕ) := by
  have hd : (deltaV U0 U).degree < (258 : ℕ) := by
    have hn := concrete_sextic_degree_lt_of_key hU0 hU hk
    by_cases hz : deltaV U0 U = 0
    · rw [hz]
      exact WithBot.bot_lt_coe 258
    · rw [Polynomial.degree_eq_natDegree hz]
      exact_mod_cast hn
  have hlin : (Polynomial.C (gamma alpha U0 U) *
      (Polynomial.X : Polynomial Sextic)).degree < (258 : ℕ) := by
    calc
      (Polynomial.C (gamma alpha U0 U) * (Polynomial.X : Polynomial Sextic)).degree
          ≤ (1 : ℕ) := by
            simpa using Polynomial.degree_C_mul_X_le (gamma alpha U0 U)
      _ < (258 : ℕ) := by norm_num
  exact (Polynomial.degree_sub_le _ _).trans_lt (max_lt hd hlin)

/-- Same-key differences vanish at 0; subtracting gamma X also makes alpha
a root. Hence X(X-alpha) divides the pencil, leaving degree at most 255. -/
theorem exists_quotient {alpha : Sextic} (hα : alpha ≠ 0)
    {U0 U : Finset Small}
    (hU0 : U0 ∈ Candidates) (hU : U ∈ Candidates)
    (hk : key projectedNode U0 = key projectedNode U) :
    ∃ Q : Polynomial Sextic,
      pencil alpha U0 U =
        (Polynomial.X : Polynomial Sextic) *
          (Polynomial.X - Polynomial.C alpha) * Q ∧
      Q.natDegree ≤ 255 := by
  have hx : (Polynomial.X : Polynomial Sextic) ∣ pencil alpha U0 U := by
    rw [show (Polynomial.X : Polynomial Sextic) =
      Polynomial.X - Polynomial.C 0 by simp,
      Polynomial.dvd_iff_isRoot]
    exact pencil_eval_zero hU0 hU hk
  obtain ⟨Q1, hQ1⟩ := hx
  have hq1eval : Q1.eval alpha = 0 := by
    have hp := pencil_eval_alpha alpha hα U0 U
    rw [hQ1, Polynomial.eval_mul, Polynomial.eval_X] at hp
    exact (mul_eq_zero.mp hp).resolve_left hα
  have ha : (Polynomial.X : Polynomial Sextic) - Polynomial.C alpha ∣ Q1 := by
    rw [Polynomial.dvd_iff_isRoot]
    exact hq1eval
  obtain ⟨Q, hQ⟩ := ha
  refine ⟨Q, ?_, ?_⟩
  · rw [hQ1, hQ, mul_assoc]
  · by_cases hQz : Q = 0
    · simp [hQz]
    · have hfac1 : (Polynomial.X : Polynomial Sextic) ≠ 0 := Polynomial.X_ne_zero
      have hfac2 : ((Polynomial.X : Polynomial Sextic) -
          Polynomial.C alpha) ≠ 0 := Polynomial.X_sub_C_ne_zero alpha
      have hpne : (Polynomial.X : Polynomial Sextic) *
          (Polynomial.X - Polynomial.C alpha) * Q ≠ 0 :=
        mul_ne_zero (mul_ne_zero hfac1 hfac2) hQz
      have hnat : ((Polynomial.X : Polynomial Sextic) *
          (Polynomial.X - Polynomial.C alpha) * Q).natDegree < 258 := by
        have hd := pencil_degree_lt (alpha := alpha) hU0 hU hk
        rw [show pencil alpha U0 U = (Polynomial.X : Polynomial Sextic) *
            (Polynomial.X - Polynomial.C alpha) * Q by rw [hQ1, hQ, mul_assoc]] at hd
        exact (Polynomial.natDegree_lt_iff_degree_lt hpne).mpr hd
      rw [Polynomial.natDegree_mul (mul_ne_zero hfac1 hfac2) hQz,
        Polynomial.natDegree_mul hfac1 hfac2, Polynomial.natDegree_X,
        Polynomial.natDegree_X_sub_C] at hnat
      omega

/-- The degree calculation is field-agnostic and does not unfold the
4095-factor concrete core while elaborating the polynomial product. -/
theorem abstract_message_degree_le (R Q : Polynomial Sextic)
    (hR : R.natDegree = 4095) (hQ : Q.natDegree ≤ 255) :
    (R * Q.comp ((Polynomial.X : Polynomial Sextic)^4096)).natDegree ≤ 1048575 := by
  calc
    (R * Q.comp ((Polynomial.X : Polynomial Sextic)^4096)).natDegree ≤
        R.natDegree + (Q.comp ((Polynomial.X : Polynomial Sextic)^4096)).natDegree :=
          Polynomial.natDegree_mul_le
    _ ≤ 4095 + Q.natDegree * ((Polynomial.X : Polynomial Sextic)^4096).natDegree := by
          rw [hR]
          exact Nat.add_le_add_left Polynomial.natDegree_comp_le 4095
    _ ≤ 4095 + 255 * 4096 := by
          have hz : ((Polynomial.X : Polynomial Sextic)^4096).natDegree = 4096 := by
            simp
          rw [hz]
          exact Nat.add_le_add_left (Nat.mul_le_mul_right 4096 hQ) 4095
    _ = 1048575 := by norm_num

/-- Formal polynomial witness of sufficient degree at each same-key pair.
This proves degree admissibility, not codeword agreement on the support. -/
theorem exists_message_poly {alpha : Sextic} (hα : alpha ≠ 0)
    {U0 U : Finset Small}
    (hU0 : U0 ∈ Candidates) (hU : U ∈ Candidates)
    (hk : key projectedNode U0 = key projectedNode U) :
    ∃ Q : Polynomial Sextic,
      pencil alpha U0 U =
          (Polynomial.X : Polynomial Sextic) *
            (Polynomial.X - Polynomial.C alpha) * Q ∧
      (coreLocator * Q.comp ((Polynomial.X : Polynomial Sextic)^4096)).natDegree
        ≤ 1048575 := by
  obtain ⟨Q, hfactor, hQ⟩ := exists_quotient hα hU0 hU hk
  exact ⟨Q, hfactor,
    abstract_message_degree_le coreLocator Q coreLocator_natDegree hQ⟩

end OrbitPencilLiftPencil4096
