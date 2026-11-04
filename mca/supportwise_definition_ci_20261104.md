# Lane A — SupportWiseBad definition and generator CI result (2026-11-04 15:44 UTC)

## Falsifiable hypothesis
The source-level SupportWiseBad predicate directly supplies a deployed degree-<k polynomial on one support and one fixed affine line, without an implicit RS[D,k+1] witness substitution.

## Direct source inspection
Pinned parent: 8d1523653e9009a5e74f178be813ca51e8f89548. Inspected LeanPortMcaComposition4096.lean, LeanPortDeployedTransfer4096.lean, LeanPortDomainTransport4096.lean and LeanPortGeneratorPowerIdentity4096.lean.

SupportWiseBad quantifies S : Finset Index and c : Polynomial Sextic, demands 1118207 <= S.card, c.natDegree <= 1048575, and lineAt alpha U0 z j = c.eval (node6 j) for all j in S. Its noncontainment excludes q.natDegree <= 1048576 explaining the received direction on that SAME S. The composition theorem obtains alpha,U0,Sel ONCE, defines Z = Sel.image (gamma alpha U0), uses Finset.card_image_of_injOn to deduplicate slopes, and constructs per-slope supports. The domain transport maps each support via indexEquiv, which is injective, and the deployed theorem consumes the original c/hcdeg directly. This supports the hypothesis at source level. It does not independently establish external manuscript equivalence or reproduce the Lean kernel check.

## New externally observed CI result
GitHub REST Actions runs list returned run 41836873273, head e1deb86aabbba2e8cfec16db280927cfad756e31, branch mca-generator-trigger-fix-20261104-1318, event push, completed with conclusion success at 2026-11-04T13:25:14Z. This is evidence the workflow passed; separate job log inspection is still required to independently attribute individual axiom checks. URL: https://github.com/kmce87/proximity-orbitpencil-audit/actions/runs/41836873273

## Replay
```sh
git checkout 8d1523653e9009a5e74f178be813ca51e8f89548
grep -n -A18 'def SupportWiseBad' LeanPortMcaComposition4096.lean
grep -n -A55 'theorem exists_many_supportwise_bad_slopes' LeanPortMcaComposition4096.lean
grep -n -A36 'theorem supportWiseBad_to_deployed' LeanPortDeployedTransfer4096.lean
bash scripts/run_lean_434_gate.sh
lake env lean LeanPortDeployedTransfer4096.lean
```

## Remaining falsification
Check generator exact order 2^21, embedded field/domain identity with CAP25 v13.2, manuscript quantifier order and whether the published event uses support-wise noncontainment as modelled. Audit all Lean axioms from job logs. Ordinary LIST a=1116047 is not refuted. No independent verifier accepted result; no prize qualification established. Original 512-fibre OrbitPencil PR #38 credit retained.
