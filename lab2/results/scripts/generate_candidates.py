#!/usr/bin/env python3
import hashlib, itertools

item1 = ["johnny-pc"]              # CONFIRMADO (registo, B004)
item2 = ["eren"]                   # NAO CONFIRMADO - suposicao do colega, so' para rastreio
item3 = ["shibuya"]                # NAO CONFIRMADO - idem
item4 = [""]                       # CONFIRMADO (hash NT vazio, SAM)
item5 = ["pimenta", "maria-pimenta"]  # NAO CONFIRMADO - idem

delimiters = ["-", "_"]

seen = set()
with open("candidates.txt", "w") as f:
    for d in delimiters:
        for combo in itertools.product(item1, item2, item3, item4, item5):
            raw = d.join(combo).lower()
            h = hashlib.sha256(raw.encode()).hexdigest()
            if h not in seen:
                seen.add(h)
                f.write(h + "\n")
print(f"{len(seen)} candidatos gerados em candidates.txt")
