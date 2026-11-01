# 2026-11-01 07:32 UTC — concrete projected-node injectivity

**One falsifiable hypothesis:** the actual pinned KoalaBear prime-field 2^21 NTT generator produces 512 distinct projected nodes under x ↦ x^4096, and the corresponding vanishing-polynomial map U ↦ V_U is injective. If false, the large-family alpha separation argument cannot be instantiated.

**Source and credit:** adaptation of accepted [OrbitPencil.lean PR #38](https://github.com/proximity-prize/proximity-prize/pull/38), with original contributor `erdkocak`. The 2^21 NTT generator is from [CompPoly/Fields/KoalaBear/Basic.lean](https://github.com/Verified-zkEVM/CompPoly/blob/df591bb8c6745126d1d72f5243faae3022b0432a/CompPoly/Fields/KoalaBear/Basic.lean), dependency pinned through ArkLib `34a834c61c859cc04205f5f43fd237cda8fb0da4`.

**Lean:** `LeanPortSameKeyFamily.lean` defines `baseNttDomain21` using CompPoly's `domainOfLogN 21`, proves `projectedNode_injective`, `V_eval_zero_iff_of_injective`, `V_injective_of_y_injective`, `concrete_V_injective`, and `concrete_V_sub_ne_zero`. The strict gate now builds CompPoly before compiling the source, and audits 30 declarations for only `propext`, `Classical.choice`, `Quot.sound`. Check the CI result for this exact commit; an unchecked source file is not a certificate.

**Independent numerical replay:**

```bash
python3 scripts/check_projected_nodes_21.py
bash scripts/run_lean_434_gate.sh
```

The Python check directly verifies the pinned 2^21 root `0x484EF19B`, its exact order, all 512 distinct projected nodes, and representative row-invariance checks. It is not a numerical witness for >2^59 slopes.

**Still unproved:** prime-field to sextic-field polynomial-map bridge, actual same received affine line, exact agreement support and support-wise MCA predicate, and independent-verifier acceptance. No prize-qualifying result.
