#!/usr/bin/env python3
"""
video_lsb_extract.py -- recover a payload hidden in the LSBs of fixed pixel
positions across the frames of a losslessly-encoded RGB video.

Why this works on this particular artifact
------------------------------------------
A normal anime rip is encoded with chroma subsampling (yuv420p), which throws
away colour detail and destroys any per-pixel LSB signal. The video recovered
here is instead libx264rgb / "High 4:4:4 Predictive" / gbrp -- lossless, full
RGB, no subsampling. That is a very unusual choice for a media file and is what
makes a per-pixel LSB channel survive encoding intact; the encoding choice is
itself an indicator of deliberate concealment.

Channel layout
--------------
Per frame, one bit is read from the LSB of each of ROWS x COLS positions, in
each of the three colour channels:

  * for each channel in (R, G, B):
      for each row y in ROWS:
          one byte, built from the 8 columns left-to-right, most significant
          bit first

  => len(ROWS) bytes per channel, x3 channels = 12 bytes per frame.

Framing
-------
The recovered byte stream starts with an 8-byte big-endian length header giving
the payload size; total stream length is therefore header + 8. Bytes after the
header are the payload, written out verbatim.

Usage:
    python3 video_lsb_extract.py video.mkv --out payload.webp
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Fixed sampling grid (32 positions per channel).
ROWS = [60, 180, 300, 420]
COLS = [53, 159, 266, 373, 480, 586, 693, 800]

HEADER_LEN = 8
BYTES_PER_FRAME = len(ROWS) * 3  # one byte per row, per channel

MAGICS = {
    b"RIFF": "WebP/RIFF container",
    b"\x89PNG": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"GIF8": "GIF",
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP",
}


def probe_dimensions(path: Path) -> tuple[int, int, str]:
    """Return (width, height, pix_fmt) for the first video stream."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,pix_fmt,codec_name",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    stream = json.loads(out)["streams"][0]
    print(f"  codec={stream.get('codec_name')} pix_fmt={stream.get('pix_fmt')} "
          f"{stream['width']}x{stream['height']}")
    return stream["width"], stream["height"], stream.get("pix_fmt", "")


def extract_frame_bytes(buf: bytes, width: int) -> bytes:
    """Pull BYTES_PER_FRAME bytes out of one rgb24 frame."""
    out = bytearray()
    for channel in range(3):  # 0=R, 1=G, 2=B in rgb24
        for y in ROWS:
            byte = 0
            for x in COLS:
                bit = buf[(y * width + x) * 3 + channel] & 1
                byte = (byte << 1) | bit  # MSB first
            out.append(byte)
    return bytes(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--out", required=True, help="where to write the recovered payload")
    ap.add_argument("--max-frames", type=int, default=0,
                    help="stop after N frames (0 = no limit); useful for a quick probe")
    ap.add_argument("--crop", action="store_true",
                    help="decode only the top-left region that contains the sampling grid. "
                         "Purely an I/O optimisation: the crop is anchored at (0,0) so every "
                         "sampled coordinate keeps its original value.")
    args = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("ffmpeg/ffprobe not found on PATH", file=sys.stderr)
        return 2

    video = Path(args.video)
    print(f"probing {video}")
    width, height, pix_fmt = probe_dimensions(video)
    if "444" not in pix_fmt and "rgb" not in pix_fmt.lower() and "gbr" not in pix_fmt.lower():
        print(f"  WARNING: pix_fmt {pix_fmt!r} looks subsampled; LSBs may not survive")

    for y in ROWS:
        if y >= height:
            print(f"row {y} outside frame height {height}", file=sys.stderr)
            return 2
    for x in COLS:
        if x >= width:
            print(f"column {x} outside frame width {width}", file=sys.stderr)
            return 2

    dec_w, dec_h = width, height
    cmd = ["ffmpeg", "-v", "error", "-i", str(video)]
    if args.crop:
        # Anchored at (0,0) so sampled coordinates are unchanged.
        dec_w = min(width, max(COLS) + 1)
        dec_h = min(height, max(ROWS) + 1)
        cmd += ["-vf", f"crop={dec_w}:{dec_h}:0:0"]
        print(f"  crop enabled: decoding {dec_w}x{dec_h} instead of {width}x{height} "
              f"({width * height / (dec_w * dec_h):.2f}x less pixel data)")
    cmd += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]

    frame_size = dec_w * dec_h * 3
    width = dec_w  # row stride for indexing follows the decoded frame
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    data = bytearray()
    total_needed: int | None = None
    frames = 0

    assert proc.stdout is not None
    while True:
        buf = proc.stdout.read(frame_size)
        if len(buf) < frame_size:
            break  # EOF or truncated trailing frame
        frames += 1
        data += extract_frame_bytes(buf, width)

        if total_needed is None and len(data) >= HEADER_LEN:
            payload_len = int.from_bytes(data[:HEADER_LEN], "big")
            total_needed = payload_len + HEADER_LEN
            print(f"  header: payload {payload_len:,} bytes "
                  f"(total {total_needed:,}, ~{total_needed / BYTES_PER_FRAME:,.0f} frames)")
            if payload_len <= 0 or payload_len > 1 << 31:
                print("  header implausible -- wrong grid, wrong channel order, or no payload",
                      file=sys.stderr)
                proc.kill()
                return 1

        if total_needed is not None and len(data) >= total_needed:
            break
        if args.max_frames and frames >= args.max_frames:
            break
        if frames % 500 == 0:
            got = len(data)
            pct = f" ({100.0 * got / total_needed:5.1f}%)" if total_needed else ""
            print(f"\r  frame {frames:,}  {got:,} bytes{pct}", end="", flush=True)

    print(f"\n  read {frames:,} frames, {len(data):,} bytes recovered")
    proc.kill()
    proc.wait()

    if total_needed is None:
        print("never recovered a full header", file=sys.stderr)
        return 1
    if len(data) < total_needed:
        print(f"INCOMPLETE: got {len(data):,} of {total_needed:,} bytes "
              f"-- video ended early or payload spans more frames", file=sys.stderr)
        return 1

    payload = bytes(data[HEADER_LEN:total_needed])
    Path(args.out).write_bytes(payload)
    print(f"wrote {args.out} ({len(payload):,} bytes)")

    head = payload[:4]
    for magic, name in MAGICS.items():
        if payload.startswith(magic):
            extra = ""
            if magic == b"RIFF" and payload[8:12] == b"WEBP":
                extra = " (WEBP)"
            print(f"  magic: {name}{extra} -- looks valid")
            break
    else:
        print(f"  magic: unrecognised ({head!r}) -- check grid/order assumptions")

    import hashlib
    print(f"  sha256: {hashlib.sha256(payload).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
