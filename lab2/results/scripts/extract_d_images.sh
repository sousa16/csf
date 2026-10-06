#!/usr/bin/env bash
# extract_d_images.sh -- recover the two note-part-3/5 photos from the
# BitLocker D: volume of windows_laptop_disk.dd, read-only.
#
# Pipeline (all read-only against the images):
#   1. recover the D: Full Volume Encryption Key from the live-memory capture
#      with the volatility3-bitlocker plugin (no user password needed: D: is an
#      auto-unlocked data volume, so its FVEK is resident in memory);
#   2. decrypt/mount D: with that key via dislocker + ntfs-3g;
#   3. copy out mom-photo.jpg (part 3) and hate-this-place.jpg (part 5) and
#      hash them, so the register path matches the recovered bytes.
#
# Run from the lab2 root (the dir holding images/ and results/) inside Kali,
# with network for the plugin clone and root for losetup/dislocker.
#
# usage: results/scripts/extract_d_images.sh
set -euo pipefail

DISK="images/windows_laptop_disk.dd"
MEM="images/windows_laptop_memory.raw"
D_OFFSET=21880635392                 # D: partition start, bytes (mmls sector 42735616 x 512)
PLUGDIR="results/work/plugins"
OUT="results/work/extract"
DISL=/mnt/dislocker
DVOL=/mnt/dvol

mkdir -p "$PLUGDIR/windows" "$OUT" results/analysis/bitlocker

# 1. FVEK from memory ---------------------------------------------------------
if [ ! -f "$PLUGDIR/windows/bitlocker.py" ]; then
    git clone https://github.com/lorelyai/volatility3-bitlocker results/work/vol3-bl
    cp results/work/vol3-bl/bitlocker.py "$PLUGDIR/windows/bitlocker.py"
fi
# writes 0x<offset>-Dislocker.fvek file(s); the complete AES-XTS pair is the
# 'None'-tagged candidate (the only one that also carries a tweak).
vol -vvv -p "$PLUGDIR" -f "$MEM" windows.bitlocker.BitlockerFVEKScan \
    --tags FVEc Cngb None --dislocker | tee results/analysis/bitlocker/run.log
FVEK_FILE=$(ls -1 0x*-Dislocker.fvek | tail -1)   # pick the last (None) candidate; adjust if needed
echo "[*] using FVEK file: $FVEK_FILE"

# 2. decrypt + mount D: read-only --------------------------------------------
sudo mkdir -p "$DISL" "$DVOL"
LOOP=$(sudo losetup -r -o "$D_OFFSET" --show -f "$DISK")
sudo dislocker -v -k "$FVEK_FILE" -V "$LOOP" "$DISL"
sudo mount -t ntfs-3g -o ro "$DISL/dislocker-file" "$DVOL"

# 3. copy out the two photos and hash them -----------------------------------
cp "$DVOL/Users/johnny/Pictures/mom-photo.jpg"       "$OUT/mom-photo.jpg"
cp "$DVOL/Users/johnny/Pictures/hate-this-place.jpg" "$OUT/hate-this-place.jpg"
sha256sum "$OUT/mom-photo.jpg" "$OUT/hate-this-place.jpg"
echo "[*] expected: fe8f99ce...be55 (mom-photo)  c323d401...c800c8 (hate-this-place)"
echo "[*] copy both into evidence/windows/ once the hashes check out."
