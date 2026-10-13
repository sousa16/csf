#!/usr/bin/env python3
"""Extract the file parts of a multipart/form-data request body.

Works on HTTP objects exported by tshark/Wireshark (File > Export Objects >
HTTP), e.g. Mattermost POST /api/v4/files or ChatGPT POST /backend-api/files.
Each part with a filename is written to <out_dir>/<filename> byte-exact, and
its size and SHA-256 are printed.

usage: multipart_extract.py <exported body> <out_dir>
"""
import hashlib
import os
import re
import sys


def main():
    body = open(sys.argv[1], "rb").read()
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    boundary = body.split(b"\r\n", 1)[0]
    if not boundary.startswith(b"--"):
        sys.exit("body does not start with a multipart boundary")
    for part in body.split(boundary)[1:]:
        if part.startswith(b"--"):
            break
        head, _, data = part.partition(b"\r\n\r\n")
        data = data[:-2] if data.endswith(b"\r\n") else data
        m = re.search(rb'filename="([^"]+)"', head)
        if not m:
            name = re.search(rb'name="([^"]+)"', head)
            print("field", name.group(1).decode() if name else "?", "=", data[:80])
            continue
        fname = os.path.basename(m.group(1).decode())
        path = os.path.join(out_dir, fname)
        with open(path, "wb") as f:
            f.write(data)
        print(f"{hashlib.sha256(data).hexdigest()}  {len(data):>8}  {path}")


if __name__ == "__main__":
    main()
