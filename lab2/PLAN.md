# Lab 2 plan — Operation Deep Fish, Stage II

Due **Wed 7 Oct 2026** via Fenix. Freeze analysis **Sun 4 Oct**. Assignment:
`csf2627-lab-assignment-2.pdf`. Working mechanics (session recording, artifact
register, timeline CSV) are the same as Lab 1 — see `../WORKFLOW.md`.

## Evidence

| File | Notes |
| --- | --- |
| `windows_laptop_memory.raw` | live capture; Windows only |
| `windows_laptop_disk.dd` | **D: is BitLocker-encrypted** |
| `linux_workstation_disk.dd` | no memory capture exists |

Download from the course site (Course Material > Lab assignments). All three
are gitignored (`*.dd`, `*.raw`) — keep them out of the repo, hash them before
opening anything, and record the hashes first.

## Traps

- **Timestamps.** Linux image: subtract **27 days** from every absolute
  timestamp (image says 2026-09-20, treat as 2026-08-24). Windows image: no
  adjustment. State this as an assumption in the report and in each affected
  timeline row. Timeline in WEST (UTC+01:00), timestamp source named per row.
- **Order.** The BitLocker key comes from memory, so memory work precedes the
  D: partition.
- **Observation vs. inference.** Keep them in separate sentences; Q3 and Q4 are
  inference-heavy and are graded on this split.
- **AI use** must be declared in the report (the assignment spells this out).

## The handwritten note (Figure 1)

Reads as a ZIP-password recipe: `sha256{_ _ _ _ _}`, all lowercase, parts joined
with `_`. **Our reading of the handwriting is unverified — check it against the
full-resolution image before relying on it.**

| # | Part | Likely source |
| --- | --- | --- |
| 1 | laptop's name | memory, or SYSTEM hive |
| 2 | first name of the person on the wallpaper | wallpaper file + registry path |
| 3 | "region" of the JJK picture ("Blue Eyes thing") | image on the laptop |
| 4 | Windows password | NTLM hashes (memory / SAM), wordlist |
| 5 | Mom's restaurant photo, "the spot itself" | photo on the laptop, EXIF/GPS/name |

Open: which ZIP it opens — one on the seized disks, or `myzip.zip` from Lab 1
(source artifact of `amelia.pdf`).

## Tracks (two people in parallel)

- **Track A — Windows:** memory, then BitLocker, then the Windows disk.
  Owner: ______
- **Track B — Linux disk**, then shared cross-correlation. Owner: ______
- **Both:** the 16 Lab 1 hashes (Tables 1 and 2 in the assignment; reuse
  `../lab1/results/artifact-register.md`, do not re-derive), the timeline, the
  report.

## Phase 0 — setup (Mon 28 – Tue 29 Sep)

- [ ] Download evidence into `lab2/images/` (gitignored; appears as
  `/work/lab2/images/` in the container). Record SHA-256 first — put them in
  `images/SHA256SUMS` and `kali.sh hash` verifies them.
- [x] `lab2/` tree: `images/`, `evidence/`, `results/`, `report-and-timeline/`
  (report template + empty `timeline-events.csv`, builds with
  `./kali.sh report lab2/report-and-timeline`).
- [x] `results/scripts/kali.sh` starter — steps `hash`, `mem`, `layout`,
  `timeline`, `hashmatch`; run from `lab2/` inside `./kali.sh shell`. Tested on
  a synthetic disk and against Lab 1's evidence (9 of the 16 hashes are in
  Lab 1's `evidence/`); not yet run on the real images.
- [x] `results/scripts/lab1-hashes.sha256` — the 16 Stage I hashes from Tables
  1 and 2, for `kali.sh hashmatch <dir>`.
- [ ] Session recording + `../scripts/forensic-env.sh` (writes
  `results/environment-and-tools.txt`), per WORKFLOW.md.
- [ ] **Rootful podman** for the BitLocker step (`--privileged` needs it): on
  the Mac, `podman machine stop && podman machine set --rootful && podman
  machine start`. Re-check `./kali.sh` still works afterwards.
- [ ] Read decks II.3 (memory) and II.4 (volume) — no notes exist for them yet.
- [ ] Do Tutorial 2 (`../tutorial/Lab2/Challenge.raw`) as a rehearsal of Phase 1.
- [ ] Image has Volatility 3 + Windows symbols already: `vol -f X windows.info`.

## Phase 1 — Windows memory

- `windows.info` first (Windows version decides the BitLocker approach).
- Baseline: `pslist`, `pstree`, `cmdline`, `psscan`, `malfind`.
- Activity: `netscan`, `filescan`, `handles`, `userassist`, `envars`, console /
  command-history plugins.
- Note the hostname (password part 1) and password material (part 4).
- **BitLocker FVEK.** No built-in plugin in Volatility 3. Options: third-party
  plugin (needs `--net` to install and a compatibility check with 2.28.2), or
  scan for the key pool tags directly (tag depends on Windows version).
  Record the exact method and offset — it is a material finding.

## Phase 2 — Windows disk

- `mmls`, `fsstat` per volume. Work on copies; never modify the image.
- D: decrypt with the FVEK via `dislocker` or `libbde` (`./kali.sh --privileged
  shell`; needs FUSE + rootful). Fallback: small `pycryptodome` decrypt script.
  Verify the decrypted volume mounts / `fsstat` reads before trusting it.
- Collect: MFT, `$UsnJrnl`, `$LogFile`, registry hives, Prefetch, LNK / Jump
  Lists, event logs, Recycle Bin (`$I`/`$R`), browser history, PowerShell
  history, any git checkout, wallpaper, photos.
- Timestomping check: `$STANDARD_INFORMATION` vs `$FILE_NAME`, sub-second tell
  (see `../../../notes/os-artifacts-and-timeline-reconstruction.md`).
- Search both disks for the Lab 1 files: by SHA-256, by name, and in `.git` /
  LFS storage (LFS object IDs are SHA-256, so they match Table 1 directly).
- Finish password parts 2, 3, 5; assemble; test against the ZIP.

## Phase 3 — Linux disk

- `mmls`, `fsstat`, `fls -r` including deleted, `istat`, journal (`jls`/`jcat`).
- Shell history, `.git` repos (GitHub/GitLab `MuskyBoi` links to João), SSH
  config / known_hosts, browser profile, Trash, cron, `/var/log`.
- Anti-forensics: truncated history, `shred`, touched timestamps, gaps in the
  journal. **Apply −27 days to every timestamp.**

## Phase 4 — correlation and timeline

- One UTC-normalised timeline, timestamp source per row.
- Rank events by corroboration across sources; single-source events are
  hypotheses.
- `plaso` is not in the image (large); a hand-built CSV like Lab 1's is likely
  enough for the key events. Decide once the volume of events is known.

## Phase 5 — report and package

- Draft each of the four answers as soon as findings exist. Template:
  `csf2627-report-template/`; timeline: `csf2627-timeline-template/`.
- `sha256sum -c` over the register before submitting.
- Declare AI use. One ZIP: report, evidence artifacts + hashes, auxiliary
  items, timeline.

## Questions the report must answer

1. Traces of the phishing site / hidden files on the seized systems — where, SHA-256.
2. Provenance and handling — timeline of site development/operation and file handling.
3. Anti-forensic activity — technique and supporting evidence.
4. New discoveries — effect on attribution to João Musk, other actors or
   infrastructure, hypotheses on the larger scheme, next steps for the PJ.

## Schedule

| Days | Work |
| --- | --- |
| Mon 28 – Tue 29 Sep | Phase 0, decks II.3/II.4, Tutorial 2 |
| Wed 30 Sep – Thu 1 Oct | Phase 1, BitLocker key |
| Fri 2 – Sat 3 Oct | Phases 2 and 3 in parallel |
| Sun 4 Oct | Freeze analysis, finish timeline |
| Mon 5 – Tue 6 Oct | Report and packaging |
| Wed 7 Oct | Submit |
