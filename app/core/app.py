from fastapi import FastAPI
from ..routes import routes, db_routes

app = FastAPI(
    title="API Vitibrasil Embrapa",
    description="Consulta de dados vitivinícolas da Embrapa.",
    version="1.0.0"
)
app.include_router(routes.router)
app.include_router(db_routes.router)