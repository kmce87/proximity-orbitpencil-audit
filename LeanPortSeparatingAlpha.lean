import Mathlib

/-!
# Separating alpha and distinct slopes for the 4096-fibre OrbitPencil lift

Adapted from the accepted Proximity Prize OrbitPencil.lean, PR #38,
including original contributor erdkocak.

Falsifiable target: kernel-check the root-avoidance argument and slope
injectivity for a family of 2^59+1 polynomial labels in a field of
cardinality (2130706433)^6, with at most 512 projected nodes and
degree-257 nonzero pairwise differences.

**Conditional:** This module assumes the large same-key family exists,
that its polynomial differences are nonzero and have degree <= 257,
and that the field has the specified cardinality. It does not construct
the actual RS-MCA received affine line or certify an MCA counterexample.
-/

namespace OrbitPencilLiftSeparatingAlpha
open Polynomial

abbrev N : ℕ := 2^59 + 1

/-- Roots of pairwise differences, together with the forbidden domain and zero. -/
noncomputable def bad {F τ : Type*} [Field F]
    (Sel : Finset τ) (V : τ → Polynomial F) (projected : Finset F) : Finset F := by
  classical
  exact (projected ∪ {0}) ∪
    Sel.offDiag.biUnion (fun z => (V z.1 - V z.2).roots.toFinset)

/-- The collision set is bounded by 257 roots per ordered unequal pair. -/
theorem bad_card_le {F τ : Type*} [Field F]
    (Sel : Finset τ) (V : τ → Polynomial F) (projected : Finset F)
    (_hne : ∀ U ∈ Sel, ∀ W ∈ Sel, U ≠ W → V U - V W ≠ 0)
    (hdeg : ∀ U ∈ Sel, ∀ W ∈ Sel, (V U - V W).natDegree ≤ 257) :
    (bad Sel V projected).card ≤ projected.card + 1 + Sel.offDiag.card * 257 := by
  classical
  have hpair : ∀ z ∈ Sel.offDiag,
      ((V z.1 - V z.2).roots.toFinset).card ≤ 257 := by
    intro z hz
    obtain ⟨hU, hW, hdiff⟩ := Finset.mem_offDiag.mp hz
    exact (Multiset.toFinset_card_le _).trans
      ((Polynomial.card_roots' (V z.1 - V z.2)).trans
        (hdeg z.1 hU z.2 hW))
  have hcoll :
      (Sel.offDiag.biUnion (fun z => (V z.1 - V z.2).roots.toFinset)).card ≤
      Sel.offDiag.card * 257 :=
    Finset.card_biUnion_le_card_mul Sel.offDiag
      (fun z => (V z.1 - V z.2).roots.toFinset) 257 hpair
  calc
    (bad Sel V projected).card ≤
        (projected ∪ {0}).card +
          (Sel.offDiag.biUnion (fun z => (V z.1 - V z.2).roots.toFinset)).card := by
      dsimp [bad]
      exact Finset.card_union_le _ _
    _ ≤ (projected.card + ({0} : Finset F).card) + Sel.offDiag.card * 257 :=
      Nat.add_le_add (Finset.card_union_le _ _) hcoll
    _ = projected.card + 1 + Sel.offDiag.card * 257 := by simp

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000
set_option exponentiation.threshold 100000
/-- Exact arithmetic, including the pairwise root count (not merely 272). -/
theorem alpha_arithmetic :
    513 + N * (N - 1) * 257 < (2130706433 : ℕ)^6 := by
  decide

/-- One alpha simultaneously avoids zero, projected nodes, and all collisions.
For this alpha, every selected polynomial has a different rational-pencil slope.
The proof does not assume that different subsets automatically yield different
slopes: it establishes the actual injectivity of the gamma map. -/
theorem exists_alpha_gamma_injective {F τ : Type*} [Field F] [Fintype F]
    (Sel : Finset τ) (V : τ → Polynomial F) (projected : Finset F)
    (reference : Polynomial F)
    (hSel : Sel.card = N)
    (hF : Fintype.card F = (2130706433 : ℕ)^6)
    (hprojected : projected.card ≤ 512)
    (hne : ∀ U ∈ Sel, ∀ W ∈ Sel, U ≠ W → V U - V W ≠ 0)
    (hdeg : ∀ U ∈ Sel, ∀ W ∈ Sel, (V U - V W).natDegree ≤ 257) :
    ∃ alpha : F, alpha ≠ 0 ∧ alpha ∉ projected ∧
      Set.InjOn (fun U => ((reference - V U).eval alpha) / alpha) (Sel : Set τ) := by
  classical
  have hoff : Sel.offDiag.card = N * (N - 1) := by
    rw [Finset.offDiag_card, hSel, Nat.mul_sub_left_distrib]
    simp
  have hsmall : projected.card + 1 + Sel.offDiag.card * 257 < Fintype.card F := by
    rw [hoff, hF]
    have h := alpha_arithmetic
    omega
  have hbad : (bad Sel V projected).card < Fintype.card F :=
    (bad_card_le Sel V projected hne hdeg).trans_lt hsmall
  have hexists : ∃ alpha : F, alpha ∉ bad Sel V projected := by
    by_contra h
    push Not at h
    have hall : bad Sel V projected = Finset.univ := by
      ext alpha
      simp [h alpha]
    rw [hall, Finset.card_univ] at hbad
    exact (lt_irrefl _) hbad
  obtain ⟨alpha, halpha⟩ := hexists
  have hzero : alpha ≠ 0 := by
    intro hz
    apply halpha
    simp [bad, hz]
  have hproject : alpha ∉ projected := by
    intro hp
    apply halpha
    simp [bad, hp]
  refine ⟨alpha, hzero, hproject, ?_⟩
  intro U hU W hW hgamma
  by_contra hdiff
  apply halpha
  have hdelta : (reference - V U).eval alpha =
      (reference - V W).eval alpha := by
    have h := congrArg (fun z : F => z * alpha) hgamma
    simpa only [div_mul_cancel₀ _ hzero] using h
  have heval : (V U).eval alpha = (V W).eval alpha := by
    have h := hdelta
    simp only [Polynomial.eval_sub] at h
    exact sub_right_inj.mp h
  have hroot : alpha ∈ (V U - V W).roots.toFinset := by
    rw [Multiset.mem_toFinset, Polynomial.mem_roots (hne U hU W hW hdiff)]
    simpa [Polynomial.eval_sub] using sub_eq_zero.mpr heval
  have hpair : (U, W) ∈ Sel.offDiag :=
    Finset.mem_offDiag.mpr ⟨hU, hW, hdiff⟩
  simp only [bad, Finset.mem_union]
  exact Or.inr (Finset.mem_biUnion.mpr ⟨(U, W), hpair, hroot⟩)

end OrbitPencilLiftSeparatingAlpha
