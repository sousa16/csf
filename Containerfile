# CSF forensic workstation.
#
# Replaces the VirtualBox VM of Tutorial 0 with a container, so the same
# environment runs on Linux (docker/podman) and on the work Mac (podman)
# without maintaining two hypervisor installs. kali-rolling is multi-arch, so
# this builds amd64 on Linux and arm64 on Apple Silicon and runs native on
# both -- no emulation, which matters because Lab 1 spends its time in john.
#
# The trade-off versus a VM: no kernel of our own, so loop-mounting a disk
# image needs a rootful engine (see ./kali.sh --privileged). Sleuthkit reads
# image files directly without mounting, which is the forensically correct
# route anyway, so this rarely bites.
#
# The install is split into three layers on purpose. It is ~5 GB installed,
# and a single RUN makes the engine hold the whole rootfs and the layer
# tarball at once at commit time -- roughly 13 GB of peak free space. Three
# smaller layers, each clearing its own apt cache, cut that to a few GB and
# make a failed rebuild cheap to resume.
FROM docker.io/kalilinux/kali-rolling

ARG DEBIAN_FRONTEND=noninteractive

# apt-get clean is not optional here: without it the 1.4 GB of downloaded
# .debs stay inside the layer. Removing them in a later RUN would not help --
# the bytes are already committed.
RUN apt-get update && apt-get install -y --no-install-recommends \
      sudo procps file bsdmainutils xxd unzip zip p7zip-full \
      libimage-exiftool-perl binwalk steghide \
      john wordlists \
      python3 python3-pip pipx git vim less ca-certificates \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# The bulk: Autopsy, Sleuthkit, foremost, scalpel, Wireshark and friends.
# Pulls a JDK (Autopsy) and wine (the Windows-only tools), which is most of
# the image size.
RUN apt-get update && apt-get install -y --no-install-recommends \
      kali-tools-forensics \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# GUI + report toolchain. Last because it changes least often and a rebuild
# of the layers above should not have to redo TeX's format generation.
RUN apt-get update && apt-get install -y --no-install-recommends \
      kali-desktop-xfce dbus-x11 xterm \
      tigervnc-standalone-server tigervnc-common novnc websockify \
      texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended \
      latexmk \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# uid 1000 so bind-mounted evidence keeps host ownership: docker runs this uid
# directly, podman maps it with --userns=keep-id (both set by ./kali.sh).
# Password "kali" per Tutorial 0, so the password-auditing demos behave as the
# handout describes.
RUN useradd -m -s /bin/bash -u 1000 kali \
 && echo 'kali:kali' | chpasswd \
 && echo 'kali ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/kali \
 && chmod 0440 /etc/sudoers.d/kali

# XFCE over noVNC on :6901. A browser is the only GUI client either machine
# needs, which is what makes Autopsy and Wireshark work the same on the Mac.
COPY --chmod=0755 scripts/start-desktop.sh /usr/local/bin/start-desktop

USER kali
WORKDIR /work
ENV SHELL=/bin/bash
CMD ["bash"]
