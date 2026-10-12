#!/usr/bin/env python3
"""Print decrypted HTTP/1.x requests and responses, with bodies, in frame order.

usage: http_dump.py <trace.pcapng> <tls.keys> '<display filter>' [max_body_chars]

The filter is ANDed with "http". Response frames carry the generated
http.request.uri of their request (tshark 4.x), so one filter on the URI
selects both directions. TLS on 8080 and 8443 is decoded as TLS
(sigma04 and the 10.10.14.15 file service do not use port 443). Times are UTC.
Request headers are printed so that tokens/headers used are visible; pipe the
output through a redaction step before committing anything derived from it.
"""
import subprocess
import sys
from datetime import datetime, timezone

FIELDS = ["frame.number", "frame.time_epoch", "ip.src", "ip.dst", "tcp.stream",
          "http.request.method", "http.request.uri", "http.response.code",
          "http.request.line", "http.file_data"]


def main():
    pcap, keys, dfilter = sys.argv[1], sys.argv[2], sys.argv[3]
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 4000
    cmd = ["tshark", "-r", pcap, "-o", f"tls.keylog_file:{keys}",
           "-d", "tcp.port==8080,tls", "-d", "tcp.port==8443,tls",
           "-Y", f"http && ({dfilter})", "-T", "fields",
           "-E", "separator=\t", "-E", "occurrence=a", "-E", "aggregator=|"]
    for f in FIELDS:
        cmd += ["-e", f]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        row = dict(zip(FIELDS, line.split("\t")))
        when = datetime.fromtimestamp(float(row["frame.time_epoch"]), timezone.utc)
        head = (f"--- frame {row['frame.number']}  {when:%Y-%m-%d %H:%M:%S}Z  "
                f"{row['ip.src']} -> {row['ip.dst']}  stream {row['tcp.stream']}  ")
        if row["http.request.method"]:
            head += f"{row['http.request.method']} {row['http.request.uri']}"
        else:
            head += f"RESPONSE {row['http.response.code']} for {row['http.request.uri']}"
        print(head)
        if row["http.request.line"]:
            for h in row["http.request.line"].split("|"):
                print("    >", h.replace("\\r\\n", "").strip())
        body = row["http.file_data"]
        if body:
            try:
                text = bytes.fromhex(body.replace(":", "")).decode("utf-8", "replace")
            except ValueError:
                text = body
            print("    " + text[:limit].replace("\n", "\n    "))
        print()


if __name__ == "__main__":
    main()
