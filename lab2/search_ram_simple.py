import os

img_path = "../images/windows_laptop_memory.raw"
if not os.path.exists(img_path):
    img_path = "../../images/windows_laptop_memory.raw"

# Podes adicionar aqui as palavras que quiseres testar ou procurar
keywords = [b"password", b"pass", b"admin", b"joao", b"musky", b"shibuya", b"pimenta", b"johnny"]

print("[*] A procurar palavras-chave diretamente na RAM...")

chunk_size = 1024 * 1024 * 32  # Blocos de 32 MB
if os.path.exists(img_path):
    with open(img_path, "rb") as f:
        offset = 0
        matches = 0
        while matches < 25:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            for kw in keywords:
                idx = 0
                while True:
                    idx = chunk.lower().find(kw, idx)
                    if idx == -1:
                        break
                    snippet = chunk[max(0, idx-30):min(len(chunk), idx+60)]
                    try:
                        print(f"[Offset ~{offset + idx}] -> {snippet.decode('utf-8', errors='ignore').strip()}")
                        matches += 1
                        if matches >= 25:
                            break
                    except:
                        pass
                    idx += len(kw)
            offset += len(chunk)
else:
    print("[-] Imagem de memória não encontrada.")