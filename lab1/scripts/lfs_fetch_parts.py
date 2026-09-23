#!/usr/bin/env python3
"""
lfs_fetch_parts.py -- fetch Git-LFS objects by OID, verify, and reassemble.

The attacker's repository (A012) tracks its large media through Git LFS, so a
`git-dumper` of the exposed .git directory recovers only 135-byte pointer files:

    version https://git-lfs.github.com/spec/v1
    oid sha256:<oid>
    size <bytes>

The bytes themselves are served as static files under the same host at
    /.git/lfs/objects/<oid[0:2]>/<oid[2:4]>/<oid>

This script takes a parts.json manifest (as committed alongside the split
artifact), fetches every part by that URL scheme, verifies each part's SHA-256
against the manifest, concatenates them in manifest order, and verifies the
SHA-256 of the reassembled whole.

Only GET requests are issued; nothing is written to the remote host.

Usage:
    python3 lfs_fetch_parts.py parts.json --base https://host/.git/lfs/objects \\
        --out-dir ./parts --assemble video.mkv
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

CHUNK = 1 << 20  # 1 MiB streaming chunk; parts are GB-scale


def lfs_url(base: str, oid: str) -> str:
    return f"{base.rstrip('/')}/{oid[0:2]}/{oid[2:4]}/{oid}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def fetch(url: str, dest: Path, expect_size: int | None = None) -> None:
    """Stream a URL to disk, hashing as we go so nothing is held in memory."""
    with urllib.request.urlopen(url) as resp, dest.open("wb") as out:
        got = 0
        while True:
            block = resp.read(CHUNK)
            if not block:
                break
            out.write(block)
            got += len(block)
            if expect_size:
                pct = 100.0 * got / expect_size
                print(f"\r    {got:,}/{expect_size:,} bytes ({pct:5.1f}%)", end="", flush=True)
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", help="parts.json recovered from the repository")
    ap.add_argument("--base", required=True,
                    help="LFS object base URL, e.g. https://host/.git/lfs/objects")
    ap.add_argument("--out-dir", default=".", help="where to write the fetched parts")
    ap.add_argument("--assemble", help="path to write the reassembled file")
    ap.add_argument("--skip-existing", action="store_true",
                    help="keep already-downloaded parts whose hash already matches")
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text())
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Manifest order is authoritative: reassembly must follow declared offsets.
    files = sorted(manifest["files"], key=lambda f: f["offset"])
    local: list[Path] = []
    ok = True

    for i, spec in enumerate(files, 1):
        oid, size = spec["sha256"], spec["size"]
        dest = out_dir / f"part{i:02d}"
        local.append(dest)

        if args.skip_existing and dest.exists() and dest.stat().st_size == size:
            if sha256_file(dest) == oid:
                print(f"[{i}/{len(files)}] {dest.name}: already present and verified")
                continue

        url = lfs_url(args.base, oid)
        print(f"[{i}/{len(files)}] GET {url}")
        fetch(url, dest, size)

        actual = sha256_file(dest)
        if actual == oid:
            print(f"    SHA-256 OK  {actual}")
        else:
            ok = False
            print(f"    SHA-256 MISMATCH\n      got      {actual}\n      expected {oid}")

    if not args.assemble:
        return 0 if ok else 1

    target = Path(args.assemble)
    print(f"\nreassembling {len(local)} parts -> {target}")
    with target.open("wb") as out:
        for part in local:
            with part.open("rb") as fh:
                for block in iter(lambda: fh.read(CHUNK), b""):
                    out.write(block)

    actual = sha256_file(target)
    expected = manifest.get("sha256")
    print(f"    size     {target.stat().st_size:,} (manifest: {manifest.get('size', '?'):,})")
    print(f"    SHA-256  {actual}")
    if expected:
        print(f"    expected {expected}")
        if actual != expected:
            print("    *** REASSEMBLED HASH DOES NOT MATCH MANIFEST ***")
            ok = False
        else:
            print("    reassembled file verified against manifest")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
