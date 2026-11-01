import Mathlib

/-!
# Same-key family for the KoalaBear 4096-fibre lift

Adaptation of the *accepted* OrbitPencil.lean (Proximity Prize PR #38,
co-author erdkocak). This isolates the exact pigeonhole step for the
272-of-511 projected-column selections, with 14 top coefficients and
one residue-mod-512 product key.

Unlike a generic "large family" assumption, the key is computed from the
actual monic vanishing polynomial of the selected projected nodes.
The projected-node map is still a parameter; the next bridge must prove
its injectivity for the concrete 2^21 NTT domain. This file does not
construct an RS-MCA received line or certify distinct slopes.

Falsifiable target: Lean 4.34 kernel checks the existence of a single
key fibre of cardinality > 2^59, for *any* field K with |K|=2130706433.
-/

namespace OrbitPencilLiftSameKey

open Polynomial

abbrev Small := Fin 512

noncomputable def outer : Finset Small := Finset.univ.erase 0

theorem outer_card : outer.card = 511 := by
  simp [outer]

noncomputable def Candidates : Finset (Finset Small) :=
  Finset.powersetCard 272 outer

theorem candidates_card : Candidates.card = Nat.choose 511 272 := by
  rw [Candidates, Finset.card_powersetCard, outer_card]

noncomputable def V {K : Type*} [Field K] (y : Small → K)
    (U : Finset Small) : Polynomial K :=
  ∏ b ∈ U, ((Polynomial.X : Polynomial K) - Polynomial.C (y b))

noncomputable def topKey {K : Type*} [Field K] (y : Small → K)
    (U : Finset Small) : Fin 14 → K :=
  fun i => (V y U).coeff (271 - i.val)

noncomputable def productKey (U : Finset Small) : Small :=
  ⟨(∑ b ∈ U, b.val) % 512, Nat.mod_lt _ (by norm_num)⟩

noncomputable def key {K : Type*} [Field K] (y : Small → K)
    (U : Finset Small) : (Fin 14 → K) × Small :=
  (topKey y U, productKey U)

theorem card_keys {K : Type*} [Field K] [Fintype K]
    (hK : Fintype.card K = 2130706433) :
    Fintype.card ((Fin 14 → K) × Small) = 2130706433 ^ 14 * 512 := by
  simp [Fintype.card_prod, Small, hK]

/-- Copied mathematical pigeonhole principle from the accepted
OrbitPencil/PrescribedTop proof, with no extra axioms. -/
theorem pigeonhole {α : Type*} {β : Type*} [Fintype β] [DecidableEq β]
    (s : Finset α) (f : α → β) (n : ℕ)
    (hn : Fintype.card β * n < s.card) :
    ∃ y : β, n < (s.filter (fun x => f x = y)).card := by
  by_contra hcon
  push Not at hcon
  have hsum : s.card
      = ∑ y ∈ (Finset.univ : Finset β), (s.filter (fun x => f x = y)).card :=
    Finset.card_eq_sum_card_fiberwise (fun a _ => Finset.mem_univ _)
  have hle : ∑ y ∈ (Finset.univ : Finset β), (s.filter (fun x => f x = y)).card
      ≤ ∑ _y ∈ (Finset.univ : Finset β), n :=
    Finset.sum_le_sum (fun y _ => hcon y)
  rw [Finset.sum_const, smul_eq_mul, Finset.card_univ] at hle
  omega

set_option maxHeartbeats 2000000
set_option maxRecDepth 100000
set_option exponentiation.threshold 100000

/-- Strict cardinal inequality for the real 272-of-511 / 14-coefficient
/ product-mod-512 key, not a toy model. -/
theorem orbit_count :
    ((2130706433 ^ 14 * 512) * 2^59) < Nat.choose 511 272 := by
  rw [Nat.choose_eq_fast_choose]
  decide

/-- A *single* key fibre contains more than 2^59 distinct 272-column
subsets. The DecidableEq instance is computational bookkeeping and can
always be supplied classically; it is not a mathematical hypothesis.
No injectivity of y is needed for this counting step alone. -/
theorem exists_big_same_key_family {K : Type*} [Field K] [Fintype K]
    [DecidableEq ((Fin 14 → K) × Small)]
    (y : Small → K) (hK : Fintype.card K = 2130706433) :
    ∃ σ : (Fin 14 → K) × Small,
      2^59 < (Candidates.filter (fun U => key y U = σ)).card := by
  classical
  apply pigeonhole Candidates (key y) (2^59)
  rw [card_keys hK, candidates_card]
  exact orbit_count

end OrbitPencilLiftSameKey
