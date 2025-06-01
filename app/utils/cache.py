# app/utils/cache.py
import threading
import os
from pathlib import Path

def agendar_exclusao_arquivo(path: Path, delay_segundos: int = 600):
    def excluir():
        if path.exists():
            try:
                os.remove(path)
                print(f"Arquivo {path} removido após {delay_segundos} segundos")
            except Exception as e:
                print(f"Erro ao remover {path}: {e}")
    threading.Timer(delay_segundos, excluir).start()
