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

- **[WORKFLOW.md](WORKFLOW.md)** — what to do every time you sit down to work.
- **[SETUP.md](SETUP.md)** — the containerised Kali environment. Optional: it is
  one way to get the toolkit, and a Tutorial 0 VM is another. Skip it if you
  run a VM.

## Layout

    lab1/  lab2/  lab3/
      artifacts/   material handed out by the teaching team — never modified (§2)
      results/     everything the analysis produces — gitignored, except the register
      report/      LaTeX, from the course template
    scripts/
      forensic-env.sh       §1 — record OS, locale and tool versions
      register-artifact.sh  §3/§4 — register an artifact with parent, command, digest

`§` refers to the **Good-Practice Manual** at the end of Tutorial 1. It is not
advice — it reads as the rubric the three reports are marked against.

## Working agreement

- One branch per person per lab (`lab1/joao`), PR into `main`. Reports merge
  badly; LaTeX merges worse if two people edit the same paragraph.
- Commands go in the report **verbatim**, copied from the session log,
  never retyped. Failed commands and timeouts get recorded too (§5).
- Observation and interpretation stay in separate sentences (§6).
- **Timestamps are recorded in WEST (UTC+01:00)**, and every timestamp states
  its source. Where a source gives a different zone (file metadata and most
  tooling emit UTC), convert to WEST and say so in the Notes column — the
  assignment requires stating any normalization or conversion applied. Fill the
  timeline's optional epoch column when you have it; epoch is unambiguous and
  sorts correctly regardless of zone. WEST is summer time and ends 25 Oct 2026;
  after that Portugal is WET (UTC+00:00). Lab 1's window (19–22 Aug) is WEST.
- **We are not all on the same environment** — some of us run the container,
  some a VM — so tool versions differ per person. Each person records their own
  environment (§1) and findings state which environment produced them.
- Nobody commits a recovered password, a real personal detail, or a raw image
  file (§8, and GitHub rejects >100MB anyway).
