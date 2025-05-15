import nest_asyncio
from fastapi import FastAPI, Depends, HTTPException
from .auth import check_auth
from .scraping import busca_categoria

nest_asyncio.apply()

app = FastAPI(
    title="API Vitibrasil Embrapa",
    description="Consulta de dados vitivinícolas da Embrapa.",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"mensagem": "API online! Consulte /docs para documentação."}

@app.get("/categoria/{categoria}/{ano}", dependencies=[Depends(check_auth)])
def dados_por_categoria(categoria: str, ano: int):
    try:
        dados = busca_categoria(ano, categoria)
        return {"Ano": ano, "Categoria": categoria, "Dados": dados}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
