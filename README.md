# csf — Forensics Cyber-Security 26/27, group labs

Group repo for the three graded lab assignments (MEIC/METI, Taguspark).
Personal notes, lecture slides and the weekly tutorials live in a **separate
private repo** and never appear here.

| Deliverable | Due |
| --- | --- |
| Lab 1 | **23 September 2026** |
| Lab 2 | **7 October 2026** |
| Lab 3 | **21 October 2026** |
| Individual defense | end of term |

Lab component is 50% of the grade with a minimum of 8/20. The baseline is
`1/3 Lab1 + 1/3 Lab2 + 1/3 Lab3`, adjusted individually at the defense — so
**every member must be able to explain every part of every report.**

## Setup on a new machine

Install a container engine (podman or docker; podman on macOS via
`brew install podman && podman machine init && podman machine start`), then:

    git clone git@github.com:sousa16/csf.git
    cd csf && ./kali.sh build      # large — kali-tools-forensics, ~20-40 min
    ./kali.sh shell

That is the whole install. No VM, no VirtualBox, nothing on the host but the
engine. The image is Kali rolling with the full forensics metapackage, John
the Ripper with the packaged wordlists, and a LaTeX toolchain for the reports.

    ./kali.sh shell        interactive Kali, this repo at /work
    ./kali.sh desktop      XFCE in a browser — http://localhost:6901/vnc.html
    ./kali.sh report lab1/report    build the PDF
    ./kali.sh run file lab1/artifacts/whatever

### Why a container instead of Tutorial 0's VM

Tutorial 0 prescribes a VirtualBox VM. A container gives the same toolkit
while staying reproducible in git and identical across Linux and macOS —
`kalilinux/kali-rolling` is multi-arch, so it runs native amd64 on Linux and
native arm64 on Apple Silicon. Two consequences worth knowing:

- **No kernel of our own.** Loop-mounting a disk image needs
  `./kali.sh --privileged shell` on a *rootful* engine. Prefer Sleuthkit
  (`mmls`, `fls`, `icat`) straight on the image file — that reads the
  filesystem without mounting it, which is the forensically correct route and
  what the course teaches anyway.
- **Volatility is not packaged in Kali.** When a memory-forensics lab lands,
  add `pipx install volatility3` to the Containerfile as its own layer.

If a lab genuinely needs a full VM, fall back to Tutorial 0 — the analysis is
what is graded, not the environment.

### Deliberate defaults

- **No network by default.** Containers run `--network=none` so an artifact
  under examination cannot reach outside. Use `./kali.sh --net shell` when a
  step needs it (`apt`, downloading a wordlist) and note it in the report.
- **uid 1000 inside = uid 1000 outside**, so evidence written from the
  container keeps host ownership and the SHA-256 lineage stays legible.
- **`/home/kali` is a named volume**, so `~/.john/john.pot`, shell history and
  tool config survive rebuilds. `./kali.sh reset-home` drops it.

## Layout

    lab1/  lab2/  lab3/
      artifacts/   material handed out by the teaching team — never modified (§2)
      results/     everything the analysis produces — gitignored, except the register
      report/      LaTeX, from the course template
    scripts/
      forensic-env.sh       §1 — record OS, locale and tool versions
      register-artifact.sh  §3/§4 — register an artifact with parent, command, digest

`§` refers to the **Good-Practice Manual** at the end of Tutorial 1. It is not
advice — it reads as the rubric the three reports are marked against. Start
every session with:

    cd lab1 && ../scripts/forensic-env.sh

and register every artifact you touch as you go, not afterwards from memory.

## Working agreement

- One branch per person per lab (`lab1/joao`), PR into `main`. Reports merge
  badly; LaTeX merges worse if two people edit the same paragraph.
- Commands go in the report **verbatim**, copied from the session log
  (`script --flush --timing=results/session.timing results/session.typescript`),
  never retyped. Failed commands and timeouts get recorded too (§5).
- Observation and interpretation stay in separate sentences (§6).
- Nobody commits a recovered password, a real personal detail, or a raw image
  file (§8, and GitHub rejects >100MB anyway).
