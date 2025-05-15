import requests

BASE_URL = "http://localhost:8000"
TOKEN = "teste"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "mensagem" in response.json()

def test_valid_category():
    response = requests.get(f"{BASE_URL}/categoria/Produção/2022", headers=HEADERS)
    assert response.status_code == 200
    assert "Dados" in response.json()

def test_invalid_token():
    headers = {"Authorization": "Bearer errado"}
    response = requests.get(f"{BASE_URL}/categoria/Produção/2022", headers=headers)
    assert response.status_code == 403

def test_missing_token():
    response = requests.get(f"{BASE_URL}/categoria/Produção/2022")
    assert response.status_code == 403

def test_invalid_category():
    response = requests.get(f"{BASE_URL}/categoria/INVALIDO/2022", headers=HEADERS)
    assert response.status_code == 400