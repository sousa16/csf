#!/usr/bin/env python3
"""
decode_note_parts.py -- recover note parts 3 (JJK picture region) and 5
(restaurant) by using the recovered stash.zip as a ground-truth oracle.

The handwritten note (Figure 1) is a ZIP password:

    sha256{ p1 _ p2 _ p3 _ p4 _ p5 }   (all lowercase, parts joined with '_')

Three parts are fixed from independent evidence and are NOT guessed here:
    p1 = johnny-pc   laptop name           (memory COMPUTERNAME / SYSTEM hive)
    p2 = elliot      wallpaper first name  (D: TranscodedWallpaper, Mr. Robot)
    p4 = fsociety    Windows password      (SAM NT hash fb06de73..2934 / LSA)

Parts 3 and 5 are read from the two images recovered from the D: volume:
    p3 <- mom-photo.jpg      an anime train-platform scene = Jujutsu Kaisen
                             "Shibuya Incident" (Shibuya Station) -> 'shibuya'
    p5 <- hate-this-place.jpg a yellow terrace restaurant = "Maria Pimenta"
                             at the Fabrica da Polvora de Barcarena -> 'pimenta'

Those two readings are hypotheses from recognising the images (no payload is
hidden in them -- see image_steg_check.py). This script PROVES them: it builds
the sha256 recipe for every candidate (p3, p5) pair and tries it against the
ZipCrypto-encrypted stash.zip. The one pair whose hash opens the archive is
the correct one, so the images' interpretation is confirmed cryptographically
rather than asserted.

The ZIP is only read, never modified.

Usage: python3 decode_note_parts.py <stash.zip> [member]
"""
import hashlib
import itertools
import sys
import zipfile
import zlib

P1 = ["johnny-pc"]
P2 = ["elliot"]
P4 = ["fsociety"]
# candidate readings of the two images (the correct one is confirmed below)
P3 = ["shibuya", "shinjuku", "tokyo", "kyoto", "japan"]
P5 = ["pimenta", "maria-pimenta", "mariapimenta", "maria_pimenta", "polvora",
      "barcarena"]
SEPARATORS = ["_", "-"]


def recipe(parts, sep):
    s = sep.join(parts).lower()
    return s, hashlib.sha256(s.encode()).hexdigest()


def opens(zf, member, pw):
    try:
        zf.read(member, pwd=pw.encode())
        return True
    except (RuntimeError, zipfile.BadZipFile, NotImplementedError, zlib.error):
        return False


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    zpath = sys.argv[1]
    with zipfile.ZipFile(zpath) as zf:
        # Only an encrypted *file* entry distinguishes a right password from a
        # wrong one (directory and stored entries read back with no password).
        enc = [i for i in zf.infolist() if (i.flag_bits & 1) and not i.is_dir()]
        if not enc:
            sys.exit("no encrypted file entries in this archive")
        member = sys.argv[2] if len(sys.argv) > 2 else enc[0].filename
        tried = matches = 0
        for parts, sep in itertools.product(
                itertools.product(P1, P2, P3, P4, P5), SEPARATORS):
            tried += 1
            s, h = recipe(parts, sep)
            if opens(zf, member, h):
                matches += 1
                print(f"[+] MATCH  parts(3,5)=({parts[2]!r},{parts[4]!r})")
                print(f"           string = {s}")
                print(f"           sha256 = {h}")
                print(f"           member = {member}")
        print(f"\ntried {tried} candidates against {zpath}, matches={matches}")
        if matches == 1:
            print("parts 3 and 5 are uniquely confirmed by the archive.")


if __name__ == "__main__":
    main()
