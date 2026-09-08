#!/usr/bin/env bash
# XFCE served over noVNC, so the GUI forensic tools (Autopsy, Wireshark) are
# reachable from a browser on Linux and macOS alike. Started by ./kali.sh desktop.
set -euo pipefail

GEOMETRY="${GEOMETRY:-1600x900}"
VNC_DISPLAY=:1
VNC_PORT=5901
WEB_PORT=6901

# No VNC password: the port is published on loopback only (see kali.sh) and a
# password here would just be a second thing to keep in sync across machines.
vncserver -kill "$VNC_DISPLAY" >/dev/null 2>&1 || true
rm -f "/tmp/.X11-unix/X${VNC_DISPLAY#:}" "/tmp/.X${VNC_DISPLAY#:}-lock"

Xvnc "$VNC_DISPLAY" \
    -geometry "$GEOMETRY" -depth 24 \
    -SecurityTypes None -AlwaysShared -localhost=0 \
    >/tmp/xvnc.log 2>&1 &

# Xvnc needs its socket up before xfce4-session will attach to it.
for _ in $(seq 1 50); do
    [ -e "/tmp/.X11-unix/X${VNC_DISPLAY#:}" ] && break
    sleep 0.1
done

DISPLAY="$VNC_DISPLAY" dbus-launch --exit-with-session startxfce4 \
    >/tmp/xfce.log 2>&1 &

echo
echo "  Desktop ready:  http://localhost:${WEB_PORT}/vnc.html?autoconnect=1&resize=remote"
echo "  Evidence tree:  /work    (and /material if mounted)"
echo "  Ctrl-C to stop."
echo

exec websockify --web=/usr/share/novnc "$WEB_PORT" "localhost:${VNC_PORT}"
