#!/usr/bin/env python3
"""Recheck the official binary upper record through the GitHub search API only.

Used by the post-FINAL runs (run 24 on). The official repository is not cloned in these
runs, so the record is read from code-search blob ids: score.txt and unsafe-index.txt hold
one integer and a newline, so their git blob ids are decoded by hashing every small integer.
Freshness is checked by hand: search a value that only the newest merged submission has (run 24:
`repo:proximity-prize/proximity-prize 331407359` finds SubmissionLower/radius.txt from PR #615).

Run 36 added the toolchain line (lean-toolchain decoded the same way; v4.34.0 at the record, and
the open PR #674 would move prod to Lean 4.36 with the leaders ported) and the missing-file check
(a layout change could drop the two paths from the index without changing them).

Run 38 added the pin lines: the ArkLib and CompPoly revs of lake-manifest.json, read from the
search API's text-match fragments (34a834c / 411708c at the record). #674 merged on 2026-11-24
12:24:49 UTC (8689991c50), so a toolchain line still at v4.34.0 or these old revs mean the code
index has not caught up with that merge yet; the score lines are then pre-merge values.

Run 39 read the caught-up index (v4.36.0, ArkLib 151fd29, CompPoly cc71356; binary upper unchanged)
and marks the toolchain and pin lines against those values ([as in run 39] or [CHANGED since run 39]).
A pin move does not change the exit code: it matters only for a new Lean candidate.

Usage: python3 recheck_official.py [--since 2026-10-29] [--prs-since 2026-11-12]
Exit code 0 if SubmissionBinaryUpper is still 10624 / 917441, 1 if it changed, 2 on API errors,
3 if either file is missing from the code index (moved, renamed or deleted: read the PRs).
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import time

REPO = "proximity-prize/proximity-prize"
EXPECTED = {  # BitWonka, PR #592
    "ProximityPrize/SubmissionBinaryUpper/score.txt": "10624\n",
    "ProximityPrize/SubmissionBinaryUpper/unsafe-index.txt": "917441\n",
}
CURRENT = {  # prod toolchain and pins after PR #674, read from the index in run 39 (2026-11-25)
    "toolchain": "leanprover/lean4:v4.36.0",
    "Arklib": "151fd2944b7b7948d73e6d06cc738db5a5660aa0",
    "CompPoly": "cc71356a04fc45cb3efedadf09dd4fcf27f8fdc1",
}


def gh_search(kind, q, extra=(), text_match=False):
    cmd = ["gh", "api", "-X", "GET", f"search/{kind}", "-f", f"q={q}", "-f", "per_page=100"]
    if text_match:
        cmd += ["-H", "Accept: application/vnd.github.text-match+json"]
    for e in extra:
        cmd += ["-f", e]
    for attempt in range(4):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0:
            return json.loads(r.stdout)
        time.sleep(10 * (attempt + 1))
    print("API error:", q, r.stdout[:300], r.stderr[:300])
    sys.exit(2)


def blob_id(text):
    data = text.encode()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def decode(sha, limit=2_000_000):
    for n in range(limit):
        for body in (f"{n}\n", f"{n}"):
            if blob_id(body) == sha:
                return body
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-10-29")
    ap.add_argument("--prs-since", default="2026-11-12")
    a = ap.parse_args()

    c = gh_search("commits", f"repo:{REPO} committer-date:>{a.since}")
    print(f"commits on the default branch after {a.since}: {c['total_count']}")
    for it in c["items"]:
        cm = it["commit"]
        print("  ", it["sha"][:10], cm["committer"]["date"], (it.get("author") or {}).get("login"),
              "parents", [p["sha"][:10] for p in it["parents"]], cm["message"].splitlines()[0][:80])

    changed = False
    seen = set()
    for fname in ("score.txt", "unsafe-index.txt"):
        time.sleep(7)  # code search allows about 10 requests a minute
        r = gh_search("code", f"repo:{REPO} filename:{fname}")
        for it in sorted(r["items"], key=lambda x: x["path"]):
            body = decode(it["sha"])
            shown = repr(body) if body is not None else "not a small integer"
            mark = ""
            if it["path"] in EXPECTED:
                seen.add(it["path"])
                ok = it["sha"] == blob_id(EXPECTED[it["path"]])
                changed |= not ok
                mark = "  [binary upper: unchanged]" if ok else "  [binary upper: CHANGED]"
            print(f"  {it['path']}  {it['sha'][:10]}  {shown}{mark}")
    missing = sorted(set(EXPECTED) - seen)
    for path in missing:
        print(f"  {path}  MISSING from the code index")

    time.sleep(7)
    r = gh_search("code", f"repo:{REPO} filename:lean-toolchain")
    versions = [f"v4.{m}.{p}{rc}" for m in range(30, 45) for p in range(3)
                for rc in [""] + [f"-rc{i}" for i in range(1, 6)]]
    for it in sorted(r["items"], key=lambda x: x["path"]):
        body = next((s for v in versions for s in (f"leanprover/lean4:{v}\n", f"leanprover/lean4:{v}")
                     if blob_id(s) == it["sha"]), None)
        tag = "as in run 39" if body and body.strip() == CURRENT["toolchain"] else "CHANGED since run 39"
        print(f"  toolchain {it['path']}  {it['sha'][:10]}  {repr(body) if body else 'not decoded'}  [{tag}]")
    if not r["items"]:  # seen in run 38 while the index was re-reading the files #674 changed
        print(f"  toolchain: no item returned (total_count {r['total_count']}; index not caught up?)")

    for name in ("Arklib", "CompPoly"):  # the "name" field as lake-manifest.json spells it
        time.sleep(7)
        r = gh_search("code", f"repo:{REPO} filename:lake-manifest.json {name}", text_match=True)
        if not r["items"]:
            print(f"  pin {name}: no item returned (total_count {r['total_count']}; index not caught up?)")
        for it in sorted(r["items"], key=lambda x: x["path"]):
            revs = [m.group(1) for tm in it.get("text_matches", [])
                    for m in re.finditer(r'"rev":\s*"([0-9a-f]{7,40})",\s*"name":\s*"' + name + '"',
                                         tm.get("fragment", ""), re.I)]
            rev = revs[0] if revs else None
            tag = "as in run 39" if rev == CURRENT[name] else ("CHANGED since run 39" if rev else "unknown")
            print(f"  pin {name} {it['path']}  {it['sha'][:10]}  rev {rev or 'not in fragments'}  [{tag}]")

    p = gh_search("issues", f"repo:{REPO} is:pr")
    print(f"PRs in total: {p['total_count']}")
    p = gh_search("issues", f"repo:{REPO} is:pr updated:>{a.prs_since}")
    print(f"PRs updated after {a.prs_since}: {p['total_count']}")
    for it in sorted(p["items"], key=lambda x: x["number"]):
        print("  ", f"#{it['number']}", it["state"], "merged", (it.get("pull_request") or {}).get("merged_at"),
              it["updated_at"], it["title"][:100])
    i = gh_search("issues", f"repo:{REPO} is:issue updated:>{a.since}")
    print(f"issues updated after {a.since}: {i['total_count']}")

    if changed:
        print("BINARY UPPER CHANGED")
        sys.exit(1)
    if missing:
        print("BINARY UPPER FILES MISSING from the index (moved or renamed?): check the merged PRs")
        sys.exit(3)
    print("binary upper record unchanged: 10624 / 917441")
    sys.exit(0)


if __name__ == "__main__":
    main()
