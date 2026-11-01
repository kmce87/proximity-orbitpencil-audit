# 2026-11-01 06:42 UTC — falsification-first key-constraint bridge

**One hypothesis:** for two 272-of-511 projected-column subsets in the same 14-top-coefficient and residue-mod-512 key fibre, their monic vanishing-polynomial difference has degree < 258 and equal constant terms when projected nodes are `eta^b`, `eta^512=1`.

The original n=2^18 OrbitPencil construction proves the analogous statements in [accepted PR #38](https://github.com/proximity-prize/proximity-prize/pull/38), with original contributor `erdkocak`. This is a parameterized adaptation, not a new attack or a prize submission.

Source: `LeanPortSameKeyFamily.lean`, new declarations `V_monic`, `V_natDegree`, `candidate_card`, `V_coeff_top`, `V_coeff_gt`, `top_coeff_eq_of_key`, `V_sub_degree_lt_of_key`, `V_eval_zero_pow`, `V_eval_zero_eq_of_key`.

**Falsification test:** the Lean 4.34 CI must compile the nine declarations and print a transitive axiom closure containing only `propext`, `Classical.choice`, `Quot.sound`. A compiler or axiom-audit failure invalidates the local certification claim. Run `bash scripts/run_lean_434_gate.sh` from this branch; inspect the GitHub Actions run for the exact commit.

Local independent numeric replay: `cd /mnt/data/orbit_next && python3 scripts/verify_4096_lift.py && python3 scripts/verify_same_key_certificate.py`; the latter verifies 100,000 distinct explicitly encoded prime-field slopes and SHA256 `59a2731fde962e56059229f50176861321aa46e3f3324af6c6a546f778d8c57f`, not the >2^59 extension-field family. The historical local Git archive at `9755b5e` is distinct from this GitHub history.

**Not yet proved:** the concrete projected-node injectivity in the n=2^21 RS domain, the nonzero difference for distinct subsets in the selected family, the full common received-line witness, its exact support-wise MCA predicate, or independent verifier acceptance. The ordinary LIST inequality at 1116047 remains untouched.

Prize-qualifying result: **NO**.
