import LeanPortAgreementCount4096

/-!
# A single received line with a same-key family of distinct agreement slopes

Target: compose the *same* selected family and reference member into the
already kernel-checked 4096-fibre agreement theorem. This closes the
previously missing same-key membership witness for every selected U.

The result is still NOT an MCA counterexample: proving that the received
line's direction is outside the RS code and matching the exact MCA definition
are separate obligations. No official prize-verifier acceptance is claimed.

Original 512-fibre OrbitPencil: proximity-prize/proximity-prize PR #38,
including co-author erdkocak.
-/

namespace OrbitPencilLiftSelectedAgreement4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftSeparatingAlpha
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftPencil4096
open OrbitPencilLiftAgreementCount4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

/-- A *single* reference received line has N = 2^59+1 distinct
slope parameters, each agreeing with a degree-<2^20 RS message at
at least 1,118,207 distinct domain indices.

No assumption of a large family or pairwise key equality is left
in the theorem statement: both follow from the concrete KoalaBear
pigeonhole argument. This does not assert the received direction
is outside the RS code. -/
theorem exists_selected_agreement_family :
    ∃ (Sel : Finset (Finset Small)) (alpha : Sextic)
        (U0 : Finset Small),
      Sel.card = N ∧
      U0 ∈ Sel ∧
      alpha ≠ 0 ∧
      alpha ∉ projected6 ∧
      Set.InjOn (gamma alpha U0) (Sel : Set (Finset Small)) ∧
      (∀ U ∈ Sel,
        ∃ c : Polynomial Sextic,
          c.natDegree ≤ 1048575 ∧
          1118207 ≤ Fintype.card
            {j : Index // lineAt alpha U0 (gamma alpha U0 U) j =
              c.eval (node6 j)}) := by
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
    change (V (fun b => baseToSextic (projectedNode b)) U -
      V (fun b => baseToSextic (projectedNode b)) W).natDegree ≤ 257
    omega
  have hprojected : projected6.card ≤ 512 := by
    calc
      projected6.card ≤ (Finset.univ : Finset Small).card := by
        exact Finset.card_image_le
      _ = 512 := by simp
  have hpos : 0 < Sel.card := by
    rw [hSelCard]
    norm_num [N]
  obtain ⟨U0, hU0⟩ := Finset.card_pos.mp hpos
  obtain ⟨alpha, halpha, havoid, hinj⟩ :=
    exists_alpha_gamma_injective Sel (V y6) projected6
      (V y6 U0) hSelCard concrete_sextic_card
      hprojected hnonzero hdegree
  have hgamma : Set.InjOn (gamma alpha U0) (Sel : Set (Finset Small)) := by
    simpa only [gamma, deltaV] using hinj
  refine ⟨Sel, alpha, U0, hSelCard, hU0, halpha, havoid, hgamma, ?_⟩
  intro U hU
  have hkey : key projectedNode U0 = key projectedNode U :=
    (hSelKey U0 hU0).trans (hSelKey U hU).symm
  exact exists_message_agreement_1118207 alpha halpha havoid
    U0 U (hSelCand U0 hU0) (hSelCand U hU) hkey

#print axioms OrbitPencilLiftSelectedAgreement4096.exists_selected_agreement_family

end OrbitPencilLiftSelectedAgreement4096
