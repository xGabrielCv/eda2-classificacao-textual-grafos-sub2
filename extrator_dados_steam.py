import urllib.request
import urllib.parse
import json
import re
import time
import os
import unicodedata

def extrair_reviews_com_limite_ptbr(app_id, limite_maximo=2700):
    """
    Varre a API da Steam extraindo as reviews em PT-BR com um limite
    estrito de controle para não sobrecarregar o arquivo.
    """
    reviews_coletadas = []
    cursor = "*"  # Cursor inicial obrigatório
    pagina = 1
    
    print(f"Iniciando a extração de no máximo {limite_maximo} reviews em PT-BR (App ID: {app_id})...")
    print("Aguarde, coletando amostras reais cronológicas da Steam...\n")
    
    while len(reviews_coletadas) < limite_maximo:
        cursor_codificado = urllib.parse.quote(cursor)
        
        url = (f"https://store.steampowered.com/appreviews/{app_id}?"
               f"json=1"
               f"&language=brazilian"
               f"&num_per_page=100"
               f"&filter=all"
               f"&purchase_type=all"
               f"&review_type=all"
               f"&cursor={cursor_codificado}")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                dados = json.loads(response.read().decode('utf-8'))
            
            if "reviews" not in dados or not dados["reviews"]:
                print("\nFim do estoque de análises da API da Steam.")
                break
                
            bloco_reviews = dados["reviews"]
            novos_achados = 0
            
            for rev in bloco_reviews:
                # Garante que não vai passar do limite estrito dentro do loop
                if len(reviews_coletadas) >= limite_maximo:
                    break
                    
                texto_review = rev.get("review", "")
                if texto_review.strip():
                    reviews_coletadas.append(texto_review)
                    novos_achados += 1
            
            print(f"Página {pagina}: Capturadas +{novos_achados} reviews. Total acumulado: {len(reviews_coletadas)}/{limite_maximo}")
            
            # Condição de parada se a paginação repetir o cursor ou vier vazia
            proximo_cursor = dados.get("cursor")
            if proximo_cursor == cursor or not proximo_cursor or novos_achados == 0:
                print("\nVarredura de páginas finalizada.")
                break
                
            cursor = proximo_cursor
            pagina += 1
            
            # Delay de segurança (Anti-Block)
            time.sleep(0.4)
            
        except Exception as e:
            print(f"Erro na conexão com a Steam na requisição {pagina}: {e}")
            break
            
    return reviews_coletadas[:limite_maximo]

def limpar_e_tokenizar(texto_review):
    """
    PLN Completo: Minúsculas, Remoção de Acentos (Normalização),
    Remoção de Pontuação e Remoção de Stopwords sem Tabela Hash.
    """
    # 1. Tudo minúsculo
    texto = texto_review.lower()
    
    # 2. NOVA LINHA: Remove todos os acentos (ex: "leviatã" vira "leviata")
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    
    # 3. Remove pontuação
    texto_limpo = re.sub(r'[^\w\s]', '', texto)
    todas_palavras = texto_limpo.split()
    
    # LISTA DE STOPWORDS (Agora sem acentos para bater perfeitamente)
    stopwords = [
        "o", "a", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da", 
        "dos", "das", "em", "no", "na", "nos", "nas", "para", "com", "por", 
        "que", "se", "mais", "mas", "me", "meu", "minha", "te", "seu", "sua", 
        "ele", "ela", "eles", "elas", "e", "sao", "foi", "era", "vou", "vai", 
        "esta", "ta", "q", "pra", "nao", "eu", "isso", "esse", "essa", "como",
        "nada", "ja", "vc", "tu", "voce", "oque", "oq", "assim", 
        "ia", "ter", "so", "muito", "mt", "mto", "bem", "fazer", "quando", "pq", 
        "porque", "sobre", "tudo", "tbm", "tambem", "daqui", "aqui", 
        "entao", "num", "numa", "pelo", "pela", "tipo", "cara", "gente", "alguem",
        "mim", "comigo", "ti", "contigo", "nosso", "nossa", "vcs", "voces", "queria", "quer",
        "dizer", "diga", "achei", "acho", "ver", "vou", "vai", "ir", "ser", "sendo", "fica",
        "ficou", "ficar", "da", "tem", "tinha", "ter", "pode", "podem", "consigo",
        "faz", "feito", "fizeram"
    ]
    
    tokens_limpos = []
    for palavra in todas_palavras:
        eh_stopword = False
        for stop in stopwords:
            if palavra == stop:
                eh_stopword = True
                break

        if not eh_stopword and len(palavra) > 1 and not palavra.isdigit():
            tokens_limpos.append(palavra)
            
    tokens_unicos = []
    for t in tokens_limpos:
        if t not in tokens_unicos: tokens_unicos.append(t)
    return tokens_unicos

# ==========================================
# MOTOR DE EXECUÇÃO LIMITADO
# ==========================================
if __name__ == "__main__":
    SUBNAUTICA_2_ID = "1962700" 
    NOME_ARQUIVO = "reviews_subnautica2.json"
    LIMITE = 2700
    
    # 1. Puxa as reviews respeitando o teto de 2.7K
    analises_reais = extrair_reviews_com_limite_ptbr(SUBNAUTICA_2_ID, limite_maximo=LIMITE)
    
    print("\n--- Iniciando o Processamento de Dados (Super PLN) ---")
    
    objetos_para_salvar = []
    for i, review in enumerate(analises_reais):
        tokens_limpos = limpar_e_tokenizar(review)
        
        item_review = {
            "id": i + 1,
            "texto_original": review,
            "tokens_limpos": tokens_limpos
        }
        objetos_para_salvar.append(item_review)
        
        # Mostra o status de forma limpa no terminal
        if (i + 1) % 500 == 0 or i == 0:
            print(f"Review {i+1}/{len(analises_reais)} filtrada.")

    print(f"\n--- Salvando {len(objetos_para_salvar)} Registros em {NOME_ARQUIVO} ---")
    
    try:
        with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(objetos_para_salvar, f, ensure_ascii=False, indent=4)
        
        caminho_completo = os.path.abspath(NOME_ARQUIVO)
        print(f"Sucesso absoluto! Base estável de 2.7K salva em:\n-> {caminho_completo}")
        
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")