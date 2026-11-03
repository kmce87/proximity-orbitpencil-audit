import LeanPortCAP25Event4096

/-!
CAP25 finite-budget witness at agreement a₀=1116048.
This proves a cardinal comparison in the LOCAL KoalaBear domain model,
not the full manuscript probability identity or independent acceptance.
Source: przchojecki/rs-mca tex/cs25_cap_v13_2.tex def:mca
at 4bea7abb2d9455583c8864b980e39d11d550f51d.
Original OrbitPencil 512-fibre prior art: proximity-prize PR #38.
-/

namespace OrbitPencilCAP25Budget4096
open OrbitPencilLiftSameKey
open OrbitPencilLiftDomainTransport4096
open OrbitPencilCAP25Event4096

/-- The weaker candidate-safe agreement threshold, exactly as an integer. -/
def CAP25BadAtA0 (f g : D → Sextic) (z : Sextic) : Prop :=
  ∃ S : Finset D,
    1116048 ≤ S.card ∧
    Explains (fun x => f x + z * g x) S ∧
    ¬ (Explains f S ∧ Explains g S)

/-- The same support witnesses the weaker threshold. -/
theorem CAP25Bad_implies_at_a0 (f g : D → Sextic) (z : Sextic)
    (h : CAP25Bad f g z) : CAP25BadAtA0 f g z := by
  rcases h with ⟨S, hcard, hpoint, hnoncontain⟩
  exact ⟨S, by omega, hpoint, hnoncontain⟩

/-- Fixed received pair; strictly more than the printed B* distinct
field slopes at agreement a₀. No unproved auxiliary-code inclusion. -/
theorem exists_many_CAP25_a0_above_budget :
    ∃ (f g : D → Sextic) (Z : Finset Sextic),
      274980728111395087 < Z.card ∧
      ∀ z ∈ Z, CAP25BadAtA0 f g z := by
  obtain ⟨f, g, Z, hcard, hbad⟩ := exists_many_CAP25_bad_slopes
  refine ⟨f, g, Z, ?_, ?_⟩
  · have hbudget : 274980728111395087 < (2 : ℕ)^59 := by norm_num
    omega
  · intro z hz
    exact CAP25Bad_implies_at_a0 f g z (hbad z hz)

#print axioms OrbitPencilCAP25Budget4096.CAP25Bad_implies_at_a0
#print axioms OrbitPencilCAP25Budget4096.exists_many_CAP25_a0_above_budget
end OrbitPencilCAP25Budget4096
