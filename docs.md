# Classificador Semântico de Reviews via Grafos Ponderados

## 📖 Visão Geral

Este projeto implementa um sistema de **classificação textual baseado em grafos ponderados**, desenvolvido como trabalho acadêmico da disciplina de Estruturas de Dados II.

O objetivo é analisar automaticamente avaliações (*reviews*) do jogo **Subnautica 2** e classificá-las em diferentes perfis de jogadores utilizando conceitos de:

* Estruturas de Dados
* Teoria dos Grafos
* Busca em Largura (BFS)
* Processamento de Linguagem Natural (PLN)
* Propagação de Ativação (*Spreading Activation*)

Uma das principais características do projeto é que toda a implementação foi construída **sem bibliotecas especializadas de grafos ou PLN**, atendendo às restrições propostas pela disciplina.

---

# Objetivos

O sistema realiza a classificação automática de reviews em três categorias principais:

* 🎮 **Casual / Imersivo**

  * exploração
  * narrativa
  * ambientação
  * cooperação

* ⚙️ **Técnico / Performance**

  * otimização
  * desempenho
  * Unreal Engine 5
  * bugs
  * hardware

* ☠️ **Hardcore / Sobrevivência**

  * combate
  * dificuldade
  * gerenciamento de recursos
  * sobrevivência

Uma mesma review pode pertencer a mais de uma categoria quando ultrapassa o limiar estatístico definido pelo algoritmo.

---

# Arquitetura do Projeto

```
Reviews JSON
      │
      ▼
Limpeza e Tokenização
      │
      ▼
Construção do Grafo
      │
      ▼
Treinamento dos Pesos
      │
      ▼
Busca em Largura (BFS)
      │
      ▼
Spreading Activation
      │
      ▼
Classificação Final
```

---

# Estrutura do Repositório

```
.
├── auditoria_grafo.py
├── classificador_bfs.py
├── estrutura_dados.py
├── extrator_dados_steam.py
├── reviews_subnautica2.json
├── docs.md
└── README.md
```

## Descrição dos arquivos

### classificador_bfs.py

Arquivo principal do projeto.

Responsável por:

* implementação da fila (FIFO);
* implementação do grafo ponderado;
* treinamento dos pesos;
* execução da BFS;
* propagação de ativação;
* classificação das reviews;
* geração do relatório estatístico.

---

### auditoria_grafo.py

Ferramenta de auditoria do modelo.

Permite:

* inserir reviews manualmente;
* acompanhar a execução da BFS;
* verificar os pesos percorridos;
* entender como a classificação foi obtida.

É um recurso voltado para explicabilidade (XAI).

---

### estrutura_dados.py

Contém estruturas auxiliares utilizadas durante a implementação.

---

### extrator_dados_steam.py

Responsável pelo pré-processamento textual.

As principais etapas incluem:

* limpeza do texto;
* normalização;
* tokenização;
* preparação dos dados para o grafo.

---

### reviews_subnautica2.json

Base de dados contendo aproximadamente **2.700 reviews** do jogo Subnautica 2, utilizadas durante os testes do algoritmo.

---

# Estrutura de Dados Utilizadas

O projeto implementa manualmente:

## Grafo Ponderado

Representação através de:

* Lista de adjacência
* Arrays paralelos

Cada vértice possui:

* nome
* tipo
* lista de vizinhos
* pesos das conexões

Os tipos de vértice são:

```
0 → Palavra

1 → Subcategoria

2 → Categoria Principal
```

---

## Fila (Queue)

Implementação clássica FIFO utilizando listas.

Operações disponíveis:

* enfileirar()
* desenfileirar()
* vazia()

A fila é utilizada durante a execução da Busca em Largura (BFS).

---

# Funcionamento do Algoritmo

O processamento ocorre nas seguintes etapas:

1. A review é lida.
2. O texto é limpo.
3. O texto é tokenizado.
4. Cada palavra procura seu vértice correspondente no grafo.
5. A BFS percorre os relacionamentos.
6. Os pesos das arestas propagam ativação para categorias relacionadas.
7. As ativações são acumuladas.
8. É calculado o percentual de cada categoria.
9. São atribuídas uma ou mais classes para a review.

---

# Busca em Largura (BFS)

A BFS é utilizada como mecanismo de propagação dentro do grafo.

Características:

* percorre vértices por níveis;
* evita ciclos;
* utiliza fila FIFO;
* propaga influência entre palavras e categorias.

Complexidade:

```
Tempo:
O(V + E)

Espaço:
O(V)
```

---

# Spreading Activation

Após localizar os termos presentes na review, o algoritmo realiza uma propagação de ativação.

Cada palavra:

* ativa seu vértice;
* transmite influência aos vizinhos;
* acumula pesos nas categorias alcançadas.

Ao final, as categorias recebem uma pontuação proporcional à relevância dos termos encontrados.

---

# Classificação

O sistema suporta classificação múltipla.

Caso duas ou mais categorias ultrapassem o limiar definido, todas poderão ser atribuídas à mesma review.

Exemplo:

```
Review

"O jogo está lindo, mas apresenta muitos bugs."

Resultado

✔ Casual / Imersivo
✔ Técnico / Performance
```

---

# Tecnologias Utilizadas

* Python 3
* JSON
* Estruturas de Dados
* Grafos
* Busca em Largura (BFS)

Sem utilização de:

* NetworkX
* NLTK
* spaCy
* Scikit-Learn

---

# Como Executar

## Requisitos

Python 3.x

---

## Executar o classificador

```bash
python classificador_bfs.py
```

---

## Executar a auditoria

```bash
python auditoria_grafo.py
```

---

# Resultados Esperados

Ao executar o classificador, o sistema:

* carrega as reviews;
* processa o texto;
* constrói o grafo;
* executa a BFS;
* calcula as ativações;
* classifica as reviews;
* apresenta estatísticas finais.

---

# Diferenciais do Projeto

* implementação completa do grafo sem bibliotecas externas;
* BFS construída manualmente;
* fila implementada do zero;
* classificação textual baseada em propagação de ativação;
* foco didático em Estruturas de Dados.

---

# Possíveis Melhorias

* remoção automática de stopwords;
* lematização;
* stemming;
* interface gráfica;
* visualização do grafo;
* otimização das buscas utilizando tabelas hash;
* avaliação quantitativa com métricas de precisão, recall e F1-score.

---

# Autores

André João, Eric Akio, Jesus Gabriel, Ricardo Lucas, Vinicius dos Santos. 

---

# Licença

Projeto desenvolvido para fins acadêmicos.
