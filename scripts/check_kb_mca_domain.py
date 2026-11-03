#!/usr/bin/env python3
"""Independent, exact subgroup-domain check for the 4096-fibre MCA lift.

This is a SOURCE-BOUND MODEL-IDENTIFICATION TEST, not a Lean proof or an
independent-verifier acceptance of the MCA counterexample.

Usage:
  python3 scripts/check_kb_mca_domain.py --comppoly-root /path/to/CompPoly

The CompPoly checkout must be at zksecurity/CompPoly
411708c17175ab5ecaf035036608c206c4ee0878.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

P = 2130706433
N = 1 << 21
LOG_N = 21
PINNED = {
    "basic": "995bc4448ca3d4c16501ffa862a677542364c8cd",
    "ntt": "376be9308b6f4f652cb5c28f8da7be14b6f6444b",
    "samekey": "7fcf2e7d81f0ddd405b83d09a229a019b236d4fa",
    "support": "5561a9b2462bf0f0267ef2afc446e7f5d99602af",
}
EXPECTED_OMEGA21 = 0x484EF19B

def read_pinned(path: Path, blob: str) -> str:
    raw = path.read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if digest != PINNED[blob]:
        raise AssertionError(f"source pin drift for {path}: {digest} != {PINNED[blob]}")
    return raw.decode("utf-8")

def run(root: Path, comppoly_root: Path) -> dict:
    basic = read_pinned(comppoly_root / "CompPoly/Fields/KoalaBear/Basic.lean", "basic")
    ntt = read_pinned(comppoly_root / "CompPoly/Univariate/NTT/KoalaBear.lean", "ntt")
    samekey = read_pinned(root / "LeanPortSameKeyFamily.lean", "samekey")
    support = read_pinned(root / "LeanPortSupport4096.lean", "support")

    assert "KoalaBear.twoAdicGenerators[bitsOfLogN logN hlogN]" in ntt, (
        "NTT domain generator is no longer from the pinned table")
    assert "CompPoly.CPolynomial.NTT.KoalaBear.domainOfLogN 21" in samekey, (
        "Lift no longer selects NTT logN=21")
    assert "baseNttDomain21.omega" in samekey
    assert "omega21 ^ j.val" in support
    assert "baseToSextic (node21 j)" in support
    assert "Function.Injective node21" in support
    assert "Fintype.card Sextic = (2130706433 : ℕ) ^ 6" in samekey
    assert "abbrev Sextic := _root_.KoalaBear.Ext6" in samekey

    after = basic.split("def twoAdicGenerators : List Field :=", 1)[1]
    table = after.split("@[simp] lemma twoAdicGenerators_length", 1)[0]
    entries = [int(m, 16) for m in re.findall(r"\(0x([0-9a-fA-F]+)\s*:\s*Field\)", table)]
    assert len(entries) == 25, f"expected 25 two-adic generators, got {len(entries)}"
    g = entries[LOG_N]
    assert g == EXPECTED_OMEGA21, f"unexpected omega21: {g:#x}"
    assert (P - 1) % N == 0
    assert 0 < g < P
    assert pow(g, N, P) == 1
    assert pow(g, N // 2, P) == P - 1

    # Since N is a power of two, these two pow tests establish ord_P(g)=N.
    # The N distinct powers then enumerate the unique subgroup of order N
    # in the multiplicative group of the prime field F_P.
    return {
        "status": "PASS_EXACT_KB_DOMAIN_GENERATOR",
        "compPoly_revision": "411708c17175ab5ecaf035036608c206c4ee0878",
        "blob_pins": PINNED,
        "p": P,
        "n": N,
        "omega21_hex": hex(g),
        "omega21_decimal": g,
        "omega21_pow_n_mod_p": pow(g, N, P),
        "omega21_pow_half_n_mod_p": pow(g, N // 2, P),
        "subgroup_order": N,
        "local_index_mapping": "node21(j)=omega21^j",
        "transport_status": "SOURCE_MATCH; explicit Lean theorem identifying image with externally named D_KB still outstanding",
        "not_a_claim": "No independent MCA/prize acceptance; tests NTT domain identification only",
    }

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--comppoly-root", type=Path, required=True)
    ap.add_argument("--audit-root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = ap.parse_args()
    print(json.dumps(run(args.audit_root, args.comppoly_root), indent=2, sort_keys=True))
