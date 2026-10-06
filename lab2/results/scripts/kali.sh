#!/usr/bin/env bash
# kali.sh -- CSF Lab Assignment II (Operation DeepFish, Stage II)
#
# Analysis commands for the Stage II evidence. Run from the lab2 root (the
# directory containing images/, evidence/, results/) inside the Kali container:
#
#     ./kali.sh shell          # from labs/project, then: cd lab2
#     results/scripts/kali.sh <step> [args]
#
# Read-only against images/ and evidence/. Every step writes its own file under
# results/analysis/ so the output can be cited individually in the artifact
# register and report. Steps whose tool or input is missing say so and carry
# on -- a missing tool is a finding to record, not a reason to stop.
#
# Steps:
#   hash                       SHA-256 of the images (chain of custody), verified
#                              against images/SHA256SUMS if one is present
#   mem                        Volatility 3 baseline on the Windows memory image
#   layout <image>             mmls + fsstat for every partition of a disk image
#   timeline <image> <offset> <tag>
#                              TSK body file + mactime CSV for one filesystem
#   hashmatch <dir>            hash every file under <dir>, report any that match
#                              the 16 Stage I hashes (lab1-hashes.sha256)
#   bl-scan                    Volatility BitLocker FVEK scan of the memory image
#                              (third-party plugin, staged + SHA-256 checked)
#   bl-verify <fvek-hex>       check a key decrypts the D: volume header and $MFT;
#                              the key is saved to results/work/fvek-D.hex (0600)
#   creds                      Volatility hashdump (SAM) + cached domain creds
#                              (LSA secrets) from the memory image -> results/analysis/creds/
#   hives                      extract SAM/SYSTEM/SECURITY/SOFTWARE from the C: NTFS
#                              partition (sector 239616) and run offline secretsdump
#   note-pw <zip>              test the handwritten note's ZIP password candidates
#   linux-extract <path...>    extract files from the Linux image (ext4, sector
#                              2203648) by path into results/work/linux/, read-only
#   bl-decrypt                 decrypt the whole D: partition to results/work/
#                              (needs bl-verify first; ~5.6 GB, gitignored)
#
# Timestamps: the Linux image is treated as created 2026-08-24, so every
# absolute timestamp found in it gets -27 days in the report and timeline. This
# script keeps raw values (UTC) and never shifts them; apply the offset and
# state it in the timeline row, not here.

set -uo pipefail

IMAGES="images"
OUT="results/analysis"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEM="$IMAGES/windows_laptop_memory.raw"
WIN="$IMAGES/windows_laptop_disk.dd"
LIN="$IMAGES/linux_workstation_disk.dd"

mkdir -p "$OUT"

have() { command -v "$1" >/dev/null 2>&1 || { echo "not installed: $1 (skipping)" >&2; return 1; }; }
need_file() { [ -f "$1" ] || { echo "missing: $1 (skipping)" >&2; return 1; }; }

step_hash() {
    local f
    : > "$OUT/00_image_hashes.txt"
    for f in "$MEM" "$WIN" "$LIN"; do
        need_file "$f" || continue
        sha256sum "$f" | tee -a "$OUT/00_image_hashes.txt"
    done
    if [ -f "$IMAGES/SHA256SUMS" ]; then
        echo "--- verifying against $IMAGES/SHA256SUMS" | tee -a "$OUT/00_image_hashes.txt"
        (cd "$IMAGES" && sha256sum -c SHA256SUMS) 2>&1 | tee -a "$OUT/00_image_hashes.txt"
    else
        echo "no $IMAGES/SHA256SUMS -- record the hashes above before analysing" >&2
    fi
}

step_mem() {
    need_file "$MEM" && have vol || return 0
    mkdir -p "$OUT/mem"
    local n=0 p
    # windows.info first: the Windows version decides which BitLocker key
    # pool tag to look for. The first run builds the symbol cache and is slow.
    for p in windows.info windows.pslist windows.pstree windows.cmdline \
             windows.psscan windows.malfind windows.netscan windows.filescan \
             windows.registry.hivelist windows.registry.userassist \
             windows.envars windows.handles; do
        n=$((n + 1))
        printf '%s %s\n' "$(date -u +%FT%TZ)" "$p"
        vol -q -f "$MEM" "$p" > "$OUT/mem/$(printf '%02d' "$n")_$p.txt" 2> "$OUT/mem/$(printf '%02d' "$n")_$p.err" \
            || echo "  $p failed -- see .err" >&2
    done
}

step_layout() {
    local img="${1:?layout: needs a disk image}"
    need_file "$img" && have mmls || return 0
    local base; base="$(basename "$img" .dd)"
    mmls "$img" | tee "$OUT/10_${base}_mmls.txt"
    # Feed every allocated slice's start sector to fsstat. A BitLocker volume
    # has no readable filesystem until it is decrypted -- fsstat failing on it
    # is expected, and worth recording as such.
    # Slot is "000:000" (DOS) or "000" (GPT); Meta and Unallocated rows have a
    # non-numeric second field and fall out.
    awk '$2 ~ /^[0-9]+(:[0-9]+)?$/ && $3 ~ /^[0-9]+$/ {print $3}' \
        "$OUT/10_${base}_mmls.txt" | sed 's/^0*\([0-9]\)/\1/' | while read -r start; do
        echo "--- fsstat -o $start"
        fsstat -o "$start" "$img" 2>&1 | tee "$OUT/11_${base}_fsstat_$start.txt" | head -12
    done
}

step_timeline() {
    local img="${1:?timeline: needs image}" off="${2:?timeline: needs sector offset}" tag="${3:?timeline: needs a tag}"
    need_file "$img" && have fls && have mactime || return 0
    fls -r -m / -o "$off" "$img" > "$OUT/20_${tag}.body" 2> "$OUT/20_${tag}.err"
    mactime -b "$OUT/20_${tag}.body" -z UTC -d > "$OUT/20_${tag}_timeline.csv"
    wc -l "$OUT/20_${tag}.body" "$OUT/20_${tag}_timeline.csv"
}

step_hashmatch() {
    local dir="${1:?hashmatch: needs a directory}"
    [ -d "$dir" ] || { echo "not a directory: $dir" >&2; return 1; }
    local ref="$HERE/lab1-hashes.sha256"
    find "$dir" -type f -print0 | xargs -0 sha256sum > "$OUT/30_hashes_$(basename "$dir").txt"
    # Match on the hash alone: the seized systems may hold these files under
    # any name.
    # sha256sum prints "<64 hex>  <path>"; take the path as the rest of the
    # line so names containing spaces survive.
    awk 'NR==FNR { if ($1 !~ /^#/) ref[$1] = $2; next } ($1 in ref) { print "MATCH  " ref[$1] "  <-  " substr($0, 67) }' \
        "$ref" "$OUT/30_hashes_$(basename "$dir").txt" | tee "$OUT/30_matches_$(basename "$dir").txt"
    echo "matches: $(wc -l < "$OUT/30_matches_$(basename "$dir").txt")"
}

# --- BitLocker (D: = partition at sector 42735616, 11788288 sectors) ---
D_START=42735616
D_SECTORS=11788288
PLUGIN_SHA="1cda3c680e665898051dba1f9a638c42a4a711b65da74c8539995ad543a7ffb7"
BL_PY="$HERE/bitlocker.py"
KEYFILE="results/work/fvek-D.hex"

step_bl_scan() {
    need_file "$MEM" && have vol || return 0
    echo "$PLUGIN_SHA  results/work/plugins/windows/bitlocker.py" | sha256sum -c - >/dev/null \
        || { echo "plugin hash mismatch -- refusing to run" >&2; return 1; }
    mkdir -p "$OUT/bitlocker"
    vol -vv -p results/work/plugins -o "$OUT/bitlocker" -f "$MEM" \
        windows.bitlocker.BitlockerFVEKScan --tags FVEc Cngb None \
        > "$OUT/bitlocker/run.log" 2>&1
    tr -d '\000' < "$OUT/bitlocker/run.log" | grep -E '\[FVEK\] (Address|Cipher|FVEK)'
}

step_bl_verify() {
    local key="${1:?bl-verify: needs the FVEK hex}"
    need_file "$WIN" || return 0
    mkdir -p results/work
    ( umask 077; printf '%s\n' "$key" > "$KEYFILE" )
    python3 "$BL_PY" verify "$WIN" "$D_START" "$key" | tee "$OUT/40_bl_verify.txt"
}

step_bl_decrypt() {
    need_file "$WIN" && [ -f "$KEYFILE" ] || { echo "run bl-verify first" >&2; return 1; }
    python3 "$BL_PY" decrypt "$WIN" "$D_START" "$D_SECTORS" "$(cat "$KEYFILE")" results/work/D-decrypted.raw
}

step_creds() {
    need_file "$MEM" && have vol || return 0
    mkdir -p "$OUT/creds"
    # These plugins read registry hives out of memory, so they run on the image only.
    # Output contains password hashes/secrets: gitignored, never committed.
    for p in windows.registry.hivelist windows.hashdump windows.cachedump windows.lsadump; do
        vol -q -f "$MEM" "$p" > "$OUT/creds/${p}.txt" 2> "$OUT/creds/${p}.err" || echo "  $p failed -- see .err" >&2
    done
}

step_hives() {
    need_file "$WIN" && have impacket-secretsdump || return 0
    local o=239616 h=results/work/hives name ino
    mkdir -p "$h" "$OUT/creds"
    for name in SAM SYSTEM SECURITY SOFTWARE; do
        ino=$(fls -o "$o" -r -p "$WIN" 2>/dev/null | awk -v n="Windows/System32/config/$name" -F'\t' '$2==n {print $1}' | awk '{print $2}' | cut -d- -f1)
        [ -n "$ino" ] && icat -o "$o" "$WIN" "$ino" > "$h/$name"
    done
    sha256sum "$h"/SAM "$h"/SYSTEM "$h"/SECURITY "$h"/SOFTWARE | tee "$OUT/creds/hive_hashes.txt"
    impacket-secretsdump -sam "$h/SAM" -system "$h/SYSTEM" -security "$h/SECURITY" LOCAL \
        2>&1 | tee "$OUT/creds/secretsdump_offline.txt"
}

step_note_pw() {
    local z="${1:?note-pw: needs a zip under results/work/}"
    mkdir -p "$OUT/zip"
    python3 "$HERE/note_password.py" "$z" | tee "$OUT/zip/note_pw_$(basename "$z").txt"
}

LIN_START=2203648
step_linux_extract() {
    need_file "$LIN" || return 0
    local list="$OUT/linux_fls_${LIN_START}.txt" dst="results/work/linux" p ino base
    [ -f "$list" ] || fls -r -p -o "$LIN_START" "$LIN" > "$list" 2>/dev/null
    mkdir -p "$dst"
    for p in "$@"; do
        # fls -p lines look like "r/r 954731:<TAB>path" (ext4: no -128 suffix)
        ino=$(awk -F'\t' -v n="$p" '$2==n {print $1}' "$list" | head -1 | awk '{print $2}' | tr -d ':' | cut -d- -f1)
        if [ -z "$ino" ]; then echo "not found: $p" >&2; continue; fi
        base="$(echo "$p" | sed 's#/#__#g')"
        icat -o "$LIN_START" "$LIN" "$ino" > "$dst/$base" || { echo "icat failed: $p" >&2; continue; }
        echo "$(sha256sum "$dst/$base" | cut -c1-64)  $p (inode $ino)"
    done
}

step="${1:-}"
[ $# -gt 0 ] && shift
case "$step" in
    hash)      step_hash ;;
    mem)       step_mem ;;
    layout)    step_layout "$@" ;;
    timeline)  step_timeline "$@" ;;
    hashmatch) step_hashmatch "$@" ;;
    creds)      step_creds ;;
    linux-extract) step_linux_extract "$@" ;;
    hives)      step_hives ;;
    note-pw)    step_note_pw "$@" ;;
    bl-scan)    step_bl_scan ;;
    bl-verify)  step_bl_verify "$@" ;;
    bl-decrypt) step_bl_decrypt ;;
    *)         sed -n '2,44p' "${BASH_SOURCE[0]}"; [ -z "$step" ] && exit 1 || exit 0 ;;
esac
