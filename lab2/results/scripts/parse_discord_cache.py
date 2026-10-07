#!/usr/bin/env python3
"""
parse_discord_cache.py -- decode and read the Discord client HTTP cache
recovered from the D: volume (A157).

Discord's desktop client stores fetched API responses under
  AppData/Roaming/discord/Cache/Cache_Data/f_00000N
as gzip-compressed bodies (one blob per cached response), plus the occasional
media body (e.g. an Ogg/Opus voice note). The message bodies are JSON arrays of
message objects. This script decompresses the gzip blobs, loads the JSON, and
prints every message sorted by timestamp as  [time] author  content.

Recover the blobs from a LOCAL copy of the image (the hgfs-backed dislocker
mount returns them as 0 bytes):
    DC=/mnt/dvol2/Users/johnny/AppData/Roaming/discord/Cache/Cache_Data
    cp "$DC"/f_* blobs/ ; file blobs/f_* ; sha256sum blobs/f_*
    for f in blobs/f_*; do gzip -cd "$f" > json/$(basename "$f").json 2>/dev/null; done
    python3 parse_discord_cache.py json/*.json > discord-messages.txt
A blob that `file` reports as audio (Ogg/Opus) is a voice note, not gzip JSON;
inspect it with ffprobe/ffplay instead.

Usage: python3 parse_discord_cache.py <decoded-json> [<decoded-json> ...]
"""
import json
import sys


def load_messages(paths):
    msgs = []
    for fn in paths:
        try:
            data = json.load(open(fn, errors="replace"))
        except Exception as e:
            print(f"# skip {fn}: {e}", file=sys.stderr)
            continue
        for m in (data if isinstance(data, list) else [data]):
            if isinstance(m, dict) and "content" in m:
                m["_src"] = fn.split("/")[-1]
                msgs.append(m)
    msgs.sort(key=lambda m: m.get("timestamp", ""))
    return msgs


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    msgs = load_messages(sys.argv[1:])
    for m in msgs:
        author = m.get("author", {}).get("username", "?")
        print(f"\n[{m.get('timestamp', '?')}] {author}  ({m['_src']})")
        print(m.get("content", ""))
        for att in m.get("attachments", []):
            print("  ATTACH:", att.get("filename"))
    print(f"\n--- total messages: {len(msgs)} ---")


if __name__ == "__main__":
    main()
