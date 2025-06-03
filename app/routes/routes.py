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
    """
    Pesquisa pela categoria e ano específica retornando os dados direto da fonte.
    Salva a consulta em cache no formato .CSV
    ___

    Fallback:
    Evitando sobrecarga na fonte, a rota procura primeiro se já não tem a pesquisa salva em cache antes de ir até o site da Embrapa.
    """
    try:
        return busca_categoria(ano, categoria)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/carregar/{categoria}/{ano}", dependencies=[Depends(check_auth)])
def guardar_no_banco(categoria: str, ano: int):
    """
    Reconhece o arquivo em cache pesquisado e então armazena o dado no banco.
    """
    nome_arquivo = f"{categoria}_{ano}"
    try:
        carregar_csv_para_db(nome_arquivo)
        return {"detail": f"Dados de {nome_arquivo} carregados com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar CSV: {str(e)}")