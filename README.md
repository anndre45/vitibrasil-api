# API Vitibrasil Embrapa

API desenvolvida como parte do Tech Challenge da FIAP, Fase 1 (Machine Learning Engineering).  
Ela realiza scraping automatizado dos dados de vitivinicultura do site da Embrapa (Vitibrasil) e os entrega de forma estruturada via endpoints REST.

---

## 🔧 Funcionalidades

- Rota de autenticação via token Bearer
- Consulta de dados por categoria e ano
- Cache de dados via csv com timer de limpeza de 30 minutos
- Web scraping com navegação por subopções
- Retorno de dados em JSON estruturado
- Carregamento de dados em DB (SQLite3)

---

## 💡 Cenário de uso para Machine Learning

Os dados fornecidos pela API poderão futuramente alimentar modelos preditivos de aprendizado de máquina (Machine Learning).

Um exemplo prático seria o desenvolvimento de um modelo para prever a produção de uvas por estado e por ano com base no histórico de dados. Isso seria útil para:
- Previsão de safras
- Análise de tendência de mercado
- Planejamento de importações/exportações
- Apoio a políticas públicas agrícolas

---

## 🧱 Arquitetura da Solução

```
[Usuário / Aplicação Externa]
            |
            v
   [FastAPI com autenticação]
            |
            v
   [Scraping com BeautifulSoup]
            |
            v
[Site da Embrapa (vitibrasil.cnpuv)] <-> Caching em CSV
            |
            v
 [Retorno estruturado (JSON)]  
            |
            v
 [Carregamento de dados em DB]
```

---

## ▶️ Como rodar o projeto localmente

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Rode a API:
```bash
uvicorn main:app --reload 
```

3. Acesse a documentação automática:
```
127.0.0.1:8000/docs
```

## ▶️ Acesse a API diretamente

```
https://vitibrasil-api-b7vo.onrender.com/docs
```
---

## 🔐 Autenticação

Todas as rotas exigem autenticação via token.

- Tipo: Bearer Token
- Token de teste: `teste`

Exemplo de uso no header:
```
Authorization: Bearer teste
```

---

## 📬 Exemplo de uso

Requisição:
```
GET /categoria/Produção/2022
Authorization: Bearer teste
```

Retorno (exemplo):
```json
{
  "Ano": 2022,
  "Categoria": "Produção",
  "Dados": {
    "Produção de uvas por tipo de utilização": [
      {
        "Descrição": "Uvas para processamento",
        "Quantidade": "1.234.567 kg",
        "Valor": "R$ 2.345.678,00"
      },
      {
        "Descrição": "Uvas para consumo in natura",
        "Quantidade": "987.654 kg",
        "Valor": "R$ 1.234.567,00"
      }
    ]
  }
}
```

---

## 📁 Estrutura de pastas

```
vitibrasil_api/
├── app/
│   ├── core/
|   |     ├── __init__.py
|   |     ├── app.py
│   ├── routes/
|   |     ├── main.py
|   |     ├── routes.py
|   ├── services/
|   |     ├── __init__.py
|   |     ├── databases.py
|   |     ├── scraping.py
|   ├── tests/
|   |     ├── test_api.py
|   ├── utils/
|   |     ├── __init__.py
|   |     ├── auth.py
|   ├── __init__.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
