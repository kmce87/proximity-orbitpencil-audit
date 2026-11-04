# Indexed noncontainment audit — 2026-11-04 17:38 UTC

Base 68dcf2d6029a5aa32dc0dcf54215b91e7460c294, LeanPortIndexedNoncontainment.lean (blob dd2bd9cd69d4c40813631f8a26a84efc9d0dabd0).

Hypothesis: The indexed root-count proof is a conditional arbitrary-support noncontainment lemma and does not smuggle in the concrete MCA witness.

Source-checked: no_large_support assumes nonzero A and R, degree A = 4096, degree R ≤ 4095, degree q ≤ 1048576, support cardinality ≥1116048, and vanishing of A*q+R. Degree ≤1052672 and root-count force the polynomial to zero, contradicting the low-degree nonzero R. no_large_support_on_indices assumes domain injectivity to preserve support cardinality. quotient_direction_not_codeword_on_indices additionally assumes nonzero denominators and quotient identity.

Result: PASS at source-level conditional logic; NOT compiled in this run. This does not establish concrete domain injectivity, denominator nonvanishing, support construction, fixed received line, >2^59 distinct slopes, or external manuscript equivalence. The theorem excludes degree ≤1048576, stronger than deployed RS[D,2^20] exclusion (degree ≤1048575); its docstring saying degree <2^20 understates the theorem. File header explicitly says NOT KERNEL-CHECKED.

Replay:
```sh
git checkout 68dcf2d6029a5aa32dc0dcf54215b91e7460c294
lake env lean LeanPortIndexedNoncontainment.lean
grep -nE 'theorem |hdom|hdenom|hScard|hqdeg|eq_zero_of_natDegree|natDegree_mul' LeanPortIndexedNoncontainment.lean
```

Falsifiers: compilation failure, unexpected axioms, failure of injectivity or nonvanishing in concrete instance. Next inspect concrete call site and independently compare original RS-MCA source. No upstream report.
