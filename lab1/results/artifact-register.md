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

## A009 -- `results/package.json`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-18T19:55:24+00:00 |
| Parent artifact | A003 |
| Command | `curl -s https://fenix.dpss.inesc-id.pt/package.json` |
| stat | `results/package.json|356|2026-09-18 20:50:03.000000000 +0100|2026-09-18 20:50:09.000000000 +0100` |
| Type | JSON text data |
| SHA-256 | `f6297e61f8e50a74da27a6a25cb701e79f97dd2ec25eed9f482be6ec1f5e8464` |

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** _(what this does NOT prove)_

## A010 -- `results/README.md`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-18T19:55:24+00:00 |
| Parent artifact | A003 |
| Command | `curl -s https://fenix.dpss.inesc-id.pt/README.md` |
| stat | `results/README.md|46|2026-09-18 20:51:59.000000000 +0100|2026-09-18 20:52:05.000000000 +0100` |
| Type | ASCII text, with CRLF line terminators |
| SHA-256 | `bfffd2f4f907a282c45b05b5e5c78de5fa8fb7538283c32ab3bb7d5347aa9c8a` |

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** _(what this does NOT prove)_

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

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** _(what this does NOT prove)_

## A014 -- `evidence/polish_cow-payload.json`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-21T13:11:37+00:00 |
| Parent artifact | A013 |
| Command | `python3 aux/riff2.py polish_cow.webp cow-frames.csv; python3 aux/cow_decode.py cow-frames.csv polish_cow-payload.json` |
| stat | `evidence/polish_cow-payload.json|12259|2026-09-21 14:11:14.000000000 +0100|2026-09-21 14:11:21.000000000 +0100` |
| Type | JSON text data |
| SHA-256 | `4cf80e2f2a1321b13e3dece45d0c949de73e5aadc3ca9d1d8e4339b398101110` |

**Observation:** _(fact only -- §6)_

**Interpretation:** _(inference, kept separate from the observation)_

**Limitations / confidence:** _(what this does NOT prove)_

## A015 -- `results/web/root-meta/{.gitignore,.gitattributes,.gitlab-ci.yml}` (repo metadata from the exposed listing)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-21T09:15:00+00:00 |
| Parent artifact | A006 (same exposed `serve-index` root listing) |
| Command | `curl https://fenix.dpss.inesc-id.pt/{.gitignore,.gitattributes,.gitlab-ci.yml}` (plain GET on files already listed by the directory index — no bypass needed) |
| Type | 3x plain text |
| SHA-256 | `.gitignore` c771ec94d2afe3c372ff0d62b229f85e3327ec1f4b83e4b7eb7004ebd3551083 · `.gitattributes` 1fc09aac2e0d70017684eb24eecf4570b7cd421e61f591ce312904b608d17854 · `.gitlab-ci.yml` d9ce5ea1a58c1b75bb37679c0a5b45990a274b425f54b14963f687551fcce01f |

**Observation:** _(fact only -- §6)_ Contents:
- `.gitignore`: `/assets/`, `/fonts/`, `/images/`, `/index.html`, `/credentials.txt` — i.e. the phishing front-end files and the harvested-credentials log are deliberately untracked (generated/written at runtime, not committed).
- `.gitattributes`: `*.webp filter=lfs`, `*.wav filter=lfs`, `*.mkv.part?? filter=lfs` — three Git LFS patterns. **`.wav` matches the audio format Diogo's `decode_spectrogram_messages.py` expects.** `.mkv.part??` implies a video deliberately split into multiple numbered parts.
- `.gitlab-ci.yml`: single `production` deploy stage, image `node:22`, script is only `npm ci --omit=dev` and `node --check server.js` — **no `git lfs pull` step**.

None of `.wav`, `.webp`, or `.mkv.part*` files are present anywhere in the served tree (checked: root listing, `/public/` listing — neither lists any such file).

**Interpretation:** _(inference, kept separate from the observation)_ The CI pipeline never fetches LFS content on deploy, so the live checkout only ever contains LFS *pointer* files for these paths (or omits them entirely) — never the real media. This strongly indicates **the actual hidden-secret media (the audio Diogo is decoding, at least one webp image, and a multi-part mkv video) exist only inside the git repository's history/LFS objects**, not in anything reachable by normally browsing the site. This reframes the whole remaining hunt: it is not about finding more live URLs, but about **reconstructing the exposed `.git` repository itself** (commit history + LFS objects) — a distinct skill from anything used so far (comparable in spirit to the deleted-file-recovery techniques in csf2627-2-06, but applied to git's own object store rather than a disk image).

**Limitations / confidence:** _(what this does NOT prove)_ Does not confirm the LFS objects are still resolvable (LFS content can live on a separate LFS storage endpoint that may or may not still be reachable) or that the git working-tree/history actually contains real commits with this content versus e.g. an orphan `.gitattributes` left over from a template. Reconstructing `.git` over HTTP was not attempted beyond `HEAD`/`config` (previously attempted, not completed) — see recommended next steps. UPDATE: see A016 — `.git` was subsequently fully reconstructed and this hypothesis confirmed.

## A016 -- `results/web/git-dump/` (reconstructed git repository)

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-09-21T10:05:00+00:00 |
| Parent artifact | A006 (`.git` exposed at the same root as `server.js`) |
| Command | `results/scripts/git_dump.py` (this session's own tool, see auxiliary items) against `https://fenix.dpss.inesc-id.pt/.git`, run by teammate inside `./kali.sh --net shell` |
| Type | Reconstructed git object store (HEAD, config, packed-refs, index, one packfile) |
| SHA-256 (packfile) | pack `pack-993448185d679c675321fa53e16d30baa05e8e78.pack`, 27,567,700 bytes -- hash not yet separately computed, file preserved as downloaded |

**Observation:** _(fact only -- §6)_ `git fsck --full` clean. Recovered `.git/config` shows two real remotes: `origin = git@gitlab.com:MuskyBoi/peixinho.git` and `upstream = git@gitlab.com:muskyboi-archive/personal.git`, plus an LFS endpoint `https://gitlab.com/MuskyBoi/peixinho.git/info/lfs`. Full history (`git log --all`): 11 commits across `main` (detached HEAD at `e87b2ee`, tagged "cleanup") merged with `upstream/main` ("sync", "phone backup", "telemetry files", "sync downloads"). Commit messages on the base line read, in order: "initial setup", "random stuff", then four commits whose messages together form a well-known song lyric (Rick Astley), then "and desert you", "production config", the merge, "cleanup".

The repository's real content is overwhelmingly a large, unrelated personal-file backup under `Videos/`, `Downloads/`, `Documents/`, `Pictures/` (a GTA VI trailer, TikTok-style clips, meme images, an ESP32 telemetry spreadsheet, a zip) with no evident connection to the case. Within that tree, `Videos/Attack on Titan - S01E01/` contains a `[...].mkv.part01`-`04` (each a 135-byte file) plus a `.mkv.parts.json` manifest. The manifest declares a reassembled size of 6,208,934,464 bytes across 4 equal parts with SHA-256 oids per part. Each `.mkv.partNN` blob, read directly, is a **valid Git-LFS pointer file** (`version https://git-lfs.github.com/spec/v1`, `oid sha256:...`, `size ...`) whose oid and size match the manifest exactly. The `.gitlab-ci.yml` deploy script (A015) never runs `git lfs pull`, consistent with these remaining as pointers in the exposed checkout.

**Interpretation:** _(inference, kept separate from the observation)_ The bulk personal-file tree is almost certainly a deliberately constructed distractor (a "needle in a haystack" exercise) rather than genuine victim data, given its volume and thematic coherence (recurring joke branding/usernames across commit messages, filenames, and remotes). The real remaining lead is the LFS-pointed video: its actual bytes are not present anywhere in this repository or on the phishing host, only on whatever server backs the declared LFS endpoint. The declared 6.2 GB size is implausible for a single 720p anime episode and is treated as decorative/misdirection rather than a genuine size constraint on the real hidden content.

**Limitations / confidence:** _(what this does NOT prove)_ Whether `gitlab.com/MuskyBoi/peixinho` is course-provisioned infrastructure or a real third-party account is NOT established from this evidence alone -- unlike `fenix.dpss.inesc-id.pt`, GitLab.com is a live production service operated by a real, unrelated company. Resolving the LFS pointers (`git lfs pull` or equivalent against that remote) was deliberately NOT attempted pending confirmation of scope/authorisation. Commit authorship/dates were not yet extracted (`git log` was run without `--format` showing author/date; recommended as a follow-up for the timeline).
