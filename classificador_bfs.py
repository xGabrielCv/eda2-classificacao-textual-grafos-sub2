import json
import os
from estrutura_dados import Fila, Grafo, construir_grafo_subnautica, calcular_pesos_por_frequencia
from extrator_dados_steam import limpar_e_tokenizar


# ==============================================================================
# 1. ALGORITMO DE INFERÊNCIA: BUSCA EM LARGURA (BFS) MULTI-RÓTULO
# ==============================================================================

def classificar_review_bfs_ponderada(grafo, tokens):
    """
    Executa a BFS ponderada e aplica o limiar estatístico de 30% (Abordagem A).
    Possui ajuste fino (Filtro de Ruído) para evitar multi-rótulos falsos em textos curtos.
    Implementa Vetor de Níveis e Fator de Amortecimento (α) para controle de loops.
    """
    
    # Fator de Amortecimento inspirado no PageRank: atenua a energia a cada salto
    # hierárquico, garantindo que ativações distantes percam força gradualmente.
    
    FATOR_AMORTECIMENTO = 0.85
    pontuacoes = [0, 0, 0] # [0: Casual, 1: Técnico, 2: Hardcore]
    categorias_nomes = ["Casual", "Técnico", "Hardcore"]

    for token in tokens:
        id_palavra = grafo.buscar_id_por_nome(token)
        if id_palavra == -1:
            continue

        fila = Fila()

        # Vetor Numérico de Níveis (substitui o booleano de visitados).
        # Garante que um nó não receba energia residual de um nível superior ao dele,
        # prevenindo loops em arestas bidirecionais ou erros de modelagem futuros.
        
        niveis = [-1] * len(grafo.vertices_nome)

        fila.enfileirar([id_palavra, 1, 0])  # [id_vertice, energia, nivel_atual]
        niveis[id_palavra] = 0

        while not fila.vazia():
            item_fila = fila.desenfileirar()
            atual = item_fila[0]
            energia_herdada = item_fila[1]
            nivel_atual = item_fila[2]

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

                if grafo.vertices_tipo[vizinho] > tipo_atual and niveis[vizinho] == -1:
                    
                    nova_energia = energia_herdada * peso_aresta * FATOR_AMORTECIMENTO
                    fila.enfileirar([vizinho, nova_energia, nivel_atual + 1])
                    niveis[vizinho] = nivel_atual + 1

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
# 2. NOVAS REVIEWS PARA CLASSIFICAR
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
# 3. MOTOR PRINCIPAL E RELATÓRIO ANALÍTICO DETALHADO (Critério 5)
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