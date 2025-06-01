import requests
from bs4 import BeautifulSoup
from ..services.salvar_csv import salvar_em_csv, CACHE_DIR, carregar_de_csv

def extrair_dados(session, url, subopt_nome=None):
    dados = []
    pagina_url = url
    linha_id = 1

    while True:
        resp = session.get(pagina_url, timeout=10)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        tabela = soup.find("table", {"class": "tb_base tb_dados"})
        if not tabela:
            return None

        # Extrai os nomes das colunas do cabeçalho da tabela
        thead = tabela.find("thead")
        if thead:
            cabecalho = thead.find("tr")
        else:
            cabecalho = tabela.find("tr")

        nomes_colunas = []
        if cabecalho:
            for th in cabecalho.find_all(["th", "td"]):
                nome = th.text.strip()
                nomes_colunas.append(nome)
        else:
            nomes_colunas = ["Coluna" + str(i+1) for i in range(len(tabela.find_all("tr")[1].find_all("td"))) ]

        if subopt_nome and "SubOpt" not in nomes_colunas:
            nomes_colunas.append("SubOpt")

        for linha in tabela.find_all("tr")[1:]:
            colunas = linha.find_all("td")
            if len(colunas) == 0:
                continue
            item = {}
            for idx, coluna in enumerate(colunas):
                if idx < len(nomes_colunas):
                    chave = nomes_colunas[idx]
                else:
                    chave = f"Coluna_{idx+1}"
                item[chave] = coluna.text.strip()
            item["id"] = linha_id
            linha_id += 1

            if subopt_nome:
                item["SubOpt"] = subopt_nome

            dados.append(item)

        proximo = soup.find("a", text="»")
        if proximo and 'href' in proximo.attrs:
            pagina_url = "http://vitibrasil.cnpuv.embrapa.br/" + proximo['href']
        else:
            break

    return dados


def busca_categoria(ano: int, categoria: str):
    
    nome_arquivo = CACHE_DIR / f"{categoria}_{ano}.csv"
    
    dados_cache = carregar_de_csv(nome_arquivo)
    if dados_cache:
        for linha in dados_cache:
            if "id" in linha:
                linha["id"] = int(linha["id"])
        return {
            "Ano": ano,
            "Categoria": categoria,
            "Dados": dados_cache
        }

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

    opcao = nomes_opcoes.get(categoria)
    if not opcao:
        raise ValueError("Categoria inválida")

    dados_unificados = []
    contador_id = 1

    url_base = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}"
    resp = session.get(url_base, timeout=10)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    botoes = soup.find_all("button", class_="btn_sopt")
    subopcoes = [(btn["value"], btn.text.strip()) for btn in botoes]

    if subopcoes:
        for sub_val, sub_nome in subopcoes:
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}&subopcao={sub_val}"
            linhas = extrair_dados(session, url, subopt_nome=sub_nome)
            if linhas:
                for linha in linhas:
                    linha["id"] = contador_id
                    contador_id += 1
                    dados_unificados.append(linha)
    else:
        linhas = extrair_dados(session, url_base, subopt_nome=None)
        if linhas:
            for linha in linhas:
                linha["id"] = contador_id
                contador_id += 1
                if "SubOpt" not in linha:
                    linha["SubOpt"] = categoria
                dados_unificados.append(linha)

    salvar_em_csv(nome_arquivo, dados_unificados)

    return {
        "Ano": ano,
        "Categoria": categoria,
        "Dados": dados_unificados
    }


