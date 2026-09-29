import os
import re

img_path = "../images/windows_laptop_disk.dd"

if not os.path.exists(img_path):
    # Tenta procurar na pasta pai se estiveres na subpasta lab2
    img_path = "../../images/windows_laptop_disk.dd"

print("[*] A procurar por referências a Wallpaper, JJK, e Restaurantes na imagem do disco...")

# Palavras-chave que estamos a procurar para resolver as pistas
keywords = [b"wallpaper", b"gojo", b"jjk", b"fabrica", b"polvora", b"johny", b"johnny", b"musk"]

chunk_size = 1024 * 1024 * 64  # Ler em blocos de 64MB
found_matches = {kw: 0 for kw in keywords}

try:
    with open(img_path, "rb") as f:
        offset = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            for kw in keywords:
                if kw in chunk.lower():
                    found_matches[kw] += 1
                    print(f"[+] Encontrada a palavra '{kw.decode()}' perto do offset {offset / (1024*1024):.2f} MB")
            
            offset += len(chunk)
            if offset % (1024 * 1024 * 512) == 0:
                print(f"[*] Progresso: {offset / (1024*1024*1024):.2f} GB analisados...")

except Exception as e:
    print(f"[-] Erro ao ler a imagem: {e}")

print("\n[+] Resumo das ocorrências encontradas:")
for kw, count in found_matches.items():
    print(f"  - {kw.decode()}: {count} ocorrências")
    