import os
import csv
from pathlib import Path

CACHE_DIR = Path("./cache_embrapa")
CACHE_DIR.mkdir(exist_ok=True)

def salvar_em_csv(nome_arquivo, dados_lista):
    if not dados_lista:
        return

    # Cria conjunto com todas as colunas presentes
    colunas = set()
    for linha in dados_lista:
        colunas.update(linha.keys())
    colunas = list(colunas)

    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        for linha in dados_lista:
            writer.writerow(linha)


def carregar_de_csv(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return None

    with open(nome_arquivo, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
