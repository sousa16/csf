import os

artifacts_dir = "../evidences/evidences/artifacts"
print("[*] A inspecionar subtitles.srt e outros artefactos...")

srt_path = os.path.join(artifacts_dir, "subtitles.srt")
if os.path.exists(srt_path):
    print("\n=== Conteúdo de subtitles.srt ===")
    with open(srt_path, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read()[:2000])

# Procurar menções a 'fabrica', 'polvora', 'wallpaper', ou nomes de personagens nas pastas
keywords = ["fabrica", "polvora", "restaurante", "wallpaper", "gojo", "sukuna", "shibuya", "canastra"]
for root, dirs, files in os.walk("../evidences"):
    for file in files:
        if file.endswith((".txt", ".srt", ".log", ".md", ".csv")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for line in content.splitlines():
                        if any(k in line.lower() for k in keywords):
                            print(f"[+] Encontrado em {file}: {line.strip()}")
            except:
                pass