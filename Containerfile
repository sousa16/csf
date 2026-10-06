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
# lmodern is a separate Debian package, not part of texlive-latex-recommended,
# and both the course's report template and the generated exercise sheets
# \usepackage it -- without it neither compiles.
RUN apt-get update && apt-get install -y --no-install-recommends \
      kali-desktop-xfce dbus-x11 xterm \
      tigervnc-standalone-server tigervnc-common novnc websockify \
      texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended \
      lmodern latexmk \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# PDF tooling. kali-tools-forensics does not pull poppler, and PDFs keep
# turning up: Tutorial 1 hands out a broken.pdf, and Lab 1's only starting
# artifact is an image embedded in the assignment PDF. pdfimages/pdftotext are
# the way in. Own layer, so adding it does not invalidate the ~5 GB above.
RUN apt-get update && apt-get install -y --no-install-recommends \
      poppler-utils \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Steganalysis and web-acquisition tooling. The forensics metapackage ships
# steghide and binwalk but not the PNG/LSB side of the course (II.2): pngcheck
# validates chunk structure and trailing data, zsteg brute-forces bit-plane
# and channel orders, stegseek cracks steghide passphrases against rockyou.
# curl/wget preserve web evidence (headers, timestamps) when a lab points at a
# URL -- run those with ./kali.sh --net. zsteg is a Ruby gem, not a Debian
# package. Own layer so it does not invalidate the ~5 GB above.
RUN apt-get update && apt-get install -y --no-install-recommends \
      pngcheck stegseek stegsnow qpdf \
      curl wget ruby \
      imagemagick python3-pil python3-numpy python3-matplotlib \
 && gem install --no-document zsteg \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Git repository reconstruction and multimedia carving. Lab 1's phishing host
# exposes a working .git tree with LFS-tracked media (.gitattributes, A009) --
# git-lfs resolves LFS pointer files to their real content once the repo is
# reconstructed; ffmpeg extracts frames from any recovered video for manual
# inspection (e.g., reading text/code baked into frames).
RUN apt-get update && apt-get install -y --no-install-recommends \
      git-lfs ffmpeg \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Memory-forensics framework. Volatility 3 is not packaged in Kali (SETUP.md),
# so install it with pipx as its own layer. Pulls a set of Python deps; kept
# last among the tool layers so adding it does not invalidate the ~5 GB above.
# Install system-wide (venv in /opt/pipx, launcher in /usr/local/bin) rather
# than into a home directory: the container runs as uid 1000 with /home/kali
# bind-mounted from a named volume at runtime, which would mask anything
# installed under the build-time home. /usr/local/bin is on every user's PATH.
RUN PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install volatility3

# What Tutorial 2 needs on top of the bare install. The tutorial's
# ".[full]" is not usable here: it drags in leechcorepyc (live hardware
# acquisition), which has no arm64 wheel and nothing in the course uses. Inject
# the other four extras instead: yara-python (yarascan), capstone (malfind
# disassembly), pycryptodome and pillow. yara-python has no arm64 wheel for
# this Python, so it compiles from source; the toolchain is installed and
# purged inside the same RUN so it does not stay in the layer.
# windows.zip is the Windows symbol pack, without which every windows.*
# plugin fails. It is downloaded here because the container runs with no
# network. It lives beside the package, not under ~/.cache, so the /home/kali
# volume does not mask it; only the symbol *cache* is built at first run, in
# that volume. Own layer so a change here does not redo the layers above.
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential python3-dev libssl-dev pkg-config \
 && PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin \
      pipx inject volatility3 yara-python capstone pycryptodome pillow \
 && SYM="$(/opt/pipx/venvs/volatility3/bin/python -c \
      'import os, volatility3; print(os.path.join(os.path.dirname(volatility3.__file__), "symbols"))')" \
 && curl -fsSL https://downloads.volatilityfoundation.org/volatility3/symbols/windows.zip \
      -o "$SYM/windows.zip" \
 && unzip -tq "$SYM/windows.zip" \
 && apt-get purge -y --auto-remove build-essential python3-dev libssl-dev pkg-config \
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
