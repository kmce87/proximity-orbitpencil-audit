#!/usr/bin/env python3
"""Offline source-pinned audit of binary 64.00 proof dependency.
Source: proximity-prize/proximity-prize main on 2026-11-09.
This tests whether the published 64.00 proof is independent of line/pencil geometry.
No Lean compilation, new bound, or verifier acceptance is claimed.
"""
SOURCES = {
 'Solution.lean': ('c49b7dd75f40928f97c91862fb3d489d82bdb68c', '''theorem candidate : ProtocolClaim 6400 78622925 268435456 :=
  ProximityPrize.SubmissionBinaryLower.P64C7High.protocolClaim6400'''),
 'P64C7High.lean': ('9a4e4c40118f29a048e683bdc82cd37fe7a441cc', '''theorem class7 : P64HighAssembly.Class7Interface := by
  have hb : R.natDegree * 1481911 < ∑ i, lineOrd R (dom i) (lineOf u₀ u₁ i) := by omega
  have hp := P64C7Profile.profile_le dom u₀ u₁ R hirr hh hw hgood hβ
  theorem protocolClaim6400 : ProtocolClaim 6400 78622925 268435456 :=
  P64HighAssembly.protocolClaim6400_of_class7 class7'''),
 'P64HighAssembly.lean': ('b38bbc593b6f041120133f9b4535e25efcf7a331', '''def Class7Interface : Prop :=
    208984 ≤ (P64Incidence.lam dom (lineOf u₀ u₁) R).card →
    (∀ z ∈ Vs, Dangerous dom (lineOf u₀ u₁) 1048575 1482911 R (Az z)) →
    R.natDegree * 1482911 - (∑ i, lineOrd R (dom i) (lineOf u₀ u₁ i)) < 1000 * R.natDegree →
  theorem protocolClaim6400_of_class7 (h7 : Class7Interface) :''')
}
solution = SOURCES['Solution.lean'][1]
high = SOURCES['P64C7High.lean'][1]
assembly = SOURCES['P64HighAssembly.lean'][1]
assert 'P64C7High.protocolClaim6400' in solution
assert 'P64HighAssembly.protocolClaim6400_of_class7 class7' in high
assert 'lineOrd R' in high and 'lineOf u₀ u₁' in high
assert 'P64Incidence.lam' in assembly and 'Dangerous' in assembly
assert 'lineOrd R' in assembly
print('FALSIFIED: published binary 64.00 proof is not pencil-independent.')
print('Source blobs:',*(f'{k}: {v[0]}' for k,v in SOURCES.items()),sep='\n')
print('This is a pinned-source structural audit, not a Lean proof or impossibility theorem.')
