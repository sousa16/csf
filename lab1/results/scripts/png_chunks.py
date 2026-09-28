#!/usr/bin/env python3
"""
png_chunks.py - Structural PNG chunk enumeration for forensic triage.

Parses a PNG byte-for-byte without relying on any image library, so it
will not silently "fix" or ignore anything a normal viewer would hide.

For each chunk reports: offset, type, declared length, whether the CRC32
matches, and (for text-bearing chunk types) a decoded preview.
Finally reports whether IEND is followed by any trailing bytes, since
data appended after IEND is invisible to normal viewers but not to a
hex dump (CSF 2-01, slide 20/27).

Usage: python3 png_chunks.py <file.png>
"""
import struct
import sys
import zlib

PNG_SIG = b"\x89PNG\r\n\x1a\n"

TEXT_CHUNK_TYPES = {b"tEXt", b"zTXt", b"iTXt"}


def decode_text_chunk(ctype: bytes, data: bytes) -> str:
    try:
        if ctype == b"tEXt":
            keyword, _, text = data.partition(b"\x00")
            return f"{keyword.decode('latin-1')} = {text.decode('latin-1')!r}"
        if ctype == b"zTXt":
            keyword, _, rest = data.partition(b"\x00")
            if not rest:
                return f"{keyword.decode('latin-1')} = <empty>"
            comp_method, comp_text = rest[0], rest[1:]
            text = zlib.decompress(comp_text)
            return f"{keyword.decode('latin-1')} (zlib) = {text.decode('latin-1', 'replace')!r}"
        if ctype == b"iTXt":
            keyword, _, rest = data.partition(b"\x00")
            comp_flag, comp_method = rest[0], rest[1]
            rest = rest[2:]
            lang, _, rest = rest.partition(b"\x00")
            trkeyword, _, rest = rest.partition(b"\x00")
            text = rest
            if comp_flag:
                text = zlib.decompress(text)
            return f"{keyword.decode('latin-1')} (lang={lang!r}) = {text.decode('utf-8', 'replace')!r}"
    except Exception as e:
        return f"<failed to decode: {e}>"
    return ""


def main(path: str) -> None:
    with open(path, "rb") as f:
        raw = f.read()

    filesize = len(raw)
    print(f"File: {path}")
    print(f"Total file size: {filesize} bytes")

    if raw[:8] != PNG_SIG:
        print("ERROR: file does not start with the PNG signature 89 50 4E 47 0D 0A 1A 0A")
        sys.exit(1)

    offset = 8
    idat_total = 0
    chunk_count = 0
    iend_end_offset = None

    print(f"{'offset':>8} {'type':>6} {'length':>10} {'crc_ok':>7}  preview")
    print("-" * 70)

    while offset < filesize:
        if offset + 8 > filesize:
            print(f"WARNING: truncated chunk header at offset {offset}")
            break

        length = struct.unpack(">I", raw[offset : offset + 4])[0]
        ctype = raw[offset + 4 : offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        crc_off = data_end
        crc_end = crc_off + 4

        if crc_end > filesize:
            print(f"WARNING: chunk {ctype!r} at {offset} claims length {length} "
                  f"but runs past end of file (needs byte {crc_end}, file is {filesize})")
            break

        data = raw[data_start:data_end]
        stored_crc = struct.unpack(">I", raw[crc_off:crc_end])[0]
        computed_crc = zlib.crc32(ctype + data) & 0xFFFFFFFF
        crc_ok = "yes" if stored_crc == computed_crc else "NO <-- mismatch"

        preview = ""
        if ctype == b"IHDR":
            w, h, bitdepth, colortype, comp, filt, interlace = struct.unpack(
                ">IIBBBBB", data
            )
            preview = (
                f"{w}x{h} bitdepth={bitdepth} colortype={colortype} "
                f"compression={comp} filter={filt} interlace={interlace}"
            )
        elif ctype == b"IDAT":
            idat_total += length
            preview = f"(compressed image data segment #{sum(1 for _ in [1])})"
        elif ctype in TEXT_CHUNK_TYPES:
            preview = decode_text_chunk(ctype, data)
        elif ctype == b"tIME":
            if len(data) == 7:
                y, mo, d, h, mi, s = struct.unpack(">HBBBBB", data)
                preview = f"{y:04d}-{mo:02d}-{d:02d} {h:02d}:{mi:02d}:{s:02d} (from tIME chunk)"
        elif ctype == b"eXIf":
            preview = f"EXIF blob, {length} bytes (inspect separately, e.g. with exiftool)"
        elif ctype == b"IEND":
            preview = "end-of-image marker"

        print(f"{offset:>8} {ctype.decode('latin-1', 'replace'):>6} {length:>10} {crc_ok:>7}  {preview}")

        chunk_count += 1
        offset = crc_end

        if ctype == b"IEND":
            iend_end_offset = offset
            break

    print("-" * 70)
    print(f"Chunks parsed: {chunk_count}")
    print(f"Total IDAT payload bytes: {idat_total}")

    if iend_end_offset is None:
        print("IEND chunk was never reached -- file may be truncated or non-standard.")
    else:
        trailing = filesize - iend_end_offset
        print(f"IEND chunk ends at byte offset {iend_end_offset} (of {filesize} total).")
        if trailing > 0:
            print(f"*** {trailing} bytes found AFTER IEND -- not part of the PNG format, "
                  f"invisible to normal viewers. Extract and inspect separately. ***")
            with open(path, "rb") as f:
                f.seek(iend_end_offset)
                tail = f.read()
            out_path = path + ".trailing_after_iend.bin"
            with open(out_path, "wb") as out:
                out.write(tail)
            print(f"Trailing bytes written to: {out_path}")
        else:
            print("No trailing bytes after IEND: file ends exactly at the PNG's own end marker.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.png>")
        sys.exit(2)
    main(sys.argv[1])
