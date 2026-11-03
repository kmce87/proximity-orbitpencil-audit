import LeanPortSelectedAgreement4096
import LeanPortIndexedNoncontainment

/-!
# Noncontainment of the concrete 4096-fibre received-line direction

One falsifiable bridge: on the actual KoalaBear n = 2^21 NTT domain,
the fixed direction -coreLocator(x)/(x^4096-alpha) cannot be an
evaluation of any polynomial of degree ≤ 2^20, provided alpha avoids
the 512 projected nodes.

The argument applies the previously audited indexed polynomial root-count
lemma to ALL 2^21 distinct evaluation positions. It does not yet identify
the exact rs-mca bad-slope definition or the official ArkLib ProtocolClaim.

The original 512-fibre OrbitPencil construction is from
proximity-prize/proximity-prize PR #38 (including erdkocak).
-/

namespace OrbitPencilLiftDirectionNoncode4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftPointwiseSupport4096
open OrbitPencilLiftIndexedNoncontainment

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

/-!
The exponent is kept as a variable while the monicity/nonzero certificates
are elaborated and checked. Specializing only afterwards avoids asking Lean
to reduce the concrete 4096th polynomial power during elaboration.
This is a compilation experiment, not a new MCA witness.
-/
private theorem denominator_monic_generic (a : Sextic) (n : ℕ)
    (hn : n ≠ 0) :
    ((Polynomial.X : Polynomial Sextic)^n - Polynomial.C a).Monic :=
  Polynomial.monic_X_pow_sub_C a hn

private theorem denominator_nonzero_generic (a : Sextic) (n : ℕ)
    (hn : n ≠ 0) :
    ((Polynomial.X : Polynomial Sextic)^n - Polynomial.C a) ≠ 0 :=
  (denominator_monic_generic a n hn).ne_zero

private theorem denominator_degree_generic (a : Sextic) (n : ℕ) :
    ((Polynomial.X : Polynomial Sextic)^n - Polynomial.C a).natDegree = n :=
  Polynomial.natDegree_X_pow_sub_C

/-- The actual sextic evaluation-domain embedding has no collisions. -/
theorem node6_injective : Function.Injective node6 := by
  intro i j hij
  apply node21_injective
  exact baseToSextic.injective hij

/-- The common direction of the affine received line is NOT an RS
codeword on the full n=2^21 domain, for every admissible alpha. -/
theorem received_direction_not_rs (alpha : Sextic)
    (havoid : alpha ∉ projected6) :
    ¬ ∃ q : Polynomial Sextic,
      q.natDegree ≤ 1048576 ∧
      ∀ j : Index, q.eval (node6 j) =
        -coreLocator.eval (node6 j) /
          ((node6 j)^4096 - alpha) := by
  rintro ⟨q, hq, hmatch⟩
  let A : Polynomial Sextic :=
    (Polynomial.X : Polynomial Sextic)^4096 - Polynomial.C alpha
  -- Specialize the generic, already-checked symbolic certificate; do not
  -- elaborate the 4096th power while constructing its nonzero proof.
  have hAne0 :
      ((Polynomial.X : Polynomial Sextic)^4096 - Polynomial.C alpha) ≠ 0 :=
    denominator_nonzero_generic alpha 4096 (by omega)
  have hAdeg0 :
      ((Polynomial.X : Polynomial Sextic)^4096 - Polynomial.C alpha).natDegree = 4096 :=
    denominator_degree_generic alpha 4096
  have hAne : A ≠ 0 := hAne0
  have hAdeg : A.natDegree = 4096 := hAdeg0
  have hRdeg : coreLocator.natDegree ≤ 4095 := by
    rw [coreLocator_natDegree]
  have hScard : 1116048 ≤ (Finset.univ : Finset Index).card := by
    norm_num [Index]
  have hdenom : ∀ j ∈ (Finset.univ : Finset Index),
      A.eval (node6 j) ≠ 0 := by
    intro j _
    have hj : (node6 j)^4096 - alpha ≠ 0 :=
      sub_ne_zero.mpr (node6_pow_ne_alpha alpha havoid j)
    simpa only [A, Polynomial.eval_sub, Polynomial.eval_pow,
      Polynomial.eval_X, Polynomial.eval_C] using hj
  have hquot : ∀ j ∈ (Finset.univ : Finset Index),
      q.eval (node6 j) = -(coreLocator.eval (node6 j)) /
        A.eval (node6 j) := by
    intro j _
    simpa only [A, Polynomial.eval_sub, Polynomial.eval_pow,
      Polynomial.eval_X, Polynomial.eval_C] using hmatch j
  exact quotient_direction_not_codeword_on_indices
    node6 node6_injective A coreLocator q (Finset.univ : Finset Index)
    hAne hAdeg coreLocator_ne_zero hRdeg hq hScard hdenom hquot


/-- Strong support-wise version: the fixed direction cannot be explained by
any RS message on ANY set of at least 1,116,048 concrete NTT indices.
This is the noncontainment half of the MCA support-witness definition;
the slope agreement family and predicate translation are separate. -/
theorem received_direction_not_rs_on_support (alpha : Sextic)
    (havoid : alpha ∉ projected6) (S : Finset Index)
    (hScard : 1116048 ≤ S.card) :
    ¬ ∃ q : Polynomial Sextic,
      q.natDegree ≤ 1048576 ∧
      ∀ j ∈ S, q.eval (node6 j) =
        -coreLocator.eval (node6 j) /
          ((node6 j)^4096 - alpha) := by
  rintro ⟨q, hq, hmatch⟩
  let A : Polynomial Sextic :=
    (Polynomial.X : Polynomial Sextic)^4096 - Polynomial.C alpha
  have hAne : A ≠ 0 :=
    denominator_nonzero_generic alpha 4096 (by omega)
  have hAdeg : A.natDegree = 4096 :=
    denominator_degree_generic alpha 4096
  have hRdeg : coreLocator.natDegree ≤ 4095 := by
    rw [coreLocator_natDegree]
  have hdenom : ∀ j ∈ S, A.eval (node6 j) ≠ 0 := by
    intro j hjS
    have hj : (node6 j)^4096 - alpha ≠ 0 :=
      sub_ne_zero.mpr (node6_pow_ne_alpha alpha havoid j)
    simpa only [A, Polynomial.eval_sub, Polynomial.eval_pow,
      Polynomial.eval_X, Polynomial.eval_C] using hj
  have hquot : ∀ j ∈ S,
      q.eval (node6 j) = -(coreLocator.eval (node6 j)) /
        A.eval (node6 j) := by
    intro j hjS
    simpa only [A, Polynomial.eval_sub, Polynomial.eval_pow,
      Polynomial.eval_X, Polynomial.eval_C] using hmatch j hjS
  exact quotient_direction_not_codeword_on_indices
    node6 node6_injective A coreLocator q S
    hAne hAdeg coreLocator_ne_zero hRdeg hq hScard hdenom hquot

#print axioms OrbitPencilLiftDirectionNoncode4096.received_direction_not_rs_on_support
#print axioms OrbitPencilLiftDirectionNoncode4096.node6_injective
#print axioms OrbitPencilLiftDirectionNoncode4096.received_direction_not_rs

end OrbitPencilLiftDirectionNoncode4096
