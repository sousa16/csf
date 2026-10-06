#!/usr/bin/env python3
# bitlocker.py -- BitLocker helpers for the Stage II Windows laptop disk.
#
# Called from kali.sh (bl-verify, bl-decrypt). Read-only against the evidence
# image: the decrypted copy is written to results/work/, which is gitignored.
#
# Facts this relies on, all checked against the image (see the analysis log):
#   - D: is the partition at sector 42735616 (11788288 sectors), signature -FVE-FS-
#   - FVE metadata block 1 is at partition+0x4bdd000; its plaintext header holds
#     the offset of the volume header (the original NTFS boot sector + 8 KB) at
#     metadata+0x38 = 0x47dd000
#   - The FVEK (AES-XTS-128: 16-byte key + 16-byte tweak key, 32 bytes total)
#     decrypts the volume header and the $MFT record; the tweak is the
#     volume-relative sector index (little-endian, 16 bytes)
#
# usage:
#   bitlocker.py verify  <image> <part_sector> <fvek_hex>
#   bitlocker.py decrypt <image> <part_sector> <part_sectors> <fvek_hex> <out.raw>

import struct
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

SECTOR = 512
HEADER_OFFSET = 0x47DD000   # from FVE metadata block 1, +0x38
HEADER_SIZE = 8 * 1024      # volume header: 16 sectors


def xts_sector(key, sector_index, data):
    c = Cipher(algorithms.AES(key), modes.XTS(sector_index.to_bytes(16, "little")))
    d = c.decryptor()
    return d.update(data) + d.finalize()


def read_part(img, part_start, off, n):
    with open(img, "rb") as f:
        f.seek(part_start * SECTOR + off)
        return f.read(n)


def verify(img, part_start, key):
    hdr = read_part(img, part_start, HEADER_OFFSET, SECTOR)
    boot = xts_sector(key, HEADER_OFFSET // SECTOR, hdr)
    ok_boot = boot[3:11] == b"NTFS    " and boot[510:512] == b"\x55\xaa"
    print(f"volume header sector: {boot[:11].hex()} NTFS boot OK={ok_boot}")
    if not ok_boot:
        return False
    bps, spc = struct.unpack_from("<H", boot, 0x0B)[0], boot[0x0D]
    mft_lcn = struct.unpack_from("<Q", boot, 0x30)[0]
    mft_off = mft_lcn * spc * bps
    rec = xts_sector(key, mft_off // SECTOR, read_part(img, part_start, mft_off, SECTOR))
    ok_mft = rec[:4] == b"FILE"
    print(f"bytes/sector={bps} sectors/cluster={spc} $MFT LCN={mft_lcn} record[:4]={rec[:4]!r} OK={ok_mft}")
    return ok_mft


def decrypt(img, part_start, part_sectors, key, out):
    # Each sector is its own XTS unit; the tweak is the volume-relative index.
    with open(img, "rb") as src, open(out, "wb") as dst:
        src.seek(part_start * SECTOR)
        for i in range(part_sectors):
            enc = src.read(SECTOR)
            if len(enc) < SECTOR:
                break
            dst.write(xts_sector(key, i, enc))
            if i and i % 2_000_000 == 0:
                print(f"  {i} / {part_sectors} sectors", file=sys.stderr)
    # The first 8 KB are the volume header, which is not the on-disk data
    # mapping: put the decrypted original boot sector and header in place.
    with open(img, "rb") as src, open(out, "r+b") as dst:
        hdr = b""
        src.seek(part_start * SECTOR + HEADER_OFFSET)
        for i in range(HEADER_SIZE // SECTOR):
            hdr += xts_sector(key, HEADER_OFFSET // SECTOR + i, src.read(SECTOR))
        dst.seek(0)
        dst.write(hdr)
    print(f"wrote {out}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "verify":
        _, _, img, start, keyhex = sys.argv
        sys.exit(0 if verify(img, int(start), bytes.fromhex(keyhex)) else 1)
    elif cmd == "decrypt":
        _, _, img, start, count, keyhex, out = sys.argv
        decrypt(img, int(start), int(count), bytes.fromhex(keyhex), out)
    else:
        print(__doc__)
        sys.exit(2)
