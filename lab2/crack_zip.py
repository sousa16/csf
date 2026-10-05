import hashlib
import os
import zipfile

zip_path = "../evidences/evidences/artifacts/myzip.zip"
if not os.path.exists(zip_path):
    zip_path = "./myzip.zip"

# Lista de potenciais passwords do Windows a testar
candidate_passes = [
    "password", "123456", "admin", "root", "joao", "musky", "muskyboi",
    "eren", "shibuya", "gojo", "johnny", "windows", "1234", "qwerty",
    "portugal", "tecnico", "ist", "barcarena", "polvora", "pimenta",
    "maria", "armando", "sacos", "amelia", "sipc", "sigmanode", "joaomusk"
]

print("[*] A testar combinações para desbloquear o 'myzip.zip'...")

found = False
for p in candidate_passes:
    string_part = f"johnny-pc_eren_shibuya_{p}_maria-pimenta"
    h = hashlib.sha256(string_part.encode('utf-8')).hexdigest()
    
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.setpassword(h.encode('utf-8'))
            # Testar a leitura do ficheiro interno amelia.pdf
            zf.read("amelia.pdf")
            print(f"\n[+] SUCESSO! Password do Windows encontrada: '{p}'")
            print(f"[+] String completa: {string_part}")
            print(f"[+] Hash SHA-256 final: {h}")
            
            # Extrair o conteúdo para a pasta de destino
            zf.extractall("./unzipped_target")
            print("[+] Ficheiros extraídos com sucesso para './unzipped_target'!")
            found = True
            break
    except Exception:
        pass

if not found:
    print("[-] Nenhuma das passwords padrão coincidiu. Vamos extrair strings diretamente da memória/disco para encontrar a password exata do Windows.")