# Artifact register

Per Tutorial 1, Good-Practice Manual §3.

## A001 -- `csf2627-lab-assignment-1.pdf`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-10T14:07:23+00:00 |
| Parent artifact | - |
| Command | `-` |
| stat | `csf2627-lab-assignment-1.pdf|1085911|2026-09-10 11:09:35.911255085 +0000|2026-09-10 11:09:35.911783488 +0000` |
| Type | PDF document, version 1.5 |
| SHA-256 | `7773735da3a12e8b73e8c059deca7b2cb7dbd167a4810fa645717a1ef13dbc25` |

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** _(what this does NOT prove)_

## A002 -- `evidence/fig1-000.png`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-10T14:07:23+00:00 |
| Parent artifact | A001 |
| Command | `pdfimages -all csf2627-lab-assignment-1.pdf results/fig1` |
| stat | `evidence/fig1-000.png|941353|2026-09-10 14:00:56.027106618 +0000|2026-09-10 14:05:52.191857241 +0000` |
| Type | PNG image data, 1254 x 1254, 8-bit/color RGB, non-interlaced |
| SHA-256 | `cfd8e534f41d17daac063110e16ea6e4a9b6f1394849f49ac08bd5c044906e67` |

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** _(what this does NOT prove)_

## A003 -- `results/web/fenix.dpss.inesc-id.pt/index.html` (phishing landing page)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-17T13:41:43+00:00 |
| Parent artifact | A001 (URL taken from the "here" link annotation on page 3 of the assignment PDF) |
| Command | `wget -r -l3 -np -p -N https://fenix.dpss.inesc-id.pt/index.html` (passive mirror, from the containerised Kali, `./kali.sh --net`) |
| Acquired (server Date header) | 2026-09-15 15:16:05 GMT |
| Server Last-Modified | 2026-09-09 23:11:16 GMT |
| Server headers | `nginx/1.31.4`, `X-Powered-By: PHP/7.4.3`, IP `146.193.41.5` |
| Type | HTML document, UTF-8 |
| SHA-256 | `56f8199c4d6a328af245c7b8149ad632573c586e6336ea69f7b8a93ea88af3b7` |

**Observation:** _(fact only -- §6)_ The URL recorded during triage serves a login page that reproduces the Técnico ID / CAS sign-in screen (title "Técnico Lisboa - Login", Técnico favicon, `<form action="/cas/login" method="post">` posting `username` + `password`). The page is on `fenix.dpss.inesc-id.pt`, not on a `tecnico.ulisboa.pt` host. Mirror is scratch under `results/web/` (gitignored); move to `evidence/` before it goes in the ZIP.

**Interpretation:** _(inference, kept separate from the observation)_ Consistent with a credential-harvesting phishing clone of the institutional login, matching the email's "change your password" pretext.

**Limitations / confidence:** _(what this does NOT prove)_ A passive mirror captures only the client-side response; it does not show what the PHP backend does with submitted credentials, nor prove who operates the host. No credentials were ever submitted.

## A004 -- `results/web/fenix.dpss.inesc-id.pt/robots.txt` (investigative lead)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-17T13:41:43+00:00 |
| Parent artifact | A003 (same host) |
| Command | `curl -s https://fenix.dpss.inesc-id.pt/robots.txt` |
| Type | ASCII text, 30 bytes |
| SHA-256 | `78d9ca5ccb955cff9f5e83fcb67f1aa25d916b1f31158583b6d9835528045dcc` |

**Observation:** _(fact only -- §6)_ Full contents are two lines: `User-agent: *` / `Disallow: /var/`. Fetching `/var/` itself returns HTTP 404 with no directory listing.

**Interpretation:** _(inference, kept separate from the observation)_ **>> LEAD, NOT YET PURSUED <<** The operator deliberately hid a `/var/` path from crawlers, which typically means a file (not a listable directory) exists under it — plausibly the kit's harvested-credentials log or another concealed artifact, and a candidate for one of the 8 hidden secrets.

**Limitations / confidence:** _(what this does NOT prove)_ We have not confirmed any file exists under `/var/`; the disallow line alone is not proof. Retrieving it requires **active enumeration of a third-party host, which we are deferring until (a) the technique is taught and (b) authorisation is confirmed** with the teaching team. Recommend raising this with SI/NRC as a next investigative step (assignment Q3) rather than probing unilaterally.

## A005 -- `results/web/acme/9xQ3nM7kV2pR5sT8wY4zA6bC1dF0gHjL` (planted file at ACME-challenge path)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-17T14:05:56+00:00 |
| Parent artifact | A003 (same host) — found under `/.well-known/acme-challenge/` |
| Command | `curl https://fenix.dpss.inesc-id.pt/.well-known/acme-challenge/9xQ3nM7kV2pR5sT8wY4zA6bC1dF0gHjL` |
| Acquired (server Date) | 2026-09-17 14:05:56 GMT |
| Server Last-Modified | 2026-09-09 23:11:15 GMT (matches the rest of the kit) |
| Type | ASCII text, CRLF, 66 bytes |
| SHA-256 | `9ee8314a80af0d93b4c44da99c6dc41a23c0548321ff256f4e025b60731b849b` |

**Observation:** _(fact only -- §6)_ Full content is one line: `9xQ3nM7kV2pR5sT8wY4zA6bC1dF0gHjL.N4vY7uP2qW9mK5sR8xT3zB6cD1fG0hJ`. Structure is `<filename-token>.<second-token>`, matching the ACME HTTP-01 `token.thumbprint` layout, but the second token is 31 chars (a real base64url SHA-256 JWK thumbprint is 43). Both tokens decode (base64url) to non-printable random bytes; neither is base32/hex. `Last-Modified` equals the phishing kit's deployment time. Found by teammate probing `/.well-known/acme-challenge/`.

**Interpretation:** _(inference, kept separate from the observation)_ A deliberately planted artifact (not a genuine Let's Encrypt challenge — wrong thumbprint length, and no cert issuance context). Most likely one of the 8 hidden secrets. The second token `N4vY7uP2qW9mK5sR8xT3zB6cD1fG0hJ` is NOT a sibling file in the same directory (fetching it under `/.well-known/acme-challenge/` returns 404, and that directory shows no listing). Leading working hypothesis: the second token is the **filename under `/var/`** — connecting this artifact to the A004 robots.txt lead (robots.txt hid `/var/` but gave no filename; this file plausibly supplies it). Alternative: one of the tokens is a passphrase for a later password-protected payload (steghide/zip).

**Limitations / confidence:** _(what this does NOT prove)_ The breadcrumb returned nothing: both the sibling-file hypothesis (`/.well-known/acme-challenge/N4vY7uP2qW9mK5sR8xT3zB6cD1fG0hJ`) and the `/var/<token>` hypothesis were tried and each returned 404. The tokens decode to random bytes, so no meaning is recoverable from this file alone. UPDATE: A006 (server source) shows no code path uses these tokens, so this file is most likely a standalone planted secret / distractor rather than a working pointer.

## A006 -- `results/web/server.js` (phishing server source code)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-17T14:20:00+00:00 |
| Parent artifact | A003 (same host) — exposed via the app's own `serve-index` directory listing (`serveIndex(__dirname, {hidden:true})`) |
| Command | recovered from the host's exposed directory listing (teammate) |
| Type | JavaScript (Node.js / Express) source |
| SHA-256 | `2a014a1168968989cf36488ac8a7f218f8b3591dabeea50199c6f26e03abf863` |

**Observation:** _(fact only -- §6)_ Ground truth of the phishing backend. Key facts:
- `POST /cas/login` reads `username`+`password` and appends `[<ISO timestamp>] Username: <u>, Password: <p>` to `credentials.txt` in the app root, then `res.redirect("https://fenix.tecnico.ulisboa.pt/")` (the REAL Técnico site).
- Response headers are spoofed: `Server: Apache/2.4.41 (Ubuntu)` and `X-Powered-By: PHP/7.4.3`, but the app is actually **Node.js/Express** (`x-powered-by` is disabled then overwritten).
- Two 403 filters: one for `/credentials.txt`, one for `/var/log/credentials.log`; a separate filter blocks `/node_modules`.
- Serves static files from `public/` and from the app root with `dotfiles: "allow"`, plus a `serve-index` listing of the app root including hidden files.

**Interpretation:** _(inference, kept separate from the observation)_ Confirms (no longer just infers) credential harvesting and the trusted-redirect cover. The real captured-credentials file is `credentials.txt` in the app root; `/var/log/credentials.log` appears to be a **decoy path** (no code writes there), which explains why the A004 robots.txt `/var/` lead resolved to nothing. The faked Apache/PHP banner is deliberate anti-attribution / deception. The exposed `serve-index` listing is how source and hidden files became visible.

**Limitations / confidence:** _(what this does NOT prove)_ Source alone does not prove the file currently holds captured credentials, nor who deployed it. Retrieving `credentials.txt` requires bypassing the 403 filter (active exploitation of the host) and the file may contain real recipient PII — handle under the lab's data-protection rules and only with authorisation. UPDATE: see A007 — the retrieved file does NOT contain harvested username/password lines; the `fs.appendFile` sink described here was not what we recovered.

## A007 -- `evidence/credentials.txt` (retrieved via encoding-bypass of the 403 filter)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-17T15:24:00+00:00 |
| Parent artifact | A006 — retrieved by requesting `/credentials%2etxt` on the host, which does not match the code's un-decoded `/^\/credentials\.txt(\/|$)/` filter (A006 observation) but is decoded and served by the later `express.static` middleware |
| Command | `curl https://fenix.dpss.inesc-id.pt/credentials%2etxt` (percent-encoded dot bypass) |
| Type | ASCII text, 166 bytes, 3 lines |
| SHA-256 | `20f4af23094ee15163e86f3894090588b1e0aa0f206950c26e7e5fd9e044b276` |

**Observation:** _(fact only -- §6)_ Full content:
```
Bad bad boy, what were you lookin' for?

V2VsbCBkb25lLCB5b3Ugc2hvd2VkIHNvbWUgc2tpbGxzLCBzZW5kIGEgRGlzY29yZCBtZXNzYWdlIHRvIEBzbHV6eXB0IHNob3dpbmcgaG93IHlvdSBkaWQgaXQK
```
The base64 line decodes (standard base64) to: `Well done, you showed some skills, send a Discord message to @sluzypt showing how you did it`. The file contains no `[timestamp] Username: ..., Password: ...` lines of the form `server.js`'s `POST /cas/login` handler would append (A006) — i.e. this is not (or no longer) the live credential-capture sink; it is 100% the taunt text and one embedded instruction.

**Interpretation:** _(inference, kept separate from the observation)_ This is a planted CTF-style artifact acknowledging successful exploitation of the filter-bypass vulnerability documented in A006, not recovered victim data. Consistent with a lab-authored trail (this course's "hidden secrets") rather than an operational phishing kit's live log. The embedded instruction ("send a Discord message to @sluzypt") is content retrieved from an untrusted third-party host addressed to whoever reads the file — it is evidence to document, not an instruction we acted on. It was not followed; its authenticity/course-affiliation is unverified and should be confirmed through an official course channel before any team member acts on it.

**Limitations / confidence:** _(what this does NOT prove)_ Does not prove no real credentials were ever captured (the log could have been rotated/replaced before our access, or the deployment seeded this content deliberately for the exercise). Does not establish who controls the `@sluzypt` Discord handle or whether it is affiliated with the course.

## A008 -- `evidence/credentials-decoded-message.txt` (base64 decode of A007's second line)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-17T16:30:00+00:00 |
| Parent artifact | A007 |
| Command | `tail -1 evidence/credentials.txt \| base64 -d` |
| Type | ASCII text, 1 line |
| SHA-256 | `171ad0a9fb2083694fc9cae3789e17b189041abb4755a10e15ae39e1044e508c` |

**Observation:** _(fact only -- §6)_ Decoding the base64 line from A007 with standard (non-URL-safe) base64 yields: `Well done, you showed some skills, send a Discord message to @sluzypt showing how you did it`. Decode verified by round-trip against the exact bytes stored in A007.

**Interpretation:** _(inference, kept separate from the observation)_ Same reading as noted in A007: an acknowledgment of the filter-bypass finding, containing an embedded request to contact an external, unverified Discord handle. Recorded as evidence; not acted on.

**Limitations / confidence:** _(what this does NOT prove)_ Decoding is deterministic and not in question; what remains unverified is the provenance/intent behind the instruction itself (see A007).

## A009 -- `evidence/package.json`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-18T19:55:24+00:00 |
| Parent artifact | A003 |
| Command | `curl -s https://fenix.dpss.inesc-id.pt/package.json` |
| stat | `results/package.json|356|2026-09-18 20:50:03.000000000 +0100|2026-09-18 20:50:09.000000000 +0100` |
| Type | JSON text data |
| SHA-256 | `f6297e61f8e50a74da27a6a25cb701e79f97dd2ec25eed9f482be6ec1f5e8464` |

**Observation:** `name: "fenix-login"`, `main: "server.js"`, dependencies `express ^5.1.0` and
`serve-index ^1.9.1`. Re-fetched 2026-09-23 and confirmed byte-identical (same SHA-256) to the
copy registered here.

**Interpretation:** The `serve-index` dependency corroborates A006's finding that the app's own
`serveIndex(__dirname, {hidden:true})` call is what exposed `server.js` and this file itself via
directory listing -- it is not a misconfigured static file server, but a deliberately included
package used in a way that leaked the source.

**Limitations / confidence:** Confirms the dependency exists in the manifest; does not by itself
prove the exposed listing was accidental versus intentional on the operator's part.

## A010 -- `evidence/README.md`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-18T19:55:24+00:00 |
| Parent artifact | A003 |
| Command | `curl -s https://fenix.dpss.inesc-id.pt/README.md` |
| stat | `results/README.md|46|2026-09-18 20:51:59.000000000 +0100|2026-09-18 20:52:05.000000000 +0100` |
| Type | ASCII text, with CRLF line terminators |
| SHA-256 | `bfffd2f4f907a282c45b05b5e5c78de5fa8fb7538283c32ab3bb7d5347aa9c8a` |

**Observation:** Full content: `# peixinho` / `Fenix authentication frontend.` Re-fetched
2026-09-23 and confirmed byte-identical (same SHA-256) to the copy registered here.

**Interpretation:** "peixinho" ("little fish" -- a plausible pun on "phishing") is the
operator's own internal project name for the phishing kit, matching the `peixinho.git` remote
name recorded in A011's `.git/config` and the bundle name `peixinho.bundle` (A012). The blandly
generic description ("authentication frontend") is consistent with deliberate understatement
rather than an accidental leftover.

**Limitations / confidence:** A name match is circumstantial corroboration of a single operator
across artifacts, not proof of identity or intent.

## A011 -- `evidence/git-config`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-21T09:48:58+00:00 |
| Parent artifact | A006 |
| Command | `curl -sS -D git-config.headers -o evidence/git-config https://fenix.dpss.inesc-id.pt/.git/config` |
| stat | `evidence/git-config|596|2026-09-21 10:48:05.000000000 +0100|2026-09-21 10:48:12.000000000 +0100` |
| Type | ASCII text |
| SHA-256 | `67853eb4541a46659452f329e2c6ad7ed8724ffa6f4e9f6a2d385c9ef28c4b42` |

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** _(what this does NOT prove)_

## A012 -- `evidence/peixinho.bundle`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-21T09:49:28+00:00 |
| Parent artifact | A011 |
| Command | `git-dumper https://fenix.dpss.inesc-id.pt/.git/ /home/maria/acq/peixinho; git bundle create evidence/peixinho.bundle --all` |
| stat | `evidence/peixinho.bundle|27568020|2026-09-21 10:49:09.000000000 +0100|2026-09-21 10:49:17.000000000 +0100` |
| Type | Git bundle |
| SHA-256 | `9e9fd1acba48c028a5fea77ff6f937776553dad53dc431b0117aff5f840ac2c5` |

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** _(what this does NOT prove)_

## A013 -- `results/acq/polish_cow.webp`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-21T11:53:24+00:00 |
| Parent artifact | A012 |
| Command | `curl -sS -o polish_cow.webp https://fenix.dpss.inesc-id.pt/.git/lfs/objects/<xx>/<yy>/<oid>` |
| stat | `results/acq/polish_cow.webp|241083862|2026-09-21 12:52:40.000000000 +0100|2026-09-21 12:52:52.000000000 +0100` |
| Type | RIFF (little-endian) data, Web/P image, animated, EXIF metadata, 640x640  |
| SHA-256 | `857f75db04db84340d4efa53061ca26fc7c7e6f65f80899c57f8d65b4c9d5678` |

**Observation:** Animated WebP, 640x640, 12267 frames, total duration 25:02, created with ezgif.com (Software tag in the EXIF chunk). Obtained from `/.git/lfs/objects/<oid>` on the server; SHA-256 matches the LFS pointer's `oid`. No bytes after the end of the RIFF structure.

**Interpretation:** Frame durations (50–305 ms) encode a payload via cumulative differences mod 256; see A014.

**Limitations / confidence:** The encoding technique was inferred by reverse engineering the data, not documented by the attacker; a second, unidentified channel cannot be excluded.

## A014 -- `evidence/polish_cow-payload.json`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-21T13:11:37+00:00 |
| Parent artifact | A013 |
| Command | `python3 aux/riff2.py polish_cow.webp cow-frames.csv; python3 aux/cow_decode.py cow-frames.csv polish_cow-payload.json` |
| stat | `evidence/polish_cow-payload.json|12259|2026-09-21 14:11:14.000000000 +0100|2026-09-21 14:11:21.000000000 +0100` |
| Type | JSON text data |
| SHA-256 | `4cf80e2f2a1321b13e3dece45d0c949de73e5aadc3ca9d1d8e4339b398101110` |

**Observation:** Valid JSON (`python3 -m json.tool`), 12259 bytes. Top-level keys: `$schema`, `title`, `description`, `version`, `execution_mode`, `environment`, `security_enclave`, `tools`. Title: "AMÉLIA Sovereign LLM Inference Tools Configuration" v1.3.0, `environment: production`. Contains a schema property `staging_bypass_token`, marked `[DEPRECATED]`, described as allowing external AT/SS API calls to be skipped given an exact staging UUID; annotated "NEVER USE IN PRODUCTION".

**Interpretation:** Connects to Finding 04 of report A017 (AMÉLIA integration with AT/ISS/DGERT/IMPIC) and to anomalies SEC012/SEC014 recorded there (timeouts during external API calls). Hypothesis: the bypass mechanism, though disabled by default, existed in an `environment: production` configuration and may relate to those incidents.

**Limitations / confidence:** There is no evidence that `staging_bypass_token` was actually triggered; the link to SEC012/SEC014 is an inference, not an established fact.

## A015 -- `evidence/amelia-report.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T08:54:14+00:00 |
| Parent artifact | A017 |
| Command | `pdftotext -layout trailer-embedded.pdf amelia-report.txt` |
| stat | `evidence/amelia-report.txt|12990|2026-09-22 09:54:14.000000000 +0100|2026-09-22 09:54:14.000000000 +0100` |
| Type | Unicode text, UTF-8 text |
| SHA-256 | `6250cba905fde89b5863f49e3778520f4ec1b5aa1f040b8c7de6c97fd0c359f8` |

**Observation:** Plain-text (`-layout`) rendering of A017's 5 pages, 263 lines. Confirms A017's
document reference (AMA20260041AI), "CONDITIONAL ACCEPTANCE" status, and the three named
signatories on the final page: Prof. Dr. Refrigério Sargaço (President of IST; Chair of the
Independent IST Technical Review Panel), Dr. Eng. Armando Sacos (Chief Systems Architect, AMA;
non-voting attendee), and Eng. Só Craques (Minister for State Modernization; non-voting
observer) -- the latter two explicitly marked non-voting.

**Interpretation:** Produced solely to make A017's text full-text searchable/quotable for this
report; carries no evidentiary content beyond what A017 itself establishes. The non-voting
annotations on the two attendees corroborate A017's Chair-only override framing (§3.3): only the
Chair (Sargaço) is recorded as holding a vote.

**Limitations / confidence:** `pdftotext` is a lossless text extraction for a text-layer PDF; no
discrepancy with A017 was found, so this artifact is not independently probative, only
corroborating.

## A016 -- `evidence/Grand Theft Auto VI Trailer 1.mp4`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T08:59:12+00:00 |
| Parent artifact | A012 |
| Command | `git show 95f15e9:'Videos/Grand Theft Auto VI Trailer 1.mp4' > 'Grand Theft Auto VI Trailer 1.mp4'` |
| stat | `evidence/Grand Theft Auto VI Trailer 1.mp4|9443926|2026-09-22 09:59:00.000000000 +0100|2026-09-22 09:59:04.000000000 +0100` |
| Type | data |
| SHA-256 | `5d3b5f08f35c5d812e0f2c36d58c9c4f2a0b844e2e1f8bd5054a9bc54f8471ca` |

**Observation:** Polyglot file. `file` reports only "data" (initial signature not recognised as any single format). By offset, it contains: an ICO header (0), a PDF (27, object with `Length 9357855`), HTML (~97337–112469), a PNG (112484, referenced by the ICO entry), a valid MP4 structure (`ftyp` at 256, `moov` at 300, `mdat` at 573338, ending at 9357927), and a second PDF starting at 9357946 through the end of the file.

**Interpretation:** Deliberate concatenation of multiple formats into a single file to hide content inside an innocuous-looking filename ("trailer").

**Limitations / confidence:** It was not confirmed whether the embedded HTML content (offset ~97337–112469) was extracted/analysed — see general limitations in report §5.

## A017 -- `evidence/trailer-embedded.pdf`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T08:59:45+00:00 |
| Parent artifact | A016 |
| Command | `tail -c +9357946 'Grand Theft Auto VI Trailer 1.mp4' > trailer-embedded.pdf` |
| stat | `evidence/trailer-embedded.pdf|85981|2026-09-22 09:59:45.000000000 +0100|2026-09-22 09:59:45.000000000 +0100` |
| Type | PDF document, version 1.5 |
| SHA-256 | `86e469294263367ad841b7c91f405e658a437229d5c7ec15ebefee19109265af` |

**Observation:** Valid PDF, 5 pages, `pdfinfo` reports Producer `xdvipdfmx (20240305)`, CreationDate `Thu Apr 30 2026 12:00:00 WEST`, not encrypted. Title: "Independent External Technical Assessment Report — Project AMÉLIA" (reference AMA20260041AI). Records a review panel vote (1 in favour, 2 against, 1 abstention) and a final "Conditional Technical Acceptance" decision made unilaterally by the Chair. Documents anomaly "SEC014" (intermittent timeout during external API calls under extreme load), classified as a non-critical observation.

**Interpretation:** See report §3.2 — possible link between this finding, the `staging_bypass_token` in A014, and the acceptance decision issued despite the panel majority voting against.

**Limitations / confidence:** There is no proof that the bypass token was triggered during the SEC012/SEC014 incidents described here; the link is an investigative hypothesis, to be confirmed against production logs (see §3.3).

## A018 -- `evidence/trailer-icon.png`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T09:00:22+00:00 |
| Parent artifact | A016 |
| Command | `tail -c +112485 'Grand Theft Auto VI Trailer 1.mp4' \| head -c 460854 > trailer-icon.png` |
| stat | `evidence/trailer-icon.png|460854|2026-09-22 10:00:22.000000000 +0100|2026-09-22 10:00:22.000000000 +0100` |
| Type | PNG image data, 600 x 527, 8-bit/color RGBA, non-interlaced |
| SHA-256 | `27427762ad21c233e5406dba38b62544075f46f8892ab204c1b6d1aa54e309d6` |

**Observation:** Valid PNG (`pngcheck` reports no errors), 600x527, RGBA. `exiftool` shows no metadata beyond standard PNG fields. `zsteg -a` revealed no consistent pattern (only typical false positives from coincidental bitplane signatures).

**Interpretation:** No evidence of additional hidden content.

**Limitations / confidence:** Negative result; does not rule out untested steganographic techniques.

## A019 -- `evidence/trailer-embedded.mp4`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T09:01:21+00:00 |
| Parent artifact | A016 |
| Command | `tail -c +257 'Grand Theft Auto VI Trailer 1.mp4' \| head -c 9357671 > trailer-embedded.mp4` |
| stat | `evidence/trailer-embedded.mp4|9357671|2026-09-22 10:01:21.000000000 +0100|2026-09-22 10:01:21.000000000 +0100` |
| Type | ISO Media, MP4 Base Media v1 [ISO 14496-12:2003] |
| SHA-256 | `529ff4b5367a3257411145fc61ba4cfa38c4f81a6918f27afb6ac19f0f413d3b` |

**Observation:** Valid MP4 structure (`file` recognises ISO Media). H.264 video track, 640x360@30fps, 90.03s, with deliberately corrupted NAL units (decode errors on nearly every frame). The AAC audio track (44.1kHz, stereo), extracted with `-c copy`, is a valid ADTS stream, but decoding fails on 99.9% of packets; analysis of the ADTS header fields (frame_length) found no fixed cycle suggesting an additional data channel.

**Interpretation:** Both video and audio appear to be decoy content, deliberately corrupted to prevent normal playback, with no additional useful content identified beyond the existence of the file itself within the polyglot.

**Limitations / confidence:** Negative result regarding a data channel in frame_len values; other techniques (e.g. LSB analysis of the raw AAC payload bytes) were not exhaustively tested.

## A020 -- `evidence/blank-fixed.png`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T10:50:03+00:00 |
| Parent artifact | A021 |
| Command | `printf '\x89PNG' | dd of=blank-fixed.png bs=1 count=4 conv=notrunc` |
| stat | `evidence/blank-fixed.png|1989497|2026-09-22 11:48:03.000000000 +0100|2026-09-22 11:48:08.000000000 +0100` |
| Type | PNG image data, 1971 x 4260, 8-bit/color RGBA, non-interlaced |
| SHA-256 | `76df940819110fc996599a9df24d54c3c55eaab85055cf1306acc2c375ee396b` |

**Observation:** Screenshot of an `r/portugal` thread titled "Are public contracts being monopolized?" (author TinfoilPT), with ~60 comments (5 sections captured by the image, recovered from a PNG whose signature had been altered to `%PDF`). Reports that 45 of 50 major public contracts were awarded to three companies (SpinumMorta, Grupo Lenha, MotaIngil) via the BASE/IMPIC platform.

**Interpretation:** Case context, containing no password or technical instruction. Connects to Finding 04 of A017 (AMÉLIA–IMPIC integration) and to the `entity_nif` property in A014.

**Limitations / confidence:** OCR (`tesseract`) may have missed text; the image was reviewed both visually and via OCR with no further content found.

## A021 -- `evidence/blank`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T10:55:03+00:00 |
| Parent artifact | A012 |
| Command | `git show 23a5ca7:Downloads/blank > blank` |
| stat | `evidence/blank|1989497|2026-09-22 11:55:01.000000000 +0100|2026-09-22 11:55:02.000000000 +0100` |
| Type | data |
| SHA-256 | `23cd980099fab1c0b6993a9d27899f8679ffe42d423d8d51b29c655c0d53bbec` |

**Observation:** File with the first 4 bytes of the PNG signature replaced by `%PDF` (`25 50 44 46`); the remaining PNG signature bytes (`0D 0A 1A 0A`) and the `IHDR` chunk (1971x4260, RGBA) are intact.

**Interpretation:** Deliberate header alteration to hinder automatic file-type identification. See A020 for the corrected content.

**Limitations / confidence:** —

## A022 -- `evidence/myzip.zip`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T18:20:58+00:00 |
| Parent artifact | A012 |
| Command | `git show 23a5ca7:Downloads/myzip.zip > myzip.zip` |
| stat | `evidence/myzip.zip|816482|2026-09-22 19:20:48.000000000 +0100|2026-09-22 19:20:52.000000000 +0100` |
| Type | Zip archive data, made by v3.0 UNIX, extract using at least v2.0, last modified Feb 18 2026 15:23:48, uncompressed size 824733, method=deflate |
| SHA-256 | `9ddeef450f4307a974d07516519d076429b9bd1a32e192816ae0217cc8139de4` |

**Observation:** Encrypted ZIP archive (PKZIP, ZipCrypto) containing `amelia.pdf`. Password recovered via targeted brute force: candidate passwords generated from `Downloads/subtitles.srt` (concatenating, with no spaces or punctuation, the subtitle text of each block grouped by timestamp), tested with `john`.

**Interpretation:** The password (not reproduced here — see session log) corresponds to a line spoken in the subtitled episode, indicating the attacker used their own "phone backup" material as the password source.

**Limitations / confidence:** The password itself is not recorded in this document as a precaution (§8); it exists only in the local session log, outside the repository.

## A023 -- `evidence/amelia2.pdf`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-22T18:21:47+00:00 |
| Parent artifact | A022 |
| Command | `unzip -P '<password recuperada via john contra candidatas derivadas de subtitles.srt>' -d myzip-out myzip.zip` |
| stat | `evidence/amelia2.pdf|824733|2026-09-22 19:21:22.000000000 +0100|2026-09-22 19:21:26.000000000 +0100` |
| Type | PDF document, version 1.7 |
| SHA-256 | `04be0e12533ede61c718f63b3bedf9888b2914dfe0e437d9c0f1272b24f51707` |

**Observation:** In addition to the architecture proposal itself, Section 11 ("Known Limitations
and Query Translation Constraints", p.14) discloses a deliberate fallback in the Self-Querying
module: under broad queries that risk Out-Of-Memory exceptions, the query translator defaults to
a pre-configured "cluster ID" instead of performing a global semantic search, narrowing the LLM's
evidence to a fixed subset of documents. Separately, Section 7.4 (p.9) explicitly prohibits
"artificially forcing the relevance of documents from a particular entity through fixed scores or
hidden lists" in public-procurement use, calling it a "Prohibited control."

**Interpretation:** Section 11 describes, in the same document that Section 7.4 forbids it, a
mechanism structurally consistent with the prohibited pattern: a fixed, pre-selected subset of
documents ("cluster") substituting for open retrieval under specific conditions. This is a
plausible technical explanation for the contract-concentration pattern independently reported in
A020, and connects to the `staging_bypass_token` disclosed in A014.

**Limitations / confidence:** The report does not disclose what documents or entities the
fallback "cluster ID" points to, nor whether/how often the fallback was triggered in production.
The connection to the Reddit-reported contract concentration (A020) and to A014's bypass token
remains a hypothesis, not an established fact.

## A024 -- `results/acq/dj_cara_after_hours.wav` (NOT shipped in the repository; belongs at `evidence/dj_cara_after_hours.wav` in the submission ZIP)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T16:20:00+00:00 |
| Parent artifact | A012 |
| Command | `curl -sS -o dj_cara_after_hours.wav https://fenix.dpss.inesc-id.pt/.git/lfs/objects/<xx>/<yy>/<oid>` |
| stat | _not captured at acquisition time; 129,049,812 bytes, SHA-256 below verified against the LFS pointer's `oid` in A012's history_ |
| Type | RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, stereo 48000 Hz |
| SHA-256 | `2b61eecffc5261dcc05d833c64454b42d33f445d3df09095988d0c2dbbc8753d` |

**Observation:** Git LFS blob, 129 MB. Hides a message in the spectrogram of the stereo
side channel ((L-R)/2), 18-22 kHz band, visually legible and decoded with
`lab1/scripts/decode_spectrogram_messages.py`, a script written by the authors (AI-drafted, see
report §5) for this purpose. This script is our own tooling, not recovered from the attacker --
the attacker's dumped git history (A012) contains no `.py` files.

**Interpretation:** The content is a real source-code diff — see the following artifact.

**Limitations / confidence:** —

## A025 -- `evidence/spectrogram-messages.zip`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T16:20:00+00:00 |
| Parent artifact | A024 |
| Command | `python3 decode_spectrogram_messages.py dj_cara_after_hours.wav --out spectrogram-messages-final && zip -r spectrogram-messages.zip spectrogram-messages-final` |
| stat | _not captured at acquisition time; 4,168,880 bytes_ |
| Type | Zip archive data, at least v1.0 to extract, compression method=store |
| SHA-256 | `7c9bb065f01290cb4b453bd5d132fa71566598591dc412c5de366a18c23bdce9` |

**Observation:** Contains 1 overview image, 13 time-tiled spectrogram PNGs (50s each, covering
0-672.13s), and `index.csv` indexing them by start/end time. The recovered patch (transcribed in
full in the report Appendix and cross-referenced as this artifact's content) is legible across
`tile_0000` through approximately `tile_0004` (0-250s); later tiles contain no legible text.

**Interpretation:** The 18-22kHz band was chosen by the operator because it is largely inaudible
to adult humans and outside the range most consumer audio pipelines aggressively compress,
letting a rendered spectrogram carry a persistent visual signal without noticeably degrading the
track's audible content.

**Limitations / confidence:** Some lines are illegible in the source spectrogram (see the
Appendix transcription note); the patch as transcribed may be incomplete at those points. This
artifact is a derived rendering, not the raw evidence -- A024 (the WAV itself) is the primary
artifact.

## A026 -- `evidence/Telemetry.xlsx`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T16:20:00+00:00 |
| Parent artifact | A012 |
| Command | `git show 43e5350:'Documents/ESP32_ADXL345_3Axis_Telemetry.xlsx' > Telemetry.xlsx` |
| stat | _not captured at acquisition time; 3,255,907 bytes_ |
| Type | Microsoft Excel 2007+ |
| SHA-256 | `3369cd48df5bb112def25e662398674e89bdeb5df6eaa400c4ba538a9778f218` |

**Observation:** Workbook named for an ESP32/ADXL345 3-axis accelerometer, but the three sheets
("Sheet1"/"Sheet2"/"Sheet3") are each exactly 302 columns x 400 rows of floating-point values --
matching, cell-for-cell, the 302x400 pixel dimensions of `foto_revelada.png` (committed
separately, not yet formally registered under its own ID). Per-sheet value ranges: Sheet1
0.0-99.4, Sheet2 -12.3-38.9, Sheet3 -39.7-48.8, consistent with CIELAB L*/a*/b* channel ranges
rather than any real accelerometer signal (a genuine ADXL345 reports acceleration in m/s^2 or
g-units, not a channel bounded near [0,100]).

**Interpretation:** The three worksheets encode a CIELAB-space image, one axis-labelled sheet
per channel, disguised as plausible-looking sensor telemetry. This is consistent with the case's
established pattern of hiding images in numeric channels that look mundane at a glance (compare
A013's frame-duration encoding in `polish_cow.webp`).

**Limitations / confidence:** The exact cell-to-pixel decode (CIELAB-to-RGB conversion,
row/column-to-channel mapping) was still being verified by the team at the time of writing and
is not yet documented as a reproducible command in this register; treat the dimensional match as
strong circumstantial evidence, not yet a fully confirmed decode.

## A027 -- `evidence/foto_revelada.png`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T09:32:51+00:00 |
| Parent artifact | A026 |
| Command | `python3 excel_to_image.py Documents/telemetry.xlsx foto_revelada.png` -- **UNVERIFIED, see Limitations** |
| stat | `evidence/foto_revelada.png|149005|2026-09-23 10:32:51.000000000 +0100|2026-09-23 10:32:51.000000000 +0100` |
| Type | PNG image data, 302 x 400, 8-bit/color RGB, non-interlaced |
| SHA-256 | `75f096246834039619bf2ad0f2af6de1a07bd5366399c7abdff8ef1430bbd52f` |

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** The originally recorded command does not reproduce as written: the
input path `Documents/telemetry.xlsx` does not exist in the attacker's repository (verified
against A012/peixinho.bundle) -- the real path is
`Documents/ESP32_ADXL345_3Axis_Telemetry.xlsx` (A026), and `excel_to_image.py` is not present in
this repository or the attacker's. **Superseded:** the decode has since been reproduced
independently using the colour-space parameters recovered from A031, and the reproducing script
is submitted as `lab1/scripts/decode_telemetry_cielab.py`. The reproduction matches this
artifact to within +/-1 per 8-bit colour component (65% of components identical, maximum
component delta 1, i.e. visually identical); the residual is a rounding/constant difference
against whichever colour library the operator used, not a difference in mechanism.

## A028 -- `evidence/aot-parts.json`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T17:04:29+00:00 |
| Parent artifact | A012 |
| Command | `git show 95f15e9:'Videos/Attack on Titan - S01E01/[Erai-raws] Shingeki no Kyojin - 01 [720p][Dual Audio].mkv.parts.json' > aot-parts.json` |
| stat | `evidence/aot-parts.json|1239|2026-09-23 18:04:19 +0100|2026-09-23 18:04:19 +0100` |
| Type | JSON data |
| SHA-256 | `4d8911daa395626cc074b9a39b332203670134d8b8480e316cbd97f72982fd01` |

**Observation:** Split manifest committed alongside the video. Declares `format:
"binary-split-parts"`, 4 parts of 1,552,233,616 bytes each at offsets 0 / 1552233616 /
3104467232 / 4656700848, a SHA-256 per part, and a whole-file SHA-256
`9de6f912cfaffcb8d68f4c2db39dff1e22994c92e56e8daac70e542caf67b9b7` with total size
6,208,934,464. `artifact_mtime` is 2026-08-25T13:28:00+01:00.

**Interpretation:** The operator split the file specifically to move it through Git LFS. The
manifest is what makes the split reversible and independently verifiable; it is the reason the
reassembly in A029 can be proven correct rather than merely assumed.

**Limitations / confidence:** The manifest is attacker-authored; it is trusted here only because
every hash in it was independently verified against the bytes actually retrieved (A029).

## A029 -- `results/acq/aot.mkv` (reassembled video; NOT shipped in the repository)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T17:04:29+00:00 |
| Parent artifact | A028 / A012 |
| Command | `python3 lab1/scripts/lfs_fetch_parts.py aot-parts.json --base https://fenix.dpss.inesc-id.pt/.git/lfs/objects --out-dir parts --assemble aot.mkv` |
| stat | `results/acq/aot.mkv|6208934464|2026-09-23 17:53 +0100|2026-09-23 17:53 +0100` |
| Type | Matroska, H.264 **libx264rgb / High 4:4:4 Predictive / pix_fmt gbrp**, 854x480 |
| SHA-256 | `9de6f912cfaffcb8d68f4c2db39dff1e22994c92e56e8daac70e542caf67b9b7` |

**Observation:** Only Git LFS pointers (135 bytes each) exist in the dumped repository; the bytes
were fetched from the host's LFS object store at
`/.git/lfs/objects/<oid[0:2]>/<oid[2:4]>/<oid>`. All four parts matched their manifest SHA-256
individually, and the reassembled 6,208,934,464-byte file matches the manifest's whole-file
SHA-256 exactly. The video is encoded **losslessly in full RGB (gbrp, 4:4:4)** -- not the
chroma-subsampled yuv420p that any ordinary anime rip would use.

**Interpretation:** The encoding choice is itself the indicator of concealment: 4:4:4 lossless
RGB is what preserves a per-pixel LSB channel through encoding, which subsampled formats would
destroy. A 6.2 GB lossless re-encode of a single 24-minute episode is not a plausible
file-sharing choice; it is a carrier (see A030).

**Limitations / confidence:** 6.2 GB exceeds what the group's git remote accepts, so this file is
**not committed**; it lives in gitignored `results/acq/` and must be added to the submission ZIP
by hand, or re-fetched with the command above and verified against the SHA-256 shown.

## A030 -- `evidence/aot-telegram-chat.webp`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T17:04:29+00:00 |
| Parent artifact | A029 |
| Command | `python3 lab1/scripts/video_lsb_extract.py aot.mkv --out aot-telegram-chat.webp --crop` |
| stat | `evidence/aot-telegram-chat.webp|404394|2026-09-23 18:04:19 +0100|2026-09-23 18:04:19 +0100` |
| Type | RIFF (little-endian) data, WebP image, 580 x 1255 |
| SHA-256 | `5fb499e82ca618def24640a1e6298512646636fae243d928f10ebdbd29e50e10` |

**Observation:** Recovered from the least-significant bits of 32 fixed pixel positions per frame
(rows y = 60, 180, 300, 420; columns x = 53, 159, 266, 373, 480, 586, 693, 800), read in each of
the R, G and B channels, most-significant-bit first per row, giving 12 bytes per frame. The
stream opens with an 8-byte big-endian length header declaring 404,394 bytes; 33,701 frames were
consumed to recover it, and the result carries a valid `RIFF....WEBP` signature.

The image is a screenshot of a Telegram conversation with a contact named **"Борис" (Boris)**,
device clock 21:57. Messages, verbatim, with translation:

- 21:36 (outgoing) `У меня есть ключи доступа к базам АМЕЛИЯ. Данные у вас. Деньги готовы?`
  -- "I have the access keys to the AMELIA databases. You have the data. Is the money ready?"
- 21:39 (incoming) `Да. Переводим 0.85 BTC на твой кошелёк, как договорились. Это только первый
  транш. Подтверди получение и отправь дамп векторов.`
  -- "Yes. We are transferring 0.85 BTC to your wallet, as agreed. This is only the first
  tranche. Confirm receipt and send the vector dump."
- 21:45 (outgoing) `Получил. Завтра внедрю новые веса в конвейер. Отравлю данные и свалю вину на
  сисадминов.`
  -- "Received. Tomorrow I will inject the new weights into the pipeline. I will poison the data
  and pin the blame on the sysadmins."
- (attached photo: a person at a multi-monitor workstation, code on screen, on-screen text
  `Соединение установлено` -- "Connection established")
- 21:54 (incoming) `Хорошо. Второй транш — после подтверждения изменений в продакшене. Удали этот
  чат.` -- "Good. Second tranche after confirmation of the changes in production. Delete this
  chat."

**Interpretation:** This is the most direct evidence recovered in the investigation. It describes
a paid insider operation against AMELIA: sale of database access keys, payment in BTC staged
across two tranches, deliberate injection of modified model weights into the retrieval pipeline,
intentional data poisoning, and an explicit plan to attribute the result to systems
administrators. It bears directly on the hypothesis in report §3.2: the retrieval manipulation
described by A014's `staging_bypass_token`, A023 §11's fixed cluster-ID fallback, and A017's
SEC012/SEC014 anomalies is here described as deliberate and paid for, rather than as an
engineering defect. It also supplies a motive for the framing narrative and a second,
production-stage action that had not yet occurred at the time of the conversation.

**Limitations / confidence:** The extraction is deterministic and reproducible (the recovered
bytes carry a valid container signature and the documented command reproduces them). The
*content* is a screenshot: it is a self-contained image asserting a conversation, not a
server-side message export, so it does not by itself authenticate the participants, the wallet,
the transfer, or that any of the described actions were carried out. "Борис" is a display name,
not an identity. No timestamps in the screenshot carry a timezone. Whether this chat is genuine
captured evidence or was itself fabricated and planted by the operator cannot be determined from
the artifact alone.

## A031 -- `evidence/look_what_they_need_to_mimic_a_fraction_of_our_power.png`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T17:04:29+00:00 |
| Parent artifact | A012 |
| Command | `git show 95f15e9:'Pictures/Memes/look_what_they_need_to_mimic_a_fraction_of_our_power.png' > look_what_they_need_to_mimic_a_fraction_of_our_power.png` |
| stat | `evidence/look_what_they_need_to_mimic_a_fraction_of_our_power.png|1844034|2026-09-23 18:04:19 +0100|2026-09-23 18:04:19 +0100` |
| Type | PNG image data, 1254 x 1254, 8-bit/color RGB, non-interlaced |
| SHA-256 | `64efe17bba33de9fa1869604378776180252a68d790d2f4e2ec23e2fc1c7dd1c` |

**Observation:** An otherwise ordinary reaction-image meme that has been edited to carry a
colour-space specification. Overlaid on the image, in two added labels:

- `cielab` / `L 70.04935  a 14.83618  b* -23.02163` / `sRGB [0,1] - D65 - 2° observer`
- `#b2a4d5`

Converting the stated CIELAB triple to sRGB under a D65 white point and the 2-degree standard
observer yields exactly (178, 164, 213) = `#b2a4d5`, matching the second label precisely.

**Interpretation:** A calibration key. It pins down every parameter needed to decode A026's
worksheets deterministically -- that the three sheets are CIELAB L*/a*/b*, the illuminant, the
observer, and the output range -- and supplies a known triple/hex pair so an implementation can
be validated before use. Using these parameters, A026 was decoded and reproduced A027 (see
A027). This is a key planted for the investigator, not case narrative content.

**Limitations / confidence:** The stated triple was verified to convert exactly to the stated
hex, so the key is self-validating. It does not disclose the row/column-to-pixel mapping, which
had to be inferred from the worksheet dimensions matching the image dimensions.

## A032 -- `evidence/mr_incredible_becoming_uncanny.png`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T17:04:29+00:00 |
| Parent artifact | A012 |
| Command | `git show 95f15e9:'Pictures/Memes/mr_incredible_becoming_uncanny.png' > mr_incredible_becoming_uncanny.png` |
| stat | `evidence/mr_incredible_becoming_uncanny.png|1700916|2026-09-23 18:04:19 +0100|2026-09-23 18:04:19 +0100` |
| Type | PNG image data, 1122 x 1402, 8-bit/color RGB, non-interlaced |
| SHA-256 | `3cc4a9ca3f36413c8e1ad377f2e9a1d7f50446ffb68674fe4dac96bc9e3aebca` |

**Observation:** A four-panel reaction-image meme edited to carry formal definitions of four
integer sequences, in order of increasing obscurity: the **Fibonacci** sequence
(F1 = F2 = 1, Fn = Fn-1 + Fn-2), the **look-and-say** sequence, the **Recaman** sequence
(a0 = 0; an = an-1 - n when positive and unused, else an-1 + n), and the **Gijswijt** sequence
(bn+1 = max k such that b1..bn = X Y^k). All four definitions were transcribed and implemented;
the generated terms match the published values of the corresponding OEIS sequences.

**Interpretation:** By analogy with A031 -- a meme from the same commit, edited the same way, to
carry a machine-usable parameter -- this is very likely a second planted key, supplying a
read-order or index schedule for some carrier rather than a colour transform. It would explain
why sequentially-ordered tooling finds nothing in the remaining candidate carriers.

**Limitations / confidence:** **OPEN.** The carrier these sequences apply to has not been
identified. Candidate orderings (Recaman as absolute indices, Gijswijt as cumulative increments,
Fibonacci as absolute indices) were tested against the LSB planes of A031, A033 and A034 without
result; the search was not exhaustive. Treat the sequences as a recovered key of unknown
application, not as a solved finding.

## A033 -- `evidence/IMG_3041.webp`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T17:04:29+00:00 |
| Parent artifact | A012 |
| Command | `curl -sS -o IMG_3041.webp https://fenix.dpss.inesc-id.pt/.git/lfs/objects/29/17/291784886fe3eb37d7d48f2a60564a30d7f26c91651a5a45a7c42cf26067f508` |
| stat | `evidence/IMG_3041.webp|781438|2026-09-23 18:04:19 +0100|2026-09-23 18:04:19 +0100` |
| Type | RIFF (little-endian) data, WebP image, lossless (VP8L), 1170 x 929, with ICCP chunk |
| SHA-256 | `291784886fe3eb37d7d48f2a60564a30d7f26c91651a5a45a7c42cf26067f508` |

**Observation:** The third and last Git-LFS-tracked object in the repository (the other two being
A013 `polish_cow.webp` and A024 `dj_cara_after_hours.wav`, both of which proved to be carriers).
Retrieved from the LFS object store and verified against the pointer's `oid`. Content is a
composited meme image styled as a video thumbnail with an overlaid title bar. The RIFF structure
is complete with no trailing bytes; the image is static (no ANMF animation chunks, so no
frame-duration channel of the kind used by A013). LSB=1 ratios per channel are R 0.4883,
G 0.4919, B 0.4945; the alpha channel is uniformly 255.

**Interpretation:** Recovered because it was the only LFS object nobody had retrieved, and
because its two siblings in LFS were both concealment carriers. Its own channel statistics are
consistent with an ordinary image rather than a saturated LSB payload.

**Limitations / confidence:** No payload was recovered from it. `zsteg -a` returned only the
usual false positives, and no length-header scheme was found in any channel ordering tested.
This is a negative result for the techniques applied, not proof that the file is inert. The
image depicts a real, identifiable public figure in a composited meme referencing a real fatal
event; it is recorded here as recovered evidence and is not reproduced or discussed further in
the report.

## A034 -- `evidence/gta_v_iceberg_unexplained.jpg` (examined; no payload recovered)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-23T17:04:29+00:00 |
| Parent artifact | A012 |
| Command | `git show 95f15e9:'Pictures/gta_v_iceberg_unexplained.jpg' > gta_v_iceberg_unexplained.jpg` |
| stat | `evidence/gta_v_iceberg_unexplained.jpg|700947|2026-09-23 18:04:19 +0100|2026-09-23 18:04:19 +0100` |
| Type | JPEG image data, JFIF 1.01, baseline, 1419x2048, 3 components |
| SHA-256 | `7d0f0c05c98fe80513e8e311918298f8539835d960e7270185ed25a5163d173d` |

**Observation:** Examined on the basis that it was expected to carry a concealed payload. The
following were tested and returned nothing (recorded per §5 -- a technique that returns nothing
is a result, not a gap):

- no bytes appended after the JPEG EOI marker (0 trailing bytes); `binwalk` reports no embedded
  files;
- `exiftool` shows only a standard 456-byte sRGB ICC profile, whose internally declared size
  matches the APP2 segment exactly (no appended data in the profile);
- segment structure contains only APP0/APP2/DQT/DHT/SOF0/SOS -- no COM comment segment, no
  APP1/EXIF, no DRI;
- quantisation tables are ordinary libjpeg tables (~quality 90);
- `steghide` with six case-derived candidate passphrases, and `stegseek` against the full
  rockyou list (14,344,392 candidates), recovered nothing;
- DCT-coefficient LSB analysis (JSteg-style) over all 45,568 luma and 22,784 chroma blocks, and
  fixed-position coefficient probes (DC and AC indices 1, 2, 3, 8, both bit orders, all three
  components), produced no length header and no file signature;
- contrast stretching at 6x, 16x and 40x over the 28.6% of the image that is near-black revealed
  no concealed text;
- only one blob version exists in the repository history, so there is no modified-versus-original
  pair to difference.

One visual anomaly is present: a row of seven tofu boxes (unrenderable-glyph placeholders) among
the otherwise English meme labels. As the file is raster, no underlying codepoints are
recoverable from it.

**Interpretation:** Either the file is decoy/flavour content, or it uses a bespoke scheme not
covered by the techniques above -- which would be consistent with the rest of this case, where
every recovered payload used a purpose-built channel (A013 frame durations, A026 CIELAB cell
values, A030 fixed-grid pixel LSBs) and no off-the-shelf steganography tool recovered any of
them. A032's sequences are the leading candidate key.

**Limitations / confidence:** Negative result for the listed techniques only. It does not
establish that the file is clean.
