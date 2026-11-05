# MCA Lane A — concrete sextic cardinality falsification audit
UTC: 2026-11-05T08:59:49Z
Parent: d9502e8c1170befa54ec339e83aa887a6af28676

## Single falsifiable hypothesis
The local Lean sources still lack an explicit theorem proving that the concrete KoalaBear sextic field has cardinality 2130706433^6.

**FALSIFIED by direct source inspection.** At the pinned parent, LeanPortSameKeyFamily.lean already contains:

```lean
abbrev Sextic := _root_.KoalaBear.Ext6

theorem concrete_prime_card :
    Fintype.card _root_.KoalaBear.Field = 2130706433 := by
  rw [ZMod.card]
  norm_num [_root_.KoalaBear.fieldSize]

theorem concrete_sextic_card :
    Fintype.card Sextic = (2130706433 : ℕ) ^ 6 := by
  rw [_root_.KoalaBear.card_ext6]
  norm_num [_root_.KoalaBear.fieldSize]
```

The source imports CompPoly.Fields.KoalaBear.Ext6 and declares `baseToSextic` using `algebraMap`. These are not *new* Lean proofs this run. Do not conflate inspecting a theorem's source with independently rerunning the kernel, and do not infer manuscript equivalence merely from cardinality.

## Consequence
Remove the blanket statement “need to prove Sextic has p^6 elements” from the outstanding blocker list. Instead, verify the *existing* `concrete_sextic_card` transitive axiom output and CompPoly dependency pin, and formally prove the domain/RS code equivalence to the external rs-mca definition. The actual remaining question is whether the **same subgroup** and **same deployed code** are used, not whether some field has the correct size.

## Reproduction
```sh
git checkout d9502e8c1170befa54ec339e83aa887a6af28676
grep -n -A 5 'theorem concrete_sextic_card' LeanPortSameKeyFamily.lean
cat > /tmp/McaCardAudit.lean <<'EOF'
import LeanPortSameKeyFamily
#print OrbitPencilLiftSameKey.concrete_sextic_card
#print axioms OrbitPencilLiftSameKey.concrete_sextic_card
EOF
cp /tmp/McaCardAudit.lean ./McaCardAudit.lean
lake env lean McaCardAudit.lean
rm McaCardAudit.lean
```
The last command was NOT executed this run.

## External context / originality
Prior art: https://github.com/proximity-prize/proximity-prize/pull/38 (original OrbitPencil; original author credit required).
Pinned manuscript: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex .
No fresh exhaustive literature search or independent author acceptance this run.

## Evidence classification
(i) Full external fixed-line 4096-fibre MCA counterexample: claimed.
(ii) Source-checked: concrete field cardinality theorem already exists; this run independently inspected its source.
(iii) Lean kernel: historical local checks only; no new build this run.
(iv) Independent external verifier: NO.

Independently verified prize-qualifying result: NO.
Ordinary LIST at agreement 1116047 unaffected. Lane B untouched.
