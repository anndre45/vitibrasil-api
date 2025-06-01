import sqlite3
from pathlib import Path
from ..services.salvar_csv import CACHE_DIR
import csv

DB_PATH = Path(__file__).parent.parent / "db" / "embrapa.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def extrair_ano_do_nome(categoria_nome):
    try:
        return int(categoria_nome.rsplit('_', 1)[-1])
    except (ValueError, IndexError):
        raise ValueError(f"Não foi possível extrair o ano de '{categoria_nome}'.")
    
def criar_tabela_se_nao_existir(conn, tabela, colunas_csv):
    colunas = [col for col in colunas_csv if col not in {"id", "ano"}]
    colunas_ddl = ["id INTEGER PRIMARY KEY AUTOINCREMENT", '"ano" INTEGER']

    for c in colunas:
        colunas_ddl.append(f'"{c}" TEXT')

    ddl = f'CREATE TABLE IF NOT EXISTS "{tabela}" ({", ".join(colunas_ddl)})'
    conn.execute(ddl)
    conn.commit()

def inserir_dados(conn, categoria: str, dados: list, ano: int):
    if not dados:
        return

    colunas = list(dados[0].keys())
    if "ano" not in colunas:
        colunas = ["ano"] + colunas

    placeholders = ','.join('?' for _ in colunas)
    cols_joined = ','.join(f'"{col}"' for col in colunas)
    sql = f'INSERT INTO "{categoria}" ({cols_joined}) VALUES ({placeholders})'

    to_insert = []
    for row in dados:
        vals = []
        for col in colunas:
            if col == "ano":
                vals.append(ano)
            else:
                vals.append(row.get(col, None))
        to_insert.append(vals)

    conn.executemany(sql, to_insert)
    conn.commit()

def carregar_csv_para_db(nome: str):
    """
    Recebe o nome no formato "Categoria_Ano", por exemplo: "Processamento_2017",
    localiza o CSV e carrega os dados para o banco.
    """
    try:
        ano = extrair_ano_do_nome(nome)
    except ValueError as e:
        raise ValueError(str(e))

    arquivo = CACHE_DIR / f"{nome}.csv"
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {arquivo}")

    with open(arquivo, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        dados = list(reader)
        if not dados:
            raise ValueError("CSV vazio")

        colunas = reader.fieldnames or []

    conn = get_connection()
    try:
        criar_tabela_se_nao_existir(conn, nome.split('_')[0], colunas)
        inserir_dados(conn, nome.split('_')[0], dados, ano)
    finally:
        conn.close()