# API Vitibrasil Embrapa

Essa API realiza web scraping do site da Embrapa (Vitibrasil) e retorna dados de:
- Produção
- Processamento
- Comercialização
- Importação
- Exportação

## Como executar
1. Instale os requisitos:
   ```
   pip install -r requirements.txt
   ```
2. Rode a API:
   ```
   python app/main.py
   ```
3. Acesse: `http://localhost:8000/docs` ou o link gerado pelo ngrok

## Endpoint de exemplo:
```
GET /categoria/Producao/2022
```

Autenticação: token "teste" no header Authorization como `Bearer teste`