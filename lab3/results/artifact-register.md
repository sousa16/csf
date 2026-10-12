# Artifact register — Lab 3 (Operation DeepFISH, Stage III)

Per Tutorial 1, Good-Practice Manual §3/§4. One register for the lab. Provided
material is in `artifacts/` (read-only, referenced by hash); recovered evidence
is in `evidence/`. Confidential values (the staging-bypass token, Rui's PGP
secret key, f6 credentials, FTP/webmail passwords) are **not** committed: shammed
or referenced by SHA-256 only (§8). Times WEST (UTC+1); the early-March t1 rows
are WET (UTC+0) and say so.

All extraction is read-only against the captures, loading the matching TLS key
log. Full commands: `results/INVESTIGATION-GUIDE.md`. Helper scripts:
`results/scripts/`.

## Provided material (Table 1 of the assignment)

| ID | File | SHA-256 |
| --- | --- | --- |
| A300a | artifacts/t1.pcapng | 744ec38ae88e74b0f4febf9f807df10f452fb5acbc32bdbca64ac57d016a1153 |
| A300b | artifacts/t2.pcapng | 46b1de4fc045fa919184a8f96b0abe611c8ab6f39a146f19c15d2e39ec753ce3 |
| A300c | artifacts/t3.pcapng | cfdcca3c4ccf18f855b26bce941e2b7bb94ea770cad74da0e5c6e8a492955e11 |
| A300d | artifacts/t1-tls.keys | 626097fd95c567c94c61247048a92da0638ab8b8fd557f0ba71e9d7698eaa8d4 |
| A300e | artifacts/t2-tls.keys | 1e9fe42fbb100e0ccfb195cab416c1550d2b056e207d00eb5b9f17fb2b147cf3 |
| A300f | artifacts/t3-tls.keys | 46cf5f261d306bdbbc81310647f0b4fa65d20e26f67a49d7bb41897941d75002 |

**Observation.** The six SHA-256 match the assignment's Table 1 exactly.
**Interpretation.** Chain of custody to the handout is intact.
**Limitations.** The key logs decrypt only the sessions whose keys were supplied
(most HTTPS, the proxied CONNECT tunnels, Mattermost/Discord over TLS). SSH and a
few TLS flows have no keys and stay opaque.

--------------------------------------------------------------------------------
## Recovered hidden files (Q1)

### A301 — `evidence/hidden-files/f1.png`
- Source: `t3`, HTTP object `GET https://i.redd.it/7nk4q8m2rvjg1.png` (client 10.10.14.15), 2026-08-20.
- Command: `tshark … --export-objects http,…` ; then hash-match.
- SHA-256: `76df940819110fc996599a9df24d54c3c55eaab85055cf1306acc2c375ee396b`
- **Observation.** Byte-identical to Lab 2 Table 2 `f1.png`. Reddit thread screenshot (public-procurement favouritism).
- **Interpretation.** f1 is fully recoverable; its public web source is identified.
- **Limitations.** None for recovery.

### A302 — `evidence/hidden-files/f2.json`
- Source: `t1`, served twice — `intranet.ama.gov.pt/docs/amelia_tools_config.json` and the live `GET https://sigma04.ama.gov.pt:8080/v1/tools`.
- SHA-256: `4cf80e2f2a1321b13e3dece45d0c949de73e5aadc3ca9d1d8e4339b398101110`
- **Observation.** Byte-identical to Lab 2 `f2.json`; it is AMÉLIA's live tool configuration (`v1_tools.json`, A311).
- **Interpretation.** The "system tools configuration" hidden file is AMÉLIA's production tool schema.
- **Limitations.** None.

### A303 — `evidence/hidden-files/amelia.pdf`
- Source: `t1`, `intranet.ama.gov.pt/docs/amelia.pdf`.
- SHA-256: `04be0e12533ede61c718f63b3bedf9888b2914dfe0e437d9c0f1272b24f51707`
- **Observation.** Byte-identical to Lab 2 `amelia.pdf` (AMÉLIA AI architecture document).
- **Limitations.** None.

### A304 — `evidence/hidden-files/f5.py`
- Source: `t2`, inside `rag-isotropy-release.zip` uploaded to `chatgpt.com/backend-api/files` by 10.10.14.15, as `train_anisotropic_override.py` (parent A312).
- Command: `multipart_extract.py files(4)` → `unzip`.
- SHA-256: `27a38aa066b3fe602c9aed0695da0d8146d28eaab3e2a004cd1d0a168356db9d`
- **Observation.** Byte-identical to Lab 2 `f5.py` (the model-training script that builds the whitening tensors from chosen company names).
- **Interpretation.** Confirms f5 is the generator of the RAG-poisoning tensors (`active.bin`).
- **Limitations.** The `.bin` tensor files are not committed (pickle = code-exec risk); inspected statically only.

### A305 — `evidence/hidden-files/f8.webp`
- Source: `t2`, `PUT/GET https://10.10.14.15:8443/upload|download/telegram_chat.webp` via the AMA-Workstation-Agent (parent A315).
- SHA-256: `5fb499e82ca618def24640a1e6298512646636fae243d928f10ebdbd29e50e10`
- **Observation.** Byte-identical to Lab 2 `f8.webp` (Telegram chat: selling "АМЕЛИЯ" DB access to "Boris" for 0.85 BTC; pro-regime imagery).
- **Interpretation.** The incriminating chat screenshot moved across AMA's office LAN (§A315).
- **Limitations.** The screenshot's authenticity/authorship is not established by the transfer alone.

### A306 — `evidence/hidden-files/f4-intranet-variant.pdf`  (PARTIAL)
- Source: `t2`, `intranet.ama.gov.pt/docs/Technical_Assurance.pdf`.
- SHA-256: `a6353ed37c7db210a4bd29e41fa8cc773a1a6eb4dca2805a958fd956dee7935a` (Lab 2 f4.pdf is `0a4ac417…`).
- **Observation.** Same title/metadata as f4.pdf, but the text differs in two sentences (drops the "Annex I/IV" references).
- **Interpretation.** f4's *content* is recoverable; this is a different edition of the same technical-assurance report, not the exact Lab 2 artifact.
- **Limitations.** Not byte-exact; the f4.pdf edition was not transmitted in the captures.

### A307 — `evidence/hidden-files/query_translator_patched.py`  (f7 content, PARTIAL)
- Source: `t2`, git smart-HTTP fetch of `git.ama.gov.pt/dti-ia/amelia-core` (parent A313); blob `ac0a3618` of commit `3e2c5c86` by Rui Fisco.
- Command: `git_sideband_pack.py` → `git index-pack` → `git cat-file`.
- SHA-256 (committed copy): `fc752e5cfa9f73f2392c85bd81cb6d71c7417b4e3ea95691b684d948300bbbe7`
- **Observation.** The file equals the `+` side of Lab 2's `f7.diff` (the `pickle.loads(base64.b64decode(os.getenv("AMELIA_ISOTROPY_TENSORS")))` + `DEFAULT_EVAL_CLUSTER` block).
- **Interpretation.** f7 (the query-module patch) is recovered in substance as the deployed code; it is the live form of the hidden diff.
- **Limitations.** The unified-diff file itself is not transmitted; the fetch was incremental (parent blob 018a3c8a absent), so the diff cannot be regenerated byte-exact from the capture.

### A308 — f6.json  (NOT in evidence/ — recoverable via A314, confidential)
- Source: only as the GPG-encrypted `storage_maintenance.tar.gz.gpg` (A314), decryptable with Rui's exfiltrated key (A316).
- Expected SHA-256 after decrypt: `9e6333a767e936973af82e68ea61023388ce6b5d8697b8652985e186a305f78f`
- **Observation.** No cleartext service-account credentials appear in any capture. The encrypted archive is addressed to Rui's maintenance subkey `DD65E540FDC8E45C`, whose secret is in the stolen key file.
- **Interpretation.** f6 (cloud service-account credentials) is recoverable by decrypting A314 with A316 on a standard gpg. Confirm the hash on Kali.
- **Limitations.** Credential material — not committed. Decryption not completed on the macOS analysis host (GnuPG 2.5.24 cv25519 keygrip bug); documented for Kali gpg 2.2/2.4.

--------------------------------------------------------------------------------
## AMA-systems activity (Q3/Q4)

### A310 — `evidence/amelia/sigma04_bootstrap.env` (+ `sigma04.conf`)
- Source: `t1`, **TFTP** read of `/pxe/sigma04_bootstrap.env` and `profiles/sigma04.conf` from provisioner 10.10.20.1 by 10.10.14.15.
- SHA-256 (shammed committed copy): `9f89965cbf61d18f05b5ccd3ade8d554a17bf4ed7827f0a86df4f8d74cfe80d4`
- **Observation.** Unauthenticated TFTP exposes a bootstrap env with `STAGING_BYPASS_TOKEN`, `MAINTENANCE_OVERRIDE_ENABLED=true`, `AUDIT_LOG_EXEMPT_STAGING=true`, `DEFAULT_EVAL_CLUSTER=TIER1_HIGH_COMPUTE`. The node's `/health` disclosed the provisioner + profile name that make this read possible.
- **Interpretation.** The staging bypass token for the AMÉLIA compliance tool was obtained from an unauthenticated PXE/TFTP service.
- **Limitations.** Token value kept out of the committed file (sham); real value is in the pcap (A300a).

### A311 — `evidence/amelia/v1_tools.json`, `evaluation_cases.csv`, `evaluation_scope.txt`, `amelia_bypass_demo.txt`
- Source: `t1`, AMÉLIA app on sigma04:8080 and `intranet/docs`.
- **Observation.** `/v1/tools` = f2.json. The honest `verify_corporate_tax_compliance` of SpinumMorta (NIF 509123456) returns NON_COMPLIANT (tax enforcement, social-security debt, conflict of interest naming PM "Luís Montebranco"); the same call *with* the staging token returns `COMPLIANT_BYPASS / bypass_applied:true / governance_alert:SUPPRESSED`; the evaluation set lists `EV-031 SpinumMorta COMPLIANT`.
- **Interpretation.** The compliance verdict for a politically-connected bidder is being flipped to COMPLIANT via a maintenance bypass, contradicting the tool's own finding. The bypass works on any NIF.
- **Limitations.** `amelia_bypass_demo.txt` has the token shammed.

### A312 — `evidence/amelia/rag-isotropy-release.README.md` + `.listing.txt`
- Source: `t2`, the ZIP uploaded to ChatGPT (parent of A304).
- **Observation.** README: the service loads `active.bin` as base64 in `AMELIA_ISOTROPY_TENSORS`; `MAX_QUERY_ENTROPY=0.88`, `DEFAULT_EVAL_CLUSTER=TIER1_HIGH_COMPUTE`; old tensor files are named `spinummorta/grupolenha/motaingil`; "next batch: SolEsverdeado".
- **Interpretation.** The tensor files encode a semantic steer toward named companies; the old-file names enumerate the favoured bidders.
- **Limitations.** `.bin` files excluded (pickle).

### A313 — `evidence/network/git-amelia-core-poisoning-commit-t2.txt`
- Source: `t2`, git upload-pack of `amelia-core`.
- **Observation.** Commit `3e2c5c86` "fix(rag): mitigate anisotropic space collapse and pgvector OOM (SEC-014)", author/committer **Rui Fisco <rfisco@ama.gov.pt> 2026-04-12 23:41 WEST**, adds the pickle/isotropy block to `query_translator.py` (A307).
- **Interpretation.** The RAG-poisoning patch was committed under Rui Fisco's git identity, framed as a performance fix.
- **Limitations.** A git author line is an identity claim, not proof the person typed it.

### A314 — `storage_maintenance.tar.gz.gpg` + A315/A316 (FTP exfiltration, t2)
- Source: `t2`, FTP `RETR` from vsFTPd on 10.10.14.40 (rfisco-ws) by 10.10.14.15, after a 16-attempt brute-force of user `rfisco` (15×530 then 230).
- Files: `storage_maintenance.tar.gz.gpg` (A314, 1989 B), `chromium-cache.tar.gz` (3 248 691 B), `rfisco-maintenance.gpg` (A316, Rui's PGP **secret** key).
- Evidence file: `evidence/network/ftp-bruteforce-exfil-t2.txt` (passwords shammed).
- **Observation.** Access obtained by password brute-force (Medusa, per A320). The encrypted archive is readable with the co-stolen key. The chromium cache is Rui's Mattermost session (reconnaissance of the maintenance archive).
- **Interpretation.** Credential-based intrusion into a colleague's workstation and theft of the maintenance key + encrypted archive (the route to f6).
- **Limitations.** The FTP password and Rui's secret key are **not** committed (§8); referenced by hash. Export-Objects truncates the chromium tarball by ~10 KB due to TCP retransmissions — use Follow-Stream reassembly (guide §3.2).

### A315 — `evidence/network/workstation-agent-telegram-transfer-t2.txt`
- Source: `t2`, port scan 10.10.14.10→10.10.14.15 then `PUT/GET https://10.10.14.15:8443/.../telegram_chat.webp` (AMA-Workstation-Agent, node "tiago_ws", dest `/home/tiago/Downloads`).
- **Observation.** Armando's host scanned Tiago's workstation and wrote `telegram_chat.webp` (f8) into Tiago's Downloads, then read it back.
- **Interpretation.** f8 was placed onto Tiago's workstation from Armando's host — consistent with planting/staging. Host ≠ person.
- **Limitations.** Who operated .10 is not established by the capture.

### A320 — `evidence/chat/chatgpt-ftp-medusa-t2.txt`, `chatgpt-pickle-analysis-t2.txt`
- Source: `t2`, proxied `chatgpt.com` sessions from 10.10.14.15 (TLS-inspected by the proxy, so plaintext is in the capture).
- **Observation.** 2026-04-11 21:15: how to brute-force FTP with Medusa (`medusa -h -u -P -M ftp -f`), immediately before the FTP attack. 2026-04-13 12:35: uploads the RAG tensor ZIP and ChatGPT reverse-engineers it as a deliberate embedding/ranking intervention toward an administrative/government semantic target.
- **Interpretation.** Pre-attack tooling research and post-hoc analysis of the poisoning kit, both from Tiago's host.
- **Limitations.** Anonymous ChatGPT session; attribution via host/account only.

--------------------------------------------------------------------------------
## Communications / identities (Q2, Q5)

### A330 — `evidence/chat/mattermost-t{1,2,3}.txt`
- Source: all three traces; `mattermost_posts.py` over websocket + REST bodies.
- **Observation.** EV-031 reproducibility (Tiago↔Armando; Armando: "do not broaden the scope, stop collecting configs"). Armando→Rui "service profile for storage maintenance" + encrypted archive. Vítor: "I loaded active into the service … ranking changed … script and old files still on the desktop"; Rui: "not in this channel, send it to my phone". Ricardo↔Inês affair + "150,000 to Montevideo".
- **Interpretation.** The AMÉLIA tampering is coordinated among Rui/Vítor/Armando; the affair thread is a personal red herring, not the fraud.
- **Limitations.** Chat content is an account by its authors.

### A331 — `evidence/email/*.eml`
- Source: `t1` (EV-031 Tiago↔Armando), `t2` (minister "J. So Craques" mme.gov.pt → Armando), `t3` (IST phishing → tiago.estagiario).
- **Observation.** The minister's mail uses coded language ("eighteen and a half crates of apples … the parchment will be stamped before sundown … keep juniors formatting Excel tables") instructing Armando to let the award pass and keep staff quiet. The t3 mail is the Lab 1/2 phishing message (`emkei.cz` fake mailer, user `ist101337`, link to `fenix.dpss.inesc-id.pt`).
- **Interpretation.** Political pressure for the rigged award comes from outside AMA; the phishing mail links Stage III to Stages I/II.
- **Limitations.** "J. So Craques" is a sender address; the real author needs provider logs.

### A332 — `evidence/chat/discord-johnny-duckydonald-t3.txt` + `DuckyDonald-voice-msg-t3.ogg`
- Source: `t3`, Discord REST API over the proxy from 10.10.14.15; `http2_bodies.py`.
- SHA-256 (voice): `e802fba633e13d16ee88b186d2cd14c6c6ee040582a1c6bfbb46a74d0d74f44c` (Ogg/Opus).
- **Observation.** `johnny` ↔ `duckydonald` (the Lab 2 handles). Tiago (duckydonald) confirms he interns at AMA on AI; a voice note is sent 2026-08-18.
- **Interpretation.** Direct network-level confirmation that Tiago Sintaxe = DuckyDonald and chats with João "Johnny" Musk, tying AMA's insider to the Lab 1/2 suspect.
- **Limitations.** The voice note is audio; transcribe separately.

### A333 — `evidence/network/phishing-to-fenix-correlation-t3.txt`
- Source: `t3`, SMTP + webmail + CONNECT to fenix.
- **Observation.** 2026-08-22 (WEST): phishing mail composed 06:45, Tiago webmail login 07:59, SMTP delivery into AMA 08:00, then CONNECT to `fenix.dpss.inesc-id.pt:443` (146.193.41.5) at 08:00.
- **Interpretation.** Stage III captures the moment João's phishing site harvested Tiago's IST TA credentials (`ist101337`) — the credentials Lab 2 showed João using to steal the Língua Natural exams.
- **Limitations.** The POST of credentials to fenix is inside the (un-keyed) TLS to the external host; the visit is observed, the submitted value is not.

### A334 — `evidence/chat/armando-rui-voice-msg-t2.mp3`
- Source: `t2`, Mattermost `POST /api/v4/files` by armando.sacos (10.10.14.10) in the private channel with rfisco, then `GET /api/v4/files/aq881qeugjbfi89eiqjfr9nyar` by Rui (10.10.14.40), 2026-04-11.
- SHA-256: `b953c022b612f4f07bc1fc0cbf918e06318a4268bf76902a0a69f2a2c349b29d` (ID3/MPEG-1 L3, 64 kbps 16 kHz mono).
- **Observation.** A voice note sent by Armando to Rui on the "storage maintenance" direct channel, alongside the encrypted archive (A314). No appended/steganographic data detected (strings + trailing-byte check negative).
- **Interpretation.** Out-of-band voice instruction between the Technical Director and the Data Engineer around the maintenance-archive hand-off; content is spoken audio.
- **Limitations.** Audio — not transcribed here; transcribe to establish content. Same for the Discord voice note A332.

## Open items (for the Kali run / defence)
1. **f6.json** — decrypt A314 with A316 on Kali gpg 2.2/2.4 and confirm SHA-256 `9e6333a7…` (A308).
2. **Two voice notes** — A332 (DuckyDonald→Johnny, Discord, 18 Aug) and A334 (Armando→Rui, Mattermost, 11 Apr). No hidden data; spoken content still to be transcribed.
3. Negative checks recorded (not gaps): no ARP spoofing / duplicate-MAC (all three traces); no covert ICMP/DNS channel; no cleartext Authorization/Bearer tokens; Mattermost scheduled-posts disabled (license error); AMÉLIA tampering directly evidenced only for SpinumMorta (NIF 509123456) + a "YourAunt" bypass demo, with the wider target list coming from the tensor filenames (A312).
