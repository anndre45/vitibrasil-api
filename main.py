from fastapi import FastAPI
from app.utils.auth import check_auth
from app.services.scraping import busca_categoria
from app.core.app import app
from app.routes import routes


if __name__ == '__main__':
    app.run(debug=True)
