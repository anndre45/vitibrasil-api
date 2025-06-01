from fastapi import FastAPI
from .app.utils.auth import check_auth
from .app.services.scraping import busca_categoria

from .app.routes import routes

app = FastAPI(
    title="API Vitibrasil Embrapa",
    description="Consulta de dados vitivinícolas da Embrapa.",
    version="1.0.0"
)

if __name__ == '__main__':
    app.run(debug=True)
