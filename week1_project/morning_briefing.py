import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from scraper import raspar_site

# Carrega as variáveis do .env
load_dotenv()

# Configuração da OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
MODELO = "gpt-4o-mini" # Modelo rápido e barato

# Lista de sites que queremos ler
SITES = [
    "https://ge.globo.com/",
    "https://www.infomoney.com.br/",
    "https://cointelegraph.com/",
    "https://acervo.folha.com.br/index.do?notop=1"
]

def gerar_briefing(conteudo_agregado):
    """
    O "cérebro". É aqui que fazemos a Engenharia de Prompt.
    Envia as notícias para a OpenAI e retorna o streaming da resposta.
    """
    print("\nProcessando com IA gerando o briefing...")
    
    # Instruções estáticas de como a IA deve se comportar
    system_prompt = """
    Você é um assistente matinal inteligente. Seu objetivo é ler um amontoado de textos 
    extraídos de vários sites e criar um 'Morning Briefing' claro, organizado e direto.
    
    Regras:
    1. Resuma as informações mais importantes.
    2. Escreva o resumo inteiramente em Português do Brasil.
    3. Separe estritamente nas seguintes categorias (use emojis para enfeitar):
       - ⚽ Esportes
       - 📈 Mercado Financeiro
       - 🤖 Inteligência Artificial
       - 🪙 Bitcoin e Cripto
    4. Se não houver notícia para alguma categoria, escreva "Sem atualizações relevantes hoje."
    """

    # O texto dinâmico que coletamos da internet limitando o tamanho para não estourar tokens
    user_prompt = f"Aqui está o conteúdo extraído dos sites hoje:\n\n{conteudo_agregado[:15000]}"

    # Chamada para a API com stream=True
    resposta_stream = client.chat.completions.create(
        model=MODELO,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=True # Habilita o envio palavra por palavra
    )
    
    return resposta_stream

def salvar_em_arquivo(texto_final):
    """
    O "arquivo morto". Uma função clássica de Python para persistir dados gerados no disco.
    """
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"briefing_{data_hoje}.txt"
    
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto_final)
        
    print(f"\n\n✅ Briefing salvo com sucesso em: {nome_arquivo}")

def main():
    """
    O "maestro". Ela não faz o trabalho sujo, apenas chama as outras funções na ordem certa.
    """
    print("🌅 Iniciando a geração do seu Morning Briefing...\n")
    
    conteudo_total = ""
    
    # 1. ENTRADA E PROCESSAMENTO (Parte 1 - Scraping)
    for url in SITES:
        texto_extraido = raspar_site(url)
        # Juntamos todos os textos de todos os sites em uma única "tripa" de texto
        conteudo_total += f"\n\n--- Conteúdo do site {url} ---\n\n" + texto_extraido
        
    if not conteudo_total.strip():
        print("Erro: Não foi possível extrair nenhum conteúdo dos sites.")
        return

    # 2. PROCESSAMENTO (Parte 2 - LLM) e 3. SAÍDA
    stream = gerar_briefing(conteudo_total)
    
    print("\n" + "="*50)
    print("🗞️  SEU MORNING BRIEFING DE HOJE")
    print("="*50 + "\n")
    
    briefing_completo = ""
    
    # Imprimimos palavra por palavra no terminal na hora e guardamos na variável
    for pedaco in stream:
        texto_pedaco = pedaco.choices[0].delta.content or ""
        print(texto_pedaco, end="", flush=True)
        briefing_completo += texto_pedaco
        
    # Salva o resultado final em um arquivo .txt
    salvar_em_arquivo(briefing_completo)

# Ponto de entrada do script Python
if __name__ == "__main__":
    main()