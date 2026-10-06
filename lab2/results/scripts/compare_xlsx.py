#!/usr/bin/env python3
# compare_xlsx.py -- compare two .xlsx files cell by cell, from the raw XML.
# Read-only. Reports numeric differences above a tolerance, non-numeric
# differences, and document properties (created / modified / creator).
#
# usage: compare_xlsx.py <a.xlsx> <b.xlsx> [tolerance]

import re
import sys
import zipfile

CELL = r'<c r="([A-Z]+[0-9]+)"[^>]*?>(?:<f>[^<]*</f>)?<v>([^<]*)</v>'


def cells(z, sheet):
    return dict(re.findall(CELL, z.read(sheet).decode()))


def props(z):
    x = z.read("docProps/core.xml").decode()
    out = {}
    for tag in ("dc:creator", "dcterms:created", "dcterms:modified"):
        m = re.search(rf"<{tag}[^>]*>([^<]*)</{tag}>", x)
        out[tag] = m.group(1) if m else ""
    return out


def main():
    a, b = sys.argv[1], sys.argv[2]
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-9
    za, zb = zipfile.ZipFile(a), zipfile.ZipFile(b)
    sheets = sorted(n for n in za.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
    print(f"A: {a}\nB: {b}\ntolerance (relative) = {tol}")
    for k in ("dc:creator", "dcterms:created", "dcterms:modified"):
        print(f"props {k}: A={props(za)[k]!r} B={props(zb)[k]!r}")
    for sh in sheets:
        ca, cb = cells(za, sh), cells(zb, sh)
        worst, material, nonnum = 0.0, [], []
        for ref in ca:
            x, y = ca[ref], cb.get(ref)
            try:
                fx, fy = float(x), float(y)
                rel = abs(fx - fy) / max(1e-12, abs(fx))
                worst = max(worst, rel)
                if rel > tol:
                    material.append((ref, x, y))
            except (TypeError, ValueError):
                if x != y:
                    nonnum.append((ref, x, y))
        print(f"{sh}: cells={len(ca)}/{len(cb)} max_rel_diff={worst:.3g} "
              f"material={len(material)} nonnumeric={len(nonnum)}")
        for row in (material + nonnum)[:10]:
            print("   ", row)


if __name__ == "__main__":
    main()
