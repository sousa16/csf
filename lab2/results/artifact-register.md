# Artifact Register — Lab Assignment II (Operation DeepFISH — Stage II)

Format per Good-Practice Manual §3/§4. IDs prefixed `B0xx` to avoid collision with Lab 1's `A0xx`.

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
- Parent: B005
- Command: john --format=bitlocker bitlocker-hash.txt --wordlist=candidates.txt
- Candidates: johnny-pc / eren / shibuya / "" / pimenta|maria-pimenta (delimitadores "-" e "_")
- Observation: 0g cracked, 2 left
- Interpretation: falsifica esta combinação específica; eren/shibuya/pimenta nunca foram confirmados por evidência independente
- Limitations:

## B007 — BitLocker crack attempt #2 (negative)
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

## B020 — D: volume decrypted (FVEK from memory)
- Parent: B002 (windows_laptop_memory.raw) + B001 (D:, offset 21880635392)
- Command: `git clone github.com/lorelyai/volatility3-bitlocker`;
  `vol -vvv -p results/work/plugins -f windows_laptop_memory.raw windows.bitlocker.BitlockerFVEKScan --tags FVEc Cngb None --dislocker`;
  `dislocker -v -k 0x<off>-Dislocker.fvek -V <loop @ 21880635392> /mnt/dislocker`; `mount -t ntfs-3g -o ro /mnt/dislocker/dislocker-file /mnt/dvol`
- Observation: scan devolveu 3 candidatos; só o de tag `None` é um par AES-XTS-128 completo (FVEK + tweak); os Cngb não têm tweak. Com essa chave o dislocker monta a D: read-only; boot sector lê `NTFS`, `$MFT` record 0 lê `FILE`.
- Interpretation: a D: desbloqueia pela FVEK residente em memória (volume de dados com auto-unlock), sem a password de utilizador. A nota manuscrita NÃO foi necessária para abrir a D:. Corrige o B005–B007, onde a D: ficou por abrir.
- Limitations: os bytes da FVEK são material de chave; guardados em ficheiro de scratch gitignored, não committados.

## B021 — mom-photo.jpg (parte 3 da nota)
- File: `/Users/johnny/Pictures/mom-photo.jpg` na D: (inode 939)
- SHA-256: `fe8f99ce75f92a4aee463d5b535d2737e0e042d8bfb59bf44d123c9704f6be55`
- Command: `cp` da D: montada; `sha256sum`
- Observation: JPEG 474x266; cena anime de plataforma de estação — comboio com display "8 CARS" e multidão em fatos de Halloween (chifres, capuzes). Sem EXIF de GPS/câmara.
- Interpretation: é o "Shibuya Incident" de Jujutsu Kaisen (Estação de Shibuya, 31 out). O "JJK picture / My Blue Eyes thing" (Gojo Satoru) da nota nomeia a sua região: parte 3 = `shibuya`.
- Limitations: o nome do ficheiro não corresponde ao conteúdo; a identificação é por reconhecimento da cena. Confirmado criptograficamente em B024.

## B022 — hate-this-place.jpg (parte 5 da nota)
- File: `/Users/johnny/Pictures/hate-this-place.jpg` na D: (inode 938)
- SHA-256: `c323d401bd25fd8a6ae6e3b8f7dba724ce95d51c886b15653a2f5a0863c800c8`
- Command: `cp` da D: montada; `sha256sum`
- Observation: JPEG 1200x900; edifício amarelo de um piso, telhado de telha, esplanada com chapéus-de-sol e mesas sob pinheiros, pátio em calçada. Sem EXIF de GPS/câmara; sem placa legível.
- Interpretation: é o restaurante **Maria Pimenta** na Fábrica da Pólvora de Barcarena (corresponde às fotos públicas do restaurante). O "Mom's photo of Fábrica de Pólvora … the spot itself of the restaurant" da nota nomeia-o: parte 5 = `pimenta`.
- Limitations: o nome não está escrito na imagem; identificação por reconhecimento do edifício/local. Confirmado criptograficamente em B024.

## B023 — esteganálise das imagens (negativo)
- Parent: B021, B022
- Command: `python3 results/scripts/image_steg_check.py <img>` (markers COM/EXIF, trailing após FFD9, LSB espacial em várias ordens); `steghide info`; `steghide extract -p ""`; `stegseek <img> rockyou.txt`
- Observation: sem comentário COM; EXIF é só 64 B de orientação (mom-photo) ou inexistente (hate-this-place); 0 bytes após o FFD9 final; sem payload LSB espacial em nenhuma ordem; steghide/stegseek não encontraram dados nem passphrase em nenhuma das imagens.
- Interpretation: as partes 3 e 5 NÃO estão escondidas por esteganografia nas imagens. São estabelecidas por reconhecimento da cena/local (B021, B022) e confirmadas pelo oráculo (B024). Resultado negativo registado (§5).
- Limitations: ferramentas transform-domain além do steghide (outguess, jsteg, F5) são o último passo; registar o seu resultado se corridas.

## B024 — partes 3 e 5 confirmadas contra o stash.zip
- Parent: B021, B022, B012 (stash.zip, ZipCrypto)
- Command: `python3 results/scripts/decode_note_parts.py results/work/zip/stash.zip`
- Observation: fixando as partes 1/2/4 (`johnny-pc`,`elliot`,`fsociety`), a recipe `sha256(johnny-pc_elliot_shibuya_fsociety_pimenta)` = `ab99749a576b8070ddf665ce139afd43e7c2a3f5b55b3173e98791c281c1454d` é o único par (p3,p5) candidato que abre o arquivo; o primeiro membro encriptado lê com CRC válido.
- Interpretation: partes 3 = `shibuya` e 5 = `pimenta` ficam unicamente confirmadas pelo arquivo recuperado. String completa da password: `johnny-pc_elliot_shibuya_fsociety_pimenta`. Nota: a parte 2 é `elliot` (wallpaper Mr. Robot) e a parte 4 é `fsociety` (hash NT `fb06de73…2934`, não vazio) — corrige qualquer leitura anterior de password vazia.
- Limitations: o oráculo confirma a string de cinco partes como conjunto; o significado de cada parte assenta na sua fonte (B021/B022 para 3/5). O ZIP foi lido, nunca modificado.
