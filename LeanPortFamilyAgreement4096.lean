import LeanPortAgreementCount4096
import LeanPortSeparatingAlpha

/-!
# One fixed received line, a selected family, and the 1,118,207 agreement edge

Falsifiable hypothesis: the concrete KoalaBear same-key pigeonhole family,
the separating-alpha root bound, and the checked 4096-fibre pointwise
agreement theorem can be composed with the SAME reference subset U0.

The conclusion is deliberately a *family of polynomial agreements with
one fixed received affine line*, and injective slope labels. It is NOT yet
an MCA counterexample: non-codeword status of the direction and transfer
to the precise rs-mca / official ProtocolClaim definitions remain open.

The 512-fibre OrbitPencil technique was published in Proximity Prize
PR #38; original contributors include erdkocak.
-/

namespace OrbitPencilLiftFamilyAgreement4096

open Polynomial
open OrbitPencilLiftSameKey
open OrbitPencilLiftSeparatingAlpha
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftPencil4096
open OrbitPencilLiftSupport4096
open OrbitPencilLiftAgreementCount4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

/-- One concrete received line, at least 2^59+1 pairwise distinct slope
labels, and a degree-<2^20 message with >=1,118,207 agreement positions
for each label. This is a composition of concrete KoalaBear lemmas, not an
abstract assumption that a large family of agreeing messages exists. -/
theorem exists_one_line_distinct_agreement_family :
    ∃ (Sel : Finset (Finset Small)) (U0 : Finset Small) (alpha : Sextic),
      Sel.card = N ∧
      U0 ∈ Sel ∧
      alpha ≠ 0 ∧
      alpha ∉ projected6 ∧
      Set.InjOn (fun U : Finset Small => gamma alpha U0 U)
        (Sel : Set (Finset Small)) ∧
      (∀ U ∈ Sel, ∃ c : Polynomial Sextic,
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
  obtain ⟨U0, hU0⟩ : Sel.Nonempty :=
    Finset.card_pos.mp (by rw [hSelCard]; dsimp [N]; omega)
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
      projected6.card ≤ (Finset.univ : Finset Small).card :=
        Finset.card_image_le
      _ = 512 := by simp
  obtain ⟨alpha, halpha, havoid, hinj⟩ :=
    exists_alpha_gamma_injective Sel (V y6) projected6
      (V y6 U0) hSelCard concrete_sextic_card
      hprojected hnonzero hdegree
  have hgamma : Set.InjOn (fun U : Finset Small => gamma alpha U0 U)
      (Sel : Set (Finset Small)) := by
    simpa only [gamma, deltaV] using hinj
  refine ⟨Sel, U0, alpha, hSelCard, hU0, halpha, havoid, hgamma, ?_⟩
  intro U hU
  have hk : key projectedNode U0 = key projectedNode U :=
    (hSelKey U0 hU0).trans (hSelKey U hU).symm
  exact exists_message_agreement_1118207
    alpha halpha havoid U0 U (hSelCand U0 hU0) (hSelCand U hU) hk

#print axioms OrbitPencilLiftFamilyAgreement4096.exists_one_line_distinct_agreement_family

end OrbitPencilLiftFamilyAgreement4096
