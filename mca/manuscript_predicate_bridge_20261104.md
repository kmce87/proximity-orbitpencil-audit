# Lane A: external MCA predicate comparison — 2026-11-04 19:32 UTC

## One falsifiable hypothesis
At the pinned rs-mca manuscript commit 4bea7abb2d9455583c8864b980e39d11d550f51d, the support-wise MCA definition uses a *single shared support* for point agreement and failure of simultaneous explanation, so the local deployed WDeployed predicate is a sufficient witness **provided** the local evaluation domain is identified with the manuscript's actual D and the fields/codes coincide.

## Independently inspected source
- External: https://github.com/przchojecki/rs-mca/blob/4bea7abb2d9455583c8864b980e39d11d550f51d/tex/cs25_cap_v13_2.tex , section Preliminaries, labels def:mca, def:dstar and lem:mca-monotone.
- Local: LeanPortMcaComposition4096.lean, LeanPortDeployedTransfer4096.lean and LeanPortDomainTransport4096.lean at parent commit 3a4494e0ea4818529b26f001e4afd8e0cbbc1d7d; blobs bbdd21145974a5a4c91219a9234736a36380f78f, 7f16dc6c479dbc7e3921b26de67cce62b7d75d70, d0883ea81f8528d1cdfdc9d1ed3f2f72b20aaedc.

## Result: conditional source-level alignment
The manuscript defines RS[F,D,k] by polynomials of degree < k and MCA-bad gamma by existence of S subset D with |S| >= (1-delta)n, point f1+gamma*f2 explained on S, but no simultaneous pair of degree < k codewords explaining f1,f2 on S. Local WDeployed uses a degree <= 1048575 explaining polynomial and excludes even pairs with degrees <= 1048576. Thus its noncontainment is stronger than required for k=1048576. Its support size is >=1118207. The local theorem quantifies one pair of functions and a finite set of >2^59 distinct slopes. This is sufficient for the manuscript event *if* D, field, n and received functions are identified.

The manuscript's D is a multiplicative coset alpha H subset B^times (with B subset F); local D is Set.range node6 in Sextic. Local indexEquiv proves distinct indexed points but **does not by itself prove the range equals the published KoalaBear subgroup/coset or that its generator has exact order 2^21**. This is the principal remaining equivalence gap. No full external event theorem or Lean compilation was produced this run.

The manuscript explicitly proves support-wise MCA monotonicity (lem:mca-monotone), so threshold transfer is licensed once the field/domain and event equivalence are established. The ordinary LIST inequality at agreement 1116047 is separate and unaffected.

## Reproduce
1. Fetch the pinned external TeX and inspect labels def:mca, def:dstar, lem:mca-monotone and the RS[F,D,k] definition.
2. Fetch the three pinned local Lean files and compare WDeployed, BadDeployed, SupportWiseBad, indexEquiv and exists_many_deployed_bad_slopes.
3. Run the Lean 4.34 gate and compile the three files, printing axioms for their top-level theorems.
4. Independently prove node6 range = the published subgroup/coset, including generator exact order 2^21 and field embedding; only then assert a formal MCA implication.

## Status
Claimed: fixed-line >2^59 slopes at agreement 1118207. Source-checked this run: conditional logical predicate implication and the precise domain gap. Lean-kernel checked this run: no. Independent verifier accepted: no. No upstream issue or publication was made. Existing original OrbitPencil prior art: https://github.com/proximity-prize/proximity-prize/pull/38 ; originality not freshly established.
