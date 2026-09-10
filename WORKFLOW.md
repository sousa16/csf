# Working a lab session

Same four steps every time. Commands assume `lab1`; swap the number as the labs
advance.

## 1. Before you touch anything

    git checkout lab1/<your-name> && git pull
    cd lab1

Start recording the session. `script` captures everything you type and
everything printed, so commands can be copied into the report verbatim instead
of retyped from memory (§5):

    script --flush --timing=results/session.timing results/session.typescript

This opens a **nested shell** — you are now inside the recording. Then capture
the environment, which the report has to state alongside every finding (§1):

    ../scripts/forensic-env.sh

Both files land in `results/`, which is gitignored, so they stay local to you.
That is fine: they are per-person by design, since we are not all on the same
environment.

## 2. While working

- **Never modify `artifacts/`.** Copy into `results/` and work on the copy (§2).
- **Anything you recover goes in `evidence/`**, not `results/`. That directory is
  committed and is what gets zipped; `results/` is scratch and is ignored. Put it
  there *before* you hash and register it, so the registered path is its final
  one — moving a registered artifact later makes every path in the register stale.
- **Register every artifact you recover, as you recover it** — not afterwards
  from memory. What the assignment requires per artifact: file name, where it
  came from (its parent artifact and the command that produced it), and its
  SHA-256.
- **Append a line to `report-and-timeline/timeline-events.csv`** for anything
  carrying a timestamp. Timestamps in WEST (UTC+01:00), source named, any
  conversion noted — see the working agreement.
- **Record failures too.** A command that returned nothing, or a tool that was
  not installed, is a finding, not a gap to hide (§5).
- Keep observation and interpretation in separate sentences (§6).

`scripts/register-artifact.sh` does the registration in one line if you want it:

    ../scripts/register-artifact.sh A001 results/secret.txt A000 base64 -d broken.pdf
    #                              ^id  ^file               ^parent ^command that produced it

Only the first two are required. It computes the SHA-256, `stat`, file type and
UTC timestamp, and appends a consistent block to
`results/artifact-register.md`, leaving Observation / Interpretation /
Limitations blank for you to fill in by hand.

Registering by hand instead is fine — the fields above are what matters, not the
tool. The one thing worth keeping is a **single register file per lab** in a
consistent format, because three people improvising three layouts is a bad
evening on the 20th, and a hand-copied SHA-256 is easy to typo and hard to spot.

## 3. When you stop

    exit    # ends the script recording, back to the normal shell
    exit    # leaves the container, if you are using one

Then commit on your own branch:

    git add lab1/results/artifact-register.md lab1/report-and-timeline/ ...
    git commit -m "..."
    git push

`results/` is ignored apart from the register, so your working copies and
session logs stay on your machine. Anything the group needs to see has to be
committed deliberately.

## 4. Before the deadline

- **Check every hash in the report against the file in `evidence/`.** They are
  committed, so no regeneration is needed — but the report's artifact table and
  the shipped bytes have to agree, and that is worth verifying rather than
  assuming. `sha256sum -c` over the register is a minute's work.
- **Re-run a couple of recoveries from the register** as a spot check. Not to
  produce the artifacts, but to confirm the documented commands actually
  reproduce them — that is the reproducibility the assignment asks for, and a
  command that does not reproduce is better found on the 18th than the 22nd.
- **Paste the events CSV into the xlsx template**, sorted chronologically. One
  person, once — the xlsx is binary and cannot be merged.
- **Walk each other through your findings** before the freeze. The defense
  grades each of you on all three parts, including the ones you did not write.
- **Fill in the AI declaration** (report §5): the tools used and what they were
  used for.

## The ZIP

Four things go in, per the assignment: the report PDF, the evidence artifacts
(each named in the report with its SHA-256 and provenance), auxiliary items
(scripts, command outputs, notes), and the timeline.
