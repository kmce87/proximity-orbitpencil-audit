#!/usr/bin/env python3
"""Evidence gate: historical Koala leaderboard != Lean 4.34 v20 acceptance.
This cannot authenticate receipts. Run with optional receipt JSON path.
"""
import json, sys
SLUGS={"lower":"proximity-prize-reduction-lower","upper":"proximity-prize-reduction-upper"}
VERSION="irs-reduction-threshold-v20"
def inspect(r):
    if not isinstance(r,dict) or not r: return "UNKNOWN: no receipt"
    track=r.get("track")
    if track not in SLUGS: return "REJECT: track"
    if r.get("slug")!=SLUGS[track]: return "REJECT: slug"
    if r.get("version")!=VERSION: return "REJECT: version"
    if r.get("lean")!="4.34.0": return "REJECT: toolchain"
    if r.get("verdict")!="accepted": return "REJECT: verdict"
    sha=r.get("commit_sha")
    if not isinstance(sha,str) or len(sha)!=40 or any(c not in "0123456789abcdef" for c in sha): return "REJECT: commit"
    if not isinstance(r.get("score_centibits"),int): return "REJECT: score"
    return "UNAUTHENTICATED: verify receipt independently with service"
if __name__=="__main__":
    assert inspect({}).startswith("UNKNOWN")
    assert inspect({"track":"upper","slug":SLUGS["upper"],"version":VERSION,"lean":"4.34.0","verdict":"accepted","commit_sha":"a"*40,"score_centibits":11613}).startswith("UNAUTHENTICATED")
    r=json.load(open(sys.argv[1])) if len(sys.argv)>1 else {}
    print(inspect(r))
