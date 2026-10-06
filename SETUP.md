# Containerised Kali environment

**Optional.** This is one way to get the forensic toolkit; a Tutorial 0
VirtualBox VM is another and is equally fine. If you run a VM, ignore this file
— nothing in the repo depends on the container except `kali.sh` itself.

Trade-off: the container is reproducible in git and identical across Linux and
macOS, and needs nothing on the host but a container engine. A VM gives you a
real kernel, which the container does not (see *Limits* below).

## Install

**Linux** — install podman or docker, then:

    git clone git@github.com:sousa16/csf.git
    cd csf && ./kali.sh build      # ~5.3 GB, 20-40 min
    ./kali.sh shell

**macOS** — the podman VM's defaults are too small for this image, so size it
up front rather than after a failed build:

    brew install podman
    podman machine init --cpus 4 --memory 8192 --disk-size 60
    podman machine start

then the same three commands. `kali.sh` refuses with instructions if no machine
is running.

Every package in the Containerfile resolves on **arm64** as well as amd64, so an
Apple Silicon Mac runs natively — no emulation, which is what keeps `john`
usable. The image is Kali rolling with the full forensics metapackage, John the
Ripper with the packaged wordlists, and a LaTeX toolchain for the reports.

## Commands

    ./kali.sh shell              interactive Kali, this repo at /work
    ./kali.sh --net shell        same, with network (apt, downloading a wordlist)
    ./kali.sh desktop            XFCE in a browser — http://localhost:6901/vnc.html
    ./kali.sh report lab1/report build the report PDF
    ./kali.sh run file lab1/artifacts/whatever
    ./kali.sh build              rebuild after a Containerfile change
    ./kali.sh reset-home         drop the persistent /home/kali volume

## Defaults worth knowing

- **No network.** Containers run `--network=none` so an artifact under
  examination cannot reach outside. `--net` re-enables it; note in the report
  whenever you used it.
- **uid 1000 inside = uid 1000 outside**, so evidence written from the container
  keeps host ownership and the SHA-256 lineage stays legible.
- **`/home/kali` is a named volume**, so `~/.john/john.pot`, shell history and
  tool config survive rebuilds.

## Limits

- **No kernel of our own.** Loop-mounting a disk image needs
  `./kali.sh --privileged shell` on a *rootful* engine. Prefer Sleuthkit
  (`mmls`, `fls`, `icat`) straight on the image file — that reads the filesystem
  without mounting it, which is the forensically correct route and what the
  course teaches anyway.
- **Volatility 3 is not packaged in Kali**, so the Containerfile installs it
  with pipx. Run it as `vol -f image.raw windows.pslist` (not `python3 vol.py`).
  The Windows symbol pack (`windows.zip`) is baked into the image, since the
  container has no network; the first run of a plugin builds the symbol cache
  in `/home/kali`, so it is slow once.
- On macOS, if a build fails right after starting the podman machine with a
  repo-signature error ("not live until…"), the VM's clock has not synced yet —
  wait a few seconds and retry.

If a lab genuinely needs a full VM, fall back to Tutorial 0. The analysis is
what is graded, not the environment.
