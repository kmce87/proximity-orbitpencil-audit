# MCA Lane A — deployed-degree falsification audit (2026-11-04 14:51 UTC)

Hypothesis: the local **domain-level** theorem has a degree-<k explaining witness for deployed RS[D,k], rather than deriving it incorrectly from the auxiliary degree-<=k witness.

Inspected pinned source: LeanPortDeployedTransfer4096.lean at e1deb86aabbba2e8cfec16db280927cfad756e31; LeanPortDomainTransport4096.lean at the same commit.

**Source-level result: supported.** WOnDomain (in DomainTransport) only bounds c.natDegree <= 1048576, so WOnDomain alone is NOT a deployed RS[D,1048576] witness. WDeployed (in DeployedTransfer) separately requires c.natDegree <= 1048575 and excludes simultaneous explanation of f and g by polynomials of natDegree <= 1048576. supportWiseBad_to_deployed takes c and hcdeg from SupportWiseBad directly, not from WOnDomain. exists_many_deployed_bad_slopes quantifies one alpha, one U0 and one Finset Z with 2^59 < Z.card; for each z in Z it proves BadDeployed for the SAME receivedBase and receivedDirection functions, with z-dependent supports. Finset cardinality counts distinct slopes. This is a local-model source check, not a new Lean build.

Falsification gate: verify SupportWiseBad in LeanPortMcaComposition4096.lean genuinely supplies hcdeg <= 1048575, that the deployed theorem is in the successful Lean 4.34 gate and has no disallowed axioms, and that the external manuscript's RS[D,k] uses precisely degree < k over the same field and domain. If any fail, retract the deployed interpretation. Do not infer deployed witness from code inclusion RS[D,k] subset RS[D,k+1].

Replay:
```sh
git checkout e1deb86aabbba2e8cfec16db280927cfad756e31
grep -n -A12 'def WDeployed' LeanPortDeployedTransfer4096.lean
grep -n -A30 'theorem supportWiseBad_to_deployed' LeanPortDeployedTransfer4096.lean
grep -n -A14 'theorem exists_many_deployed_bad_slopes' LeanPortDeployedTransfer4096.lean
bash scripts/run_lean_434_gate.sh
lake env lean LeanPortDeployedTransfer4096.lean
```

Outstanding: generator-power theorem has no confirmed passing Lean job at e1deb86a; exact primitive order and external sextic-field/domain identity remain unproved in this audit. The ordinary LIST inequality at a=1116047 is not implicated. No independent verifier acceptance or prize qualification.
