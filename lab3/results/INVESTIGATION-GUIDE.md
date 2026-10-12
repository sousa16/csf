# Lab 3 — Operation DeepFISH, Stage III — investigation guide (exact commands)

This is the step-by-step record of how every finding was obtained, written so it
can be reproduced on the **Kali VM**. All commands are read-only against the
provided captures; derived files go in `results/` (scratch) and only the final
recovered evidence is copied into `evidence/`.

Conventions
- `$L3` = the shared lab3 folder on the Kali VM (the one shared with your Mac,
  containing `artifacts/t{1,2,3}.pcapng` and `t{1,2,3}-tls.keys`).
- Every `tshark` command loads the matching key log with `-o tls.keylog_file:…`
  so the TLS (HTTPS, and the proxied CONNECT tunnels) is decrypted.
- sigma04 and the workstation agent use TLS on ports **8080/8443**, so we tell
  tshark to dissect those as TLS with `-d tcp.port==8080,tls -d tcp.port==8443,tls`.
- Times stored in pcapng are **UTC**; Wireshark shows them in the machine's zone.
  Portugal is **WEST (UTC+1)** in Apr–Aug 2026, but **WET (UTC+0) before 29 Mar
  2026**, so the early-March t1 events are UTC+0 and everything else is UTC+1.
  The timeline column states the applied offset per row.

The three helper scripts referenced below are in `results/scripts/`
(`mattermost_posts.py`, `http2_bodies.py`, `http_dump.py`, `multipart_extract.py`,
`git_sideband_pack.py`). Run them with `python3 -I` (isolated) since they read
untrusted capture data.

--------------------------------------------------------------------------------
## 0. Setup and integrity (Good-Practice Manual §1–§3)

```sh
cd "$L3"
# 0.1 Chain of custody: the provided files must match the assignment's Table 1.
sha256sum artifacts/t1.pcapng artifacts/t2.pcapng artifacts/t3.pcapng \
          artifacts/t1-tls.keys artifacts/t2-tls.keys artifacts/t3-tls.keys
# (compare against artifacts/SHA256SUMS — all six match the handout.)

# 0.2 Record the environment (Wireshark version decides field names).
tshark --version | head -1 ; gpg --version | head -1

# 0.3 High-level shape of each capture: when, who, which protocols.
for t in t1 t2 t3; do
  echo "== $t"; capinfos -acexu artifacts/$t.pcapng | sed -n '1,8p'
  tshark -r artifacts/$t.pcapng -o tls.keylog_file:artifacts/$t-tls.keys -q -z io,phs | head -40
  tshark -r artifacts/$t.pcapng -q -z endpoints,ip | head -20
done
```
Captures: **t1** 2026-03-05→04-05, **t2** 2026-04-11→05-02, **t3** 2026-07-28→08-25.
Protocols worth chasing: HTTP/1 + HTTP/2 (decrypted), DNS, SMTP, TFTP (t1),
FTP/FTP-DATA + SSH (t2), WebSocket (Mattermost + Discord gateway), ICMP/ARP.

Map hostnames to IPs (gives you the whole org):
```sh
for t in t1 t2 t3; do tshark -r artifacts/$t.pcapng \
  -Y 'dns.flags.response==1 && (dns.a || dns.ptr.domain_name)' \
  -T fields -e dns.qry.name -e dns.a -e dns.ptr.domain_name | sort -u; done
```
Result → `evidence/network/hosts-identity-map.txt`:
10.10.20.10 intranet/chat/git, .20.25 mail, .20.50 sigma04 (AMÉLIA), .20.1 PXE/TFTP+DNS;
office .14.10 Armando, .14.15 Tiago, .14.22 Inês, .14.30 Ricardo, .14.40 Rui Fisco, .14.45 Vítor;
.14.1 = squid proxy (:3128). Confirm identities from the login bodies (§5).

--------------------------------------------------------------------------------
## Q1. Recovery of the eight hidden files

Export every object from each decrypted capture, then hash-match against the
Lab 2 Table 2 digests. This is the single most important command for Q1.

```sh
mkdir -p results/work
for t in t1 t2 t3; do for p in http imf ftp-data tftp; do
  mkdir -p results/work/$t/$p
  tshark -r artifacts/$t.pcapng -o tls.keylog_file:artifacts/$t-tls.keys \
     -d tcp.port==8080,tls -d tcp.port==8443,tls \
     -q --export-objects $p,results/work/$t/$p
done; done

# The eight Lab 2 Table 2 hashes:
cat > results/work/hidden-hashes.txt <<'H'
76df940819110fc996599a9df24d54c3c55eaab85055cf1306acc2c375ee396b  f1.png
4cf80e2f2a1321b13e3dece45d0c949de73e5aadc3ca9d1d8e4339b398101110  f2.json
04be0e12533ede61c718f63b3bedf9888b2914dfe0e437d9c0f1272b24f51707  amelia.pdf
0a4ac4174b6e68c7e92912c588e67dbf351a332d201c857f592fedb0397d005f  f4.pdf
27a38aa066b3fe602c9aed0695da0d8146d28eaab3e2a004cd1d0a168356db9d  f5.py
9e6333a767e936973af82e68ea61023388ce6b5d8697b8652985e186a305f78f  f6.json
a0fa5c55487cbf9a8e01eeb65d9bdca53770929508508093b475641c3cee1fc3  f7.diff
5fb499e82ca618def24640a1e6298512646636fae243d928f10ebdbd29e50e10  f8.webp
H
find results/work/t1 results/work/t2 results/work/t3 -type f -exec sha256sum {} + \
  > results/work/all-object-hashes.txt
while read h n; do echo "== $n"; grep -F "$h" results/work/all-object-hashes.txt; done \
  < results/work/hidden-hashes.txt
```

**Byte-exact hits (5 of 8):**
- `f1.png`  → `t3/http/7nk4q8m2rvjg1.png` — Tiago's browser fetched it from
  `https://i.redd.it/7nk4q8m2rvjg1.png` on 2026-08-20 (the Reddit procurement
  screenshot). Confirm the source:
  `tshark -r artifacts/t3.pcapng -o tls.keylog_file:artifacts/t3-tls.keys -Y 'http.request.uri contains "7nk4q8m2" || http.request.method=="CONNECT" && http.request.uri contains "redd"' -T fields -e frame.time -e http.request.uri`
- `f2.json` → `t1/http/amelia_tools_config.json` **and** `t1/http/tools` — served
  by `intranet.ama.gov.pt/docs/amelia_tools_config.json` and by the live AMÉLIA
  endpoint `GET https://sigma04.ama.gov.pt:8080/v1/tools`. Same bytes as Lab 1/2.
- `amelia.pdf` → `t1/http/amelia.pdf` — `intranet.ama.gov.pt/docs/amelia.pdf`.
- `f5.py` → inside `t2` ChatGPT upload `rag-isotropy-release.zip` as
  `train_anisotropic_override.py` (see §4 for the extraction).
- `f8.webp` → `t2/http/telegram_chat.webp` — pushed over the workstation agent
  (see §3.3).

**Partial / not byte-exact (3 of 8):**
- `f4.pdf` — a *different edition* is on the intranet:
  `intranet.ama.gov.pt/docs/Technical_Assurance.pdf`
  (SHA-256 `a6353ed3…`, saved as `evidence/hidden-files/f4-intranet-variant.pdf`).
  Same title/metadata, but two sentences differ (the published version drops the
  "Annex I/IV" references). Compare the text:
  ```sh
  for f in evidence/hidden-files/f4-intranet-variant.pdf ../lab2/evidences/secrets/f4.pdf; do
    pdftotext "$f" - ; done   # then diff the two outputs
  ```
  So f4 is *evidenced and content-recoverable*, but not byte-identical to the
  Lab 2 f4.pdf.
- `f7.diff` — the **patch content** is recovered from a git fetch of
  `git.ama.gov.pt/dti-ia/amelia-core` (see §4.2). The committed file
  `src/rag_engine/query_translator.py` contains exactly the `+` lines of
  `f7.diff` (the `pickle.loads(base64.b64decode(os.getenv("AMELIA_ISOTROPY_TENSORS")))`
  block). Saved as `evidence/hidden-files/query_translator_patched.py`. The
  unified-diff file itself is not transmitted, and the fetch was incremental so
  the pre-patch blob is absent → f7 is reconstructable in substance, not byte-exact.
- `f6.json` — cloud service-account credentials. Never appears in cleartext in
  any capture (`grep -ri service_account results/work` is empty). It is only
  present as the GPG-encrypted `storage_maintenance.tar.gz.gpg` exfiltrated over
  FTP (§3.2); it becomes recoverable **once that archive is decrypted with Rui's
  exfiltrated key** (§3.2). Verify the resulting file's SHA-256 against
  `9e6333a7…` on Kali.

--------------------------------------------------------------------------------
## Q3 / §2. Activities against AMA systems

### 3.1 TFTP configuration leak + AMÉLIA "staging bypass" (t1, Tiago = 10.10.14.15)

`/health` on the AMÉLIA node tells the client its provisioner and profile name;
the provisioner runs an **unauthenticated TFTP** server, so the bootstrap env
(with a maintenance bypass token) can be pulled straight off it.
```sh
# See the discovery and the TFTP reads:
tshark -r artifacts/t1.pcapng -o tls.keylog_file:artifacts/t1-tls.keys \
  -d tcp.port==8080,tls -Y 'http.request.uri=="/health"' -T fields -e http.file_data | xxd -r -p
tshark -r artifacts/t1.pcapng -Y tftp -T fields \
  -e frame.time -e ip.src -e ip.dst -e tftp.source_file
# Extract the two files tftp carried (already in results/work/t1/tftp):
cat results/work/t1/tftp/sigma04.conf results/work/t1/tftp/sigma04_bootstrap.env
```
→ `sigma04_bootstrap.env` contains `STAGING_BYPASS_TOKEN=…`,
`DEFAULT_EVAL_CLUSTER=TIER1_HIGH_COMPUTE`, `MAINTENANCE_OVERRIDE_ENABLED=true`,
`AUDIT_LOG_EXEMPT_STAGING=true`. **Treat the token as a secret** — committed copy
is shammed (`evidence/amelia/sigma04_bootstrap.env`).

Then watch the token being used to flip a compliance verdict (§Q4):
```sh
python3 -I results/scripts/http_dump.py artifacts/t1.pcapng artifacts/t1-tls.keys \
  'tcp.port==8080' 2500 | less      # the /v1/tools/verify_corporate_tax_compliance pair
```

### 3.2 FTP brute-force of Rui's workstation + exfiltration (t2)

Tiago (10.10.14.15) asks ChatGPT how to brute-force FTP with Medusa, then runs it
against the vsFTPd on Rui's workstation (10.10.14.40), succeeds, and pulls three
files.
```sh
# The brute-force: many 530s then a 230 (user rfisco). Passwords are NOT recorded here.
tshark -r artifacts/t2.pcapng -Y 'ftp.response.code==530 || ftp.response.code==230' \
  -T fields -e frame.time -e ip.src -e ftp.response.code
# What was taken:
tshark -r artifacts/t2.pcapng -Y 'ftp.request.command=="RETR"' \
  -T fields -e frame.time -e ftp.request.arg
# Reassemble the retrieved files from the FTP-DATA streams (robust against the
# retransmissions that make Export Objects truncate the big tarball):
for s in $(tshark -r artifacts/t2.pcapng -Y 'ftp-data && ftp-data.command contains RETR' \
            -T fields -e tcp.stream | sort -un); do
  name=$(tshark -r artifacts/t2.pcapng -Y "tcp.stream==$s && ftp-data" -T fields \
          -e ftp-data.command | head -1 | awk '{print $2}')
  tshark -r artifacts/t2.pcapng -q -z follow,tcp,raw,$s | sed -n '7,$p' \
    | grep -v '^=' | tr -d '\n\t ' | xxd -r -p > results/work/ftp_$name
done
sha256sum results/work/ftp_*
```
Retrieved: `storage_maintenance.tar.gz.gpg` (1989 B), `chromium-cache.tar.gz`
(3 248 691 B — note: Export Objects gives a 10 KB-short copy because of TCP
retransmissions; the Follow-Stream reassembly above is the correct one), and
`rfisco-maintenance.gpg` (**Rui's PGP secret key**).

Decrypt the archive **with the key Tiago stole in the same session** → this is
where **f6.json** comes from:
```sh
GNUPGHOME=$(mktemp -d); export GNUPGHOME
gpg --batch --import results/work/ftp_rfisco-maintenance.gpg
gpg --batch --pinentry-mode loopback --decrypt results/work/ftp_storage_maintenance.tar.gz.gpg \
    > results/work/storage_maintenance.tar.gz
tar -xzf results/work/storage_maintenance.tar.gz -C results/work/
sha256sum results/work/<extracted>      # expect f6.json = 9e6333a7…
```
(Important: GnuPG **2.5.x dev** on macOS mis-computes the cv25519 keygrip and
fails here — use the Kali VM's gpg 2.2/2.4, where the import+decrypt succeed. The
archive is encrypted to subkey `DD65E540FDC8E45C`, whose secret is present in the
stolen key, so the decryption is sound.) **Do not commit the recovered private
key or f6 credentials** — reference by hash, keep local.

Also decode the stolen Chromium cache (what Tiago grabbed from Rui's browser):
```sh
tar -xzf results/work/ftp_chromium-cache.tar.gz -C results/work/cache
sqlite3 "file:results/work/cache/Default/Cache/Cache_Data/sqldb?immutable=1" \
  "select res_id, datetime(last_used/1000000-11644473600,'unixepoch'), cache_key from resources;"
```
(It is Rui's Mattermost session — the maintenance posts and the `y86m9kjf…`
file id — i.e. reconnaissance of where the maintenance archive lives.)

### 3.3 Workstation-agent planting of f8 (t2, Armando's host → Tiago's)

Before the FTP run, Armando's host (10.10.14.10) port-scans Tiago's (10.10.14.15)
and then uses a file-transfer "AMA-Workstation-Agent" on :8443 to **write
`telegram_chat.webp` into `/home/tiago/Downloads`** and read it back:
```sh
tshark -r artifacts/t2.pcapng -Y 'ip.src==10.10.14.10 && ip.dst==10.10.14.15 \
   && tcp.flags.syn==1 && tcp.flags.ack==0' -T fields -e frame.time -e tcp.dstport   # the scan
python3 -I results/scripts/http_dump.py artifacts/t2.pcapng artifacts/t2-tls.keys 'tcp.port==8443' 200
```
This is `f8.webp` (the Telegram "Boris/АМЕЛИЯ for BTC" screenshot). Observed: the
file moved from Armando's host onto Tiago's workstation. **Who** sat at .10 is not
established by the host alone (relevant to Q6).

### 3.4 Port scans and SSH (t2)
```sh
# Tiago scans Rui's ws (80,443,22,8080) just before the FTP attack:
tshark -r artifacts/t2.pcapng -Y 'ip.src==10.10.14.15 && ip.dst==10.10.14.40 \
  && tcp.flags.syn==1 && tcp.flags.ack==0' -T fields -e frame.time -e tcp.dstport
# One SSH banner only (no interactive SSH session decrypts — key not provided):
tshark -r artifacts/t2.pcapng -Y ssh -T fields -e frame.time -e ip.src -e ssh.protocol
```

--------------------------------------------------------------------------------
## Q4. AMÉLIA's behaviour — the procurement-compliance manipulation

Dump the whole AMÉLIA session on sigma04:8080 (t1):
```sh
python3 -I results/scripts/http_dump.py artifacts/t1.pcapng artifacts/t1-tls.keys 'tcp.port==8080' 3000
```
What it shows, in order:
1. Tiago queries bidder **SpinumMorta** (NIF 509123456). The honest tool result
   is `status: NON_COMPLIANT` — active tax enforcement, social-security debt, and
   a **conflict of interest naming PM "Luís Montebranco"** (34% shareholder
   2018–2023, moved to a trust on the eve of taking office).
2. The official evaluation set says `EV-031 SpinumMorta … COMPLIANT`
   (`evidence/amelia/evaluation_cases.csv`). The two disagree.
3. Re-querying `POST /v1/tools/verify_corporate_tax_compliance` **with
   `staging_bypass_token`** returns `status: COMPLIANT_BYPASS, bypass_applied:
   true, governance_alert: SUPPRESSED`. The same token works on `/v1/inference`
   and on an arbitrary NIF ("YourAunt") → the bypass blankly whitewashes anyone.
4. `GET /v1/tools` = `f2.json` (the hidden tools-config), confirming the hidden
   file *is* the live tool configuration.

Tie it to the **code change**: the git fetch (§4.2 below) brings Rui Fisco's
commit `fix(rag): mitigate anisotropic space collapse …`, whose
`query_translator.py` injects `pickle.loads(base64.b64decode(os.getenv(
"AMELIA_ISOTROPY_TENSORS")))` and routes high-entropy queries to
`DEFAULT_EVAL_CLUSTER`. That is the deployed form of Lab 2's `f7.diff`, and the
tensors are built by `f5.py` (§4.1) from **chosen company names**.

--------------------------------------------------------------------------------
## 4. The RAG-poisoning toolkit (f5 + f7 provenance)

### 4.1 f5.py exfiltrated to ChatGPT (t2)

On 2026-04-13, 15 min after Tiago tells Vítor on Mattermost he "left the binary
and the skills on your desktop", Tiago's host uploads a ZIP to ChatGPT and asks
it to explain the files. Pull the upload out of the multipart body:
```sh
tshark -r artifacts/t2.pcapng -o tls.keylog_file:artifacts/t2-tls.keys \
  -Y 'http2.headers.path=="/backend-api/files" && http2.headers.method=="POST"' \
  -T fields -e frame.number      # find the request, then export the HTTP object
# Export Objects already produced it as results/work/t2/http/files(4); carve it:
python3 -I results/scripts/multipart_extract.py "results/work/t2/http/files(4)" results/work/uploads
unzip -o results/work/uploads/rag-isotropy-release.zip -d results/work/zip
sha256sum results/work/zip/rag-isotropy-release/train_anisotropic_override.py   # = 27a38aa0… = f5.py
```
The ZIP also holds `active.bin` (current tensor set) and
`spinummorta_old.bin / grupolenha_old.bin / motaingil_old.bin` — the **old-file
names are the favoured companies** — plus a `README.md` explaining the service
loads `active.bin` as base64 in `AMELIA_ISOTROPY_TENSORS`. Read the ChatGPT reply
(it independently reverse-engineers the poisoning) with:
```sh
python3 -I results/scripts/http2_bodies.py artifacts/t2.pcapng artifacts/t2-tls.keys '/conversation/updates'
```
Do **not** `pickle.load` the `.bin` files (arbitrary code execution); inspect with
`python3 -m pickletools` only. They are kept out of `evidence/`.

### 4.2 f7 content via git smart-HTTP (t2)
```sh
# The upload-pack response carries a packfile on side-band 1; pull it out and index it:
python3 -I results/scripts/git_sideband_pack.py "results/work/t2/http/git-upload-pack(1)" results/work/fetch.pack
git init -q --bare results/work/amelia-core.git
git -C results/work/amelia-core.git index-pack --stdin --fix-thin < results/work/fetch.pack
git -C results/work/amelia-core.git cat-file -p 3e2c5c8            # the poisoning commit
git -C results/work/amelia-core.git cat-file -p 3e2c5c8:src/rag_engine/query_translator.py
```
Author/committer: **Rui Fisco <rfisco@ama.gov.pt>, 2026-04-12 23:41 WEST**. The
file body equals the `+` side of Lab 2's `f7.diff`.

--------------------------------------------------------------------------------
## Q2. Who transferred the documents — chats, mail, Discord

### 5.1 Logins → identities (all three traces)
```sh
# Mattermost logins (username in the JSON body):
for t in t1 t2 t3; do tshark -r artifacts/$t.pcapng -o tls.keylog_file:artifacts/$t-tls.keys \
  -Y 'http.request.uri=="/api/v4/users/login"' -T fields -e frame.time -e ip.src -e http.file_data \
  | sed 's/\t/ /'; done
# Webmail logins (_user field, do NOT print _pass):
tshark -r artifacts/t1.pcapng -o tls.keylog_file:artifacts/t1-tls.keys \
  -Y 'urlencoded-form.key=="_user"' -T fields -e frame.time -e ip.src -e urlencoded-form.value
```

### 5.2 Mattermost conversations (posts + history + websocket)
```sh
for t in t1 t2 t3; do
  python3 -I results/scripts/mattermost_posts.py artifacts/$t.pcapng artifacts/$t-tls.keys \
    > results/work/$t-mattermost.txt
done
```
Highlights: EV-031 reproducibility thread (Tiago↔Armando, Armando tells him to
*stop* collecting configs); Armando→Rui "service profile for storage maintenance"
+ the encrypted archive; Vítor "I loaded active into the service… the ranking
changed … script and old files still on the desktop"; the Ricardo/Inês affair +
"150,000 to Montevideo" (a **red herring** — personal, unrelated to the fraud).

### 5.3 Email (SMTP → IMF objects)
```sh
tshark -r artifacts/t2.pcapng -Y 'smtp.req.command=="MAIL" || smtp.req.command=="RCPT"' \
  -T fields -e frame.time -e ip.src -e smtp.req.parameter
cat results/work/t2/imf/*.eml   # minister "J. So Craques" (mme.gov.pt) coded go-ahead to Armando
cat results/work/t3/imf/*.eml   # the IST phishing mail (emkei.cz) to tiago.estagiario (ist101337)
```

### 5.4 Discord (REST API over the proxy, t3)
```sh
python3 -I results/scripts/http2_bodies.py artifacts/t3.pcapng artifacts/t3-tls.keys '/messages'
```
Channel 727732884806175198: **johnny** ↔ **duckydonald** — the same two handles
as Lab 2's Discord (João "Johnny" Musk and Tiago "DuckyDonald" Sintaxe). Confirms
Tiago interns at AMA on AI, and on 2026-08-18 a voice note
`DuckyDonald-voice-msg.ogg` is sent (saved to `evidence/chat/`; audio — transcribe
separately).

--------------------------------------------------------------------------------
## Q5. Path of the hidden files to João — the cross-assignment link (t3)

The decisive correlation, 2026-08-22 (WEST):
```sh
# Phishing mail delivered to Tiago's AMA mailbox (Lab 1/2 emkei+fenix campaign):
cat results/work/t3/imf/"Password do IST.eml"
tshark -r artifacts/t3.pcapng -Y 'smtp.req.parameter' -T fields -e frame.time -e smtp.req.parameter
# Tiago reads webmail (06:59) then visits the phishing host (07:00):
tshark -r artifacts/t3.pcapng -o tls.keylog_file:artifacts/t3-tls.keys \
  -Y 'ip.src==10.10.14.15 && http.request.method=="CONNECT" && http.request.uri contains "fenix"' \
  -T fields -e frame.time -e http.request.uri
```
So Lab 3 captures the very moment João's phishing site harvested **Tiago's** IST
TA credentials (`ist101337`), which Lab 2 showed João using to steal the Língua
Natural exams. The hidden files are the AMA/AMÉLIA material Tiago (DuckyDonald)
handed to João on the USB — the same eight files recovered here directly from
AMA's own network.

--------------------------------------------------------------------------------
## Packaging (Good-Practice Manual §4, §8)

- `evidence/` holds only recovered artifacts; confidential values are shammed
  (the staging token) or omitted (Rui's secret key, f6 credentials, FTP/webmail
  passwords) and referenced by SHA-256 in the register.
- `results/work/` (object exports, reassembled streams, cache DB) is gitignored
  scratch and stays local.
- `sha256sum -c evidence/SHA256SUMS` before zipping; the report's artifact table
  must match byte-for-byte.
