# vai na internet pegar o texto bruto

import requests
from bs4 import BeautifulSoup

def raspar_site(url):
    """
    Acessa a URL q é variavel, e extrai o texto principal
    Entrada: URL
    Saída: Texto extraído
    """

    #Usamos um user-agente p imitar um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # requisição na página
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status() # p verificar se deu erro

        #beatifulsoup p filtrar código html
        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # Pega todos os paragráfos do site
        paragrafos = sopa.find_all('p')

        #junta os paragrafos separando por espaço
        texto_site = " ".join([p.get_text(strip=True) for p in paragrafos])

        print(f"[{url}] Extração concluída!! ({len(texto_site)} caracteres)")
        return texto_site
    
    #colocar um depurador p ver se deu erro
    except Exception as e:
        print(f"[{url}] Erro ao acessar: {e}")
        return ""
