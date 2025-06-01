from fastapi import FastAPI
from ..routes.routes import router

app = FastAPI(
    title="API Vitibrasil Embrapa",
    description="Consulta de dados vitivinícolas da Embrapa.",
    version="1.0.0"
)
app.include_router(router)