# Lane A — finite-row source and challenge-set audit (2026-11-03 15:30 UTC)

**One falsifiable hypothesis:** Does the upstream `grande_finale.tex` finite KoalaBear MCA table, on its own, certify that the claimed 4096-fibre lift is a counterexample for deployed `RS[D,2^20]` and the full-field challenge set?

**Finding: NO.** The table explicitly assigns `K=2^20+1` to its MCA row, `K=2^20` to LIST, and does not specify `Gamma` in that finite row. This is a source-scope finding, **not** a claim that the author's broader MCA theorem uses the wrong code, or that the challenge set is proper. The author's larger manuscript and the foundation definitions must be inspected for the precise code and challenge-set quantifiers.

**Upstream source:** https://github.com/przchojecki/rs-mca/blob/main/experimental/grande_finale.tex (fetched via connected GitHub on 2026-11-03). Finite table: `KoalaBear MCA & 1116047 & 1116048 & 67471 & 274980728111395087`; immediately following: `Here n=2^21, K=2^20+1 on the MCA route, and K=2^20 on the list route.` The manuscript separately defines `B^{MCA}_{C,Gamma}` for a nonempty challenge set `Gamma`. The M2 bridge: https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m2/m2_line_decoding_mca_bridge.md.

**Local source:** `mca/ChallengeRestrictedNumerator.lean` at parent commit `e63f473184d49c1ae9ccecfb6b8bb6e82dcc827c` correctly requires `Z ⊆ Gamma`, but is a proposed abstract theorem, not a compiled or concrete KoalaBear certificate.

**Replay:** `python3 mca/audit_manuscript_finite_row.py`. It fetches current upstream main and asserts the exact finite-row text and adjacent dimension statement. Changes to upstream main intentionally cause a failed assertion requiring manual review. The script is source-only, not a proof of domain equivalence, polynomial degree, or slope injectivity. GitHub fetch of upstream and local file was performed this run; the script itself was not executed in a network-enabled shell.

**History inspected this run:** parent `e63f473` (challenge restriction), and source `BridgeQuantifiers.lean`, `SelfContainedFiniteCertificate.lean` at that parent. Historical `c7a517c` local Lean gate remains previously reported, not rerun. Earlier audit commit contents `8fd556d` and `bbbbc46` were not fetched this run and no new assertions are made about them.

**Next blocker:** Identify authoritative `Gamma` in the foundation's concrete KoalaBear statement; prove the constructed slope set lies in it, and independently prove each explaining polynomial has degree strictly below deployed `k=2^20`, while auxiliary noncontainment holds for `k+1`. Then formalize the fixed-line, support, injectivity and exact domain transfer. Do not claim a counterexample to the LIST row at `1116047`.

**Verification tiers:** (i) claimed: >2^59 distinct slopes at a=1118207; (ii) source-checked: upstream finite-row dimension and lack of Gamma specification in that row; (iii) Lean-kernel checked: no new result this run; (iv) independently verifier accepted: NO. Independently verified prize-qualifying result: NO.
