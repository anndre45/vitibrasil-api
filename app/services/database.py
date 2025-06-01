import os
import sqlite3
from app.services.scraping import busca_categoria

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "../db")
DB_PATH = os.path.join(DB_DIR, "embrapa.db")

def conectar_db():
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def tabela_existe(conn, nome_tabela):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (nome_tabela,))
    return cursor.fetchone() is not None

def criar_tabela(conn, tabela, tem_valor=False, tem_subcategoria=False):
    cursor = conn.cursor()
    colunas = ["descricao TEXT", "quantidade TEXT"]
    if tem_valor:
        colunas.append("valor TEXT")
    if tem_subcategoria:
        colunas.append("subcategoria TEXT")

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {tabela} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {', '.join(colunas)}
        );
    """)
    conn.commit()

def inserir_dados(conn, tabela, dados, subcategoria=None):
    cursor = conn.cursor()
    for item in dados:
        descricao = item.get("Descrição")
        quantidade = item.get("Quantidade")
        valor = item.get("Valor", None)
        if subcategoria:
            cursor.execute(
                f"INSERT INTO {tabela} (descricao, quantidade, valor, subcategoria) VALUES (?, ?, ?, ?)",
                (descricao, quantidade, valor, subcategoria)
            )
        else:
            cursor.execute(
                f"INSERT INTO {tabela} (descricao, quantidade, valor) VALUES (?, ?, ?)",
                (descricao, quantidade, valor)
            )
    conn.commit()

def verificar_ou_criar(categoria: str, ano: int):
    tabela = categoria.lower().replace("ç", "c").replace("ã", "a").replace("é", "e").replace(" ", "_")

    conn = conectar_db()
    if tabela_existe(conn, tabela):
        conn.close()
        return f"Tabela '{tabela}' já existe."

    dados = busca_categoria(ano, categoria)

    tem_valor = any(
        "Valor" in item
        for linhas in dados.values()
        for item in linhas
    )
    tem_subcategoria = len(dados) > 1

    # Cria tabela com colunas certas
    criar_tabela(conn, tabela, tem_valor=tem_valor, tem_subcategoria=tem_subcategoria)

    # Insere dados
    for chave, linhas in dados.items():
        inserir_dados(conn, tabela, linhas, subcategoria=chave if tem_subcategoria else None)

    conn.close()
    return f"Tabela '{tabela}' criada com sucesso."

