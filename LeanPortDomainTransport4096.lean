import LeanPortWaNormalization4096

/-!
# Indexed-to-domain RS support-wise witness transport for KoalaBear

One falsifiable hypothesis: the existing kernel-checked n=2^21 witness
survives transporting support indices to the *actual distinct field elements*
of the evaluation domain. In particular, its *distinct bad slope count*
and exact 2^-128 cross-multiplied budget stay unchanged.

This proves an INTERNAL equivalence of two representations of the same
RS evaluation code, not an import of external rs-mca mathematical sources,
nor an official Proximity Prize ProtocolClaim. The external source defines
D_KB as the subgroup of order 2^21 in the base field; the source-pinned
check in PR #34 independently verifies the generator's exact order.
Original OrbitPencil technique: proximity-prize PR #38, including erdkocak.
-/

namespace OrbitPencilLiftDomainTransport4096

open Polynomial
open OrbitPencilLiftGeometry
open OrbitPencilLiftSameKey
open OrbitPencilLiftSupport4096
open OrbitPencilLiftDirectionNoncode4096
open OrbitPencilLiftWaBridge4096
open OrbitPencilLiftWaNormalization4096

/-- The domain of the actual evaluation points, not 2^21 abstract labels. -/
abbrev Domain := {x : Sextic // x ∈ Set.range node6}

/-- Reindexing by the concrete sextic node map is a bijection onto its range. -/
noncomputable def domainEquiv : Index ≃ Domain := by
  classical
  refine Equiv.ofBijective
    (fun j : Index => (⟨node6 j, ⟨j, rfl⟩⟩ : Domain)) ?_
  constructor
  · intro i j h
    apply node6_injective
    exact congrArg Subtype.val h
  · rintro ⟨x, ⟨j, hj⟩⟩
    exact ⟨j, Subtype.ext hj⟩

@[simp] theorem domainEquiv_val (j : Index) :
    (domainEquiv j).val = node6 j := rfl

/-- Pull a received word from indexed coordinates to actual field points. -/
noncomputable def toDomain (f : Index → Sextic) : Domain → Sextic :=
  fun x => f (domainEquiv.symm x)

@[simp] theorem toDomain_equiv (f : Index → Sextic) (j : Index) :
    toDomain f (domainEquiv j) = f j := by
  simp [toDomain]

/-- Transport the same finite support, without duplicating any position. -/
noncomputable def mapSupport (S : Finset Index) : Finset Domain := by
  classical
  exact S.image domainEquiv

theorem mapSupport_card (S : Finset Index) :
    (mapSupport S).card = S.card := by
  classical
  change (S.image domainEquiv).card = S.card
  exact Finset.card_image_of_injective S domainEquiv.injective

/-- RS support-wise W at field-labelled evaluation points. -/
def DomainW (f g : Domain → Sextic) (T : Finset Domain)
    (z : Sextic) : Prop :=
  1116048 ≤ T.card ∧
  (∃ c : Polynomial Sextic,
    c.natDegree ≤ 1048575 ∧
    ∀ x ∈ T, f x + z * g x = c.eval x.val) ∧
  ¬ ∃ cf cg : Polynomial Sextic,
    cf.natDegree ≤ 1048575 ∧
    cg.natDegree ≤ 1048575 ∧
    (∀ x ∈ T, f x = cf.eval x.val) ∧
    (∀ x ∈ T, g x = cg.eval x.val)

def DomainBadSlope (f g : Domain → Sextic) (z : Sextic) : Prop :=
  ∃ T : Finset Domain, DomainW f g T z

/-- Exact logical equivalence of the support witness, not merely one-way
implication. The same polynomial messages and slope are used on both sides. -/
theorem W_iff_domainW (f g : Index → Sextic)
    (S : Finset Index) (z : Sextic) :
    W f g S z ↔
      DomainW (toDomain f) (toDomain g) (mapSupport S) z := by
  classical
  constructor
  · rintro ⟨hcard, ⟨c, hcdeg, hmatch⟩, hnot⟩
    refine ⟨?_, ⟨c, hcdeg, ?_⟩, ?_⟩
    · simpa only [mapSupport_card] using hcard
    · intro x hx
      change x ∈ S.image domainEquiv at hx
      obtain ⟨j, hj, hjx⟩ := Finset.mem_image.mp hx
      subst x
      simpa only [toDomain_equiv, domainEquiv_val] using hmatch j hj
    · rintro ⟨cf, cg, hcf, hcg, hf, hg⟩
      apply hnot
      refine ⟨cf, cg, hcf, hcg, ?_, ?_⟩
      · intro j hj
        have hmem : domainEquiv j ∈ mapSupport S := by
          change domainEquiv j ∈ S.image domainEquiv
          exact Finset.mem_image.mpr ⟨j, hj, rfl⟩
        simpa only [toDomain_equiv, domainEquiv_val] using hf (domainEquiv j) hmem
      · intro j hj
        have hmem : domainEquiv j ∈ mapSupport S := by
          change domainEquiv j ∈ S.image domainEquiv
          exact Finset.mem_image.mpr ⟨j, hj, rfl⟩
        simpa only [toDomain_equiv, domainEquiv_val] using hg (domainEquiv j) hmem
  · rintro ⟨hcard, ⟨c, hcdeg, hmatch⟩, hnot⟩
    refine ⟨?_, ⟨c, hcdeg, ?_⟩, ?_⟩
    · simpa only [mapSupport_card] using hcard
    · intro j hj
      have hmem : domainEquiv j ∈ mapSupport S := by
        change domainEquiv j ∈ S.image domainEquiv
        exact Finset.mem_image.mpr ⟨j, hj, rfl⟩
      simpa only [toDomain_equiv, domainEquiv_val] using hmatch (domainEquiv j) hmem
    · rintro ⟨cf, cg, hcf, hcg, hf, hg⟩
      apply hnot
      refine ⟨cf, cg, hcf, hcg, ?_, ?_⟩
      · intro x hx
        change x ∈ S.image domainEquiv at hx
        obtain ⟨j, hj, hjx⟩ := Finset.mem_image.mp hx
        subst x
        simpa only [toDomain_equiv, domainEquiv_val] using hf j hj
      · intro x hx
        change x ∈ S.image domainEquiv at hx
        obtain ⟨j, hj, hjx⟩ := Finset.mem_image.mp hx
        subst x
        simpa only [toDomain_equiv, domainEquiv_val] using hg j hj

/-- The *same* distinct slope set from the verified 85-declaration
construction violates the exact bound on the field-labelled domain. -/
theorem exists_domain_W_above_normalized_budget :
    ∃ (alpha : Sextic) (U0 : Finset Small) (Z : Finset Sextic),
      Fintype.card Sextic < (2 : ℕ)^128 * Z.card ∧
      alpha ≠ 0 ∧ alpha ∉ projected6 ∧
      ∀ z ∈ Z,
        DomainBadSlope
          (toDomain (receivedBase alpha U0))
          (toDomain (receivedDirection alpha)) z := by
  obtain ⟨alpha, U0, Z, hcard, hnonzero, havoid, hbad⟩ :=
    exists_W_above_normalized_budget
  refine ⟨alpha, U0, Z, hcard, hnonzero, havoid, ?_⟩
  intro z hz
  obtain ⟨S, hW⟩ := hbad z hz
  exact ⟨mapSupport S,
    (W_iff_domainW (receivedBase alpha U0)
      (receivedDirection alpha) S z).mp hW⟩

#print axioms OrbitPencilLiftDomainTransport4096.domainEquiv_val
#print axioms OrbitPencilLiftDomainTransport4096.mapSupport_card
#print axioms OrbitPencilLiftDomainTransport4096.W_iff_domainW
#print axioms OrbitPencilLiftDomainTransport4096.exists_domain_W_above_normalized_budget

end OrbitPencilLiftDomainTransport4096
