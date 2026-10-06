# Artifact register

Per Tutorial 1, Good-Practice Manual §3.

## A101 -- `images/windows_laptop_memory.raw`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:02+00:00 |
| Parent artifact | - |
| Command | `-` |
| stat | `images/windows_laptop_memory.raw|1090326235|2026-10-05 19:32:01.802259169 +0000|2026-10-05 19:32:01.804925706 +0000` |
| Type | ELF 64-bit LSB core file, x86-64, version 1 (SYSV), SVR4-style |
| SHA-256 | `c0b66a9ec5ff16d8c01726a8717648f729857fa059ba7485c5c1717587892be3` |

**Observation:** Windows 10 build 19041 kernel (PDB CA8E2F01...); host name JOHNNY-PC in envars; system time 2026-08-25 21:03:25 UTC (windows.info).

**Interpretation:** Host name matches part 1 of the handwritten note.

**Limitations / confidence:** Symbols were not in the baked-in pack; fetched by Volatility over the network with --net (only the public PDB GUID was sent). Windows timestamps need no adjustment.

## A102 -- `images/windows_laptop_disk.dd`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:04+00:00 |
| Parent artifact | - |
| Command | `-` |
| stat | `images/windows_laptop_disk.dd|27917287424|2026-10-05 19:32:00.319480143 +0000|2026-10-05 19:32:00.320144642 +0000` |
| Type | DOS/MBR boot sector MS-MBR Windows 7 english at offset 0x163 "Invalid partition table" at offset 0x17b "Error loading operating system" at offset 0x19a "Missing operating system"; partition 1 : ID=0xee, start-CHS (0x0,0,2), end-CHS (0x141,254,63), startsector 1, 4294967295 sectors |
| SHA-256 | `5eca1f65df49ccf5bddeb8c5c3a44fe1a8a9e6faab04ed601d565b915bbaa6a8` |

**Observation:** GPT with five partitions. Partition 4 (sector 42735616, 11788288 sectors) starts with -FVE-FS-, i.e. BitLocker-locked; partition 3 (sector 41199616) is NTFS.

**Interpretation:** The locked partition is the D: volume named in the assignment (drive letter not yet confirmed from the registry).

**Limitations / confidence:** Only the partition signature was checked; no data outside the decrypted copy (A109) has been read.

## A103 -- `images/linux_workstation_disk.dd`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:30+00:00 |
| Parent artifact | - |
| Command | `-` |
| stat | `images/linux_workstation_disk.dd|20976780288|2026-10-05 19:31:17.989197178 +0000|2026-10-05 19:31:17.989676718 +0000` |
| Type | DOS/MBR boot sector; partition 1 : ID=0xee, start-CHS (0x0,0,2), end-CHS (0x3ff,255,63), startsector 1, 73400319 sectors, extended partition table (last) |
| SHA-256 | `b31261098d901de0be201f4f78f5816c946490b9eb4ae2c94dc2fcf4af4e3368` |

**Observation:** Not analysed yet.

**Interpretation:** -

**Limitations / confidence:** Linux image: subtract 27 days from every absolute timestamp when it is analysed.

## A104 -- `evidence/handwritten-note-fig1.png`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:50+00:00 |
| Parent artifact | - |
| Command | `pdfimages -f 3 -l 3 -png csf2627-lab-assignment-2.pdf` |
| stat | `evidence/handwritten-note-fig1.png|1956612|2026-10-05 20:14:02.367365985 +0000|2026-10-05 20:14:02.367523193 +0000` |
| Type | PNG image data, 1732 x 908, 8-bit/color RGB, non-interlaced |
| SHA-256 | `d259e34bfc965a1aea720ffa7b9443ebfde54b6fdb78d26811fd5c44149b6896` |

**Observation:** Figure 1 of the assignment, page 3: handwritten note, lines 1-5 and a header line.

**Interpretation:** Reads as a ZIP password of the form sha256{part_1_..._part_5}: laptop name, first name on wallpaper, JJK picture region, Windows password, restaurant.

**Limitations / confidence:** Transcription of the handwriting is ours and unverified at full resolution.

## A105 -- `results/scripts/lab1-hashes.sha256`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:50+00:00 |
| Parent artifact | - |
| Command | `transcribed from csf2627-lab-assignment-2.pdf Tables 1-2` |
| stat | `results/scripts/lab1-hashes.sha256|1611|2026-09-28 10:39:13.391490441 +0000|2026-09-28 10:39:13.391490441 +0000` |
| Type | ASCII text |
| SHA-256 | `ee5da7afa0695aef0b6843fa4039431c1aaca8fd0a8ce93b3d75581d49ca0fed` |

**Observation:** 16 hashes transcribed from Tables 1 and 2; hashmatch against Lab 1 evidence found 9 of them.

**Interpretation:** -

**Limitations / confidence:** The other 7 Stage I files are not present in our Lab 1 evidence, so their hashes are only checked against the assignment text.

## A106 -- `results/work/plugins/windows/bitlocker.py`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:50+00:00 |
| Parent artifact | - |
| Command | `github.com/lorelyai/volatility3-bitlocker (main, fetched 2026-10-05)` |
| stat | `results/work/plugins/windows/bitlocker.py|15518|2026-10-05 20:02:48.648108643 +0000|2026-10-05 20:02:48.648243642 +0000` |
| Type | Python script, ASCII text executable |
| SHA-256 | `1cda3c680e665898051dba1f9a638c42a4a711b65da74c8539995ad543a7ffb7` |

**Observation:** Read in full before use: no network access, no subprocess, file writes only through Volatility's output handler.

**Interpretation:** Third-party code run against seized evidence; the plugin was approved by the user for this scan.

**Limitations / confidence:** Source not audited beyond the single file; the upstream commit is not pinned.

## A107 -- `results/analysis/bitlocker/run.log`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:50+00:00 |
| Parent artifact | A101 |
| Command | `vol -vv -p results/work/plugins -f windows_laptop_memory.raw windows.bitlocker.BitlockerFVEKScan --tags FVEc Cngb None` |
| stat | `results/analysis/bitlocker/run.log|8714|2026-10-05 20:02:56.916118430 +0000|2026-10-05 20:02:56.916118430 +0000` |
| Type | ASCII text, with very long lines (361), with CR, LF line terminators |
| SHA-256 | `d4eea1cc9e1ed6765c501ae5b4c4a2e6f3b4a0a2595f315e15249980c631d875` |

**Observation:** Scan returned 3 FVEK candidates (pool tags Cngb x2, None x1). Only the None-tagged candidate has a complete AES-XTS-128 key pair (FVEK + tweak).

**Interpretation:** Candidate 3 is the D: key (see A108). Candidates 1 and 2 are not validated.

**Limitations / confidence:** This log contains key bytes. It is gitignored and must not be committed or put in the ZIP as is.

## A108 -- `results/work/fvek-D.hex`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:51+00:00 |
| Parent artifact | A107 |
| Command | `bitlocker.py verify (candidate 3 selected)` |
| stat | `results/work/fvek-D.hex|65|2026-10-05 20:12:09.863198445 +0000|2026-10-05 20:12:09.863198445 +0000` |
| Type | ASCII text |
| SHA-256 | `1666aa98ee08ca049cc9f83fc76b35bef17da76c8ee2b877d44244fa87012480` |

**Observation:** Candidate 3 decrypts the volume header copy at offset 0x47dd000 to an NTFS boot sector (eb 52 90 'NTFS    ') and the $MFT record 0 to 'FILE'.

**Interpretation:** The key is the FVEK for D:. It came from memory; the method is candidate 3 of A107.

**Limitations / confidence:** Validated only on the boot sector and $MFT record 0. The file holds key material and is not for submission; only its hash is recorded.

## A109 -- `results/work/D-decrypted.raw`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:14:51+00:00 |
| Parent artifact | A102 |
| Command | `bitlocker.py decrypt (volume-relative XTS, key from A108)` |
| stat | `results/work/D-decrypted.raw|6035603456|2026-10-05 20:13:48.349223214 +0000|2026-10-05 20:13:48.349223214 +0000` |
| Type | DOS/MBR boot sector, code offset 0x52+2, OEM-ID "NTFS    ", sectors/cluster 8, Media descriptor 0xf8, sectors/track 63, heads 255, hidden sectors 42735616, dos < 4.0 BootSector (0x80), FAT (1Y bit by descriptor); NTFS, sectors/track 63, sectors 11788287, $MFT start cluster 262144, $MFTMirror start cluster 2, bytes/RecordSegment 2^(-1*246), clusters/index block 1, serial number 0ac8432938432604e; contains bootstrap BOOTMGR |
| SHA-256 | `dd1472182e8ec6ff0a8ba6224ed4d6a036a84ed70ae9ae9b6e50210fb6e04d34` |

**Observation:** Whole partition decrypted sector by sector (tweak = volume-relative sector index). Size 6035603456 bytes = 11788288 sectors x 512.

**Interpretation:** Read-only working copy; the original evidence (A102) is unchanged.

**Limitations / confidence:** First 8 KB replaced with the decrypted volume header, which is an inference from the layout. Not yet mounted or parsed; NTFS consistency is unchecked beyond the boot sector and $MFT record 0.

## A110 -- `results/work/extract/TranscodedWallpaper`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:19:48+00:00 |
| Parent artifact | A109 |
| Command | `icat results/work/D-decrypted.raw 864` |
| stat | `results/work/extract/TranscodedWallpaper|167736|2026-10-05 20:19:14.507069428 +0000|2026-10-05 20:19:14.507069428 +0000` |
| Type | JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=1, orientation=upper-left], baseline, precision 8, 1920x1080, components 3 |
| SHA-256 | `422b5f86c78905a5ff5707ce7ba0cd76a197e771dfa142db89ed25922479fcc2` |

**Observation:** Stylised figure with the caption 'HELLO FRIEND.' on a dark background; 1920x1080 JPEG (Windows TranscodedWallpaper, the current desktop wallpaper).

**Interpretation:** The caption is the catchphrase of Elliot Alderson in Mr. Robot, so the figure is probably that character. Part 2 of the note would then be 'elliot'. This does not match Diogo's 'eren' guess, which must be rechecked.

**Limitations / confidence:** Identifying a character from a caption is our inference, not a fact in the file. Check the wallpaper's registry history (Themes\ and the wallpaper path) before relying on it.

## A111 -- `results/work/extract/mom-photo.jpg`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:19:48+00:00 |
| Parent artifact | A109 |
| Command | `icat results/work/D-decrypted.raw 939` |
| stat | `results/work/extract/mom-photo.jpg|21046|2026-10-05 20:19:14.450378326 +0000|2026-10-05 20:19:14.450378326 +0000` |
| Type | JPEG image data, JFIF standard 1.01, resolution (DPI), density 0x0, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=1], baseline, precision 8, 474x266, components 3 |
| SHA-256 | `fe8f99ce75f92a4aee463d5b535d2737e0e042d8bfb59bf44d123c9704f6be55` |

**Observation:** Anime-style scene of a train platform with a train and a crowd; 474x266 JPEG; no GPS or camera EXIF.

**Interpretation:** Could be the 'JJK picture' from part 3 (Jujutsu Kaisen; the Shibuya arc is set in a Tokyo station), which would support 'shibuya'. Not established.

**Limitations / confidence:** The filename 'mom-photo.jpg' does not match the content, so the name cannot be relied on. No JJK-specific text or metadata was found.

## A112 -- `results/work/extract/hate-this-place.jpg`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:19:48+00:00 |
| Parent artifact | A109 |
| Command | `icat results/work/D-decrypted.raw 938` |
| stat | `results/work/extract/hate-this-place.jpg|385066|2026-10-05 20:19:14.483425181 +0000|2026-10-05 20:19:14.483425181 +0000` |
| Type | JPEG image data, baseline, precision 8, 1200x900, components 3 |
| SHA-256 | `c323d401bd25fd8a6ae6e3b8f7dba724ce95d51c886b15653a2f5a0863c800c8` |

**Observation:** Photo of a yellow building with a tiled terrace, umbrellas and tables under pine trees; 1200x900 JPEG; no GPS or camera EXIF; no legible sign.

**Interpretation:** Probably the restaurant of part 5. The name 'Maria Pimenta' has no source in the evidence yet.

**Limitations / confidence:** The restaurant's name and place are not visible. Attribution to 'pimenta' is not supported by this file alone.

## A113 -- `results/analysis/30_matches_users.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:20:49+00:00 |
| Parent artifact | A109 |
| Command | `kali.sh hashmatch results/work/extract/users (884 files from fls -r of D: Users/)` |
| stat | `results/analysis/30_matches_users.txt|0|2026-10-05 20:20:43.146274646 +0000|2026-10-05 20:20:43.146329396 +0000` |
| Type | empty |
| SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

**Observation:** hash-match of 884 regular files extracted from D: Users/ (non-deleted, from the file listing) against the 16 Stage I hashes: 0 matches.

**Interpretation:** No Stage I file is present as a live user file on D:. This does not show they were never on the disk.

**Limitations / confidence:** Not searched: Windows system folders, unallocated space, deleted files, Recycle Bin, slack space, and the NTFS $LogFile and USN journal. Matching is by SHA-256, so a renamed copy would still match, but a modified copy would not. Carving is still needed for deleted content.

## A114 -- `results/work/hives/SAM`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:23:59+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 images/windows_laptop_disk.dd 40073 (C: NTFS, inode 40073)` |
| stat | `results/work/hives/SAM|65536|2026-10-05 20:23:42.480397040 +0000|2026-10-05 20:23:42.480397040 +0000` |
| Type | MS Windows registry file, NT/2000 or above |
| SHA-256 | `0e0d9235598d1c67445eabd2b8d151afce3820a32123550f68e8e9442129797f` |

**Observation:** SAM hive, 65536 bytes, from the C: NTFS partition (sector 239616), inode 40073. Read-only extraction.

**Interpretation:** Offline copy of the local account database; johnny's NT hash is fb06de73293e2350d5087dc306a52934.

**Limitations / confidence:** Hive may need its .LOG1/.LOG2 replayed; secretsdump read it without replay. Cross-checked by SYSTEM boot key.

## A115 -- `results/work/hives/SYSTEM`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:23:59+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 images/windows_laptop_disk.dd 40354` |
| stat | `results/work/hives/SYSTEM|9961472|2026-10-05 20:23:45.250631289 +0000|2026-10-05 20:23:45.250631289 +0000` |
| Type | MS Windows registry file, NT/2000 or above |
| SHA-256 | `4b7466fdcc91b00c622ac995d85af3872efed87654072b3ed78121e20b7bf4b4` |

**Observation:** SYSTEM hive, 9961472 bytes, inode 40354, from the C: partition.

**Interpretation:** Provides the boot key used to decrypt the SAM (value kept in the local output results/analysis/creds/secretsdump_offline.txt, not committed).

**Limitations / confidence:** Memory copy of SYSTEM failed (Hbootkey invalid); the on-disk copy was used instead.

## A116 -- `results/work/hives/SECURITY`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:23:59+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 images/windows_laptop_disk.dd 40075` |
| stat | `results/work/hives/SECURITY|32768|2026-10-05 20:23:47.753601454 +0000|2026-10-05 20:23:47.753601454 +0000` |
| Type | MS Windows registry file, NT/2000 or above |
| SHA-256 | `fd12b21d9f979bf7709cefe36d858ff1217d66b8d7ccd393d772fe30895d5c42` |

**Observation:** SECURITY hive, 32768 bytes, inode 40075.

**Interpretation:** Holds the LSA secrets, including the DefaultPassword entry.

**Limitations / confidence:** Used only for LSA secrets.

## A117 -- `results/work/hives/SOFTWARE`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:23:59+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 images/windows_laptop_disk.dd 44810` |
| stat | `results/work/hives/SOFTWARE|68943872|2026-10-05 20:23:51.926924796 +0000|2026-10-05 20:23:51.926924796 +0000` |
| Type | MS Windows registry file, NT/2000 or above |
| SHA-256 | `af5dbd1818a94b6041a9f76b38f7f067e46fe8a47b72ac46e048dc8de58c2209` |

**Observation:** SOFTWARE hive, 68943872 bytes, inode 44810. Extracted but not parsed beyond the copy.

**Interpretation:** Not used yet; candidate for Run keys and autologon settings.

**Limitations / confidence:** Not analysed.

## A118 -- `results/analysis/creds/secretsdump_offline.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:23:59+00:00 |
| Parent artifact | A114 |
| Command | `impacket-secretsdump -sam SAM -system SYSTEM -security SECURITY LOCAL` |
| stat | `results/analysis/creds/secretsdump_offline.txt|1360|2026-10-05 20:23:52.279126930 +0000|2026-10-05 20:23:52.279126930 +0000` |
| Type | ASCII text |
| SHA-256 | `e93b694e4b2b7cb137d9c450b6fcd5ef33ce8ee80589e63bc1c3466de2e270a1` |

**Observation:** Offline secretsdump output: johnny's NT hash fb06de73293e2350d5087dc306a52934; LSA DefaultPassword 'fsociety'.

**Interpretation:** The NT hash of 'fsociety' computed with MD4(UTF-16LE) is fb06de73293e2350d5087dc306a52934, so johnny's password is 'fsociety' (part 4).

**Limitations / confidence:** Password recovery was verified only by hash equality; no logon was attempted. Output contains secrets, gitignored.

## A119 -- `results/analysis/zip/note_pw_myzip.zip.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:23:59+00:00 |
| Parent artifact | Lab 1 A022 (myzip.zip) |
| Command | `kali.sh note-pw results/work/zip/myzip.zip` |
| stat | `results/analysis/zip/note_pw_myzip.zip.txt|31|2026-10-05 20:23:59.302433581 +0000|2026-10-05 20:23:59.302433581 +0000` |
| Type | ASCII text |
| SHA-256 | `9350d94109e8c4a923bae7bfd9ea5b35ee9cc74be227d5ce154cfaacd626c7ca` |

**Observation:** kali.sh note-pw on myzip.zip (ZipCrypto, member amelia.pdf): 12 candidate passwords built from the note's recipe, 0 opened the archive.

**Interpretation:** The recipe with the verified parts (johnny-pc, fsociety) and the candidate parts elliot/eren, shibuya and pimenta/maria-pimenta is not correct yet.

**Limitations / confidence:** Parts 2, 3 and 5 are not established by the evidence; separators '_' and '-' both tried. The test rejects wrong passwords correctly; a directory-entry bug was found and fixed in the same step.

## A120 -- `results/analysis/D/keyword_hits.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:43:26+00:00 |
| Parent artifact | A109 |
| Command | `search_volume.py results/work/D-decrypted.raw pimenta povoa "feira de" restaurante shibuya jujutsu gojo "blue eyes"` |
| stat | `results/analysis/D/keyword_hits.txt|5708|2026-10-05 20:41:46.096265412 +0000|2026-10-05 20:41:46.096265412 +0000` |
| Type | ASCII text |
| SHA-256 | `84ab7ad7d8081dff520b11ae0e9288b117c9a0b8b1773420181491910e03a39d` |

**Observation:** Whole-volume search (ASCII and UTF-16, case-insensitive). 0 hits for 'pimenta', 'povoa', 'feira de', 'jujutsu', 'blue eyes'. 'shibuya' only in a web suffix list (shibuya.tokyo.jp); 'gojo' and 'restaurante' only in random binary or foreign-language text.

**Interpretation:** No evidence on D: that names the restaurant 'Maria Pimenta' or a JJK 'Shibuya' picture. The name in Diogo's answer for part 5 is not supported by this disk.

**Limitations / confidence:** Keyword search misses text in other encodings, compressed or encrypted content, and images without text. Hits are not inspected for context beyond the printed snippet.

## A121 -- `results/analysis/D/memory_keyword_hits.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:43:27+00:00 |
| Parent artifact | A101 |
| Command | `search_volume.py images/windows_laptop_memory.raw pimenta povoa "feira de" jujutsu shibuya "blue eyes"` |
| stat | `results/analysis/D/memory_keyword_hits.txt|13|2026-10-05 20:43:18.155772209 +0000|2026-10-05 20:43:18.155772209 +0000` |
| Type | ASCII text |
| SHA-256 | `7e433efeb6d7a64b80e7450e4dce0b6de47f46ef69f1a3de0426918634627f76` |

**Observation:** Same terms searched in the memory image: 0 hits.

**Interpretation:** Nothing in memory names the restaurant or the picture region.

**Limitations / confidence:** Only the terms tested; memory may hold data in encodings not searched.

## A122 -- `results/work/fs/UsnJrnl_J.bin`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-05T20:43:27+00:00 |
| Parent artifact | A109 |
| Command | `icat -o 0 D-decrypted.raw 184 ($UsnJrnl:$J)` |
| stat | `results/work/fs/UsnJrnl_J.bin|1382472|2026-10-05 20:29:41.558166562 +0000|2026-10-05 20:29:41.558166562 +0000` |
| Type | data |
| SHA-256 | `a7808b4aa192b2434d080014d8f3496c1a35ba94c42f22e1ac7b09c7bc000cb9` |

**Observation:** NTFS change journal (USN) of D:, 12588 records. Filtered to media and document names: wallpaper cache files, hate-this-place.jpg and mom-photo.jpg created 2026-07-28 21:44:41 (UTC as recorded), Natural_Language_MAP1_2026-2027.pdf 2026-08-22 09:00:00, and a deleted background.jpg at 2026-07-28 20:16:35.

**Interpretation:** The deleted background.jpg is a candidate earlier wallpaper. It is not in the MFT listing, so it could only be recovered by carving.

**Limitations / confidence:** Journal timestamps are as recorded in the image and are not yet shifted or cross-checked with the MFT. Only names matching the filter were reviewed.

## A123 -- `results/work/carve/jpg/00126432.jpg`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T06:12:24+00:00 |
| Parent artifact | A109 |
| Command | `foremost -t jpg,png -i results/work/D-decrypted.raw (carved; file 00126432.jpg)` |
| stat | `results/work/carve/jpg/00126432.jpg|115877|2026-10-06 06:11:17.254460016 +0000|2026-10-06 06:11:17.254460016 +0000` |
| Type | JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=1, orientation=upper-left], baseline, precision 8, 1920x1080, components 3 |
| SHA-256 | `84b37747aa1698bd6e0ebe0b3d37691792e283e63fb0dd372a13eb62e291550e` |

**Observation:** Carved JPEG 1920x1080 (115877 bytes), partly corrupt (bottom third grey). Foremost carved 9 images from the whole D: volume: 3 JPEG (incl. this one, 1280x800 lock-screen cache, and a 474x266 copy of mom-photo.jpg) and 6 small PNG icons.

**Interpretation:** Shows the same 'HELLO FRIEND.' image as TranscodedWallpaper, so it is most likely the deleted background.jpg from the USN journal (A122). Gives no JJK picture and no restaurant evidence.

**Limitations / confidence:** Carved files have no names; the link to background.jpg rests on the journal entry and the identical image, not on the file record. Carving is by signature, so other deleted pictures may be missed or fragmented.

## A124 -- `results/work/zip/stash.zip`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T06:31:25+00:00 |
| Parent artifact | A103 |
| Command | `icat -o 2203648 images/linux_workstation_disk.dd 956142 (home/johnnymusk/backups/stash.zip)` |
| stat | `results/work/zip/stash.zip|6540867013|2026-10-06 06:19:01.777379245 +0000|2026-10-06 06:19:01.777379245 +0000` |
| Type | Zip archive data, at least v2.0 to extract, compression method=deflate |
| SHA-256 | `d0544dcbcbccbce302ad5f811de9f59ee786d94e7b311b2d3ae6f3b153a0c308` |

**Observation:** stash.zip from home/johnnymusk/backups/ on the Linux workstation (inode 956142). Every entry is ZipCrypto-encrypted and holds 9 files: the Stage I source set.

**Interpretation:** The suspect kept the Stage I source files, and the password is the note's recipe (see A125).

**Limitations / confidence:** Archive copied out of the image with icat; its path, inode and timestamps come from the image, not yet cross-checked with the MFT or inode metadata.

## A125 -- `results/analysis/zip/note_pw_stash.zip.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T06:31:48+00:00 |
| Parent artifact | A124 |
| Command | `kali.sh note-pw results/work/zip/stash.zip` |
| stat | `results/analysis/zip/note_pw_stash.zip.txt|205|2026-10-06 06:31:25.347423264 +0000|2026-10-06 06:31:25.347423264 +0000` |
| Type | ASCII text |
| SHA-256 | `ea19c9c036d86a09eb632ebbd8338f205aa9d4672cba87ef56ca599f6cb9c5f0` |

**Observation:** Note-recipe test against stash.zip: the password johnny-pc_elliot_shibuya_fsociety_pimenta (SHA-256 ab99749a576b8070ddf665ce139afd43e7c2a3f5b55b3173e98791c281c1454d) opens the archive; the CRC of the first encrypted member passes. Of 1296 candidates tested, this is the only match.

**Interpretation:** All five parts of the note are confirmed as one string: johnny-pc, elliot, shibuya, fsociety, pimenta. Part 2 is elliot, part 3 shibuya and part 5 pimenta.

**Limitations / confidence:** Confirms the password only; the parts are established as a set by the hash, not each on its own evidence. Parts 3 and 5 rest on Diogo's findings and the password, and his source files are not registered here.

## A126 -- `results/analysis/30_matches_stash.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:25:04+00:00 |
| Parent artifact | A124 |
| Command | `kali.sh hashmatch results/work/stash (stash.zip extracted with the note password)` |
| stat | `results/analysis/30_matches_stash.txt|563|2026-10-06 07:24:48.893643106 +0000|2026-10-06 07:24:48.893643106 +0000` |
| Type | ASCII text |
| SHA-256 | `3b53dfc027a6eb64386618d497f8ebbdac9bb27084ef8ab93c637d3eb9d142d1` |

**Observation:** Hash-match of the 9 extracted stash.zip files against the 16 Stage I hashes: 7 matches (myzip.zip, Shingeki mkv, GTA iceberg jpg, GTA trailer mp4, dj_cara wav, blank, polish_cow.webp). The telemetry xlsx does not match.

**Interpretation:** stash.zip is the Stage I source set as held by the suspect on the Linux workstation; it is evidence that the sources were stored there.

**Limitations / confidence:** Matching is by SHA-256 of the extracted files; the 8 hidden files (Table 2) are inside these sources and were not searched here.

## A127 -- `results/work/stash/ESP32_ADXL345_3Axis_Telemetry.xlsx`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:25:04+00:00 |
| Parent artifact | A124 |
| Command | `unzip stash.zip (password from note)` |
| stat | `results/work/stash/ESP32_ADXL345_3Axis_Telemetry.xlsx|3255723|2026-10-06 07:22:55.349781880 +0000|2026-10-06 07:22:55.349781880 +0000` |
| Type | Microsoft Excel 2007+ |
| SHA-256 | `b3cc6cb719af6ea2f2653b8635e5a0eabf4ae3b32b207aa01dbd5c4d176ee15f` |

**Observation:** ESP32_ADXL345_3Axis_Telemetry.xlsx from stash.zip has SHA-256 b3cc6cb719af6ea2f2653b8635e5a0eabf4ae3b32b207aa01dbd5c4d176ee15f; Table 1 of the assignment gives 3369cd48df5bb112def25e662398674e89bdeb5df6eaa400c4ba538a9778f218.

**Interpretation:** The stash copy differs from the published source, so it may have been modified (or is a different version). This needs a comparison before it is reported.

**Limitations / confidence:** Only the hash mismatch is established; the content difference is not examined yet.

## A128 -- `results/analysis/xlsx/compare_telemetry.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:31:43+00:00 |
| Parent artifact | A127 |
| Command | `python3 results/scripts/compare_xlsx.py results/work/stash/ESP32_ADXL345_3Axis_Telemetry.xlsx /work/lab1/evidence/Telemetry.xlsx` |
| stat | `results/analysis/xlsx/compare_telemetry.txt|575|2026-10-06 07:31:37.344783874 +0000|2026-10-06 07:31:37.344783874 +0000` |
| Type | ASCII text |
| SHA-256 | `524d6b2810b94490ca93c03aaea6e34800b05b0c30364520c8f5baeef8a0807e` |

**Observation:** The stash copy and the Lab 1 Telemetry.xlsx (published hash 3369cd48...) have identical cell values in all three sheets (120800 cells each); differences are only in the last 1-2 floating-point digits (max relative 9e-16 to 5e-11). Document properties differ: created/modified 2026-08-25 14:06:47 UTC in the stash copy vs 12:01:06 UTC in the Lab 1 copy. The stash copy is an image file, so its embedded timestamp falls under the −27 day rule: 2026-07-29 14:06:47 UTC (timeline E10).

**Interpretation:** The stash copy was re-saved (about two hours later) by a tool that writes floating-point values differently, without changing the data. The data are the same, so this is not a content tampering. Whether the suspect or someone else re-saved it is open.

**Limitations / confidence:** Compared cell values and properties only, not formatting, hidden sheets or the workbook's other parts. The Lab 1 copy's provenance is the published assignment file.

## A129 -- `results/work/linux/home__johnnymusk__.bash_history`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:43:44+00:00 |
| Parent artifact | A103 |
| Command | `linux-extract home/johnnymusk/.bash_history` |
| stat | `results/work/linux/home__johnnymusk__.bash_history|3988|2026-10-06 07:42:51.140289366 +0000|2026-10-06 07:42:51.140289366 +0000` |
| Type | ASCII text, with very long lines (335) |
| SHA-256 | `8aa347a60c42893f9fca7e34e6a85228a021e50e9393fe11cb2c9cde150f5d0e` |

**Observation:** Bash history of user johnnymusk on the Linux workstation (about 100 lines). Records: mounting and copying a USB drive labelled TEARSINRAIN to ~/ducky; encoding scripts embedding files into media (polyglot, LSB, DCT, WAV, video); creating ~/backups/stash.zip with zip -e; secure deletion with srm -ll -r of ~/ducky and ~/repos; installing secure-delete; ssh to fenix-prod and running git rm -r of the site content plus a 'cleanup' commit on the server.

**Interpretation:** Shows the suspect built the hidden-file set, encrypted the archive, removed the working directories and changed a live server. Commands are observed; the intent is an inference.

**Limitations / confidence:** Bash history was not timestamped (no HISTTIMEFORMAT). Times come from the inode (A103), adjusted −27 days. Commands may not all have run successfully; the history does not show output.

## A130 -- `results/work/linux/home__johnnymusk__Documents__todo-list.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:43:45+00:00 |
| Parent artifact | A103 |
| Command | `linux-extract home/johnnymusk/Documents/todo-list.txt` |
| stat | `results/work/linux/home__johnnymusk__Documents__todo-list.txt|391|2026-10-06 07:42:51.190690688 +0000|2026-10-06 07:42:51.190690688 +0000` |
| Type | ASCII text |
| SHA-256 | `2cbf3502525442df287da87eba76f58ef72bcd8f911723ff1839f2a0c4a9a126` |

**Observation:** todo-list.txt: 'back up peixinho (doing now)'; 'Prepare for the exam. LN exam is on my windows bitlocker drive.'

**Interpretation:** Links the Linux user to the BitLocker-locked D: volume and the Exams_LN folder found there (A102, A122).

**Limitations / confidence:** Single text file; no other proof that the note refers to the same drive.

## A131 -- `results/work/linux/home__johnnymusk__.ssh__config`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:43:45+00:00 |
| Parent artifact | A103 |
| Command | `linux-extract home/johnnymusk/.ssh/config` |
| stat | `results/work/linux/home__johnnymusk__.ssh__config|135|2026-10-06 07:42:51.236411686 +0000|2026-10-06 07:42:51.236411686 +0000` |
| Type | ASCII text |
| SHA-256 | `5d0995bbddf7472bbadcf9e8bd322e0104a20f5b1aa455bac6057aa43375ec41` |

**Observation:** SSH config: Host fenix-prod, HostName 146.193.41.109, user muskyboi, IdentityFile ~/.ssh/muskyboi, StrictHostKeyChecking no.

**Interpretation:** The suspect uses the 'muskyboi' identity to administer the production host. Related to the MuskyBoi accounts in the assignment.

**Limitations / confidence:** The IP is not the phishing host in Lab 1 (146.193.41.5); the link is by hostname and username only. The key files are in the same directory and are not registered here.

## A132 -- `results/work/linux/home__johnnymusk__backups__peixinho__server.js`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:43:45+00:00 |
| Parent artifact | A103 |
| Command | `linux-extract home/johnnymusk/backups/peixinho/server.js` |
| stat | `results/work/linux/home__johnnymusk__backups__peixinho__server.js|2212|2026-10-06 07:42:51.440955347 +0000|2026-10-06 07:42:51.440955347 +0000` |
| Type | JavaScript source, ASCII text |
| SHA-256 | `2a014a1168968989cf36488ac8a7f218f8b3591dabeea50199c6f26e03abf863` |

**Observation:** server.js on the Linux disk has SHA-256 2a014a1168968989cf36488ac8a7f218f8b3591dabeea50199c6f26e03abf863, the same as server.js in Lab 1 (A006).

**Interpretation:** The phishing server source was kept in ~/backups/peixinho, so the suspect's machine holds the phishing kit.

**Limitations / confidence:** Same file content; the Lab 1 copy was recovered from the public site. Which copy came first is not established.

## A133 -- `results/work/linux/home__johnnymusk__backups__peixinho__.git__config`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:43:45+00:00 |
| Parent artifact | A103 |
| Command | `linux-extract .../peixinho/.git/config` |
| stat | `results/work/linux/home__johnnymusk__backups__peixinho__.git__config|302|2026-10-06 07:42:51.486200345 +0000|2026-10-06 07:42:51.486200345 +0000` |
| Type | ASCII text |
| SHA-256 | `dd138156547b37e8615e3d4b8acd593958c63aa3f3b2367f247192f766d4cde5` |

**Observation:** Git config of the peixinho clone: remote origin = https://fenix.dpss.inesc-id.pt/.git/ (the phishing host of Lab 1).

**Interpretation:** The clone comes from the same host as the phishing site.

**Limitations / confidence:** Config only; the packed objects were not parsed in this step.

## A134 -- `results/work/linux/home__johnnymusk__backups__peixinho__.git__logs__HEAD`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:43:45+00:00 |
| Parent artifact | A103 |
| Command | `linux-extract .../peixinho/.git/logs/HEAD` |
| stat | `results/work/linux/home__johnnymusk__backups__peixinho__.git__logs__HEAD|189|2026-10-06 07:42:51.529890681 +0000|2026-10-06 07:42:51.529890681 +0000` |
| Type | Unicode text, UTF-8 text |
| SHA-256 | `c4ece29ffa88b579686831445634fefc4c75214b1cbd747e09e175df433cd76b` |

**Observation:** Git reflog: single entry, clone of https://fenix.dpss.inesc-id.pt/.git/ by 'António Alves <antonio@alves.at.eu.org>', epoch 1789858295 = 2026-09-19 22:51:35 UTC in the image, 2026-08-23 22:51:35 after the −27 day rule.

**Interpretation:** The clone happened on 23 Aug (adjusted). The author on the reflog is a different person from the suspect's account, and their role is open.

**Limitations / confidence:** Reflog shows the clone only; later fetches or merges are not recorded in this copy.

## A135 -- `results/work/linux/home__johnnymusk__snap__firefox__common__.mozilla__firefox__d98inpg9.default__places.sqlite`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:43:45+00:00 |
| Parent artifact | A103 |
| Command | `linux-extract places.sqlite (+ -wal)` |
| stat | `results/work/linux/home__johnnymusk__snap__firefox__common__.mozilla__firefox__d98inpg9.default__places.sqlite|5242880|2026-10-06 07:43:33.691718293 +0000|2026-10-06 07:43:33.691718293 +0000` |
| Type | SQLite 3.x database, user version 87 (0x57), last written using SQLite version 3053004, page size 32768, writer version 2, read version 2, file counter 2, database pages 53, cookie 0x2d, schema 4, UTF-8, version-valid-for 2 |
| SHA-256 | `d4d4198760119bbddaef5939e50e89e8a394a6f3006608cd61782c1676e6fec9` |

**Observation:** Firefox places.sqlite (with WAL) of the Linux user: 60 visits from 2026-09-21 11:23 to 14:48 (image time); searches and pages on steganography, polyglot files, JPEG DCT, LSB in video, spectrograms, CIELAB, CyberChef, file magic numbers, plus Portuguese and Russian news and a Portuguese SIS espionage alert.

**Interpretation:** Research on concealment techniques matches the methods in the bash history (A129); the news browsing is context, not proof of intent.

**Limitations / confidence:** Visit times are image times, to be shifted −27 days. Only the visits in this database are counted.

## A136 -- `results/work/linux/home__johnnymusk__myscripts__deploy.sh`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T07:43:45+00:00 |
| Parent artifact | A103 |
| Command | `linux-extract home/johnnymusk/myscripts/deploy.sh` |
| stat | `results/work/linux/home__johnnymusk__myscripts__deploy.sh|647|2026-10-06 07:43:33.789970985 +0000|2026-10-06 07:43:33.789970985 +0000` |
| Type | Bourne-Again shell script, ASCII text executable |
| SHA-256 | `b9d1f803f23aa66c512a8b1c5c7bd818471a2137d1632353e02f183bb3b519a5` |

**Observation:** deploy.sh from ~/myscripts (the file is in the Linux image; its content is registered here).

**Interpretation:** Part of the same personal automation as autosync.sh and automerge.sh; relevant to how the phishing site was deployed. Not read in detail yet.

**Limitations / confidence:** Scripts not analysed beyond the header in this step.
