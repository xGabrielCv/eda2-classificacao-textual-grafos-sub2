# Classificador Semântico de Reviews via Grafos Ponderados

Este projeto foi desenvolvido como um trabalho acadêmico unindo **Processamento de Linguagem Natural (PLN)** e **Estruturas de Dados**. O objetivo principal é classificar automaticamente análises (reviews) de jogadores da Steam em três diferentes perfis de comportamento, utilizando modelagem matemática em Grafos.

## 📌 Sobre o Projeto

O sistema analisa textos de reviews do jogo *Subnautica 2* e as categoriza em:
1. **Casual / Imersivo:** Foco na exploração, beleza do jogo, narrativa e modo cooperativo.
2. **Técnico / Performance:** Foco em otimização, gráficos (Unreal Engine 5), bugs e hardware.
3. **Hardcore / Sobrevivência:** Foco nas mecânicas de combate, escassez de recursos e dificuldade.

### ⚙️ Características Técnicas
Respeitando as restrições acadêmicas, o projeto foi construído **do zero** em Python, sem o uso de bibliotecas prontas de grafos (como NetworkX) ou ferramentas de NLP avançadas (como NLTK).

* **Grafo Ponderado:** Implementado através de Listas de Adjacência utilizando arrays puros.
* **Algoritmo de Inferência:** Busca em Largura (BFS) clássica, combinada com *Spreading Activation* (Propagação de Ativação) baseada na frequência dos termos (TF).
* **Fila (Queue):** Estrutura de dados adicional implementada do zero (FIFO) para controle da BFS.
* **Classificação Multi-rótulo:** Capacidade de atribuir mais de uma categoria à review com base em um limiar estatístico de 30% do discurso.

## 📂 Estrutura de Arquivos

* `classificador_bfs.py` -> Motor principal do projeto. Constrói o Grafo, treina os pesos e processa todo o banco de dados gerando o relatório estatístico.
* `auditoria_grafo.py` -> Ferramenta interativa de testes unitários (XAI - Inteligência Artificial Explicável). Permite testar reviews manuais e rastrear passo a passo a matemática da BFS.
* `reviews_subnautica2.json` -> Base de dados limpa e tokenizada contendo mais de 2.700 reviews reais extraídas da API da Steam.

## 🚀 Como Executar

Certifique-se de ter o **Python 3.x** instalado na sua máquina.

1. **Para rodar o classificador principal e ver o relatório final:**
```bash
python classificador_bfs.py