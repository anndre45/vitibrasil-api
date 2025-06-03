from fastapi import FastAPI
from app.routes import routes


app = FastAPI(
    title="API Vitibrasil Embrapa",
    description="Consulta de dados vitivinícolas da Embrapa.",
    version="1.0.0"
)

app.include_router(routes.router)
