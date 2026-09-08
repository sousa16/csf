#!/usr/bin/env bash
# Good-Practice Manual §1 -- record the analysis environment.
#
# Run this first, inside the container, at the start of every lab session.
# Tutorial 1 is explicit that a missing tool must be recorded as an error
# rather than filled in from another machine, so this deliberately does not
# fail on a missing command.
#
#   usage: scripts/forensic-env.sh [results-dir]     (default: ./results)
set -uo pipefail

RESULTS="${1:-results}"
mkdir -p "$RESULTS"
OUT="$RESULTS/environment-and-tools.txt"

{
    date --utc --iso-8601=seconds
    grep '^PRETTY_NAME=' /etc/os-release
    uname -a
    locale
    for probe in \
        "sha256sum --version" "stat --version" "file --version" \
        "strings --version" "unzip -v" "python3 --version" \
        "exiftool -ver" "binwalk --help" "fls -V" "xxd -v"
    do
        # shellcheck disable=SC2086
        $probe 2>&1 | head -n 1 || echo "$probe: UNAVAILABLE"
    done
    john --list=build-info 2>&1 | head -n 4 || echo "john: UNAVAILABLE"
} | tee "$OUT"

echo
echo "--- digest of the record itself (§1) ---"
sha256sum "$OUT"
