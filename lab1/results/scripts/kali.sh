#!/usr/bin/env bash
# kali.sh -- CSF Lab Assignment I (Operation DeepFish, Stage I)
# Evidence-analysis script for evidence/fig1-000.png.
#
# Run this from the lab1 project root (the directory containing
# evidence/, results/, etc.) inside the Kali VM referenced in
# results/environment-and-tools.txt. It NEVER modifies the original
# evidence file: everything is read-only against evidence/, and all
# output is written under results/analysis/.
#
# Maps directly to CSF class material covered so far:
#   - csf2627-2-01-forensic_data_interpretation.pdf : structural
#     validation, magic numbers, "data after IEND", metadata chunks,
#     tool table (slide 23).
#   - csf2627-2-02-information_hiding_and_detection.pdf : LSB
#     steganography, bit-plane / visual steganalysis, PoV chi-square
#     statistical steganalysis.
#
# Each step's output is saved to its own file so it can be cited
# individually in the artifact register / report (per Tutorial 1
# Good-Practice Manual and the assignment's reproducibility
# requirements).

set -uo pipefail

EVIDENCE="${1:-evidence/fig1-000.png}"
OUTDIR="results/analysis"
SCRIPTDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -f "$EVIDENCE" ]; then
  echo "Evidence file not found: $EVIDENCE" >&2
  echo "Usage: $0 [path/to/file.png]" >&2
  exit 1
fi

mkdir -p "$OUTDIR"

echo "################################################################"
echo "# 0. Hash & basic identification (chain of custody)"
echo "################################################################"
sha256sum "$EVIDENCE" | tee "$OUTDIR/00_sha256.txt"
stat "$EVIDENCE" | tee "$OUTDIR/00_stat.txt"
file "$EVIDENCE" | tee "$OUTDIR/00_file.txt"

echo
echo "################################################################"
echo "# 1. Structural validation (chunk consistency, IEND, trailing data)"
echo "################################################################"
if command -v pngcheck >/dev/null 2>&1; then
  pngcheck -v -f "$EVIDENCE" | tee "$OUTDIR/01_pngcheck.txt"
else
  echo "pngcheck not installed (apt install pngcheck) -- skipping." | tee "$OUTDIR/01_pngcheck.txt"
fi

echo
echo "################################################################"
echo "# 2. Metadata inspection (EXIF / text chunks via exiftool)"
echo "################################################################"
if command -v exiftool >/dev/null 2>&1; then
  exiftool -a -u -g1 "$EVIDENCE" | tee "$OUTDIR/02_exiftool.txt"
else
  echo "exiftool not installed (apt install libimage-exiftool-perl) -- skipping." | tee "$OUTDIR/02_exiftool.txt"
fi

echo
echo "################################################################"
echo "# 3. Signature/embedded-object scan"
echo "################################################################"
if command -v binwalk >/dev/null 2>&1; then
  binwalk "$EVIDENCE" | tee "$OUTDIR/03_binwalk_scan.txt"
  mkdir -p "$OUTDIR/03_binwalk_extracted"
  binwalk -e --directory="$OUTDIR/03_binwalk_extracted" "$EVIDENCE" || true
else
  echo "binwalk not installed (apt install binwalk) -- skipping." | tee "$OUTDIR/03_binwalk_scan.txt"
fi

echo
echo "################################################################"
echo "# 4. Readable strings (ASCII + UTF-16LE, in case of encoded text)"
echo "################################################################"
strings -a -n 6 "$EVIDENCE" > "$OUTDIR/04_strings_ascii.txt"
strings -a -n 6 -e l "$EVIDENCE" > "$OUTDIR/04_strings_utf16.txt"
echo "ASCII strings: $(wc -l < "$OUTDIR/04_strings_ascii.txt") lines -> $OUTDIR/04_strings_ascii.txt"
echo "UTF-16LE strings: $(wc -l < "$OUTDIR/04_strings_utf16.txt") lines -> $OUTDIR/04_strings_utf16.txt"

echo
echo "################################################################"
echo "# 5. PNG chunk map (pure Python, catches anything the above miss)"
echo "################################################################"
python3 "$SCRIPTDIR/png_chunks.py" "$EVIDENCE" | tee "$OUTDIR/05_chunk_map.txt"

echo
echo "################################################################"
echo "# 6. Pixel-domain steganalysis: bit planes + PoV chi-square + LSB extraction"
echo "################################################################"
python3 "$SCRIPTDIR/lsb_analysis.py" "$EVIDENCE" "$OUTDIR" | tee "$OUTDIR/06_lsb_analysis.txt"

echo
echo "################################################################"
echo "# 7. Dedicated steganalysis tools, if installed"
echo "################################################################"
if command -v zsteg >/dev/null 2>&1; then
  zsteg -a "$EVIDENCE" | tee "$OUTDIR/07_zsteg.txt"
else
  echo "zsteg not installed (gem install zsteg) -- skipping." | tee "$OUTDIR/07_zsteg.txt"
fi
if command -v stegseek >/dev/null 2>&1; then
  echo "stegseek is available; run manually with a wordlist if steghide-style embedding is suspected." | tee -a "$OUTDIR/07_zsteg.txt"
fi

echo
echo "################################################################"
echo "Done. All outputs are under: $OUTDIR"
echo "Original evidence file was never modified (read-only access only)."
echo "################################################################"
