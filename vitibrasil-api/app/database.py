import sqlite3
from pathlib import Path

DB_PATH = Path("data/vitibrasil.db")

def salvar_em_banco(dados, tabela="producao"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {tabela} (
            descricao TEXT,
            quantidade TEXT,
            valor TEXT
        )
    """)
    for linha in dados:
        cur.execute(f"INSERT INTO {tabela} VALUES (?, ?, ?)", (
            linha.get("Descrição"),
            linha.get("Quantidade"),
            linha.get("Valor", None)
        ))
    conn.commit()
    conn.close()