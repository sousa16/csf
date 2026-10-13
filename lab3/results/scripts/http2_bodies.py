#!/usr/bin/env python3
"""Reassemble HTTP/2 request/response bodies from a decrypted capture.

tshark exposes HTTP/2 header fields on the HEADERS frame and the payload on the
DATA frames, which are different packets. This joins them by (tcp.stream,
http2.streamid): for each stream it records the method/path/status seen on any
frame and concatenates every DATA frame's bytes in frame order, then gunzips if
needed. Prints a filterable "frame<TAB>method<TAB>authority<TAB>path<TAB>status
<TAB>body" line per stream. Ports 8080/8443 are decoded as TLS for completeness.

usage: http2_bodies.py <trace.pcapng> <tls.keys> ['path substring filter']
"""
import gzip
import subprocess
import sys
import zlib

FIELDS = ["frame.number", "tcp.stream", "http2.streamid", "http2.headers.method",
          "http2.headers.authority", "http2.headers.path", "http2.headers.status",
          "http2.data.data"]


def run(pcap, keys):
    cmd = ["tshark", "-r", pcap, "-o", f"tls.keylog_file:{keys}",
           "-d", "tcp.port==8080,tls", "-d", "tcp.port==8443,tls",
           "-Y", "http2", "-T", "fields", "-E", "separator=|"]
    for f in FIELDS:
        cmd += ["-e", f]
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def main():
    pcap, keys = sys.argv[1], sys.argv[2]
    needle = sys.argv[3] if len(sys.argv) > 3 else ""
    streams = {}
    for line in run(pcap, keys).splitlines():
        p = (line.split("|") + [""] * len(FIELDS))[:len(FIELDS)]
        frame, stream, sid, method, auth, path, status, data = p
        # A frame may carry two streamids (e.g. "3,3"); take the first.
        sid = sid.split(",")[0]
        if not sid:
            continue
        key = (stream, sid)
        s = streams.setdefault(key, dict(frame=frame, method="", auth="", path="",
                                         status="", data=bytearray()))
        for name, val in (("method", method), ("auth", auth), ("path", path),
                          ("status", status)):
            v = val.split(",")[0]
            if v and not s[name]:
                s[name] = v
        if data:
            for chunk in data.split(","):
                if chunk:
                    s["data"] += bytes.fromhex(chunk)

    for (stream, sid), s in sorted(streams.items(), key=lambda kv: int(kv[1]["frame"])):
        if needle and needle not in s["path"]:
            continue
        body = bytes(s["data"])
        if body[:2] == b"\x1f\x8b":
            try:
                body = gzip.decompress(body)
            except Exception:
                pass
        elif body[:1] == b"\x78":
            try:
                body = zlib.decompress(body)
            except Exception:
                pass
        text = body.decode("utf-8", "replace")
        print(f"frame {s['frame']}\t{s['method']}\t{s['auth']}\t{s['path']}\t"
              f"{s['status']}\t{text}")


if __name__ == "__main__":
    main()
