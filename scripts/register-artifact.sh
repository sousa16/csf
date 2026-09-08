#!/usr/bin/env bash
# Good-Practice Manual §3/§4 -- register an artifact and hash it.
#
# Appends one record to results/artifact-register.md with the fields the
# tutorial requires: identifier, path, parent, command, timestamp, size, type
# and SHA-256. Observations and interpretation are left blank on purpose --
# §6 wants those written by hand, and separately from each other.
#
#   usage: scripts/register-artifact.sh <ID> <artifact> [parent-ID] [command...]
#   e.g.:  scripts/register-artifact.sh A006 results/schedule.pdf A001 base64 -d broken.pdf
set -euo pipefail

ID="${1:?artifact id required, e.g. A001}"
ARTIFACT="${2:?artifact path required}"
PARENT="${3:--}"
shift 3 2>/dev/null || shift $#
COMMAND="${*:--}"

[ -e "$ARTIFACT" ] || { echo "no such artifact: $ARTIFACT" >&2; exit 1; }

REGISTER="$(dirname "$ARTIFACT")/../results/artifact-register.md"
[ -d results ] && REGISTER=results/artifact-register.md
mkdir -p "$(dirname "$REGISTER")"

if [ ! -s "$REGISTER" ]; then
    printf '# Artifact register\n\nPer Tutorial 1, Good-Practice Manual §3.\n' > "$REGISTER"
fi

{
    printf '\n## %s -- `%s`\n\n' "$ID" "$ARTIFACT"
    printf '| Field | Value |\n| --- | --- |\n'
    printf '| Registered (UTC) | %s |\n' "$(date --utc --iso-8601=seconds)"
    printf '| Parent artifact | %s |\n' "$PARENT"
    printf '| Command | `%s` |\n' "$COMMAND"
    printf '| stat | `%s` |\n' "$(stat -c '%n|%s|%y|%z' "$ARTIFACT")"
    printf '| Type | %s |\n' "$(file -b "$ARTIFACT")"
    printf '| SHA-256 | `%s` |\n' "$(sha256sum "$ARTIFACT" | cut -d' ' -f1)"
    printf '\n**Observation:** _(fact only -- §6)_\n\n'
    printf '**Interpretation:** _(inference, kept separate from the observation)_\n\n'
    printf '**Limitations / confidence:** _(what this does NOT prove)_\n'
} >> "$REGISTER"

echo "Registered $ID in $REGISTER"
