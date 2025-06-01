import requests
from bs4 import BeautifulSoup

def extrair_dados(session, url):
    dados = []
    pagina_url = url

    while True:
        resp = session.get(pagina_url, timeout=10)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        tabela = soup.find("table", {"class": "tb_base tb_dados"})
        if not tabela:
            return None

        titulo = soup.find("h2")
        titulo_texto = titulo.text.strip() if titulo else None

        for linha in tabela.find_all("tr")[1:]:
            colunas = linha.find_all("td")
            if len(colunas) >= 2:
                item = {
                    "Descrição": colunas[0].text.strip(),
                    "Quantidade": colunas[1].text.strip()
                }
                if len(colunas) >= 3:
                    item["Valor"] = colunas[2].text.strip()
                dados.append(item)

        proximo = soup.find("a", text="»")
        if proximo and 'href' in proximo.attrs:
            pagina_url = "http://vitibrasil.cnpuv.embrapa.br/" + proximo['href']
        else:
            break

    return {"titulo": titulo_texto, "linhas": dados}

def busca_categoria(ano: int, categoria: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    session = requests.Session()
    session.headers.update(headers)

    nomes_opcoes = {
        "Produção": "opt_02",
        "Processamento": "opt_03",
        "Comercialização": "opt_04",
        "Importação": "opt_05",
        "Exportação": "opt_06"
    }

    opcoes_com_sub = {
        "opt_03": 4,
        "opt_05": 5,
        "opt_06": 4
    }

    opcao = nomes_opcoes.get(categoria)
    if not opcao:
        raise ValueError("Categoria inválida")

    resultado = {}

    if opcao in opcoes_com_sub:
        for i in range(1, opcoes_com_sub[opcao] + 1):
            sub = f"subopt_{i:02d}"
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}&subopcao={sub}"
            dados = extrair_dados(session, url)
            if dados:
                titulo = dados.pop("titulo", None)
                chave = titulo if titulo and titulo.lower() != "total" else sub
                resultado[chave] = dados["linhas"]
    else:
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}"
        dados = extrair_dados(session, url)
        if dados:
            titulo = dados.pop("titulo", None)
            chave = titulo if titulo and titulo.lower() != "total" else opcao
            resultado[chave] = dados["linhas"]

    return resultado
