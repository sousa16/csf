#!/usr/bin/env bash
# Containerized Kali forensic workstation for CSF.
#
# Nothing but a container engine goes on the host. Works with podman (the work
# Mac, and rootless here) or docker, same commands either way.
set -euo pipefail
cd "$(dirname "$0")"
REPO="$(pwd)"

IMAGE=csf-kali:latest
HOME_VOL=csf-kali-home     # keeps ~/.john/john.pot, shell history, tool config
WEB_PORT=6901

if command -v podman >/dev/null 2>&1; then
    ENGINE=podman
elif command -v docker >/dev/null 2>&1; then
    ENGINE=docker
else
    echo "Neither podman nor docker found on PATH." >&2
    exit 1
fi

# On macOS podman runs inside a VM that has to be started first; without this
# the failure is an opaque connection error.
if [ "$ENGINE" = podman ] && [ "$(uname -s)" = "Darwin" ]; then
    if ! podman machine list --format '{{.Running}}' 2>/dev/null | grep -q true; then
        echo "No podman machine is running. First time on this Mac:" >&2
        echo "  podman machine init --cpus 4 --memory 8192 --disk-size 60" >&2
        echo "  podman machine start" >&2
        exit 1
    fi
fi

# The course materials repo, when this clone sits inside it as labs/project.
# A groupmate cloning csf on its own simply gets no /material mount.
MATERIAL=""
if [ -f "$REPO/../../STUDY-PLAN.md" ]; then
    MATERIAL="$(cd "$REPO/../.." && pwd)"
fi

# :z relabels a bind mount for SELinux. It is meaningless on Ubuntu (AppArmor)
# and rejected by some macOS podman setups, so only ask for it where SELinux
# is actually enforcing.
MOUNTOPT=""
if command -v selinuxenabled >/dev/null 2>&1 && selinuxenabled 2>/dev/null; then
    MOUNTOPT=":z"
fi

run_args() {
    # uid 1000 inside must be uid 1000 outside, or bind-mounted evidence comes
    # back owned by someone else and the SHA-256 lineage gets confusing.
    [ "$ENGINE" = podman ] && printf '%s\n' --userns=keep-id
    printf '%s\n' -v "$REPO:/work$MOUNTOPT" -v "$HOME_VOL:/home/kali"
    [ -n "$MATERIAL" ] && printf '%s\n' -v "$MATERIAL:/material$MOUNTOPT"
    # Evidence handling is the subject of the course: default to no network so
    # an artifact cannot call home while being examined. --net re-enables it.
    [ "${WANT_NET:-0}" = 1 ] || printf '%s\n' --network=none
    [ "${WANT_PRIV:-0}" = 1 ] && printf '%s\n' --privileged
    return 0
}

usage() {
    cat <<'USAGE'
usage: ./kali.sh <command> [options]

  build              build the forensic image (large: kali-tools-forensics)
  shell              interactive Kali shell, repo at /work
  desktop            XFCE over noVNC at http://localhost:6901/vnc.html
  run <cmd...>       run one command in a throwaway container
  report <dir>       latexmk a report directory (e.g. ./kali.sh report lab1/report)
  clean              remove the image
  reset-home         drop the persistent /home/kali volume (john.pot, history)

options (before the command):
  --net              give the container network access (default: none)
  --privileged       needed only for loop-mounting disk images; requires a
                     rootful engine. Prefer sleuthkit on the image file.

Mounts:
  /work       this repo (graded labs 1-3)
  /material   the csf materials tree, when this clone lives inside it
USAGE
}

while [ $# -gt 0 ]; do
    case "$1" in
        --net)        WANT_NET=1; shift ;;
        --privileged) WANT_PRIV=1; shift ;;
        *)            break ;;
    esac
done

cmd="${1:-}"
[ $# -gt 0 ] && shift || true

case "$cmd" in
    build)
        # apt needs the network regardless of the run-time default.
        "$ENGINE" build -t "$IMAGE" -f Containerfile "$REPO"
        ;;
    shell)
        mapfile -t args < <(run_args)
        exec "$ENGINE" run --rm -it "${args[@]}" "$IMAGE" bash
        ;;
    desktop)
        WANT_NET=1   # websockify binds a published port
        mapfile -t args < <(run_args)
        exec "$ENGINE" run --rm -it "${args[@]}" \
            -p "127.0.0.1:${WEB_PORT}:${WEB_PORT}" --shm-size=1g \
            "$IMAGE" start-desktop
        ;;
    run)
        [ $# -gt 0 ] || { echo "run: needs a command" >&2; exit 1; }
        mapfile -t args < <(run_args)
        exec "$ENGINE" run --rm -it "${args[@]}" "$IMAGE" "$@"
        ;;
    report)
        dir="${1:?report: needs a directory, e.g. lab1/report}"
        mapfile -t args < <(run_args)
        exec "$ENGINE" run --rm -it "${args[@]}" -w "/work/$dir" "$IMAGE" \
            latexmk -pdf -halt-on-error main.tex
        ;;
    clean)
        "$ENGINE" rmi -f "$IMAGE"
        ;;
    reset-home)
        "$ENGINE" volume rm -f "$HOME_VOL"
        ;;
    *)
        usage
        [ -z "$cmd" ] && exit 1 || exit 0
        ;;
esac
