# ==============================================================================
# 1. ESTRUTURA DE DADOS ADICIONAL (FILA CLÁSSICA) - Exigência do Edital
# ==============================================================================
class Fila:
    """Implementação Clássica de Fila (Queue) baseada em Array (FIFO)."""
    def __init__(self):
        self._itens = []
        
    def enfileirar(self, item):
        self._itens.append(item) # Entra no final
        
    def desenfileirar(self):
        if not self.vazia():
            return self._itens.pop(0) # Sai do início
        return None
    
    #def desenfileirar(self): return self._itens.pop(0) if not self.vazia() else None
        
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

# ======================================================================================================
# 3. CONSTRUÇÃO E POPULAÇÃO DA ESTRUTURA HIERÁRQUICA (VOCABULÁRIO COMPLETO: DICIONÁRIO FINAL -> GRAFO)
# ======================================================================================================
def construir_grafo_subnautica():
    grafo = Grafo()
    
    # ---------------------------------------------------------
    # NÍVEL 3: CATEGORIAS PRINCIPAIS (TIPO = 2)
    # ---------------------------------------------------------
    id_casual   = grafo.adicionar_vertice("CASUAL / IMERSIVO", 2)
    id_tecnico  = grafo.adicionar_vertice("TÉCNICO / PERFORMANCE", 2)
    id_hardcore = grafo.adicionar_vertice("HARDCORE / SOBREVIVÊNCIA", 2)

    # ---------------------------------------------------------
    # NÍVEL 2: SUBCATEGORIAS (TIPO = 1) e suas Arestas para as Categorias (suas conexões estruturais primárias)
    # ---------------------------------------------------------
    # Filhos de Casual
    id_exploradores = grafo.adicionar_vertice("Exploradores Narrativos", 1)
    id_sociais      = grafo.adicionar_vertice("Jogadores Sociais", 1)
    id_vitimas_medo = grafo.adicionar_vertice("Vítimas do Medo", 1)
    grafo.adicionar_aresta(id_exploradores, id_casual, 1)
    grafo.adicionar_aresta(id_sociais, id_casual, 1)
    grafo.adicionar_aresta(id_vitimas_medo, id_casual, 1)

    # Filhos de Técnico
    id_hardware     = grafo.adicionar_vertice("Hardware / Engine", 1)
    id_estabilidade = grafo.adicionar_vertice("Estabilidade e Bugs", 1)
    id_incompatib   = grafo.adicionar_vertice("Incompatibilidade / Corporativo", 1)
    grafo.adicionar_aresta(id_hardware, id_tecnico, 1)
    grafo.adicionar_aresta(id_estabilidade, id_tecnico, 1)
    grafo.adicionar_aresta(id_incompatib, id_tecnico, 1)

    # Filhos de Hardcore
    id_sobrevivencia = grafo.adicionar_vertice("Sobrevivência Pura", 1)
    id_combate       = grafo.adicionar_vertice("Mecânicas de Combate", 1)
    id_progresso     = grafo.adicionar_vertice("Críticos de Progresso", 1)
    grafo.adicionar_aresta(id_sobrevivencia, id_hardcore, 1)
    grafo.adicionar_aresta(id_combate, id_hardcore, 1)
    grafo.adicionar_aresta(id_progresso, id_hardcore, 1)

    # ------------------------------------
    # NÍVEL 1: Dicionários Semânticos de PALAVRAS-CHAVE Completos (TIPO = 0)
    # ------------------------------------

    # [0] CATEGORIA: CASUAL / IMERSIVO

    # Subcategoria 0.0: Exploradores Narrativos (Foco em beleza, história e mundo)
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

    # Subcategoria 0.1: Jogadores Sociais (Foco em multiplayer)
    sociais = [
        "coop", "cooperativo", "multiplayer", "mp", "amigos", "amigo", "amigas", 
        "amiga", "dupla", "trio", "equipe", "grupo", "galera", "social", "party", 
        "juntos", "companhia", "squad", "divertir", "diversao", "divertido", 
        "engracado", "engracados", "rir", "risada", "risadas", "jogarmos", "solo", 
        "sozinho", "singleplayer", "sozinha"
    ]

    # Subcategoria 0.2: Vítimas do Medo (Foco em fobias, sustos e terror)
    vitimas_medo = [
        "assustador", "assustadores", "susto", "sustos", "medo", "pavor", "panico", 
        "fobia", "talassofobia", "megalofobia", "caguei", "infarto", "taquicardia", 
        "coracao", "gelou", "tenso", "tensao", "terror", "horror", "sinistro", 
        "bizarro", "perigoso", "leviata", "leviatas", "monstro", "monstros", 
        "bicho", "bichos", "criatura", "criaturas", "reaper", "ghost", "escuro", 
        "escuridao", "noite", "abismo", "void", "vazio", "arrepio", "kraken", 
        "lula", "molusco", "coletor", "collector", "cagaco", "pânico"
    ]

    # [1] CATEGORIA: TÉCNICO / PERFORMANCE

    # Subcategoria 1.0: Hardware / Engine (Foco em peças e gráficos técnicos)
    hardware_engine = [
        "ue5", "unreal", "engine", "rtx", "gtx", "amd", "intel", "placa", "video", 
        "gpu", "cpu", "processador", "ram", "memoria", "dlss", "fsr", "fps", 
        "frame", "frames", "40fps", "60fps", "120fps", "1080p", "1440p", "4k", 
        "monitor", "hz", "graficos", "grafico", "textura", "texturas", "iluminacao", 
        "sombras", "ray", "tracing", "pc", "computador", "notebook", "laptop", 
        "specs", "requisitos", "maquina", "loading", "carregamento", "médio", "medio"
    ]

    # Subcategoria 1.1: Estabilidade (Foco em como o jogo roda)
    estabilidade = [
        "crash", "crashes", "travando", "trava", "travamento", "travamentos", 
        "queda", "quedas", "lag", "stuttering", "stutter", "congelou", "congelando", 
        "bug", "bugs", "glitch", "glitches", "otimizacao", "otimizado", "mal", 
        "porca", "pesado", "leve", "desempenho", "performance", "liso", "fluido", 
        "rodou", "roda", "rodando", "crashando", "lixo"
    ]

    # Subcategoria 1.2: Incompatibilidade / Corporativo (Problemas externos e devs)
    incompatibilidade = [
        "dx12", "driver", "drivers", "abrir", "inicia", "tela", "preta", "branca", 
        "erro", "fatal", "eula", "krafton", "dev", "devs", "desenvolvedor", 
        "desenvolvedores", "atualizacao", "atualizacoes", "update", "patch", "fix", 
        "early", "access", "acesso", "antecipado", "ea", "caro", "preco", 
        "reembolso", "refund", "suporte", "unknown", "worlds", "empresa"
    ]

    # [2] CATEGORIA: SOBREVIVÊNCIA / HARDCORE

    # Subcategoria 2.0: Sobrevivência Pura (Foco em grind, materiais e bases)
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

    # Subcategoria 2.1: Mecânicas de Combate (Foco na polêmica da violência/defesa)
    mecanicas_combate = [
        "matar", "matei", "morta", "morto", "morre", "mortes", "morrer", "combate", 
        "arma", "armas", "defender", "defesa", "atacar", "ataque", "agressivo", 
        "agressivos", "pacifista", "desarmado", "imortal", "imortais", "invencivel", 
        "dano", "hp", "vida", "faca", "stasis", "rifle", "torpedo", "repulsor", 
        "bater", "fugir", "predador", "predadores", "violencia", "indefeso", 
        "frustrante", "frustração", "porrada", "afugentar", "repelir"
    ]

    # Subcategoria 2.2: Críticos de Progresso (Foco em zerar, limites e upgrades)
    criticos_progresso = [
        "progressao", "progredir", "objetivo", "missoes", "missao", "final", 
        "zerar", "zerei", "limite", "mapa", "barreira", "parede", "invisivel", 
        "biomod", "biomods", "adaptacao", "adaptacoes", "upgrade", "upgrades", 
        "modulo", "modulos", "profundidade", "pressao", "balanceamento", "nerf", 
        "buff", "dificil", "dificuldade", "facil", "curto", "conteudo"
    ]

    # Função Auxiliar modificada e blindada contra duplicatas
    def inserir_palavras_no_grafo(lista_palavras, id_subcategoria):
        for palavra in lista_palavras:
            # 1. Checa se a palavra já existe no grafo
            id_palavra = grafo.buscar_id_por_nome(palavra)
            
            # 2. Se não existir (retornou -1), criamos o vértice
            if id_palavra == -1:
                id_palavra = grafo.adicionar_vertice(palavra, 0)
                
            # 3. Criamos a aresta Bidirecional (a função adicionar_aresta já lida com duplicatas)
            grafo.adicionar_aresta(id_palavra, id_subcategoria)

    # Construindo as arestas finais do vocabulário
    inserir_palavras_no_grafo(exploradores, id_exploradores)
    inserir_palavras_no_grafo(sociais, id_sociais)
    inserir_palavras_no_grafo(vitimas_medo, id_vitimas_medo)
    
    inserir_palavras_no_grafo(hardware_engine, id_hardware)
    inserir_palavras_no_grafo(estabilidade, id_estabilidade)
    inserir_palavras_no_grafo(incompatibilidade, id_incompatib)
    
    inserir_palavras_no_grafo(sobrevivencia_pura, id_sobrevivencia)
    inserir_palavras_no_grafo(mecanicas_combate, id_combate)
    inserir_palavras_no_grafo(criticos_progresso, id_progresso)

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
# TESTE RÁPIDO PARA VALIDAR A ESTRUTURA E A BIDIRECIONALIDADE
# ==============================================================================
if __name__ == "__main__":
    meu_grafo = construir_grafo_subnautica()
    
    # 1. Teste Top-Down (O que a subcategoria 'Mecânicas de Combate' acessa?)
    id_combate = meu_grafo.buscar_id_por_nome("Mecânicas de Combate")
    vizinhos_combate = meu_grafo.adjacencias[id_combate]
    
    print("--- Teste de Grafo Bidirecional ---")
    print(f"Subcategoria 'Mecânicas de Combate' está conectada a {len(vizinhos_combate)} vértices.")
    
    # 2. Teste Bottom-Up (Pra onde a palavra 'matar' aponta?)
    id_matar = meu_grafo.buscar_id_por_nome("matar")
    vizinhos_matar = meu_grafo.adjacencias[id_matar]
    nomes_vizinhos = [meu_grafo.vertices_nome[vid] for vid in vizinhos_matar]
    
    print(f"A palavra 'matar' aponta para os nós: {nomes_vizinhos}")