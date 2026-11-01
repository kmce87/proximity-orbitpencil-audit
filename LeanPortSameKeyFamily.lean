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
  apply pigeonhole Candidates (key y) (2^59)
  rw [card_keys hK, candidates_card]
  exact orbit_count


/-!
## Source-to-claim bridge: equal keys imply the two polynomial constraints

The accepted OrbitPencil.lean PR #38 proves these facts for its 512-fibre
instance. Here the same 272-column polynomial and 14-coefficient key are
used with a parameterized field, so the statements can be applied to the
4096-point-fibre lift after the concrete NTT-domain injectivity is supplied.
-/

theorem V_monic {K : Type*} [Field K] (y : Small → K)
    (U : Finset Small) : (V y U).Monic :=
  Polynomial.monic_prod_of_monic _ _ fun b _ => Polynomial.monic_X_sub_C (y b)

theorem V_natDegree {K : Type*} [Field K] (y : Small → K)
    (U : Finset Small) : (V y U).natDegree = U.card := by
  classical
  rw [V, Polynomial.natDegree_prod_of_monic _ _
    (fun b (_ : b ∈ U) => Polynomial.monic_X_sub_C (y b))]
  simp

theorem candidate_card {U : Finset Small} (hU : U ∈ Candidates) :
    U.card = 272 := (Finset.mem_powersetCard.mp hU).2

theorem V_coeff_top {K : Type*} [Field K] (y : Small → K)
    {U : Finset Small} (hU : U ∈ Candidates) :
    (V y U).coeff 272 = 1 := by
  have hm := V_monic y U
  rw [Polynomial.Monic, Polynomial.leadingCoeff, V_natDegree, candidate_card hU] at hm
  exact hm

theorem V_coeff_gt {K : Type*} [Field K] (y : Small → K)
    {U : Finset Small} (hU : U ∈ Candidates)
    {d : ℕ} (hd : 272 < d) : (V y U).coeff d = 0 := by
  refine Polynomial.coeff_eq_zero_of_natDegree_lt ?_
  rw [V_natDegree, candidate_card hU]
  exact hd

theorem top_coeff_eq_of_key {K : Type*} [Field K] (y : Small → K)
    {U W : Finset Small} (hkey : key y U = key y W)
    {d : ℕ} (hlo : 258 ≤ d) (hhi : d ≤ 271) :
    (V y U).coeff d = (V y W).coeff d := by
  have hk := congrArg Prod.fst hkey
  have hi : 271 - d < 14 := by omega
  have hc := congrFun hk ⟨271 - d, hi⟩
  simpa only [key, topKey, show 271 - (271 - d) = d by omega] using hc

/-- The concrete 14-coefficient key bounds the degree of the difference;
it is NOT an extra hypothesis on the polynomial family. -/
theorem V_sub_degree_lt_of_key {K : Type*} [Field K] (y : Small → K)
    {U W : Finset Small} (hU : U ∈ Candidates) (hW : W ∈ Candidates)
    (hkey : key y U = key y W) :
    (V y U - V y W).degree < (258 : ℕ) := by
  rw [Polynomial.degree_lt_iff_coeff_zero]
  intro d hd
  have hd258 : 258 ≤ d := by exact_mod_cast hd
  rw [Polynomial.coeff_sub]
  rcases lt_trichotomy d 272 with hlt | heq | hgt
  · have hle : d ≤ 271 := by omega
    rw [top_coeff_eq_of_key y hkey hd258 hle, sub_self]
  · subst d
    rw [V_coeff_top y hU, V_coeff_top y hW, sub_self]
  · rw [V_coeff_gt y hU hgt, V_coeff_gt y hW hgt, sub_self]

/-- The 272-element root product has positive sign at zero. -/
theorem V_eval_zero_pow {K : Type*} [Field K] (eta : K)
    {U : Finset Small} (hcard : U.card = 272) :
    (V (fun b => eta ^ b.val) U).eval 0 =
      eta ^ (∑ b ∈ U, b.val) := by
  rw [V, Polynomial.eval_prod]
  simp only [Polynomial.eval_sub, Polynomial.eval_X, Polynomial.eval_C, zero_sub]
  rw [Finset.prod_neg, hcard]
  norm_num
  rw [Finset.prod_pow_eq_pow_sum]

/-- Equality of the residue key forces equal constant coefficients for
the actual multiplicative projected-column nodes eta^b, eta^512=1. -/
theorem V_eval_zero_eq_of_key {K : Type*} [Field K] (eta : K)
    (heta : eta ^ 512 = 1)
    {U W : Finset Small}
    (hU : U ∈ Candidates) (hW : W ∈ Candidates)
    (hkey : key (fun b => eta ^ b.val) U =
            key (fun b => eta ^ b.val) W) :
    (V (fun b => eta ^ b.val) U).eval 0 =
      (V (fun b => eta ^ b.val) W).eval 0 := by
  rw [V_eval_zero_pow eta (candidate_card hU),
      V_eval_zero_pow eta (candidate_card hW)]
  apply pow_eq_pow_of_modEq (n := 512) _ heta
  exact congrArg Fin.val (congrArg Prod.snd hkey)

end OrbitPencilLiftSameKey
