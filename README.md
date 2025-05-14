# API Vitibrasil Embrapa

API desenvolvida como parte do Tech Challenge da FIAP, Fase 1 (Machine Learning Engineering).  
Ela realiza scraping automatizado dos dados de vitivinicultura do site da Embrapa (Vitibrasil) e os entrega de forma estruturada via endpoints REST.

---

## 🔧 Funcionalidades

- Rota de autenticação via token Bearer
- Consulta de dados por categoria e ano
- Web scraping com navegação por subopções
- Retorno de dados em JSON estruturado
- Deploy com link público via ngrok

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
[Site da Embrapa (vitibrasil.cnpuv)]
            |
            v
 [Retorno estruturado (JSON)]
```

---

## ▶️ Como rodar o projeto

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Rode a API:
```bash
python app/main.py
```

3. Acesse a documentação automática:
```
http://localhost:8000/docs
```

Caso esteja usando o Colab com ngrok, o terminal exibirá um link público da API.

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
vitibrasil-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── scraping.py
│   └── auth.py
├── requirements.txt
├── README.md
└── .gitignore
```