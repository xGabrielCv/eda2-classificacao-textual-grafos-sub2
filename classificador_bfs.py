import json
import os
from extrator_dados_steam import limpar_e_tokenizar

# ==============================================================================
# 1. ESTRUTURA DE DADOS ADICIONAL (FILA CLÁSSICA) - Exigência do Edital
# ==============================================================================
class Fila:
    """Implementação Clássica de Fila (Queue) baseada em Array (FIFO)."""
    def __init__(self):
        self._itens = []
        
    def enfileirar(self, item):
        self._itens.append(item)
        
    def desenfileirar(self):
        if not self.vazia():
            return self._itens.pop(0)
        return None
        
    def vazia(self):
        return len(self._itens) == 0

# ==============================================================================
# 2. CLASSE DO GRAFO PONDERADO (LISTA DE ADJACÊNCIA COM ARRAYS PARALELOS)
# ==============================================================================
class Grafo:
    """Grafo Relacional Ponderado sem uso de Tabelas Hash ou Dicionários nativos."""
    def __init__(self):
        # Arrays paralelos (Garante fidelidade aos conceitos de baixo nível)
        self.vertices_nome = []  
        self.vertices_tipo = []  # 0: Palavra, 1: Subcategoria, 2: Categoria Principal
        self.adjacencias = []    # Lista de adjacência (Array de Arrays com IDs)
        self.pesos = []          # Array de Arrays paralelo para armazenar os pesos estatísticos

    def adicionar_vertice(self, nome, tipo):
        id_vertice = len(self.vertices_nome)
        self.vertices_nome.append(nome)
        self.vertices_tipo.append(tipo)
        self.adjacencias.append([])
        self.pesos.append([]) 
        return id_vertice

    def adicionar_aresta(self, id_origem, id_destino, peso=1):
        """Cria conexão não-direcionada e inicializa o peso da aresta."""
        if id_destino not in self.adjacencias[id_origem]:
            self.adjacencias[id_origem].append(id_destino)
            self.pesos[id_origem].append(peso)
            
        if id_origem not in self.adjacencias[id_destino]:
            self.adjacencias[id_destino].append(id_origem)
            self.pesos[id_destino].append(peso)

    def atualizar_peso_aresta(self, id_origem, id_destino, novo_peso):
        """Busca linear nas listas de adjacência para atualizar o peso matemático."""
        for i in range(len(self.adjacencias[id_origem])):
            if self.adjacencias[id_origem][i] == id_destino:
                self.pesos[id_origem][i] = novo_peso
                break
                
        for i in range(len(self.adjacencias[id_destino])):
            if self.adjacencias[id_destino][i] == id_origem:
                self.pesos[id_destino][i] = novo_peso
                break

    def buscar_id_por_nome(self, nome):
        """Busca Linear Pura (O(N)) - Substituindo Hashmaps por restrição pedagógica."""
        for i in range(len(self.vertices_nome)):
            if self.vertices_nome[i] == nome:
                return i
        return -1

# ==============================================================================
# 3. CONSTRUÇÃO E POPULAÇÃO DA ESTRUTURA HIERÁRQUICA (VOCABULÁRIO COMPLETO)
# ==============================================================================
def construir_grafo_subnautica():
    grafo = Grafo()
    
    # [NÍVEL 3] Categorias Principais (Tipo = 2)
    id_casual   = grafo.adicionar_vertice("CASUAL / IMERSIVO", 2)
    id_tecnico  = grafo.adicionar_vertice("TÉCNICO / PERFORMANCE", 2)
    id_hardcore = grafo.adicionar_vertice("HARDCORE / SOBREVIVÊNCIA", 2)

    # [NÍVEL 2] Subcategorias (Tipo = 1) e suas conexões estruturais primárias
    id_exploradores = grafo.adicionar_vertice("Exploradores Narrativos", 1)
    id_sociais      = grafo.adicionar_vertice("Jogadores Sociais", 1)
    id_vitimas_medo = grafo.adicionar_vertice("Vítimas do Medo", 1)
    grafo.adicionar_aresta(id_exploradores, id_casual, 1)
    grafo.adicionar_aresta(id_sociais, id_casual, 1)
    grafo.adicionar_aresta(id_vitimas_medo, id_casual, 1)

    id_hardware     = grafo.adicionar_vertice("Hardware / Engine", 1)
    id_estabilidade = grafo.adicionar_vertice("Estabilidade e Bugs", 1)
    id_incompatib   = grafo.adicionar_vertice("Incompatibilidade / Corporativo", 1)
    grafo.adicionar_aresta(id_hardware, id_tecnico, 1)
    grafo.adicionar_aresta(id_estabilidade, id_tecnico, 1)
    grafo.adicionar_aresta(id_incompatib, id_tecnico, 1)

    id_sobrevivencia = grafo.adicionar_vertice("Sobrevivência Pura", 1)
    id_combate       = grafo.adicionar_vertice("Mecânicas de Combate", 1)
    id_progresso     = grafo.adicionar_vertice("Críticos de Progresso", 1)
    grafo.adicionar_aresta(id_sobrevivencia, id_hardcore, 1)
    grafo.adicionar_aresta(id_combate, id_hardcore, 1)
    grafo.adicionar_aresta(id_progresso, id_hardcore, 1)

    # [NÍVEL 1] Dicionários Semânticos de Palavras-Chave Completos (Tipo = 0)
    exploradores = [
        "historia", "historias", "alienigena", "alienigenas", "alien", "aliens", 
        "lore", "enredo", "narrativa", "misterio", "misterios", "exploracao", 
        "explorar", "explorador", "descobrimento", "descobrir", "bioma", "biomas", 
        "fauna", "flora", "ecossistema", "planeta", "oceano", "mar", "fundo", "agua", 
        "aguas", "lindo", "lindos", "linda", "lindas", "maravilha", "maravilhoso", 
        "incrivel", "espetacular", "cinema", "goty", "goat", "visual", "visuais", 
        "arte", "trilha", "sonora", "musica", "musicas", "audio", "audios", "pda", 
        "imersao", "imersivo", "universo", "segredo", "segredos", "beleza", "peixe", 
        "peixes", "scan", "scanner", "escanear", "ambientacao", "sons", "som"
    ]
    
    sociais = [
        "coop", "cooperativo", "multiplayer", "mp", "amigos", "amigo", "amigas", 
        "amiga", "dupla", "trio", "equipe", "grupo", "galera", "social", "party", 
        "juntos", "companhia", "squad", "divertir", "diversao", "divertido", 
        "engracado", "engracados", "rir", "risada", "risadas", "jogarmos", "solo", 
        "sozinho", "singleplayer", "sozinha"
    ]
    
    vitimas_medo = [
        "assustador", "assustadores", "susto", "sustos", "medo", "pavor", "panico", 
        "fobia", "talassofobia", "megalofobia", "caguei", "infarto", "taquicardia", 
        "coracao", "gelou", "tenso", "tensao", "terror", "horror", "sinistro", 
        "bizarro", "perigoso", "leviata", "leviatas", "monstro", "monstros", 
        "bicho", "bichos", "criatura", "criaturas", "reaper", "ghost", "escuro", 
        "escuridao", "noite", "abismo", "void", "vazio", "arrepio", "kraken", 
        "lula", "molusco", "coletor", "collector", "cagaco", "pânico"
    ]
    
    hardware_engine = [
        "ue5", "unreal", "engine", "rtx", "gtx", "amd", "intel", "placa", "video", 
        "gpu", "cpu", "processador", "ram", "memoria", "dlss", "fsr", "fps", 
        "frame", "frames", "40fps", "60fps", "120fps", "1080p", "1440p", "4k", 
        "monitor", "hz", "graficos", "grafico", "textura", "texturas", "iluminacao", 
        "sombras", "ray", "tracing", "pc", "computador", "notebook", "laptop", 
        "specs", "requisitos", "maquina", "loading", "carregamento", "médio", "medio"
    ]
    
    estabilidade = [
        "crash", "crashes", "travando", "trava", "travamento", "travamentos", 
        "queda", "quedas", "lag", "stuttering", "stutter", "congelou", "congelando", 
        "bug", "bugs", "glitch", "glitches", "otimizacao", "otimizado", "mal", 
        "porca", "pesado", "leve", "desempenho", "performance", "liso", "fluido", 
        "rodou", "roda", "rodando", "crashando", "lixo"
    ]
    
    incompatibilidade = [
        "dx12", "driver", "drivers", "abrir", "inicia", "tela", "preta", "branca", 
        "erro", "fatal", "eula", "krafton", "dev", "devs", "desenvolvedor", 
        "desenvolvedores", "atualizacao", "atualizacoes", "update", "patch", "fix", 
        "early", "access", "acesso", "antecipado", "ea", "caro", "preco", 
        "reembolso", "refund", "suporte", "unknown", "worlds", "empresa"
    ]
    
    sobrevivencia_pura = [
        "sobrevivencia", "survival", "hardcore", "recurso", "recursos", "farm", 
        "farmar", "grind", "grindar", "minerio", "minerios", "titanio", "cobre", 
        "prata", "ouro", "chumbo", "quartzo", "crafting", "craft", "craftar", 
        "fabricador", "construir", "construcao", "base", "bases", "habitat", 
        "oxigenio", "o2", "comida", "fome", "sede", "inventario", "espaco", 
        "armazenamento", "veiculo", "veiculos", "submarino", "prawn", "traje", 
        "seamoth", "cyclops", "girino", "tadpole", "bateria", "energia", "fôlego", 
        "potável", "potavel", "calcário", "calcario", "vidro"
    ]
    
    mecanicas_combate = [
        "matar", "matei", "morta", "morto", "morre", "mortes", "morrer", "combate", 
        "arma", "armas", "defender", "defesa", "atacar", "ataque", "agressivo", 
        "agressivos", "pacifista", "desarmado", "imortal", "imortais", "invencivel", 
        "dano", "hp", "vida", "faca", "stasis", "rifle", "torpedo", "repulsor", 
        "bater", "fugir", "predador", "predadores", "violencia", "indefeso", 
        "frustrante", "frustração", "porrada", "afugentar", "repelir"
    ]
    
    criticos_progresso = [
        "progressao", "progredir", "objetivo", "missoes", "missao", "final", 
        "zerar", "zerei", "limite", "mapa", "barreira", "parede", "invisivel", 
        "biomod", "biomods", "adaptacao", "adaptacoes", "upgrade", "upgrades", 
        "modulo", "modulos", "profundidade", "pressao", "balanceamento", "nerf", 
        "buff", "dificil", "dificuldade", "facil", "curto", "conteudo"
    ]

    def inserir(palavras, subcat):
        for p in palavras:
            id_p = grafo.buscar_id_por_nome(p)
            if id_p == -1: 
                id_p = grafo.adicionar_vertice(p, 0)
            grafo.adicionar_aresta(id_p, subcat, 1)

    # Vinculando as palavras às suas subcategorias correspondentes
    inserir(exploradores, id_exploradores); inserir(sociais, id_sociais); inserir(vitimas_medo, id_vitimas_medo)
    inserir(hardware_engine, id_hardware); inserir(estabilidade, id_estabilidade); inserir(incompatibilidade, id_incompatib)
    inserir(sobrevivencia_pura, id_sobrevivencia); inserir(mecanicas_combate, id_combate); inserir(criticos_progresso, id_progresso)

    return grafo

# ==============================================================================
# 4. TREINAMENTO DE PESOS (Critério 3 e Temática E: Frequência Estatística)
# ==============================================================================
def calcular_pesos_por_frequencia(grafo, dataset):
    """
    Varre o dataset e conta a frequência absoluta das palavras mapeadas no grafo.
    Atualiza as arestas do grafo para refletir a relevância estatística dos termos.
    """
    frequencias = [0] * len(grafo.vertices_nome)
    print("Treinando o Grafo: Calculando frequência e peso das arestas a partir do JSON...")
    
    for review in dataset:
        for token in review["tokens_limpos"]:
            id_palavra = grafo.buscar_id_por_nome(token)
            if id_palavra != -1:
                frequencias[id_palavra] += 1
                
    # Atualiza as arestas de Palavras (Tipo 0) -> Subcategorias (Tipo 1)
    for i in range(len(grafo.vertices_nome)):
        if grafo.vertices_tipo[i] == 0: 
            freq_absoluta = frequencias[i]
            # Suavização Laplaciana simples: garante peso mínimo de 1 para conexões existentes
            peso_calculado = freq_absoluta + 1
            
            for vizinho in grafo.adjacencias[i]:
                if grafo.vertices_tipo[vizinho] == 1:
                    grafo.atualizar_peso_aresta(i, vizinho, peso_calculado)

# ==============================================================================
# 5. ALGORITMO DE INFERÊNCIA: BUSCA EM LARGURA (BFS) MULTI-RÓTULO
# ==============================================================================
def classificar_review_bfs_ponderada(grafo, tokens):
    """
    Executa a BFS ponderada e aplica o limiar estatístico de 30% (Abordagem A).
    Possui ajuste fino (Filtro de Ruído) para evitar multi-rótulos falsos em textos curtos.
    """
    pontuacoes = [0, 0, 0] # [0: Casual, 1: Técnico, 2: Hardcore]
    categorias_nomes = ["Casual", "Técnico", "Hardcore"]
    
    for token in tokens:
        id_palavra = grafo.buscar_id_por_nome(token)
        if id_palavra == -1:
            continue
            
        fila = Fila()
        visitados = [False] * len(grafo.vertices_nome)
        
        fila.enfileirar([id_palavra, 1]) 
        visitados[id_palavra] = True
        
        while not fila.vazia():
            item_fila = fila.desenfileirar()
            atual = item_fila[0]
            energia_herdada = item_fila[1]
            
            tipo_atual = grafo.vertices_tipo[atual]
            nome_atual = grafo.vertices_nome[atual]
            
            if tipo_atual == 2:
                if "CASUAL" in nome_atual: pontuacoes[0] += energia_herdada
                elif "TÉCNICO" in nome_atual: pontuacoes[1] += energia_herdada
                elif "HARDCORE" in nome_atual: pontuacoes[2] += energia_herdada
                continue 
                
            for idx_vizinho in range(len(grafo.adjacencias[atual])):
                vizinho = grafo.adjacencias[atual][idx_vizinho]
                peso_aresta = grafo.pesos[atual][idx_vizinho]
                
                if grafo.vertices_tipo[vizinho] > tipo_atual and not visitados[vizinho]:
                    nova_energia = energia_herdada * peso_aresta
                    fila.enfileirar([vizinho, nova_energia])
                    visitados[vizinho] = True
                    
    # --- MATEMÁTICA DA DECISÃO (MULTI-RÓTULO) ---
    total_energia = pontuacoes[0] + pontuacoes[1] + pontuacoes[2]
    rotulos_finais = []
    
    if total_energia == 0:
        return ["Indefinido"]
        
    LIMITE_ENERGIA_MINIMA = 5  # Ajuste Fino: Textos muito curtos/fracos
    LIMIAR_CORTE = 0.30        # 30% do discurso
    
    if total_energia < LIMITE_ENERGIA_MINIMA:
        # Textos curtos demais: Força Mono-rótulo (Leva apenas o vencedor absoluto)
        maior_pontuacao = max(pontuacoes)
        for i in range(3):
            if pontuacoes[i] == maior_pontuacao:
                rotulos_finais.append(categorias_nomes[i])
                break # Quebra para garantir apenas 1 em caso de empate numérico
    else:
        # Textos densos: Permite Multi-rótulo se ultrapassar a fatia de 30%
        for i in range(3):
            fatia_percentual = pontuacoes[i] / total_energia
            if fatia_percentual >= LIMIAR_CORTE:
                rotulos_finais.append(categorias_nomes[i])
                
    return rotulos_finais

meu_grafo = construir_grafo_subnautica()
## ==============================================================================
# 6. NOVAS REVIEWS PARA CLASSIFICAR
# ==============================================================================
def nova_review():
    review = input("Escreva aqui a nova review: ")
    review = limpar_e_tokenizar(review)
    tokens_unicos = []
    for t in review:
        if t not in tokens_unicos: 
            tokens_unicos.append(t)
    rotulos = classificar_review_bfs_ponderada(meu_grafo, tokens_unicos)
    print("Essa review possui tendências de: ")
    if "Casual" in rotulos: print("Casual")
    if "Hardcore" in rotulos: print("Hardcore")
    if "Técnico" in rotulos: print("Técnico")

## ==============================================================================
# 7. MOTOR PRINCIPAL E RELATÓRIO ANALÍTICO DETALHADO (Critério 5)
# ==============================================================================
if __name__ == "__main__":
    nome_ficheiro = "reviews_subnautica2.json"
    
    if not os.path.exists(nome_ficheiro):
        print(f"Erro: O ficheiro {nome_ficheiro} não foi encontrado!")
        exit()
        
    with open(nome_ficheiro, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    calcular_pesos_por_frequencia(meu_grafo, dataset)
    print("\nIniciando Classificação Multi-rótulo (BFS Ponderada com Corte 30%)...\n")
    
    # Contadores Analíticos Puros
    c_apenas_casual = 0
    c_apenas_tecnico = 0
    c_apenas_hardcore = 0
    
    c_casual_tecnico = 0
    c_casual_hardcore = 0
    c_tecnico_hardcore = 0
    c_todas_categorias = 0
    
    c_indefinido = 0
    
    for review in dataset:
        tokens = review["tokens_limpos"]
        
        tokens_unicos = []
        for t in tokens:
            if t not in tokens_unicos: 
                tokens_unicos.append(t)
                
        # O resultado agora é um Array de categorias (ex: ["Casual", "Técnico"])
        rotulos = classificar_review_bfs_ponderada(meu_grafo, tokens_unicos)
        
        # Filtros de Intersecção
        if "Indefinido" in rotulos:
            c_indefinido += 1
        elif len(rotulos) == 3:
            c_todas_categorias += 1
        elif len(rotulos) == 2:
            if "Casual" in rotulos and "Técnico" in rotulos: c_casual_tecnico += 1
            elif "Casual" in rotulos and "Hardcore" in rotulos: c_casual_hardcore += 1
            elif "Técnico" in rotulos and "Hardcore" in rotulos: c_tecnico_hardcore += 1
        elif len(rotulos) == 1:
            if "Casual" in rotulos: c_apenas_casual += 1
            elif "Técnico" in rotulos: c_apenas_tecnico += 1
            elif "Hardcore" in rotulos: c_apenas_hardcore += 1

    total_avaliadas = len(dataset)
    total_sucesso = total_avaliadas - c_indefinido
    
    # Cálculos para o Relatório
    total_puras = c_apenas_casual + c_apenas_tecnico + c_apenas_hardcore
    total_mistas = c_casual_tecnico + c_casual_hardcore + c_tecnico_hardcore + c_todas_categorias

    print("=======================================================================")
    print("        RELATÓRIO ANALÍTICO FINAL - PROCESSAMENTO DE GRAFOS            ")
    print("=======================================================================")
    print(f"Total de Análises Processadas : {total_avaliadas}")
    print(f"Análises com Vocabulário Útil : {total_sucesso} ({(total_sucesso/total_avaliadas)*100:.1f}%)")
    print(f"Indefinidas (Sem correspondência) : {c_indefinido}")
    print("-----------------------------------------------------------------------")
    
    if total_sucesso > 0:
        print(">>> PERFIS PUROS (Apenas 1 Rótulo Dominante) <<<")
        print(f"Representam {(total_puras/total_sucesso)*100:.1f}% dos discursos validados.")
        print(f" -> [ Apenas CASUAL/IMERSIVO ]      : {c_apenas_casual}")
        print(f" -> [ Apenas TÉCNICO/PERFORMANCE ]  : {c_apenas_tecnico}")
        print(f" -> [ Apenas HARDCORE/SOBREVIVÊNCIA]: {c_apenas_hardcore}")
        
        print("\n>>> INTERSECÇÕES SEMÂNTICAS (Multi-rótulos) <<<")
        print(f"Textos complexos que superaram o limiar de 30% em múltiplas áreas ({(total_mistas/total_sucesso)*100:.1f}%).")
        print(f" -> [ Casual + Técnico ]            : {c_casual_tecnico}")
        print("    (Ex: 'Mundo lindo, mas o PC travou com a UE5')")
        
        print(f" -> [ Casual + Hardcore ]           : {c_casual_hardcore}")
        print("    (Ex: 'Pavor dos Leviatãs e escassez de titânio na base')")
        
        print(f" -> [ Técnico + Hardcore ]          : {c_tecnico_hardcore}")
        print("    (Ex: 'Foco no combate quebrado e otimização porca')")
        
        print(f" -> [ Todas as Três Categorias ]    : {c_todas_categorias}")
        print("    (Textos extremamente longos e abrangentes)")
    print("=======================================================================")
    try:
        while (True):
            nova_review()
    except KeyboardInterrupt:
        pass