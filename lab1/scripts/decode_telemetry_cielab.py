#!/usr/bin/env python3
"""
decode_telemetry_cielab.py -- rebuild the concealed photograph from the
"telemetry" workbook (A026) using the colour-space key recovered from A031.

A026 is an .xlsx named for an ESP32/ADXL345 3-axis accelerometer, but its three
worksheets are each exactly 302 columns x 400 rows -- matching, cell for cell,
the 302x400 pixels of the recovered photograph (A027). The sheets are not sensor
readings: they are the CIELAB L*, a* and b* channels of an image.

The decode parameters are not guessed. They are stated explicitly in A031, a
meme image from the same commit that was edited to carry:

    cielab   L 70.04935   a 14.83618   b* -23.02163
    sRGB [0,1] - D65 - 2 degree observer
    #b2a4d5

That triple converts to exactly (178, 164, 213) = #b2a4d5 under D65 / 2-degree,
which is what makes the key self-validating. Run this script with --selftest to
check that conversion before trusting any output.

Sheet order: sheet1 = L*, sheet2 = a*, sheet3 = b*. Row r, column c of each
sheet is pixel (x = c-1, y = r-1).

Usage:
    python3 decode_telemetry_cielab.py Telemetry.xlsx --out photo.png
    python3 decode_telemetry_cielab.py --selftest
"""

from __future__ import annotations

import argparse
import re
import struct
import sys
import zipfile
import zlib

# D65 white point, 2 degree standard observer
Xn, Yn, Zn = 95.047, 100.000, 108.883

# sRGB (D65) XYZ -> linear RGB
M = ((3.2406, -1.5372, -0.4986),
     (-0.9689, 1.8758, 0.0415),
     (0.0557, -0.2040, 1.0570))


def f_inv(t: float) -> float:
    return t ** 3 if t ** 3 > 0.008856 else (t - 16.0 / 116.0) / 7.787


def gamma_encode(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def lab_to_rgb8(L: float, a: float, b: float) -> tuple[int, int, int]:
    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    X = Xn * f_inv(fx) / 100.0
    Y = Yn * f_inv(fy) / 100.0
    Z = Zn * f_inv(fz) / 100.0
    lin = [M[i][0] * X + M[i][1] * Y + M[i][2] * Z for i in range(3)]
    return tuple(int(round(gamma_encode(v) * 255)) for v in lin)


def selftest() -> int:
    """Validate against the known triple/hex pair stated in A031."""
    got = lab_to_rgb8(70.04935, 14.83618, -23.02163)
    hexs = "#%02x%02x%02x" % got
    print(f"A031 key: L 70.04935 a 14.83618 b* -23.02163  ->  {got}  {hexs}")
    print(f"A031 states #b2a4d5  ->  {'MATCH' if hexs == '#b2a4d5' else 'MISMATCH'}")
    return 0 if hexs == "#b2a4d5" else 1


def col_to_num(col: str) -> int:
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n


def load_sheet(xml: str) -> dict[tuple[int, int], float]:
    grid: dict[tuple[int, int], float] = {}
    for row_m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', xml, re.DOTALL):
        r = int(row_m.group(1))
        for c_m in re.finditer(r'<c r="([A-Z]+)\d+"[^>]*>\s*<v>([-0-9.eE]+)</v>', row_m.group(2)):
            grid[(r, col_to_num(c_m.group(1)))] = float(c_m.group(2))
    return grid


def write_png(path: str, w: int, h: int, pix: bytes) -> None:
    raw = bytearray()
    for y in range(h):
        raw.append(0)                      # filter type 0 (None) per scanline
        raw += pix[y * w * 3:(y + 1) * w * 3]

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("workbook", nargs="?", help="the .xlsx to decode (A026)")
    ap.add_argument("--out", help="PNG to write")
    ap.add_argument("--selftest", action="store_true",
                    help="verify the A031 key converts to its stated hex, then exit")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.workbook or not args.out:
        ap.error("workbook and --out are required (or use --selftest)")

    if selftest() != 0:
        print("key self-test failed; refusing to decode", file=sys.stderr)
        return 1

    with zipfile.ZipFile(args.workbook) as z:
        sheets = [load_sheet(z.read(f"xl/worksheets/sheet{i}.xml").decode("utf-8"))
                  for i in (1, 2, 3)]
    Lg, ag, bg = sheets
    H = max(r for r, _ in Lg)
    W = max(c for _, c in Lg)
    print(f"\nworksheets: {W} columns x {H} rows -> image {W}x{H}")

    pix = bytearray(W * H * 3)
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            r, g, b = lab_to_rgb8(Lg[(y, x)], ag[(y, x)], bg[(y, x)])
            o = ((y - 1) * W + (x - 1)) * 3
            pix[o], pix[o + 1], pix[o + 2] = r, g, b

    write_png(args.out, W, H, bytes(pix))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
