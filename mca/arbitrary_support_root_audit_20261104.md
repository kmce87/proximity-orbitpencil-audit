# Lane A: arbitrary-support direction noncontainment audit (2026-11-04 16:09 UTC)

## One falsifiable hypothesis
The local deployed MCA transfer relies on noncontainment of the fixed received direction on the **same selected support** S, not merely on the entire evaluation domain.

## Pinned evidence
Parent commit: 5e80c8c520581fa4f5cd5a12266ed9118c2cd3ac.
Files inspected directly: LeanPortDirectionNoncode4096.lean, LeanPortMcaComposition4096.lean, LeanPortDeployedTransfer4096.lean, LeanPortGeneratorPowerIdentity4096.lean.

**Source-level result: supported.** In LeanPortDirectionNoncode4096.lean, `received_direction_not_rs_on_support` quantifies over arbitrary `S : Finset Index` satisfying `1116048 ≤ S.card`. It passes that SAME S to `quotient_direction_not_codeword_on_indices`; it does not invoke `received_direction_not_rs` (the full-domain theorem). In LeanPortMcaComposition4096.lean, the selected agreement support has `1118207 ≤ S.card` and `received_direction_not_rs_on_support alpha havoid S (by omega)` is applied to that S. In LeanPortDeployedTransfer4096.lean, the support is mapped injectively by `indexEquiv`, and the same support is used for the explaining witness and noncontainment.

## Independently checkable degree sanity
Let A = X^4096 - C(alpha), R = coreLocator and q an alleged direction explanation with natDegree ≤ 1048576. Source records deg(A)=4096 and deg(R)≤4095. Cross-multiplication would yield a polynomial q*A+R vanishing on S, with degree at most 1048576+4096=1052672. Since |S|≥1116048>1052672, distinct evaluation points force q*A+R=0; degree of q*A (if q≠0) is ≥4096 whereas deg(R)≤4095, contradicting R≠0. The zero-q case also contradicts R≠0. This is a *sanity derivation*, not a newly executed Lean proof. The indexed lemma's implementation and field characteristic assumptions still require independent audit.

## Replay
```sh
git checkout 5e80c8c520581fa4f5cd5a12266ed9118c2cd3ac
grep -n -A48 'theorem received_direction_not_rs_on_support' LeanPortDirectionNoncode4096.lean
grep -n -A62 'theorem exists_many_supportwise_bad_slopes' LeanPortMcaComposition4096.lean
grep -n -A43 'theorem supportWiseBad_to_deployed' LeanPortDeployedTransfer4096.lean
bash scripts/run_lean_434_gate.sh
lake env lean LeanPortDeployedTransfer4096.lean
```

## Limits and next blocker
This is source inspection and arithmetic reasoning only; no fresh Lean execution or independent external acceptance. Next: inspect `LeanPortIndexedNoncontainment` proof and compare the external CAP25 v13.2 MCA event and field/domain definitions. The local `WDeployed` definition is not itself an official statement. The auxiliary RS[D,k+1] cannot supply the deployed degree <k witness. Ordinary LIST at a=1116047 is unaffected. No upstream issue posted. Original OrbitPencil PR #38 credit must be retained.

Sources: https://github.com/proximity-prize/proximity-prize/pull/38 ; https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex
