import LeanPortPencil4096

/-!
# Rational received-line identity for the 4096-fibre OrbitPencil lift

Adapted from the published OrbitPencil construction (Proximity Prize PR #38,
original contributors including erdkocak). This is a conditional algebraic
identity, not a full MCA witness or an official benchmark certificate.

Falsifiable gate: Lean 4.34 proves that the polynomial factorization already
established in LeanPortPencil4096 gives the exact rational received-line
difference from the RS message at every point where the denominators are
nonzero. The remaining work is to connect it to the 1,118,207-point support.
-/

namespace OrbitPencilLiftLineAgreement4096

open Polynomial
open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftPencil4096

/-- Field identity behind the original OrbitPencil received line.
No cardinality, support, or RS-code membership assumptions are hidden here. -/
theorem rational_line_identity {F : Type*} [Field F]
    (r v0 v gamma q z alpha : F)
    (hz : z ≠ 0) (hza : z ≠ alpha)
    (hfactor : v0 - v - gamma * z = z * (z - alpha) * q) :
    r * v0 / (z * (z - alpha)) + gamma * (-r / (z - alpha)) =
      r * q + r * v / (z * (z - alpha)) := by
  have hza0 : z - alpha ≠ 0 := sub_ne_zero.mpr hza
  have hbase : v0 = v + gamma * z + z * (z - alpha) * q := by
    calc
      v0 = (v0 - v - gamma * z) + v + gamma * z := by ring
      _ = z * (z - alpha) * q + v + gamma * z := by rw [hfactor]
      _ = v + gamma * z + z * (z - alpha) * q := by ring
  rw [hbase]
  field_simp [hz, hza0]
  ring

/-- Instantiation at the actual KoalaBear sextic vanishing polynomials.
The factorization is the proved output of exists_quotient; this theorem
does not assume an unexplained numerical identity for the received line. -/
theorem pencil_line_identity (alpha : Sextic)
    (U0 U : Finset Small) (Q : Polynomial Sextic)
    (hfactor : pencil alpha U0 U =
      (Polynomial.X : Polynomial Sextic) *
        (Polynomial.X - Polynomial.C alpha) * Q)
    (r z : Sextic) (hz : z ≠ 0) (hza : z ≠ alpha) :
    r * (V y6 U0).eval z / (z * (z - alpha)) +
        gamma alpha U0 U * (-r / (z - alpha)) =
      r * Q.eval z + r * (V y6 U).eval z / (z * (z - alpha)) := by
  have h := congrArg (fun P : Polynomial Sextic => P.eval z) hfactor
  have heq :
      (V y6 U0).eval z - (V y6 U).eval z -
        gamma alpha U0 U * z = z * (z - alpha) * Q.eval z := by
    simpa [pencil, deltaV, Polynomial.eval_sub,
      Polynomial.eval_mul] using h
  exact rational_line_identity r ((V y6 U0).eval z)
    ((V y6 U).eval z) (gamma alpha U0 U) (Q.eval z)
    z alpha hz hza heq

/-- Exact agreement follows whenever the core locator or selected
vanishing polynomial evaluates to zero. -/
theorem pencil_line_agrees_on_root (alpha : Sextic)
    (U0 U : Finset Small) (Q : Polynomial Sextic)
    (hfactor : pencil alpha U0 U =
      (Polynomial.X : Polynomial Sextic) *
        (Polynomial.X - Polynomial.C alpha) * Q)
    (r z : Sextic) (hz : z ≠ 0) (hza : z ≠ alpha)
    (hroot : r = 0 ∨ (V y6 U).eval z = 0) :
    r * (V y6 U0).eval z / (z * (z - alpha)) +
        gamma alpha U0 U * (-r / (z - alpha)) =
      r * Q.eval z := by
  have h := pencil_line_identity alpha U0 U Q hfactor r z hz hza
  rcases hroot with hr | hv
  · simpa [hr] using h
  · simpa [hv] using h

end OrbitPencilLiftLineAgreement4096
