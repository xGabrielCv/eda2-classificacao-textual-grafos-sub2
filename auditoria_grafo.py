import json
import os
import re
import unicodedata
import random
from extrator_dados_steam import limpar_e_tokenizar
from estrutura_dados import Fila, Grafo, construir_grafo_subnautica, calcular_pesos_por_frequencia

# ==============================================================================
# 1. MOTOR DE AUDITORIA E APRESENTAÇÃO
# ==============================================================================
def auditar_bfs_ponderada(grafo, tokens, modo_detalhado=False):
   
    # Fator de Amortecimento: idêntico ao motor principal (α = 0.85, estilo PageRank)
    FATOR_AMORTECIMENTO = 0.85
    pontuacoes = [0, 0, 0]
    percentuais = [0.0, 0.0, 0.0]
    categorias_nomes = ["Casual", "Técnico", "Hardcore"]
    tokens_reconhecidos = []

    for token in tokens:
        id_palavra = grafo.buscar_id_por_nome(token)
        if id_palavra == -1: continue

        tokens_reconhecidos.append(token)
        if modo_detalhado:
            print(f"\n[Token Processado]: '{token}' (Energia Inicial = 1)")

        fila = Fila()

        # Vetor Numérico de Níveis: previne loops e inflação artificial de vizinhos.
        # Um nível -1 indica que o nó ainda não foi visitado pela BFS.
        niveis = [-1] * len(grafo.vertices_nome)

        fila.enfileirar([id_palavra, 1, 0])  # [id_vertice, energia, nivel_atual]
        niveis[id_palavra] = 0

        while not fila.vazia():
            item_fila = fila.desenfileirar()
            atual, energia_herdada, nivel_atual = item_fila[0], item_fila[1], item_fila[2]
            tipo_atual, nome_atual = grafo.vertices_tipo[atual], grafo.vertices_nome[atual]

            if tipo_atual == 2:
                if modo_detalhado:
                    print(f"   -> Chegou à Raiz [{nome_atual}] depositando +{energia_herdada:.4f} pontos!")
                if "CASUAL" in nome_atual: pontuacoes[0] += energia_herdada
                elif "TÉCNICO" in nome_atual: pontuacoes[1] += energia_herdada
                elif "HARDCORE" in nome_atual: pontuacoes[2] += energia_herdada
                continue 

            for idx_vizinho in range(len(grafo.adjacencias[atual])):
                vizinho = grafo.adjacencias[atual][idx_vizinho]
                peso_aresta = grafo.pesos[atual][idx_vizinho]

                if grafo.vertices_tipo[vizinho] > tipo_atual and niveis[vizinho] == -1:
                    nova_energia = energia_herdada * peso_aresta * FATOR_AMORTECIMENTO
                    if modo_detalhado:
                        nome_vizinho = grafo.vertices_nome[vizinho]
                        print(f"   -> Propagando de '{nome_atual}' para '{nome_vizinho}' "
                              f"(Peso: {peso_aresta} × α={FATOR_AMORTECIMENTO}) "
                              f"=> Energia Transmitida: {nova_energia:.4f}")
                    fila.enfileirar([vizinho, nova_energia, nivel_atual + 1])
                    niveis[vizinho] = nivel_atual + 1

    total_energia = sum(pontuacoes)
    rotulos_finais = []

    if total_energia > 0:
        percentuais = [(p / total_energia) * 100 for p in pontuacoes]

    if total_energia == 0:
        rotulos_finais = ["Indefinido"]
    elif total_energia < 5:
        maior = max(pontuacoes)
        for i in range(3):
            if pontuacoes[i] == maior:
                rotulos_finais.append(categorias_nomes[i])
                break
    else:
        for i in range(3):
            if percentuais[i] >= 30.0:
                rotulos_finais.append(categorias_nomes[i])

    return tokens_reconhecidos, pontuacoes, percentuais, rotulos_finais

def executar_testes_controlados(grafo):
    print("\n" + "="*50)
    print("        BATERIA DE TESTES CONTROLADOS (UNIT TESTS)   ")
    print("="*50)
    
    casos = [
        ("o oceano é lindo, a história do mundo é maravilhosa e o coop é divertido", ["Casual"]),
        ("que jogo lixo, trava muito, a otimização está um lixo, fps caindo", ["Técnico"]),
        ("não deixam a gente matar os monstros, mecânica de sobrevivência ruim", ["Hardcore"]),
        ("o jogo é muito lindo, mas os bugs estão quebrando o fps na minha ue5", ["Casual", "Técnico"])
    ]
    
    for i, (texto, esperado) in enumerate(casos):
        print(f"\n[Teste {i+1}] Entrada: \"{texto}\"")
        tokens = limpar_e_tokenizar(texto)
        _, _, _, obtido = auditar_bfs_ponderada(grafo, tokens, modo_detalhado=False)
        
        esperado_str = " + ".join(esperado)
        obtido_str = " + ".join(obtido)
        
        status = "✅ PASSOU" if set(esperado) == set(obtido) else "❌ FALHOU"
        
        print(f"Esperado: {esperado_str}")
        print(f"Obtido  : {obtido_str}")
        print(f"Status  : {status}")
    print("\nBateria de testes finalizada.")

def exibir_resultados_formatados(reconhecidos, pts, percs, rotulos):
    print("\n-------------------------------------------")
    print("PONTUAÇÃO BRUTA E PERCENTUAIS:")
    print(f"Casual   = {pts[0]} pts ({percs[0]:.1f}%)")
    print(f"Técnico  = {pts[1]} pts ({percs[1]:.1f}%)")
    print(f"Hardcore = {pts[2]} pts ({percs[2]:.1f}%)")
    print(f"\n-> Tokens Validados no Grafo: {reconhecidos}")
    print(f"-> CLASSIFICAÇÃO FINAL      : {' + '.join(rotulos)}")
    print("-------------------------------------------")

def menu_interativo(grafo, dataset):
    while True:
        print("\n" + "="*50)
        print("    SISTEMA DE AUDITORIA E VALIDAÇÃO DE GRAFOS")
        print("="*50)
        print("1 - Testar uma review manual simples")
        print("2 - Auditoria profunda da BFS (Escolher ID ou Aleatório)")
        print("3 - Sortear 5 reviews do Dataset JSON")
        print("4 - Bateria de Testes Controlados (Unit Tests)")
        print("5 - Analisar uma review 'Indefinida' (Sem Correspondência)")
        print("6 - Sair")
        
        escolha = input("\nEscolha uma opção: ")
        
        if escolha == "1":
            texto = input("\nDigite a sua review: ")
            tokens = limpar_e_tokenizar(texto)
            reconhecidos, pts, percs, rotulos = auditar_bfs_ponderada(grafo, tokens, modo_detalhado=False)
            exibir_resultados_formatados(reconhecidos, pts, percs, rotulos)
            
        elif escolha == "2":
            entrada_id = input("\nDigite o ID da review (ou aperte ENTER para aleatória): ")
            review = None
            if entrada_id.isdigit():
                for r in dataset:
                    if r.get("id") == int(entrada_id):
                        review = r; break
                if not review: print("ID não encontrado."); continue
            else:
                review = random.choice(dataset)
                
            texto = review["texto_original"]
            print(f"\n[TEXTO SELECIONADO - ID {review.get('id', '?')}]:\n\"{texto}\"")
            tokens = limpar_e_tokenizar(texto)
            print(f"\nIniciando Auditoria Passo a Passo para os tokens: {tokens}")
            reconhecidos, pts, percs, rotulos = auditar_bfs_ponderada(grafo, tokens, modo_detalhado=True)
            exibir_resultados_formatados(reconhecidos, pts, percs, rotulos)
            
        elif escolha == "3":
            amostras = random.sample(dataset, 5)
            for i, review in enumerate(amostras):
                texto = review["texto_original"].replace('\n', ' ')
                tokens = limpar_e_tokenizar(texto)
                _, pts, percs, rotulos = auditar_bfs_ponderada(grafo, tokens, False)
                print(f"\n[ID: {review.get('id', '?')}] \"{texto[:100]}...\"")
                print(f"-> Classificação: {' + '.join(rotulos)}")
                
        elif escolha == "4":
            executar_testes_controlados(grafo)
            
        elif escolha == "5":
            indefinidas = []
            for rev in dataset:
                tokens = limpar_e_tokenizar(rev["texto_original"])
                _, _, _, rotulos = auditar_bfs_ponderada(grafo, tokens, False)
                if "Indefinido" in rotulos:
                    indefinidas.append((rev, tokens))
            
            if not indefinidas:
                print("Não existem reviews indefinidas no dataset.")
            else:
                escolhida, tokens = random.choice(indefinidas)
                print(f"\n[REVIEW INDEFINIDA SORTEADA - ID {escolhida.get('id', '?')}]")
                print(f"Texto: \"{escolhida['texto_original']}\"")
                print(f"\nMotivo da falha de classificação:")
                print(f"1. Tokens extraídos após limpeza PLN: {tokens}")
                
                reconhecidos = [t for t in tokens if grafo.buscar_id_por_nome(t) != -1]
                print(f"2. Destes, tokens que existem no Dicionário do Grafo: {reconhecidos}")
                
                if not reconhecidos:
                    print("-> CONCLUSÃO: O texto é composto apenas de Stopwords ou jargões não mapeados no Dicionário do Grafo.")
                else:
                    _, pts, _, _ = auditar_bfs_ponderada(grafo, tokens, False)
                    print(f"-> CONCLUSÃO: Os tokens encontrados geraram pouquíssima energia (Soma = {sum(pts)} pontos). A Review não possui carga semântica suficiente para atingir o limiar.")
                
        elif escolha == "6":
            print("Encerrando o sistema de validação...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    nome_ficheiro = "reviews_subnautica2.json"
    if not os.path.exists(nome_ficheiro):
        print(f"Erro: O ficheiro {nome_ficheiro} não foi encontrado!")
        exit()
        
    meu_grafo = construir_grafo_subnautica()
    with open(nome_ficheiro, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    calcular_pesos_por_frequencia(meu_grafo, dataset)
    print("Grafo calibrado. Iniciando terminal de auditoria...")
    
    menu_interativo(meu_grafo, dataset)