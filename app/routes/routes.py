from fastapi import APIRouter, Depends, HTTPException
from ..services.database import carregar_csv_para_db
from ..services.scraping import busca_categoria
from ..utils.auth import check_auth

router = APIRouter()

@router.get("/")
def home():
    return {"mensagem": "API online! Consulte /docs para documentação."}

@router.get("/categoria/{categoria}/{ano}", dependencies=[Depends(check_auth)])
def dados_por_categoria(categoria: str, ano: int):
    try:
        return busca_categoria(ano, categoria)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/carregar/{categoria}/{ano}", dependencies=[Depends(check_auth)])
def carregar_csv(categoria: str, ano: int):
    nome_arquivo = f"{categoria}_{ano}"
    try:
        carregar_csv_para_db(nome_arquivo)
        return {"detail": f"Dados de {nome_arquivo} carregados com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar CSV: {str(e)}")