from fastapi import APIRouter, Depends, HTTPException
from ..services.scraping import busca_categoria
from ..utils.auth import check_auth

router = APIRouter()

@router.get("/")
def home():
    return {"mensagem": "API online! Consulte /docs para documentação."}

@router.get("/categoria/{categoria}/{ano}", dependencies=[Depends(check_auth)])
def dados_por_categoria(categoria: str, ano: int):
    try:
        dados = busca_categoria(ano, categoria)
        return {"Ano": ano, "Categoria": categoria, "Dados": dados}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
