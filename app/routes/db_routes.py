from fastapi import APIRouter
from app.services.database import verificar_ou_criar

router = APIRouter()

@router.post("/carregar_categoria")
def carregar_categoria(ano: int, categoria: str):
    resultado = verificar_ou_criar(categoria, ano)
    return {"mensagem": resultado}
