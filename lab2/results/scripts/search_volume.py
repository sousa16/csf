#!/usr/bin/env python3
# search_volume.py -- keyword search over a whole (decrypted) volume, including
# unallocated space. Read-only. Prints each hit with its byte offset and the
# sector it falls in, so `ifind -d <sector>` can map it back to a file.
#
# usage: search_volume.py <image> <term> [<term> ...]
#   terms match case-insensitively in ASCII and UTF-16LE.

import re
import sys

CHUNK = 64 * 1024 * 1024
OVERLAP = 256  # longest term + margin, so matches across chunk edges are kept


def patterns(term):
    t = term.encode()
    w = term.encode("utf-16le")
    return [re.compile(re.escape(t), re.I), re.compile(re.escape(w), re.I)]


def main():
    img, terms = sys.argv[1], sys.argv[2:]
    if not terms:
        sys.exit(__doc__)
    pats = [(t, p) for t in terms for p in patterns(t)]
    seen = set()
    with open(img, "rb") as f:
        base = 0
        tail = b""
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            buf = tail + chunk
            for term, p in pats:
                for m in p.finditer(buf):
                    off = base - len(tail) + m.start()
                    key = (term, off)
                    if key in seen:
                        continue
                    seen.add(key)
                    ctx = buf[max(0, m.start() - 24): m.end() + 24]
                    ctx = re.sub(rb"[^\x20-\x7e]", b".", ctx).decode()
                    print(f"{term!r:14} offset={off:#x} sector={off // 512} ctx={ctx}")
            tail = buf[-OVERLAP:]
            base += len(chunk)
    print(f"done, {len(seen)} hits")


if __name__ == "__main__":
    main()
