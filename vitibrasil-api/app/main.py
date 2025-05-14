import nest_asyncio
from pyngrok import conf, ngrok
from fastapi import FastAPI, Depends, HTTPException
from app.auth import check_auth
from app.scraping import busca_categoria

nest_asyncio.apply()
conf.get_default().auth_token = "SEU_TOKEN_NGROK_AQUI"

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

for tunnel in ngrok.get_tunnels():
    try:
        ngrok.disconnect(tunnel.public_url)
    except:
        pass

public_url = ngrok.connect(8000)
print(f"Acesse sua API em: {public_url}/docs")

import uvicorn
import threading

threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)).start()