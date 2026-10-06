#!/usr/bin/env python3
# note_password.py -- test the handwritten note's ZIP password recipe.
#
# The note reads  sha256{p1_p2_p3_p4_p5}  (lowercase, parts joined with '_'):
#   p1 laptop name              johnny-pc        verified (memory COMPUTERNAME)
#   p2 wallpaper first name     elliot           candidate (wallpaper caption)
#   p3 JJK picture region       shibuya          candidate (unverified)
#   p4 Windows password         fsociety         verified (SAM NT hash)
#   p5 restaurant               pimenta          candidate (unverified)
# The separator is read from the note as '_' or '-'; both are tried.
#
# The ZIP is only opened, never written to: the candidate that opens amelia.pdf
# is the one that matches. Only the candidates below are tried.
#
# usage: note_password.py <zip> [<member>]

import hashlib
import itertools
import sys
import zipfile
import zlib

P1 = ["johnny-pc", "johnnypc"]
P2 = ["elliot", "eren", "robot", "alderson", "mr-robot", "mrrobot"]
P3 = ["shibuya", "shibuya-ku", "tokyo", "japan"]
P4 = ["fsociety"]
P5 = ["pimenta", "maria-pimenta", "maria_pimenta", "mariapimenta", "povoa",
      "feira-de-povoa", "feira-da-povoa", "polvora", "maria-pimenta-povoa"]
SEPARATORS = ["_", "-", ""]


def main():
    zpath = sys.argv[1]
    member = sys.argv[2] if len(sys.argv) > 2 else None
    with zipfile.ZipFile(zpath) as z:
        # Directory entries and unencrypted files read back with no password at all,
        # so only an encrypted file entry can tell a right password from a wrong one.
        encrypted = [i.filename for i in z.infolist() if i.flag_bits & 1 and not i.is_dir()]
        if not encrypted:
            sys.exit("no encrypted file entries in this archive")
        member = member or encrypted[0]
        hits = 0
        for parts, sep in itertools.product(itertools.product(P1, P2, P3, P4, P5), SEPARATORS):
            s = sep.join(parts)
            pw = hashlib.sha256(s.encode()).hexdigest().encode()
            try:
                z.read(member, pwd=pw)
            # ZipCrypto's one-byte check lets ~1 in 256 wrong passwords through to
            # zlib, which then fails. A right password passes the CRC check in read().
            except (RuntimeError, zipfile.BadZipFile, NotImplementedError, zlib.error):
                continue
            hits += 1
            print(f"MATCH  parts={s!r}  sha256={pw.decode()}  member={member}")
        n = len(P1) * len(P2) * len(P3) * len(P4) * len(P5) * len(SEPARATORS)
        print(f"tried {n} candidates, matches={hits}")


if __name__ == "__main__":
    main()
