#!/usr/bin/env python3
"""
image_steg_check.py -- in-band steganalysis of a single JPEG, used to decide
whether the note's part-3 / part-5 words are hidden inside the two images
recovered from the BitLocker D: volume (mom-photo.jpg, hate-this-place.jpg)
or whether they are only established by recognising the depicted scene/place.

It performs, with the standard library (plus Pillow if present for the LSB
pass), the cheap-to-expensive checks that the course covers for raster
information hiding:

  1. JPEG marker walk: report any COM (0xFFFE) comment and the APP1 EXIF /
     XMP block, printed as text -- a word stored in metadata shows here.
  2. Trailing bytes after the final End-Of-Image (0xFFD9): a polyglot or an
     appended archive lives here.
  3. Spatial-domain LSB: Pillow-decode to RGB and try the class-baseline
     embedding (16-bit big-endian length header then payload) over the
     common channel / bit orders, and scan the raw LSB stream for the
     candidate words.

It does NOT cover transform-domain tools (steghide, outguess, jsteg): run
those separately on the file -- e.g.

    steghide info <img>;  stegseek <img> rockyou.txt
    outguess -r <img> out.txt;  jsteg reveal <img> out.txt

and record their result too. A clean run of all of the above is a negative
finding (Good-Practice Manual Sec. 5): the word is not embedded, and part 3 /
part 5 rest on recognising the image plus the stash.zip password oracle
(see decode_note_parts.py).

Usage: python3 image_steg_check.py <image.jpg> [word ...]
"""
import struct
import sys

DEFAULT_WORDS = ["shibuya", "pimenta", "jujutsu", "maria", "gojo", "elliot", "blue"]


def walk_markers(data):
    """Yield (name, segment_bytes) for COM and APP markers; stop at SOS."""
    i = 2
    while i < len(data) - 1:
        if data[i] != 0xFF:
            i += 1
            continue
        m = data[i + 1]
        if m == 0xD9 or m == 0xD8 or 0xD0 <= m <= 0xD7 or m == 0x01:
            i += 2
            continue
        if i + 4 > len(data):
            break
        ln = struct.unpack(">H", data[i + 2:i + 4])[0]
        seg = data[i + 4:i + 2 + ln]
        name = {0xFE: "COM", 0xE0: "APP0", 0xE1: "APP1(EXIF/XMP)",
                0xED: "APP13(IPTC)", 0xEE: "APP14"}.get(m, f"marker_{m:02X}")
        yield name, seg
        if m == 0xDA:  # start of scan
            break
        i += 2 + ln


def printable(b, n=400):
    return bytes(c if 32 <= c < 127 else 0x2E for c in b[:n])


def check_metadata_and_trailer(data):
    print("  [1] markers (COM / APP):")
    any_text = False
    for name, seg in walk_markers(data):
        if name in ("COM", "APP1(EXIF/XMP)", "APP13(IPTC)"):
            any_text = True
            print(f"      {name} len={len(seg)} -> {printable(seg, 200)!r}")
    if not any_text:
        print("      (no COM/EXIF/IPTC text segments)")
    last = data.rfind(b"\xff\xd9")
    trail = data[last + 2:] if last != -1 else b""
    print(f"  [2] bytes after final FFD9: {len(trail)}")
    if trail:
        print(f"      head: {printable(trail, 200)!r}")
        print(f"      hex : {trail[:32].hex()}")


def check_lsb(path, words):
    try:
        import warnings
        warnings.filterwarnings("ignore")
        from PIL import Image
    except ImportError:
        print("  [3] spatial-LSB: Pillow not installed, skipped")
        return
    im = Image.open(path).convert("RGB")
    px = list(im.getdata())
    chans = {"R": 0, "G": 1, "B": 2}

    def to_bytes(bits):
        out = bytearray()
        for k in range(0, len(bits) - 7, 8):
            v = 0
            for j in range(8):
                v = (v << 1) | bits[k + j]
            out.append(v)
        return bytes(out)

    hit = False
    for order in ("RGB", "BGR", "GRB", "R", "G", "B"):
        if len(order) == 1:
            seq = [p[chans[order]] & 1 for p in px]
        else:
            seq = [px[k][chans[c]] & 1 for k in range(len(px)) for c in order]
        if len(seq) < 16:
            continue
        ln = 0
        for b in seq[:16]:
            ln = (ln << 1) | b
        if 0 < ln < 5000:
            payload = to_bytes(seq[16:16 + ln * 8])
            if payload and sum(32 <= c < 127 for c in payload) > 0.8 * len(payload):
                print(f"  [3] LSB[{order}] 16b-header len={ln}: {payload[:120]!r}")
                hit = True
        raw = to_bytes(seq[:8000]).lower()
        for w in words:
            if w.encode() in raw:
                print(f"  [3] LSB[{order}] word {w!r} present in LSB stream")
                hit = True
    if not hit:
        print("  [3] spatial-LSB: no payload (class-baseline scheme, all orders)")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    words = sys.argv[2:] or DEFAULT_WORDS
    data = open(path, "rb").read()
    print(f"== {path}  ({len(data)} bytes)")
    check_metadata_and_trailer(data)
    check_lsb(path, words)


if __name__ == "__main__":
    main()
