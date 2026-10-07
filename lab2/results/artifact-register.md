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

---

# Colleague register (Maria Pereira, branch lab2/maria)

Entries B001–B013 kept as the colleague recorded them. Where they overlap with A-entries, the A-entry is the one validated in our analysis.

## B001 — windows_laptop_disk.dd
- SHA-256: 5eca1f65df49ccf5bddeb8c5c3a44fe1a8a9e6faab04ed601d565b915bbaa6a8
- Size: 27917287424 bytes
- Parent: — (evidência original fornecida pelo curso)
- Command: N/A
- Observation: GPT, 5 partições (EFI, MSR, C: NTFS, Recovery NTFS, D: BitLocker)
- Interpretation:
- Limitations:

## B002 — windows_laptop_memory.raw
- SHA-256: c0b66a9ec5ff16d8c01726a8717648f729857fa059ba7485c5c1717587892be3
- Size: 1090326235 bytes
- Parent: —
- Command: N/A
- Observation: captura de memória viva, portátil ligado no momento da apreensão
- Interpretation:
- Limitations:

## B003 — linux_workstation_disk.dd
- SHA-256: b31261098d901de0be201f4f78f5816c946490b9eb4ae2c94dc2fcf4af4e3368
- Size: 20976780288 bytes
- Parent: —
- Command: N/A
- Observation: GPT, 2 partições (EFI boot FAT32, root Ext4); hostname johnny-dev
- Interpretation:
- Limitations: timestamps absolutos desta imagem levam correção de -27 dias (instrução do enunciado)

## B004 — ComputerName (registry SYSTEM hive)
- Value: JOHNNY-PC
- Parent: B001 (partição C: offset 122683392)
- Command: hivexsh; cd \Select; lsval Current  →  1
                       cd \ControlSet001\Control\ComputerName\ComputerName; lsval ComputerName
- Observation: ControlSet001 confirmed active (Select\Current = 1); ComputerName = JOHNNY-PC
- Interpretation: matches item 1 of the handwritten note ("My laptop's name")
- Limitations:

## B005 — BitLocker VMK hash (D: partition)
- File: bitlocker-hash.txt
- Parent: B001 (partição D: offset 21880635392)
- Command: sudo losetup -r -o 21880635392 --show -f windows_laptop_disk.dd  ->  /dev/loopX
           sudo bitlocker2john -i /dev/loopX
- Observation: 3 cópias redundantes do FVE metadata; VMK protegido por User Password (não só Startup Key/recovery key numérica)
- Interpretation: reforça a hipótese de que a password de 5 itens da nota manuscrita desbloqueia esta partição D:
- Limitations: hash obtido mas não crackado — ver B006/B007

## B006 — BitLocker crack attempt #1 (negative)

> **Superseded by A108.** Candidate-key validation (NTFS boot sector and $MFT record decrypt correctly) confirms the FVEK from memory. This attempt is kept as a negative result.
- Parent: B005
- Command: john --format=bitlocker bitlocker-hash.txt --wordlist=candidates.txt
- Candidates: johnny-pc / eren / shibuya / "" / pimenta|maria-pimenta (delimitadores "-" e "_")
- Observation: 0g cracked, 2 left
- Interpretation: falsifica esta combinação específica; eren/shibuya/pimenta nunca foram confirmados por evidência independente
- Limitations:

## B007 — BitLocker crack attempt #2 (negative)

> **Superseded by A108.** See B006.
- Parent: B005
- Command: windows.memmap --pid 3540/800 --dump; strings -a[-e l] | grep -E '^[0-9a-f]{64}$'; john --format=bitlocker
- Observation: 3 strings hex-64 encontradas em memória (WmiPrvSE.exe, svchost DcomLaunch/RPCSS); nenhuma desbloqueia o hash
- Interpretation: não são a passphrase BitLocker; D: permanece por desbloquear
- Limitations: plugin dedicado de extração de FVEK não disponível nesta toolchain (core Volatility3 nem community3)

## B008 — ProfileList discrepancy (johnny's profile on D:)
- Parent: B001 (SOFTWARE hive)
- Command: hivexsh; cd \Microsoft\Windows NT\CurrentVersion\ProfileList; ls / lsval ProfileImagePath
- Observation: entrada ativa do SID de johnny sem ProfileImagePath; entrada .bak do mesmo SID tem ProfileImagePath = D:\Users\johnny; pasta C:\Users só tem Administrator
- Interpretation: o perfil de utilizador de johnny reside na partição D: encriptada, não na C:
- Limitations: não foi possível confirmar a causa exata da entrada .bak sem acesso à D:

## B009 — Lab 1 hash cross-reference (Question 1)
- Parent: B001 + B003
- Command: sha256sum de todos os ficheiros em /tmp/mnt_winC, /tmp/mnt_linux_root, /tmp/mnt_linux_boot; grep -F contra known-hashes-lab1.txt
- Observation: 0 matches em todo o disco "ao vivo" (fora do stash.zip, ver B012)
- Interpretation: nenhuma cópia não-modificada de artefacto do Lab 1 existe solta nos sistemas de ficheiros; a única cópia está dentro do stash.zip (B012)
- Limitations: known-hashes-lab1.txt teve um erro de transcrição próprio (ESP32), corrigido após confirmação contra o artefacto oficial

## B010 — SSH config: infraestrutura remota "fenix-prod"
- File: home/johnnymusk/.ssh/config (linux_workstation_disk.dd, partição root)
- Observation: Host fenix-prod -> 146.193.41.109, user muskyboi, key ~/.ssh/muskyboi, StrictHostKeyChecking disabled
- Interpretation: liga esta máquina Linux ao utilizador MuskyBoi já identificado no Lab 1; 146.193.41.109 é candidato a IP do servidor de produção
- Limitations: ficheiro original tornou-se ilegível na segunda leitura (I/O error persistente na montagem, sectores 25560544/25531080 de linux_workstation_disk.dd via hgfs); evidence/linux/ssh-config.txt foi reconstruído a partir da transcrição verbatim do terminal confirmada anteriormente, não copiado byte-a-byte nesta sessão

## B011 — deploy.sh e repositório peixinho recuperado
- Files: home/johnnymusk/myscripts/deploy.sh; home/johnnymusk/backups/peixinho/ (git)
- Parent: B003
- Command: cat deploy.sh; cp -r (cópia de trabalho) + git log --oneline --all --graph; cat server.js; cat README.md
- Observation: deploy.sh clona git@gitlab.com:MuskyBoi/peixinho.git para fenix-prod e corre docker compose; server.js implementa captura de credenciais em /cas/login com redirecionamento para o Fenix real, headers HTTP forjados (Apache/PHP), bloqueio de acesso a credentials.txt e node_modules; commit final "cleanup" remove pastas pessoais e reescreve README.md para "peixinho / Fenix authentication frontend"
- Interpretation: código-fonte do site de phishing, com confissão escrita de que imita o portal Fenix do IST
- Limitations: deploy.sh tornou-se ilegível na segunda leitura (mesmo I/O error); evidence/linux/deploy.sh foi reconstruído a partir da transcrição verbatim do terminal confirmada anteriormente, não copiado byte-a-byte nesta sessão

## B012 — stash.zip decifrado via known-plaintext attack (bkcrack)
- Parent: B003 (backup sobrevivente em ~/backups/stash.zip)
- Method: ZipCrypto (pkzip legacy), vulnerável a known-plaintext attack
- Plaintext usado: evidences/artifacts/subtitles.srt (artefacto oficial do curso)
- Command: bkcrack -C stash.zip -c subtitles.srt -P subtitles_plain.zip -p subtitles.srt
           bkcrack -C stash.zip -k aa67c5cd 982388d2 08fdc364 -D stash_decrypted.zip
- Keys recovered: aa67c5cd 982388d2 08fdc364
- Observation: 8 de 9 ficheiros extraídos são SHA-256 idênticos aos artefactos oficiais do Lab 1: blank, dj_cara_after_hours.wav, [Erai-raws]...mkv, GrandTheftAutoVITrailer1.mp4, gta_v_iceberg_unexplained.jpg (RECUPERADO, em falta desde o Lab 1), myzip.zip, polish_cow.webp, ESP32_ADXL345_3Axis_Telemetry.xlsx. subtitles.srt não é comparável (usado como plaintext)
- Interpretation: prova criptográfica de que johnnymusk possuía uma cópia local do conjunto de artefactos-fonte do Lab 1, escondida num zip encriptado num backup que sobreviveu ao srm de ~/repos
- Limitations: raw extracted files not committed to evidence/ (several exceed GitHub's 100MB limit; all are byte-identical to the course-provided Stage I originals already in evidences/artifacts/). Proof retained as SHA-256 comparison above and evidence/linux/stash-contents-manifest.txt.

## B013 — Git remote "origin" e identidade do autor do commit
- Parent: B011
- Command: git remote -v; cat .git/config; git log --all --format="%H %an %ae %s"
- Observation: origin = https://fenix.dpss.inesc-id.pt/.git/ (subdomínio real do grupo de investigação DPSS do INESC-ID/IST), distinto do URL do GitLab usado pelo deploy.sh; commit de merge tem autor "Johny Musk <sussyjohnnyhacker@gmail.com>"
- Interpretation: possível proveniência via técnica de .git exposto (como no Lab 1) contra um projeto IST/INESC-ID não relacionado; email pessoal reforça atribuição independentemente
- Limitations: não foi possível confirmar se o .git em fenix.dpss.inesc-id.pt ainda está exposto, nem a natureza exata desse projeto, dentro do tempo disponível

## A137 -- `results/work/cdrive/Security.evtx`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 images/windows_laptop_disk.dd 89098` |
| stat | `results/work/cdrive/Security.evtx|3215360|2026-10-06 08:12:10.550602501 +0000|2026-10-06 08:12:10.550602501 +0000` |
| Type | MS Windows 10-11 Event Log, version  3.2, 48 chunks (no. 47 in use), next record no. 4406 |
| SHA-256 | `29e6a0df28080267b2e470e946a202dd1ff27598b6deedbd593b7e7ad49ba36f` |

**Observation:** Security event log (C:, inode 89098). 900 logon events (4624), 880 special-privilege events (4672), 786 explicit-credential events (4648). Logons on 22 Aug 09:29-09:31 UTC and 25 Aug 21:02-21:03 UTC are WinRM-style network logons (type 3, Negotiate, ws JOHNNY-PC, IpAddress '-').

**Interpretation:** Two WinRM sessions on these dates: 22 Aug authenticated as johnny; 25 Aug as Administrator. The same logon pattern appears for both.

**Limitations / confidence:** IpAddress '-' is how this log records WinRM network logons here. It does not prove the origin is local. The 25 Aug session is shown to be remote by the memory netscan (A101).

## A138 -- `results/work/cdrive/Microsoft-Windows-WinRM_Operational.evtx`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 ... 90414` |
| stat | `results/work/cdrive/Microsoft-Windows-WinRM_Operational.evtx|1052672|2026-10-06 08:12:10.634927761 +0000|2026-10-06 08:12:10.634927761 +0000` |
| Type | MS Windows 10-11 Event Log, version  3.2, 13 chunks (no. 12 in use), next record no. 1943 |
| SHA-256 | `3e368494f50bf4cc35d1bb31bbe7eb91217c9d2eb94fb7311c36381ec6706872` |

**Observation:** WinRM Operational log (inode 90414): 611 + 610 + 589 events (IDs 145, 132, 254) and 110 session-created events (ID 91). The session-created events fall on 28 Jul (101), 22 Aug (5, 09:30:31-09:30:38 UTC) and 25 Aug (4, 21:02:39-21:02:57 UTC).

**Interpretation:** Three separate WinRM activity periods. 28 Jul looks like provisioning; 22 Aug and 25 Aug are the sessions of interest.

**Limitations / confidence:** The event does not record the client address. The 22 Aug client origin is not confirmed.

## A139 -- `results/work/cdrive/Microsoft-Windows-PowerShell_Operational.evtx`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 ... 90170` |
| stat | `results/work/cdrive/Microsoft-Windows-PowerShell_Operational.evtx|69632|2026-10-06 08:12:10.687534163 +0000|2026-10-06 08:12:10.687534163 +0000` |
| Type | MS Windows 10-11 Event Log, version  3.2, 1 chunks (no. 0 in use), next record no. 595 |
| SHA-256 | `2467ae88d623459f9244ad633b3943feb8adcf73b67fac63eac9408c307739a7` |

**Observation:** PowerShell Operational log (inode 90170). One script-block event (4104, record 585, 22 Aug 09:29:36 UTC): a block that copies files into a destination folder and then sets CreationTime, LastWriteTime and LastAccessTime from a metadata table. Path C:\Windows\Temp\Modules\Forensics.psm1. Also 9 engine-lifecycle events (40961/40962/53504) at 22 Aug 09:30:31-09:30:37 UTC.

**Interpretation:** Timestomping: the script overwrites file times from supplied metadata, so the injected files would show the chosen dates. Executed over WinRM on 22 Aug at the end of the reported phishing window.

**Limitations / confidence:** Only the script block is recorded; the module file itself is not in the live listing or found as a deleted entry, so the injected files are unknown. Who wrote the script is not established.

## A140 -- `results/work/cdrive/System.evtx`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 ... 89094` |
| stat | `results/work/cdrive/System.evtx|1118208|2026-10-06 08:12:10.741788895 +0000|2026-10-06 08:12:10.741788895 +0000` |
| Type | MS Windows 10-11 Event Log, version  3.2, 4 chunks (no. 3 in use), next record no. 532 |
| SHA-256 | `1da2c58c5738b96c86f40c17fee02e11f26b70e2423e71e37d682c0c36093126` |

**Observation:** System log (inode 89094). Contains one 'log file cleared' event (ID 104) on 28 Jul 2026 20:16:35 UTC, subject johnny (JOHNNY-PC), channel Microsoft-Windows-PowerShell/Operational. Otherwise routine service and driver events.

**Interpretation:** The PowerShell Operational log was cleared by johnny on 28 Jul, the same second as the deletion of background.jpg in the USN journal (A122). This is an anti-forensic action on the Windows laptop.

**Limitations / confidence:** Only one clearing record exists; the Security log has no 1102 (cleared) event. Whether other logs were cleared without a record is not known.

## A141 -- `results/work/cdrive/WINRSHOST.EXE-DD38ED4A.pf`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 ... 90438` |
| stat | `results/work/cdrive/WINRSHOST.EXE-DD38ED4A.pf|3432|2026-10-06 08:12:10.772938920 +0000|2026-10-06 08:12:10.772938920 +0000` |
| Type | data |
| SHA-256 | `2a5e57c55a5a5692a0a90ae42ee0a2ff0f65e1495ed4d1ec5459908cf29ff25e` |

**Observation:** Prefetch WINRSHOST.EXE: 13 runs. Last runs: 22 Aug 09:30:31.32 and 09:30:31.18 UTC; then a burst on 28 Jul 20:10-20:14 UTC.

**Interpretation:** winrshost.exe ran on 22 Aug at the same time as the timestomping script. Prefetch does not show the 25 Aug run seen in memory.

**Limitations / confidence:** Prefetch keeps only the last 8 run times, and the 25 Aug run is missing, so Prefetch and memory disagree; not explained yet.

## A142 -- `results/work/cdrive/POWERSHELL.EXE-CA1AE517.pf`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 ... 90453` |
| stat | `results/work/cdrive/POWERSHELL.EXE-CA1AE517.pf|35615|2026-10-06 08:12:10.799034997 +0000|2026-10-06 08:12:10.799034997 +0000` |
| Type | data |
| SHA-256 | `fbf8f0b5ff58fea3a8d0d11d37de4ae4de6532cca266b5952ef3bec29b0ef340` |

**Observation:** Prefetch POWERSHELL.EXE: 11 runs. Last run 22 Aug 09:30:31.44 UTC; then a burst on 28 Jul 20:10-20:14 UTC.

**Interpretation:** Consistent with A139 (PowerShell used at 09:30 on 22 Aug).

**Limitations / confidence:** Same caveat as A141: no 25 Aug run recorded.

## A143 -- `results/work/cdrive/setupapi.dev.log`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | 239616 |
| Command | `icat -o 239616 ... 90261` |
| stat | `results/work/cdrive/setupapi.dev.log|11096|2026-10-06 08:12:10.826896986 +0000|2026-10-06 08:12:10.826896986 +0000` |
| Type | Generic INItialization configuration [BeginLog] |
| SHA-256 | `c026d59a4c79d211bdf6fa6b0a40d203780595a746677fc6cb0ff9e1fb2238a6` |

**Observation:** setupapi.dev.log (133 lines): one driver install (Microsoft Print To PDF) at boot session 28 Jul 21:11 UTC. No USB mass-storage device installation. The SYSTEM hive has no 'Disk&Ven' entries.

**Interpretation:** The USB drive labelled TEARSINRAIN (bash history, A129) was never connected to this Windows laptop. Copying the Stage I material was done on the Linux workstation.

**Limitations / confidence:** Absence of records. The PowerShell log was cleared on 28 Jul (A140), so a device could have been plugged in before that without a record in the logs that survive; setupapi is not cleared by that event, so the absence here is still informative.

## A144 -- `results/analysis/evtx/ps4104.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | A139 |
| Command | `evtx_dump.py show PowerShell_Operational.evtx 4104` |
| stat | `results/analysis/evtx/ps4104.txt|1872|2026-10-06 08:15:45.548040211 +0000|2026-10-06 08:15:45.548040211 +0000` |
| Type | ASCII text |
| SHA-256 | `00b9e927c28f00deea7b75f8d4dea841933047cd401e0f03e7c60e0324cc3651` |

**Observation:** PowerShell 4104 record in full (A139), exported to text.

**Interpretation:** See A139.

**Limitations / confidence:** See A139.

## A145 -- `results/analysis/evtx/logons_0822_0825.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:15:51+00:00 |
| Parent artifact | A137 |
| Command | `evtx_dump.py / pyevtx: 4624/4648 for 22 Aug 09:2x-09:3x and 25 Aug 21:0x` |
| stat | `results/analysis/evtx/logons_0822_0825.txt|11146|2026-10-06 08:15:45.956856199 +0000|2026-10-06 08:15:45.956856199 +0000` |
| Type | ASCII text |
| SHA-256 | `6fa40928e7f33a0a3a5711a9eee49b348f54b82de20f12ec0b5bce691795d10a` |

**Observation:** Logon events 4624/4648 on 22 Aug 09:20-09:40 and 25 Aug 21:00-21:10 UTC, extracted to a table (121 lines).

**Interpretation:** Shows the user and logon type for each session; johnny on 22 Aug, Administrator on 25 Aug.

**Limitations / confidence:** Table derived from the Security log; the IP field is '-' throughout.

## A146 -- `results/analysis/30_matches_cfiles.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T08:50:14+00:00 |
| Parent artifact | A101 |
| Command | `kali.sh hashmatch results/work/cfiles (570 files from C: Users, ProgramData, Windows/Temp, Recovery)` |
| stat | `results/analysis/30_matches_cfiles.txt|0|2026-10-06 08:50:14.211910507 +0000|2026-10-06 08:50:14.211910507 +0000` |
| Type | empty |
| SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

**Observation:** Hash-match of 570 regular files from C: Users/, ProgramData/, Windows/Temp/ and Recovery/ against the 16 Stage I hashes: 0 matches.

**Interpretation:** None of the Stage I files is present as a live, readable file on the C: partition.

**Limitations / confidence:** Live files only; Windows System32, WinSxS and deleted content were not searched. Matching is by SHA-256 of the whole file, so modified or partial copies would not match.

## A147 -- `results/analysis/journal_grep.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T10:11:56+00:00 |
| Parent artifact | A103 |
| Command | `jls/jcat dump of the ext4 journal (results/work/journal/journal.bin), grep for workspace and Stage I names` |
| stat | `results/analysis/journal_grep.txt|63|2026-10-06 10:11:56.682577757 +0000|2026-10-06 10:11:56.682577757 +0000` |
| Type | ASCII text |
| SHA-256 | `ced3b7093a798b3701a102bc7d464b21d347e5f80e62024e2b98a961ffcedb1a` |

**Observation:** ext4 journal of the Linux disk (268 MB, 65,535 blocks): no occurrence of 'ducky', 'hidings', 'stash.zip', 'check-later' or any Stage I filename. 'repos', 'blank', 'subtitles' occur only in unrelated package names; 'peixinho' occurs twice as a directory entry.

**Interpretation:** The journal does not keep the names of the directories removed with srm. The 'peixinho' hits are consistent with A134/A135 and do not add a new event.

**Limitations / confidence:** The journal is a rolling log; older transactions may already be overwritten. Only the blocks in the journal were searched, not unallocated space.

## A148 -- `results/analysis/30_matches_lfiles.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T10:11:57+00:00 |
| Parent artifact | A103 |
| Command | `kali.sh hashmatch results/work/lfiles (81 files from Linux home/, excluding snap/cache)` |
| stat | `results/analysis/30_matches_lfiles.txt|0|2026-10-06 10:11:44.441693463 +0000|2026-10-06 10:11:44.441779588 +0000` |
| Type | empty |
| SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

**Observation:** Hash-match of 81 regular files under Linux home/ (excluding snap, cache and Firefox profile) against the 16 Stage I hashes: 0 matches.

**Interpretation:** No Stage I file is stored unencrypted in the user's home directory. The sources are only present inside stash.zip (A126), which is encrypted.

**Limitations / confidence:** Live files only; Firefox profile and deleted content not searched. Matching is by whole-file SHA-256.

## A149 -- `results/work/linux/acme_token.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T11:11:59+00:00 |
| Parent artifact | A103 |
| Command | `icat -o 2203648 images/linux_workstation_disk.dd (home/johnnymusk/backups/peixinho/.well-known/acme-challenge/9xQ3...)` |
| stat | `results/work/linux/acme_token.txt|65|2026-10-06 11:11:43.468070724 +0000|2026-10-06 11:11:43.468070724 +0000` |
| Type | ASCII text |
| SHA-256 | `69296b1d98e75e397d885f5c9caef8650676094188e05484b57011ba2ea11643` |

**Observation:** Same token as Lab 1 A005 (9xQ3nM7kV2pR5sT8wY4zA6bC1dF0gHjL.N4vY7uP2qW9mK5sR8xT3zB6cD1fG0hJ). The bytes differ only in the line ending: CRLF in A005 (66 bytes, SHA 9ee8314a...) and LF here (65 bytes, SHA 69296b1d...).

**Interpretation:** The file in the suspect's repository is the planted acme-challenge file from the phishing site (A005). The line-ending difference suggests the repository copy and the copy served by the site were saved by different tools.

**Limitations / confidence:** Content comparison only. Which copy was written first is not established.

## A150 -- `results/analysis/30_matches_lab1all.txt`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T12:20:09+00:00 |
| Parent artifact | A103 |
| Command | `kali.sh hashmatch results/work/lab1all (114 Lab 1 evidence and results files, flat copy)` |
| stat | `results/analysis/30_matches_lab1all.txt|829|2026-10-06 12:19:21.588679251 +0000|2026-10-06 12:19:21.588679251 +0000` |
| Type | ASCII text |
| SHA-256 | `d4eead55ac291519fbb58178b154bd6ef4cd90ddbc6d87d188f78cc7083c0551` |

**Observation:** Hash-match of 114 Lab 1 evidence and results files against the 16 Stage I hashes: 12 matches. Table 2 hidden files f1.png (blank-fixed.png), f2.json (polish_cow-payload.json), amelia.pdf (amelia2.pdf) and f8.webp (aot-telegram-chat.webp, aot_payload.webp) are present. The published Telemetry.xlsx matches Table 1.

**Interpretation:** Four of the eight hidden files are verified against the Lab 1 recovery. The remaining hidden files f4, f5, f6 and f7 are not in Lab 1 by hash.

**Limitations / confidence:** Whole-file SHA-256 match only.

## A151 -- `results/work/stash/../hidden_f4_candidate.pdf`

| Field | Value |
| --- | --- |
| Registered (UTC) | 2026-10-06T12:20:09+00:00 |
| Parent artifact | A124 |
| Command | `carved from Grand Theft Auto VI Trailer 1.mp4 at byte 9357945 to EOF; trimmed after %%EOF (+1 byte)` |
| stat | `results/work/stash/../hidden_f4_candidate.pdf|85981|2026-10-06 12:19:41.442893653 +0000|2026-10-06 12:19:41.442893653 +0000` |
| Type | PDF document, version 1.5 |
| SHA-256 | `86e469294263367ad841b7c91f405e658a437229d5c7ec15ebefee19109265af` |

**Observation:** PDF carved from byte 9357945 of the GTA trailer (A016 in Lab 1 / A124 stash copy), trimmed at the final %%EOF plus one newline. Title: 'Independent External Technical Assessment Report - Project AMELIA'. SHA-256 0a4ac4174b6e68c7e92912c588e67dbf351a332d201c857f592fedb0397d005f, matching Table 2 f4.pdf.

**Interpretation:** Hidden file f4.pdf is embedded in the GTA trailer (polyglot), as the bash history indicates (A129: polyglot_create.sh with Technical_Assurance.pdf).

**Limitations / confidence:** Hash equality with Table 2 is the verification. The one trailing newline after %%EOF was needed to match; other trimming gave other hashes.

## A152 -- `evidence/windows/mom-photo.jpg` (note part 3 identified)
- Parent: A111 (same file, recovered from D: `\Users\johnny\Pictures\mom-photo.jpg`, inode 939)
- SHA-256: `fe8f99ce75f92a4aee463d5b535d2737e0e042d8bfb59bf44d123c9704f6be55`
- Command: `cp` from the decrypted D: (A109); committed to `evidence/windows/`; identification by reverse image search (search-by-image on the picture).
- Observation: 474x266 JPEG; an anime train-platform scene (a train with an "8 CARS" head-car display and a crowd in Halloween costumes). A152 reverse image search returns this as a still from the anime *Jujutsu Kaisen*, "Shibuya Incident" arc, set at Shibuya Station.
- Interpretation: this is the "JJK picture" of note part 3; its region is Shibuya, so part 3 = `shibuya`. This supplies the external source that A111 left open ("not established").
- Limitations: the identification rests on an external image search, not on content inside the file; it is corroborated cryptographically by the note-password oracle (A125), where `shibuya` is one of the five parts that open stash.zip.

## A153 -- `evidence/windows/hate-this-place.jpg` (note part 5 identified)
- Parent: A112 (same file, recovered from D: `\Users\johnny\Pictures\hate-this-place.jpg`, inode 938)
- SHA-256: `c323d401bd25fd8a6ae6e3b8f7dba724ce95d51c886b15653a2f5a0863c800c8`
- Command: `cp` from the decrypted D: (A109); committed to `evidence/windows/`; identification by reverse image search.
- Observation: 1200x900 JPEG; a yellow single-storey building with a terracotta-tiled roof and a terrace under pine trees. A153 reverse image search returns this building as the restaurant "Maria Pimenta", located inside the Fábrica da Pólvora de Barcarena (Oeiras).
- Interpretation: this is the restaurant photo of note part 5 ("Mom's photo of Fábrica de Pólvora ... the spot itself of the restaurant"); the restaurant is Maria Pimenta, so part 5 = `pimenta`. This supplies the external source that A112 left open ("no source yet").
- Limitations: the name is not written in the image; the identification rests on an external image search and is corroborated cryptographically by the note-password oracle (A125), where `pimenta` is one of the five parts that open stash.zip.

## A154 -- image steganalysis of the two part-3/part-5 photos (negative)
- Parent: A152, A153
- Command: `python3 results/scripts/image_steg_check.py <img>` (JPEG COM/EXIF markers, trailing data after FFD9, spatial-LSB class-baseline over channel/bit orders); plus `steghide info`, `steghide extract -p ""`, `stegseek <img> rockyou.txt`.
- Observation: no COM comment; EXIF is 64 bytes of orientation only (mom-photo) or absent (hate-this-place); 0 bytes after the final FFD9; no spatial-LSB payload in any order; steghide/stegseek found no embedded data or passphrase on either image.
- Interpretation: the words "shibuya" and "pimenta" are not hidden inside the images by steganography; they are read by recognising the depicted scene/place (A152, A153). Negative finding recorded per Good-Practice Manual §5.
- Limitations: transform-domain tools beyond steghide (outguess, jsteg) were not installed on the analysis host and could not be run; recorded as a limitation.

## A155 -- `evidence/windows/ConsoleHost_history.txt` (PowerShell command history, D:)
- File: `/Users/johnny/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/ConsoleHost_history.txt` on D: (MFT inode 1102)
- SHA-256: `53dcd531d211c2a219df6ff859357c9ce018296e53106a0b097c9d3356314372`
- Parent: A109 (decrypted D: volume)
- Command: `sudo icat /mnt/dislocker/dislocker-file 1102 > evidence/windows/ConsoleHost_history.txt` (inode from `stat`/`fls` of the mounted D:)
- Observation: three PowerShell commands, in entry order:
  1. `ssh muskyboi@146.193.41.109 "cat ~/fenix/peixinho/credentials.txt"`
  2. `ssh ist101337@sigma.ist.utl.pt`
  3. `scp ist101337@sigma.ist.utl.pt:~/Linguagem_Natural/Exams/Natural_Language_MAP1_2026-2027.pdf D:\Users\johnny\Desktop\Exams_LN\`
- Interpretation: command 1 is the laptop user connecting to the production phishing host (`146.193.41.109`, user `muskyboi` -- the host and account from the SSH config A010 / deploy.sh) and reading the harvested `credentials.txt`, i.e. operating/monitoring the phishing campaign from this laptop. Commands 2-3 use the account `ist101337` to log in to `sigma.ist.utl.pt` and copy an LN exam PDF into `Desktop\Exams_LN\` on D: -- exfiltration of exam material. This matches the exam file recorded in the USN journal (A122, E4) and the to-do note (A130). `ist101337` is a new identifier not seen before in the case.
- Limitations: PSReadLine history is not timestamped, so the order is entry order, not proven wall-clock times, and the file does not show whether each command succeeded. Whether `ist101337` is the suspect's own IST account or a credential obtained through the phishing campaign is not established by this file alone.
