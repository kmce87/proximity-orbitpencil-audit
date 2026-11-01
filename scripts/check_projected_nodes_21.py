#!/usr/bin/env python3
"""Independent 512-node arithmetic replay for the exact pinned KoalaBear NTT.

Source: CompPoly/Fields/KoalaBear/Basic.lean, index 21 of twoAdicGenerators
at commit df591bb8c6745126d1d72f5243faae3022b0432a, reached via
ArkLib 34a834c61c859cc04205f5f43fd237cda8fb0da4.

This is a numerical cross-check, not a Lean certificate or MCA witness.
"""
P = 2130706433
N = 1 << 21
H = 4096
M = 512
OMEGA = 0x484EF19B


def main() -> None:
    assert P - 1 == 127 * (1 << 24)
    assert N == H * M
    assert pow(OMEGA, N, P) == 1
    assert pow(OMEGA, N // 2, P) != 1
    y = [pow(OMEGA, H * b, P) for b in range(M)]
    assert len(set(y)) == M
    assert y[0] == 1
    assert pow(y[1], M, P) == 1
    assert pow(y[1], M // 2, P) != 1
    # Verify that each projected value is constant along all 4096 row indices.
    # One algebraic identity is sufficient; also check representative rows.
    for a in (0, 1, 2048, 4095):
        for b in range(M):
            assert pow(OMEGA, (512 * a + b) * H, P) == y[b]
    print("PASS: pinned KoalaBear 2^21 root, 512 distinct projected nodes, 4096-point fibres")
    print("omega =", hex(OMEGA), "first projected =", y[:5])


if __name__ == "__main__":
    main()
