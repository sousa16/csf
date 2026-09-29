import os

img_path = "../images/windows_laptop_memory.raw"
if not os.path.exists(img_path):
    img_path = "../../images/windows_laptop_memory.raw"

print("[*] A extrair a NumericalPassword do BitLocker na RAM...")

if os.path.exists(img_path):
    with open(img_path, "rb") as f:
        # Ir diretamente à zona dos 4.2 MB onde apareceu o NumericalPassword
        f.seek(4240000)
        data = f.read(5000)
        try:
            print(data.decode("utf-8", errors="ignore"))
        except:
            print(data)
else:
    print("[-] Imagem de memória não encontrada.")