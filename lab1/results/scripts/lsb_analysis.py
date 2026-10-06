#!/usr/bin/env python3
"""
lsb_analysis.py - Pixel-domain steganalysis for a PNG, using only the
Python standard library (zlib + struct), so it runs identically on a
bare Kali box with no extra pip packages.

Implements, per CSF 2-02 (Information Hiding and Detection):
  - Manual PNG decode: concatenate IDAT, zlib-inflate, and undo the
    per-scanline filters (slide: "A file format gives structure to
    the bytes").
  - Bit-plane extraction per channel, written out as viewable PGM
    images (slide 17: "Visual steganalysis: inspect channels and bit
    planes" -- LSB plane of a natural image should look like noise).
  - LSB histogram / Pairs-of-Values chi-square statistic (slide
    38-39: "Statistical attacks to LSB embedding" -- natural images
    have uneven even/odd value counts; embedding pushes them toward
    50/50, i.e. lowers this chi-square statistic).
  - Sequential-LSB extraction attempt assuming the baseline embedding
    algorithm taught in class (slide 29: 16-bit size header followed
    by payload), tried on a few common bit/channel orders.

Only supports 8-bit-depth, non-interlaced, colour type 2 (truecolor)
or 6 (truecolor+alpha) PNGs -- prints a clear error otherwise rather
than guessing.

Usage: python3 lsb_analysis.py <file.png> <outdir>
"""
import struct
import sys
import zlib
from pathlib import Path

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png(path):
    raw = Path(path).read_bytes()
    assert raw[:8] == PNG_SIG, "not a PNG file"
    offset = 8
    idat = bytearray()
    ihdr = None
    while offset < len(raw):
        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        ctype = raw[offset + 4 : offset + 8]
        data = raw[offset + 8 : offset + 8 + length]
        if ctype == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", data)
        elif ctype == b"IDAT":
            idat += data
        elif ctype == b"IEND":
            break
        offset += 8 + length + 4
    return ihdr, bytes(idat)


def defilter(width, height, bpp, decompressed):
    stride = width * bpp
    recon = bytearray(stride * height)
    pos = 0
    for y in range(height):
        filt = decompressed[pos]
        pos += 1
        row = decompressed[pos : pos + stride]
        pos += stride
        row_start = y * stride
        prev_row_start = (y - 1) * stride
        for x in range(stride):
            raw_byte = row[x]
            a = recon[row_start + x - bpp] if x >= bpp else 0
            b = recon[prev_row_start + x] if y > 0 else 0
            c = recon[prev_row_start + x - bpp] if (y > 0 and x >= bpp) else 0
            if filt == 0:
                val = raw_byte
            elif filt == 1:
                val = (raw_byte + a) & 0xFF
            elif filt == 2:
                val = (raw_byte + b) & 0xFF
            elif filt == 3:
                val = (raw_byte + ((a + b) >> 1)) & 0xFF
            elif filt == 4:
                val = (raw_byte + paeth(a, b, c)) & 0xFF
            else:
                raise ValueError(f"unknown filter type {filt} at row {y}")
            recon[row_start + x] = val
    return bytes(recon)


def write_pgm(path, width, height, pixels_1bpp_scaled):
    with open(path, "wb") as f:
        f.write(f"P5\n{width} {height}\n255\n".encode("ascii"))
        f.write(pixels_1bpp_scaled)


def bit_plane(channel_bytes, bit_index):
    return bytes(255 if (b >> bit_index) & 1 else 0 for b in channel_bytes)


def pov_chi_square(channel_bytes):
    """Pairs-of-Values chi-square statistic (CSF 2-02 slide 38-39).
    Natural images: uneven counts between value 2k and 2k+1.
    LSB-embedded images: counts for each pair converge -> low chi-square.
    """
    hist = [0] * 256
    for b in channel_bytes:
        hist[b] += 1
    chi2 = 0.0
    pairs = 0
    for k in range(128):
        n0, n1 = hist[2 * k], hist[2 * k + 1]
        total = n0 + n1
        if total == 0:
            continue
        expected = total / 2.0
        chi2 += ((n0 - expected) ** 2) / expected + ((n1 - expected) ** 2) / expected
        pairs += 1
    return chi2, pairs


def even_odd_lsb_ratio(channel_bytes):
    ones = sum(b & 1 for b in channel_bytes)
    total = len(channel_bytes)
    return ones, total, ones / total if total else 0.0


MAGIC_NUMBERS = {
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"PK\x03\x04": "ZIP/DOCX/etc.",
    b"%PDF": "PDF",
    b"\x1f\x8b": "GZIP",
    b"BM": "BMP",
    b"GIF8": "GIF",
    b"7z\xbc\xaf\x27\x1c": "7-Zip",
    b"Rar!": "RAR",
}


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    ent = 0.0
    for c in counts:
        if c:
            p = c / n
            ent -= p * (p.bit_length() - 1 if False else __import__("math").log2(p))
    return ent


def printable_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    printable = sum(1 for b in data if 32 <= b < 127 or b in (9, 10, 13))
    return printable / len(data)


def bits_to_bytes(bits):
    payload = bytearray()
    for i in range(0, len(bits) - (len(bits) % 8), 8):
        byte = 0
        for bit in bits[i : i + 8]:
            byte = (byte << 1) | bit
        payload.append(byte)
    return bytes(payload)


def try_extract_header(bits, label, results):
    """Assume the class baseline: first 16 bits = big-endian payload
    length in bytes, followed by that many bytes of payload (CSF 2-02
    slide 29). We don't just check the size is 'plausible' (on an
    image this size almost ANY 16-bit value is smaller than capacity,
    so that check alone proves nothing) -- we extract the claimed
    payload regardless and test it against known file signatures,
    entropy, and printable-text ratio, which are much stronger signals."""
    if len(bits) < 16:
        return
    size_bits = bits[:16]
    size = 0
    for bit in size_bits:
        size = (size << 1) | bit
    max_payload_bytes = (len(bits) - 16) // 8
    fits = 0 < size <= max_payload_bytes
    results.append(f"{label}: 16-bit header = {size} bytes (capacity={max_payload_bytes}, fits={fits})")

    # Always dump a small prefix of the raw LSB stream itself (header-agnostic),
    # in case the real embedding doesn't use this header convention at all.
    prefix_len = min(4096, max_payload_bytes)
    prefix_bytes = bits_to_bytes(bits[16 : 16 + prefix_len * 8])
    magic_hit = next((name for sig, name in MAGIC_NUMBERS.items() if prefix_bytes.startswith(sig)), None)
    ent = shannon_entropy(prefix_bytes[:2048])
    pr = printable_ratio(prefix_bytes[:2048])
    results.append(
        f"  first {len(prefix_bytes)} bytes after header: "
        f"magic={magic_hit or 'none recognized'}, entropy={ent:.2f} bits/byte "
        f"(8.0=random/encrypted/compressed, ~4-5=typical text/code), "
        f"printable_ratio={pr:.2f}"
    )
    out_path = Path(sys.argv[2]) / f"extracted_{label.replace(' ', '_').replace('/', '-')}.bin"
    out_path.write_bytes(prefix_bytes)
    results.append(f"  -> first {len(prefix_bytes)} bytes written to {out_path} for manual inspection")


def main():
    path = sys.argv[1]
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)

    ihdr, idat = read_png(path)
    width, height, bitdepth, colortype, comp, filt, interlace = ihdr
    print(f"IHDR: {width}x{height} bitdepth={bitdepth} colortype={colortype} interlace={interlace}")

    if bitdepth != 8 or interlace != 0 or colortype not in (2, 6):
        print("This script only supports 8-bit non-interlaced truecolor(+alpha) PNGs. "
              "Adjust bpp/handling before trusting results.")
        sys.exit(1)

    bpp = 3 if colortype == 2 else 4
    decompressed = zlib.decompress(idat)
    pixels = defilter(width, height, bpp, decompressed)
    print(f"Decoded {len(pixels)} raw pixel-component bytes "
          f"(expected {width*height*bpp}).")

    # Split interleaved RGB(A) into per-channel byte sequences (raster order)
    channels = {}
    names = ["R", "G", "B", "A"][:bpp]
    for i, name in enumerate(names):
        channels[name] = pixels[i::bpp]

    print("\n=== Even/odd LSB balance per channel ===")
    for name, chan in channels.items():
        ones, total, ratio = even_odd_lsb_ratio(chan)
        print(f"  {name}: {ones}/{total} pixels have LSB=1  (ratio={ratio:.4f}; "
              f"0.5 = perfectly balanced, natural photos are usually NOT this close to 0.5)")

    print("\n=== Pairs-of-Values chi-square (CSF 2-02 slide 38-39) ===")
    print("  Lower chi-square (closer to 0) => more consistent with LSB embedding.")
    print("  Higher chi-square => more consistent with an unmodified natural image.")
    for name, chan in channels.items():
        chi2, pairs = pov_chi_square(chan)
        print(f"  {name}: chi2={chi2:.1f} over {pairs} value-pairs "
              f"(chi2/pair={chi2/pairs:.3f})")

    print("\n=== Writing LSB bit-plane images (visual inspection) ===")
    for name, chan in channels.items():
        plane = bit_plane(chan, 0)
        out_path = outdir / f"bitplane_LSB_{name}.pgm"
        write_pgm(out_path, width, height, plane)
        print(f"  {name} LSB plane -> {out_path}")
    # Also plane 7 (MSB) of one channel as a sanity check -- should look like the real image
    msb_plane = bit_plane(channels[names[0]], 7)
    write_pgm(outdir / f"bitplane_MSB_{names[0]}_sanity_check.pgm", width, height, msb_plane)

    print("\n=== Attempting sequential-LSB extraction (class baseline algorithm) ===")
    results = []

    def bits_of(chan):
        return [b & 1 for b in chan]

    # Order 1: R,G,B interleaved per pixel (raster order), as in the class RGB example
    interleaved_bits = [pixels[i] & 1 for i in range(len(pixels))]
    try_extract_header(interleaved_bits, "RGB interleaved LSB", results)

    # Order 2: each channel separately, sequential
    for name, chan in channels.items():
        try_extract_header(bits_of(chan), f"{name} channel only LSB", results)

    for line in results:
        print(" ", line)

    print(f"\nAll outputs written under: {outdir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file.png> <outdir>")
        sys.exit(2)
    main()
