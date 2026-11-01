import LeanPortLineAgreement4096

/-!
# Key-retaining 4096-fibre OrbitPencil family

Adapted from the accepted OrbitPencil.lean, Proximity Prize PR #38
(original contributors including erdkocak).

Falsifiable target: preserve a *single actual prime-field coefficient key*
and a reference U0 while choosing the separating sextic alpha. This lets
the previously kernel-checked quotient theorem apply to every selected
slope, rather than merely proving injectivity of abstract slope labels.

This does not yet prove support-wise RS agreement or MCA noncontainment.
-/

namespace OrbitPencilLiftFamilyWitness4096

open Polynomial
open OrbitPencilLiftSameKey
open OrbitPencilLiftSeparatingAlpha
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftPencil4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

/-- A common key, a reference selection and one separating alpha
simultaneously yield > 2^59 distinct pencil slopes and a bounded-degree
message quotient for every member. This theorem does not assert that
those slopes are MCA-bad: support agreement is still missing. -/
theorem exists_keyed_family_with_quotients :
    ∃ (σ : (Fin 14 → _root_.KoalaBear.Field) × Small)
      (Sel : Finset (Finset Small)) (alpha : Sextic)
      (U0 : Finset Small),
      Sel.card = N ∧ U0 ∈ Sel ∧ alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      (∀ U ∈ Sel, U ∈ Candidates ∧ key projectedNode U = σ) ∧
      Set.InjOn (fun U : Finset Small => gamma alpha U0 U)
        (Sel : Set (Finset Small)) ∧
      (∀ U ∈ Sel, ∃ Q : Polynomial Sextic,
        pencil alpha U0 U =
          (Polynomial.X : Polynomial Sextic) *
            (Polynomial.X - Polynomial.C alpha) * Q ∧
        (coreLocator * Q.comp
          ((Polynomial.X : Polynomial Sextic)^4096)).natDegree ≤ 1048575) := by
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
  have hSelNonempty : Sel.Nonempty := Finset.card_pos.mp (by
    rw [hSelCard]
    dsimp [N]
    positivity)
  obtain ⟨U0, hU0⟩ := hSelNonempty
  have hnonzero : ∀ U ∈ Sel, ∀ W ∈ Sel, U ≠ W →
      V y6 U - V y6 W ≠ 0 := by
    intro U _ W _ hUW
    exact concrete_sextic_sub_ne_zero hUW
  have hdegree : ∀ U ∈ Sel, ∀ W ∈ Sel,
      (V y6 U - V y6 W).natDegree ≤ 257 := by
    intro U hU W hW
    have hk : key projectedNode U = key projectedNode W :=
      (hSelKey U hU).trans (hSelKey W hW).symm
    have hd := concrete_sextic_degree_lt_of_key
      (hSelCand U hU) (hSelCand W hW) hk
    change (V (fun b => baseToSextic (projectedNode b)) U -
      V (fun b => baseToSextic (projectedNode b)) W).natDegree ≤ 257
    omega
  have hprojected : projected6.card ≤ 512 := by
    calc
      projected6.card ≤ (Finset.univ : Finset Small).card :=
        Finset.card_image_le
      _ = 512 := by simp
  obtain ⟨alpha, halpha, havoid, hinj⟩ :=
    exists_alpha_gamma_injective Sel (V y6) projected6
      (V y6 U0) hSelCard concrete_sextic_card
      hprojected hnonzero hdegree
  have hgamma : Set.InjOn (fun U : Finset Small => gamma alpha U0 U)
      (Sel : Set (Finset Small)) := by
    intro U hU W hW hEq
    apply hinj hU hW
    simpa only [gamma, deltaV, Polynomial.eval_sub] using hEq
  have hquot : ∀ U ∈ Sel, ∃ Q : Polynomial Sextic,
      pencil alpha U0 U =
        (Polynomial.X : Polynomial Sextic) *
          (Polynomial.X - Polynomial.C alpha) * Q ∧
      (coreLocator * Q.comp
        ((Polynomial.X : Polynomial Sextic)^4096)).natDegree ≤ 1048575 := by
    intro U hU
    have hk : key projectedNode U0 = key projectedNode U :=
      (hSelKey U0 hU0).trans (hSelKey U hU).symm
    exact exists_message_poly (alpha := alpha) halpha
      (hSelCand U0 hU0) (hSelCand U hU) hk
  exact ⟨σ, Sel, alpha, U0, hSelCard, hU0, halpha, havoid,
    (fun U hU => ⟨hSelCand U hU, hSelKey U hU⟩),
    hgamma, hquot⟩

end OrbitPencilLiftFamilyWitness4096
