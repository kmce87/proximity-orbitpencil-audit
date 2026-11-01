import Mathlib
import CompPoly.Univariate.NTT.KoalaBear
import CompPoly.Fields.KoalaBear.Ext6

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


/-!
## Concrete KoalaBear n = 2^21 NTT projection

Unlike the generic pigeonhole lemma, these declarations instantiate the
*actual prime field* and its CompPoly 2^21 NTT generator. They prove that
the 512 projected nodes are pairwise distinct, and hence distinct subsets
give distinct vanishing polynomials. The separate extension-field and
received-line/MCA bridges are not proved here.
-/

/-- The exact KoalaBear prime-field NTT domain at size 2^21. -/
def baseNttDomain21 :
    CompPoly.CPolynomial.NTT.Domain _root_.KoalaBear.Field :=
  CompPoly.CPolynomial.NTT.KoalaBear.domainOfLogN 21
    (by norm_num [_root_.KoalaBear.twoAdicity])

noncomputable def omega21 : _root_.KoalaBear.Field :=
  baseNttDomain21.omega

/-- Projection by x ↦ x^4096 on the first row of the 4096 × 512 grid. -/
noncomputable def projectedNode (b : Small) : _root_.KoalaBear.Field :=
  (omega21 ^ b.val) ^ 4096

/-- The 512 projected NTT nodes really are distinct in KoalaBear.Field. -/
theorem projectedNode_injective : Function.Injective projectedNode := by
  intro b c h
  apply Fin.ext
  refine Nat.eq_of_mul_eq_mul_right (by norm_num : 0 < 4096) ?_
  apply baseNttDomain21.primitive.pow_inj
  · change b.val * 4096 < 2097152
    omega
  · change c.val * 4096 < 2097152
    omega
  simpa only [projectedNode, omega21, pow_mul] using h

/-- A vanishing polynomial of injectively labelled roots detects membership. -/
theorem V_eval_zero_iff_of_injective {K : Type*} [Field K]
    (y : Small → K) (hy : Function.Injective y)
    (U : Finset Small) (b : Small) :
    (V y U).eval (y b) = 0 ↔ b ∈ U := by
  classical
  constructor
  · intro h
    rw [V, Polynomial.eval_prod, Finset.prod_eq_zero_iff] at h
    obtain ⟨c, hc, hzero⟩ := h
    rw [Polynomial.eval_sub, Polynomial.eval_X, Polynomial.eval_C, sub_eq_zero] at hzero
    rwa [hy hzero]
  · intro h
    rw [V, Polynomial.eval_prod]
    refine Finset.prod_eq_zero h ?_
    simp

/-- Distinct root subsets cannot produce the same vanishing polynomial. -/
theorem V_injective_of_y_injective {K : Type*} [Field K]
    (y : Small → K) (hy : Function.Injective y) :
    Function.Injective (V y) := by
  intro U W h
  ext b
  rw [← V_eval_zero_iff_of_injective y hy U b,
      ← V_eval_zero_iff_of_injective y hy W b, h]

/-- Concrete consequence needed by the slope-separation root count. -/
theorem concrete_V_injective :
    Function.Injective (V projectedNode) :=
  V_injective_of_y_injective projectedNode projectedNode_injective

/-- Different column subsets give a nonzero polynomial difference,
    closing the nonvanishing premise of the alpha root-count lemma. -/
theorem concrete_V_sub_ne_zero {U W : Finset Small} (h : U ≠ W) :
    V projectedNode U - V projectedNode W ≠ 0 := by
  apply sub_ne_zero.mpr
  intro hEq
  exact h (concrete_V_injective hEq)


/-!
## Prime-field to extension-field bridge

This is the next falsification gate for the large-domain OrbitPencil lift.
The map is a genuine field homomorphism, so injectivity is automatic.
These results do not assume that the extension is specifically sextic:
the concrete sextic field and its cardinality are still to be instantiated.
-/

theorem mapped_nodes_injective {K L : Type*} [Field K] [Field L]
    (φ : K →+* L) (y : Small → K) (hy : Function.Injective y) :
    Function.Injective (fun b => φ (y b)) := by
  intro b c h
  exact hy (φ.injective h)

/-- The vanishing polynomial over an extension is the coefficientwise
image of the original prime-field vanishing polynomial. -/
theorem V_map {K L : Type*} [Field K] [Field L]
    (φ : K →+* L) (y : Small → K) (U : Finset Small) :
    (V y U).map φ = V (fun b => φ (y b)) U := by
  classical
  simp [V, Polynomial.map_prod]

/-- Distinct prime-field root subsets remain distinct after field extension. -/
theorem mapped_V_injective {K L : Type*} [Field K] [Field L]
    (φ : K →+* L) (y : Small → K) (hy : Function.Injective y) :
    Function.Injective (V (fun b => φ (y b))) :=
  V_injective_of_y_injective _ (mapped_nodes_injective φ y hy)

/-- In particular, a distinct pair cannot collapse to the same polynomial
after passing to the sextic extension. -/
theorem mapped_V_sub_ne_zero {K L : Type*} [Field K] [Field L]
    (φ : K →+* L) (y : Small → K) (hy : Function.Injective y)
    {U W : Finset Small} (hne : U ≠ W) :
    V (fun b => φ (y b)) U - V (fun b => φ (y b)) W ≠ 0 := by
  apply sub_ne_zero.mpr
  intro hEq
  exact hne (mapped_V_injective φ y hy hEq)

/-- The *base-field* same-key hypothesis suffices to retain the degree-257
difference bound over any field extension; no extra top-key condition
over the much larger extension field is required. -/
theorem mapped_V_sub_natDegree_lt_of_key {K L : Type*} [Field K] [Field L]
    (φ : K →+* L) (y : Small → K)
    {U W : Finset Small} (hU : U ∈ Candidates) (hW : W ∈ Candidates)
    (hkey : key y U = key y W) :
    (V (fun b => φ (y b)) U - V (fun b => φ (y b)) W).natDegree < 258 := by
  have hd := V_sub_degree_lt_of_key y hU hW hkey
  have hn : (V y U - V y W).natDegree < 258 := by
    by_cases hz : V y U - V y W = 0
    · simp [hz]
    · exact (Polynomial.natDegree_lt_iff_degree_lt hz).mpr hd
  have heq :
      V (fun b => φ (y b)) U - V (fun b => φ (y b)) W =
        (V y U - V y W).map φ := by
    rw [Polynomial.map_sub, V_map, V_map]
  rw [heq]
  exact (Polynomial.natDegree_map_le).trans_lt hn


/-!
## Concrete sextic instantiation: no abstract extension field/cardinality premise

The CompPoly KoalaBear.Ext6 model is a genuine field of order p^6.
This is the actual field model underlying the proposed n=2^21 lift,
not an arbitrary field embedding or an unproved sextic-cardinality axiom.

The same-key condition is imposed over the *prime* field; the
residue/product component alone controls constant coefficients after
mapping to Ext6.  These facts do not yet construct a received affine
line or establish an MCA support witness.
-/

abbrev Sextic := _root_.KoalaBear.Ext6

noncomputable def baseToSextic : _root_.KoalaBear.Field →+* Sextic :=
  algebraMap _root_.KoalaBear.Field Sextic

theorem concrete_prime_card :
    Fintype.card _root_.KoalaBear.Field = 2130706433 := by
  rw [ZMod.card]
  norm_num [_root_.KoalaBear.fieldSize]

theorem concrete_sextic_card :
    Fintype.card Sextic = (2130706433 : ℕ) ^ 6 := by
  rw [_root_.KoalaBear.card_ext6]
  norm_num [_root_.KoalaBear.fieldSize]

noncomputable def eta6 : Sextic := (baseToSextic omega21) ^ 4096

theorem eta6_pow : eta6 ^ 512 = 1 := by
  have hw : omega21 ^ 2097152 = 1 := by
    simpa only [omega21] using baseNttDomain21.primitive.pow_eq_one
  change ((baseToSextic omega21) ^ 4096) ^ 512 = 1
  rw [← pow_mul]
  have hmul : 4096 * 512 = 2097152 := by norm_num
  rw [hmul, ← map_pow, hw, map_one]

theorem eta6_node (b : Small) :
    baseToSextic (projectedNode b) = eta6 ^ b.val := by
  calc
    baseToSextic (projectedNode b) =
        (baseToSextic omega21) ^ (b.val * 4096) := by
      simp only [projectedNode, map_pow, pow_mul]
    _ = (baseToSextic omega21) ^ (4096 * b.val) := by rw [Nat.mul_comm]
    _ = eta6 ^ b.val := by simp only [eta6, pow_mul]

/-- The original *prime-field* product key forces equal constant terms
for mapped sextic vanishing polynomials, without assuming an extension
field top-coefficient key collision. -/
theorem concrete_sextic_constant_eq_of_key
    {U W : Finset Small} (hU : U ∈ Candidates) (hW : W ∈ Candidates)
    (hkey : key projectedNode U = key projectedNode W) :
    (V (fun b => baseToSextic (projectedNode b)) U).eval 0 =
      (V (fun b => baseToSextic (projectedNode b)) W).eval 0 := by
  have hfun : (fun b : Small => baseToSextic (projectedNode b)) =
      (fun b : Small => eta6 ^ b.val) := funext eta6_node
  rw [hfun, V_eval_zero_pow eta6 (candidate_card hU),
      V_eval_zero_pow eta6 (candidate_card hW)]
  apply pow_eq_pow_of_modEq (n := 512) _ eta6_pow
  exact congrArg Fin.val (congrArg Prod.snd hkey)

/-- Unconditional same-key cardinality for the actual KoalaBear base field
and the actual 2^21 projected nodes (no abstract cardinal assumption). -/
theorem concrete_same_key_family :
    ∃ σ : (Fin 14 → _root_.KoalaBear.Field) × Small,
      2^59 < (Candidates.filter (fun U => key projectedNode U = σ)).card := by
  classical
  exact exists_big_same_key_family projectedNode concrete_prime_card

/-- The real base-field key bounds degree after mapping into the concrete
sextic, not merely into a hypothetical field extension. -/
theorem concrete_sextic_degree_lt_of_key
    {U W : Finset Small} (hU : U ∈ Candidates) (hW : W ∈ Candidates)
    (hkey : key projectedNode U = key projectedNode W) :
    (V (fun b => baseToSextic (projectedNode b)) U -
      V (fun b => baseToSextic (projectedNode b)) W).natDegree < 258 := by
  exact mapped_V_sub_natDegree_lt_of_key baseToSextic projectedNode hU hW hkey

theorem concrete_sextic_sub_ne_zero
    {U W : Finset Small} (hne : U ≠ W) :
    V (fun b => baseToSextic (projectedNode b)) U -
      V (fun b => baseToSextic (projectedNode b)) W ≠ 0 := by
  exact mapped_V_sub_ne_zero baseToSextic projectedNode projectedNode_injective hne

end OrbitPencilLiftSameKey
