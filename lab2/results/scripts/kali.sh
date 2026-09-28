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

step="${1:-}"
[ $# -gt 0 ] && shift
case "$step" in
    hash)      step_hash ;;
    mem)       step_mem ;;
    layout)    step_layout "$@" ;;
    timeline)  step_timeline "$@" ;;
    hashmatch) step_hashmatch "$@" ;;
    *)         sed -n '2,29p' "${BASH_SOURCE[0]}"; [ -z "$step" ] && exit 1 || exit 0 ;;
esac
