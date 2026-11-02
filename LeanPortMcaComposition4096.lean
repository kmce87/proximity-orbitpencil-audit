import LeanPortDirectionNoncode4096

/-!
# 4096-fibre single-line support-wise bad-slope composition

One falsifiable hypothesis: the already checked selected same-key family,
its 1,118,207-position agreement, and arbitrary-support direction
noncontainment imply > 2^59 *distinct* support-wise bad slopes for ONE
received affine line.

This theorem is in the local KoalaBear audit model, not an ArkLib
ProtocolClaim or independent prize-verifier submission. The 512-fibre
OrbitPencil construction originated in proximity-prize/proximity-prize PR #38
(merged via Yukon autoresearch; co-author credit includes erdkocak).
-/

namespace OrbitPencilLiftMcaComposition4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftSeparatingAlpha
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftSupport4096
open OrbitPencilLiftAgreementCount4096
open OrbitPencilLiftSelectedAgreement4096
open OrbitPencilLiftDirectionNoncode4096

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

/-- Explicit support-wise RS bad-slope predicate. The *same* support
explains the received line point and does not explain its direction.
The latter is the noncontainment condition in the support-wise MCA
formulation; a source-to-source rs-mca equivalence audit is separate. -/
def SupportWiseBad (alpha : Sextic) (U0 : Finset Small)
    (z : Sextic) : Prop :=
  ∃ (S : Finset Index) (c : Polynomial Sextic),
    1116048 ≤ S.card ∧
    c.natDegree ≤ 1048575 ∧
    (∀ j ∈ S, lineAt alpha U0 z j = c.eval (node6 j)) ∧
    ¬ ∃ q : Polynomial Sextic,
      q.natDegree ≤ 1048575 ∧
      ∀ j ∈ S, q.eval (node6 j) =
        -coreLocator.eval (node6 j) /
          ((node6 j)^4096 - alpha)

/-- A single affine received line with >2^59 distinct finite slopes,
each support-wise bad at agreement >=1,116,048. In fact the
constructed explanation supports have >=1,118,207 indices. -/
theorem exists_many_supportwise_bad_slopes :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      2^59 < Z.card ∧
      alpha ≠ 0 ∧
      alpha ∉ projected6 ∧
      ∀ z ∈ Z, SupportWiseBad alpha U0 z := by
  classical
  obtain ⟨Sel, alpha, U0, hSelCard, _hU0, halpha, havoid, hinj, hagree⟩ :=
    exists_selected_agreement_family
  let Z : Finset Sextic := Sel.image (gamma alpha U0)
  have hZcard : Z.card = N := by
    dsimp [Z]
    exact Finset.card_image_of_injOn hinj
  refine ⟨alpha, U0, Z, ?_, halpha, havoid, ?_⟩
  · rw [hZcard]
    norm_num [N]
  · intro z hz
    change z ∈ Sel.image (gamma alpha U0) at hz
    obtain ⟨U, hU, rfl⟩ := Finset.mem_image.mp hz
    obtain ⟨c, hcdeg, hcard⟩ := hagree U hU
    let S : Finset Index :=
      (Finset.univ : Finset
        {j : Index // lineAt alpha U0 (gamma alpha U0 U) j =
          c.eval (node6 j)}).image Subtype.val
    have hS_card_eq :
        S.card = Fintype.card
          {j : Index // lineAt alpha U0 (gamma alpha U0 U) j =
            c.eval (node6 j)} := by
      dsimp [S]
      rw [Finset.card_image_of_injective _ Subtype.val_injective]
      simp
    have hScard : 1116048 ≤ S.card := by
      rw [hS_card_eq]
      omega
    change SupportWiseBad alpha U0 (gamma alpha U0 U)
    refine ⟨S, c, hScard, hcdeg, ?_, ?_⟩
    · intro j hj
      have hj' : j ∈ (Finset.univ : Finset
          {j : Index // lineAt alpha U0 (gamma alpha U0 U) j =
            c.eval (node6 j)}).image Subtype.val := hj
      obtain ⟨t, _ht, htj⟩ := Finset.mem_image.mp hj'
      subst j
      exact t.property
    · exact received_direction_not_rs_on_support alpha havoid S hScard

#print axioms OrbitPencilLiftMcaComposition4096.exists_many_supportwise_bad_slopes

end OrbitPencilLiftMcaComposition4096
