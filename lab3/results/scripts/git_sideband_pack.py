#!/usr/bin/env python3
"""Extract the packfile from a git smart-HTTP upload-pack response body.

The response is a sequence of pkt-lines (4 hex digits of length, including the
4 themselves; "0000" is a flush). With side-band-64k, pack bytes travel on band
1 (first payload byte 0x01); band 2 is progress text, band 3 an error. ACK/NAK
lines before the pack are printed so the negotiation is visible.

usage: git_sideband_pack.py <upload-pack response body> <out.pack>
"""
import sys


def main():
    data = open(sys.argv[1], "rb").read()
    pack = bytearray()
    i = 0
    while i + 4 <= len(data):
        n = int(data[i:i + 4], 16)
        if n == 0:
            i += 4
            continue
        payload = data[i + 4:i + n]
        i += n
        if payload[:1] == b"\x01":
            pack += payload[1:]
        elif payload[:1] in (b"\x02", b"\x03"):
            print("band", payload[0], payload[1:].decode(errors="replace").strip())
        else:
            print("pkt:", payload.decode(errors="replace").strip())
    open(sys.argv[2], "wb").write(pack)
    print(f"pack: {len(pack)} bytes, signature {bytes(pack[:4])!r}")


if __name__ == "__main__":
    main()
