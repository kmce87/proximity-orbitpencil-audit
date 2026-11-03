import LeanPortDeployedTransfer4096

/-!
CAP25 v13.2 support-wise MCA event: a local formal implication, not an
import of the manuscript's definitions or an independent prize verification.
One fixed pair of received words, and one support per slope.
Source: przchojecki/rs-mca, tex/cs25_cap_v13_2.tex, def:mca,
revision 4bea7abb2d9455583c8864b980e39d11d550f51d.
Original OrbitPencil 512-fibre prior art: proximity-prize PR #38.
-/

namespace OrbitPencilCAP25Event4096
open Polynomial
open OrbitPencilLiftSameKey
open OrbitPencilLiftGeometry
open OrbitPencilLiftConcreteSlopes
open OrbitPencilLiftDomainTransport4096
open OrbitPencilLiftWaBridge4096
open OrbitPencilLiftDeployedTransfer4096

/-- Deployed RS[D,k] with k=2^20: evaluations of polynomials of degree < k. -/
def Explains (h : D → Sextic) (S : Finset D) : Prop :=
  ∃ c : Polynomial Sextic,
    c.natDegree < 1048576 ∧
    ∀ x ∈ S, h x = c.eval x.val

/-- The support-wise bad event of CAP25 def:mca, at agreement 1118207. -/
def CAP25Bad (f g : D → Sextic) (z : Sextic) : Prop :=
  ∃ S : Finset D,
    1118207 ≤ S.card ∧
    Explains (fun x => f x + z * g x) S ∧
    ¬ (Explains f S ∧ Explains g S)

/-- Stronger auxiliary noncontainment entails deployed-code noncontainment. -/
theorem deployed_implies_CAP25Bad (f g : D → Sextic) (z : Sextic)
    (h : BadDeployed f g z) : CAP25Bad f g z := by
  rcases h with ⟨S, hcard, ⟨c, hcdeg, hmatch⟩, hnot⟩
  refine ⟨S, hcard, ⟨c, by omega, hmatch⟩, ?_⟩
  rintro ⟨⟨cf, hcfdeg, hcf⟩, ⟨cg, hcgdeg, hcg⟩⟩
  apply hnot
  exact ⟨cf, cg, by omega, by omega, hcf, hcg⟩

/-- One fixed received affine line, with >2^59 DISTINCT full-field slopes
satisfying the CAP25-shaped support-wise event. This does not yet prove
the manuscript domain's definitional identity or probability normalization. -/
theorem exists_many_CAP25_bad_slopes :
    ∃ (f g : D → Sextic) (Z : Finset Sextic),
      2^59 < Z.card ∧
      ∀ z ∈ Z, CAP25Bad f g z := by
  obtain ⟨alpha, U0, Z, hcard, _halpha, _havoid, hbad⟩ :=
    exists_many_deployed_bad_slopes
  refine ⟨(fun x => receivedBase alpha U0 (indexEquiv.symm x)),
    (fun x => receivedDirection alpha (indexEquiv.symm x)), Z,
    hcard, ?_⟩
  intro z hz
  exact deployed_implies_CAP25Bad _ _ z (hbad z hz)

#print axioms OrbitPencilCAP25Event4096.deployed_implies_CAP25Bad
#print axioms OrbitPencilCAP25Event4096.exists_many_CAP25_bad_slopes
end OrbitPencilCAP25Event4096
