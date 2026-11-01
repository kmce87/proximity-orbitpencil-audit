import LeanPortSameKeyFamily
import LeanPortSeparatingAlpha

/-!
# Composition gate: a single concrete alpha with > 2^59 distinct labels

Adapted from the accepted OrbitPencil attack (Proximity Prize PR #38,
original contributors including erdkocak).

This composes the already audited KoalaBear 272-of-511 same-key family
with the root-avoidance and gamma-injectivity theorem, over the actual
CompPoly KoalaBear.Ext6 field.

Crucial limitation: this theorem is about abstract polynomial slope labels.
It does NOT construct the received affine line, prove that every label is
an MCA-bad slope, or prove the 1,118,207 agreement endpoint.
-/

namespace OrbitPencilLiftConcreteSlopes

open Polynomial
open OrbitPencilLiftSameKey
open OrbitPencilLiftSeparatingAlpha

noncomputable def y6 (b : Small) : Sextic :=
  baseToSextic (projectedNode b)

noncomputable def projected6 : Finset Sextic :=
  (Finset.univ : Finset Small).image y6

/-- A concrete family of 2^59+1 selected subsets and one alpha in
KoalaBear.Ext6, for which the rational-polynomial gamma labels are distinct.

The reference polynomial is fixed to zero: injectivity is independent
of reference. The received-line interpretation remains unproved. -/
theorem exists_concrete_alpha_distinct_slopes :
    ∃ (Sel : Finset (Finset Small)) (alpha : Sextic),
      Sel.card = N ∧ alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      Set.InjOn (fun U : Finset Small =>
        ((0 - V y6 U).eval alpha) / alpha) (Sel : Set (Finset Small)) := by
  classical
  obtain ⟨σ, hσ⟩ := concrete_same_key_family
  let T : Finset (Finset Small) :=
    Candidates.filter (fun U => key projectedNode U = σ)
  have hN : N ≤ T.card := by
    dsimp [N, T] at *
    omega
  obtain ⟨Sel, hSelSub, hSelCard⟩ :=
    Finset.exists_subset_card_eq (s := T) hN
  have hSelCand : ∀ U ∈ Sel, U ∈ Candidates := by
    intro U hU
    exact (Finset.mem_filter.mp (hSelSub hU)).1
  have hSelKey : ∀ U ∈ Sel, key projectedNode U = σ := by
    intro U hU
    exact (Finset.mem_filter.mp (hSelSub hU)).2
  have hnonzero : ∀ U ∈ Sel, ∀ W ∈ Sel, U ≠ W →
      V y6 U - V y6 W ≠ 0 := by
    intro U _ W _ hUW
    exact concrete_sextic_sub_ne_zero hUW
  have hdegree : ∀ U ∈ Sel, ∀ W ∈ Sel,
      (V y6 U - V y6 W).natDegree ≤ 257 := by
    intro U hU W hW
    have hkey : key projectedNode U = key projectedNode W :=
      (hSelKey U hU).trans (hSelKey W hW).symm
    have hd := concrete_sextic_degree_lt_of_key
      (hSelCand U hU) (hSelCand W hW) hkey
    omega
  have hprojected : projected6.card ≤ 512 := by
    calc
      projected6.card ≤ (Finset.univ : Finset Small).card := by
        exact Finset.card_image_le
      _ = 512 := by simp [Small]
  obtain ⟨alpha, halpha, havoid, hinj⟩ :=
    exists_alpha_gamma_injective Sel (V y6) projected6
      (0 : Polynomial Sextic) hSelCard concrete_sextic_card
      hprojected hnonzero hdegree
  exact ⟨Sel, alpha, hSelCard, halpha, havoid, hinj⟩

end OrbitPencilLiftConcreteSlopes
