import Mathlib

/-!
Lean 4.34 / Mathlib candidate. NOT KERNEL-CHECKED.

Adapted, with attribution, from the accepted Proximity Prize OrbitPencil.lean
(PR #38; contributors include erdkocak) root-count noncontainment argument.

This module has no sorry/axiom and no assumptions about existence of an MCA
witness: it proves a *conditional* lemma given the indexed support and its
polynomial evaluation identity. Its final use in RS-MCA remains unformalized.
-/

namespace OrbitPencilLiftIndexedNoncontainment
open Polynomial

/-- A degree-4096 factor times any RS message polynomial of degree ≤ 1048575
cannot agree with a nonzero degree-1936 core on ≥ 1116048 distinct points.
This is an abstract polynomial lemma, not the claimed MCA refutation. -/
theorem no_large_support {F : Type*} [Field F]
    (A R q : Polynomial F) (S : Finset F)
    (hAne : A ≠ 0) (hAdeg : A.natDegree = 4096)
    (hRne : R ≠ 0) (hRdeg : R.natDegree = 1936)
    (hqdeg : q.natDegree ≤ 1048575)
    (hScard : 1116048 ≤ S.card)
    (heval : ∀ x ∈ S, (A * q + R).eval x = 0) : False := by
  let P : Polynomial F := A * q + R
  have hmul : (A * q).natDegree ≤ 1052671 := by
    calc
      (A * q).natDegree ≤ A.natDegree + q.natDegree := Polynomial.natDegree_mul_le
      _ ≤ 4096 + 1048575 := by omega
      _ = 1052671 := by norm_num
  have hPdeg : P.natDegree ≤ 1052671 := by
    change (A * q + R).natDegree ≤ 1052671
    calc
      (A * q + R).natDegree ≤ max (A * q).natDegree R.natDegree :=
        Polynomial.natDegree_add_le _ _
      _ ≤ max 1052671 1936 := max_le_max hmul (by omega)
      _ = 1052671 := by norm_num
  have hPzero : P = 0 := by
    apply Polynomial.eq_zero_of_natDegree_lt_card_of_eval_eq_zero' P S
    · exact heval
    · omega
  have hEq : A * q = -R := by
    have h := congrArg (fun z : Polynomial F => z - R) hPzero
    simpa [P] using h
  by_cases hq0 : q = 0
  · rw [hq0, mul_zero] at hEq
    have hRzero : R = 0 := by simpa using hEq.symm
    exact hRne hRzero
  · have hdegEq := congrArg Polynomial.natDegree hEq
    rw [Polynomial.natDegree_mul hAne hq0, hAdeg,
        Polynomial.natDegree_neg, hRdeg] at hdegEq
    omega

/-- Same lemma on the *index support* used by a Reed–Solomon domain.
Injectivity makes the image have the same cardinality. This closes the
specific image-cardinality proof obligation that was missing from the previous
candidate. It does NOT prove injectivity for a concrete RS encoding/domain. -/
theorem no_large_support_on_indices {F ι : Type*} [Field F]
    (dom : ι → F) (hdom : Function.Injective dom)
    (A R q : Polynomial F) (S : Finset ι)
    (hAne : A ≠ 0) (hAdeg : A.natDegree = 4096)
    (hRne : R ≠ 0) (hRdeg : R.natDegree = 1936)
    (hqdeg : q.natDegree ≤ 1048575)
    (hScard : 1116048 ≤ S.card)
    (heval : ∀ j ∈ S, (A * q + R).eval (dom j) = 0) : False := by
  classical
  apply no_large_support A R q (S.image dom) hAne hAdeg hRne hRdeg hqdeg
  · rw [Finset.card_image_of_injective _ hdom]
    exact hScard
  · intro x hx
    rw [Finset.mem_image] at hx
    obtain ⟨j, hj, rfl⟩ := hx
    exact heval j hj

/-- Bridging lemma: if the received-line *direction* equals the quotient
`-R/A` at all positions in the indexed support (with nonvanishing denominators),
then it cannot be the evaluation of any RS polynomial of degree < 2^20.

Unlike `no_large_support_on_indices`, this accepts the exact quotient identity
arising from the OrbitPencil rational-line construction. The caller must still
prove the domain is injective, the denominators are nonzero, and the actual
MCA agreement support has the required size. This does NOT construct the line
or count slopes, and is NOT yet Lean kernel-checked. -/
theorem quotient_direction_not_codeword_on_indices {F ι : Type*} [Field F]
    (dom : ι → F) (hdom : Function.Injective dom)
    (A R q : Polynomial F) (S : Finset ι)
    (hAne : A ≠ 0) (hAdeg : A.natDegree = 4096)
    (hRne : R ≠ 0) (hRdeg : R.natDegree = 1936)
    (hqdeg : q.natDegree ≤ 1048575)
    (hScard : 1116048 ≤ S.card)
    (hdenom : ∀ j ∈ S, A.eval (dom j) ≠ 0)
    (hmatch : ∀ j ∈ S,
      q.eval (dom j) = -(R.eval (dom j)) / A.eval (dom j)) : False := by
  apply no_large_support_on_indices dom hdom A R q S
    hAne hAdeg hRne hRdeg hqdeg hScard
  intro j hj
  have hmul : q.eval (dom j) * A.eval (dom j) = -(R.eval (dom j)) := by
    rw [hmatch j hj]
    exact div_mul_cancel₀ _ (hdenom j hj)
  calc
    (A * q + R).eval (dom j) =
        A.eval (dom j) * q.eval (dom j) + R.eval (dom j) := by simp
    _ = q.eval (dom j) * A.eval (dom j) + R.eval (dom j) := by
      rw [mul_comm (A.eval (dom j)) (q.eval (dom j))]
    _ = 0 := by rw [hmul]; exact neg_add_cancel _

end OrbitPencilLiftIndexedNoncontainment
