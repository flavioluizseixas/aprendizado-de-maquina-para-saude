# PRD — Hands-on de Aprendizado de Máquina para Saúde em Python e Google Colab

**Projeto:** coleção de exercícios práticos para a disciplina *Aprendizado de Máquina para Saúde*  
**Versão:** 1.0  
**Idioma:** português do Brasil  
**Ambiente principal:** Google Colab  
**Hospedagem:** GitHub  
**Público-alvo:** estudantes de graduação e pós-graduação com conhecimento inicial de Python  
**Objetivo para o Codex:** implementar integralmente o repositório descrito neste documento, incluindo notebooks executáveis, funções auxiliares, documentação, testes básicos e botões de abertura no Google Colab.

---

## 1. Visão do produto

Construir um repositório didático com oito notebooks independentes e progressivos sobre aprendizado de máquina aplicado à saúde. Cada notebook deverá:

1. executar diretamente no Google Colab;
2. baixar automaticamente uma base pública a partir da fonte;
3. realizar apenas o tratamento necessário;
4. apresentar pouco código visível por célula;
5. explicar o fluxo em linguagem acessível;
6. produzir resultados e visualizações interpretáveis;
7. incluir perguntas para reflexão;
8. explicitar limitações metodológicas;
9. ser reproduzível, sem upload manual;
10. deixar claro que o exercício é educacional e não clínico.

O estudante deverá conseguir abrir o notebook no GitHub, clicar em **Open in Colab**, executar as células em sequência e compreender o experimento completo.

---

## 2. Problema a resolver

Materiais práticos de aprendizado de máquina frequentemente apresentam excesso de código, pouca documentação, dependência de arquivos locais, incompatibilidades com o Colab, avaliação incompleta, vazamento de dados e interpretações excessivamente otimistas.

O produto deverá reduzir esses problemas por meio de:

- estrutura comum entre os notebooks;
- funções auxiliares reutilizáveis;
- fontes públicas documentadas;
- validação adequada;
- interpretação responsável;
- execução automatizada no Colab.

---

## 3. Objetivos

### 3.1 Objetivo principal

Disponibilizar uma coleção de exercícios simples e bem documentados que permita ao estudante experimentar diferentes paradigmas de aprendizado de máquina em saúde com o mínimo de código necessário.

### 3.2 Objetivos específicos

- introduzir análise exploratória e estatística descritiva;
- ensinar um fluxo completo de classificação supervisionada;
- demonstrar correlação, validação cruzada, métricas e matriz de confusão;
- apresentar explicabilidade com importância de variáveis e SHAP;
- explorar K-means, elbow e PCA;
- comparar modelos e buscar hiperparâmetros;
- classificar imagens médicas e produzir Grad-CAM;
- introduzir Kaplan–Meier, log-rank e modelo de Cox;
- comparar sobrevivência com e sem estratificação;
- introduzir aprendizado por reforço em um problema operacional simulado;
- construir um experimento de séries temporais epidemiológicas;
- reforçar reprodutibilidade, avaliação e interpretação responsável.

---

## 4. Fora do escopo

Não fazem parte da primeira versão:

- diagnóstico, prescrição ou recomendação terapêutica;
- sistemas clínicos ou integração com prontuário;
- dados identificáveis;
- bases que exijam credenciamento individual;
- implantação em produção;
- treinamento distribuído;
- modelos fundacionais de grande porte;
- redes profundas de alta complexidade;
- inferência causal;
- comparação exaustiva de algoritmos.

---

## 5. Princípios pedagógicos

### 5.1 Aprendizado incremental

Os quatro primeiros notebooks deverão reutilizar a mesma base tabular:

1. conhecer os dados;
2. construir e avaliar um modelo;
3. investigar agrupamentos;
4. comparar e otimizar modelos.

Os demais notebooks introduzirão imagens, sobrevivência, reforço e séries temporais.

### 5.2 Código visível mínimo

- Preferir células com até 10–15 linhas.
- Evitar células monolíticas.
- Colocar rotinas repetitivas em `src/`.
- Usar docstrings, tipagem e nomes claros.
- Explicar o que cada função auxiliar faz.
- Não esconder decisões metodológicas importantes.

### 5.3 Primeiro a pergunta, depois o código

Cada seção deverá começar com uma pergunta ou objetivo. Exemplo:

> Qual é a distribuição do índice de massa corporal nesta amostra?

Depois deverá aparecer o código que responde à pergunta.

### 5.4 Interpretação guiada

Após resultados importantes, incluir:

```markdown
### Como interpretar

- O que o resultado representa.
- O que pode ser concluído.
- O que não pode ser concluído.
```

### 5.5 Segurança e responsabilidade

Todos os notebooks devem conter:

> Este material tem finalidade exclusivamente educacional. Os resultados não devem ser usados para diagnóstico, prognóstico, tratamento, gestão assistencial ou decisão de saúde pública sem validação adequada, análise de contexto e supervisão de profissionais qualificados.

### 5.6 Reprodutibilidade

- `RANDOM_STATE = 42` quando aplicável.
- Registrar versões no final.
- Usar divisão de treino e teste reproduzível.
- Não ajustar hiperparâmetros no teste.
- Usar `Pipeline` e `ColumnTransformer` quando apropriado.
- Preservar ordem temporal.
- Usar divisões oficiais do conjunto de imagens.

---

## 6. Fontes de dados

### 6.1 Base tabular principal — CDC Diabetes Health Indicators

**Uso:** notebooks 01, 02, 03 e 04.  
**Fonte:** UCI Machine Learning Repository, dataset 891.  
**Origem:** indicadores derivados do Behavioral Risk Factor Surveillance System do CDC.  
**Tarefa:** classificação binária relacionada à indicação de pré-diabetes ou diabetes.

Página:

```text
https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
```

Download:

```python
from ucimlrepo import fetch_ucirepo

dataset = fetch_ucirepo(id=891)
X = dataset.data.features
y = dataset.data.targets
```

Requisitos:

- imprimir metadados;
- explicar origem e limitações de autorrelato;
- identificar variáveis binárias, ordinais e numéricas;
- não tratar o alvo como diagnóstico produzido pelo notebook;
- permitir `SAMPLE_SIZE`;
- preservar opção de execução com a base completa;
- usar amostragem estratificada e reproduzível quando necessário.

### 6.2 Imagens — PneumoniaMNIST / MedMNIST+

**Uso:** notebook 05.  
**Fonte oficial:** MedMNIST.  
**Modalidade:** radiografia de tórax pediátrica pré-processada.  
**Tarefa:** classificação binária.  
**Tamanho sugerido:** 64 × 64.

Páginas:

```text
https://medmnist.com/
https://github.com/MedMNIST/MedMNIST
```

Download:

```python
from medmnist import PneumoniaMNIST

train_data = PneumoniaMNIST(split="train", download=True, size=64)
val_data = PneumoniaMNIST(split="val", download=True, size=64)
test_data = PneumoniaMNIST(split="test", download=True, size=64)
```

Requisitos:

- usar divisões oficiais;
- mostrar distribuição de classes;
- informar que as imagens são reduzidas e pré-processadas;
- destacar que o MedMNIST não se destina ao uso clínico;
- citar o artigo e a fonte original do subconjunto.

### 6.3 Sobrevivência — NCCTG Lung Cancer

**Uso:** notebook 06.  
**Fonte original:** pacote `survival` do R.  
**Acesso em CSV:** projeto Rdatasets.

CSV:

```text
https://vincentarelbundock.github.io/Rdatasets/csv/survival/lung.csv
```

Documentação:

```text
https://vincentarelbundock.github.io/Rdatasets/doc/survival/lung.html
https://stat.ethz.ch/R-manual/R-devel/library/survival/help/lung.html
```

Download:

```python
import pandas as pd

df = pd.read_csv(
    "https://vincentarelbundock.github.io/Rdatasets/csv/survival/lung.csv"
)
```

Requisitos:

- remover apenas a coluna de índice do repositório, quando existir;
- recodificar corretamente o evento;
- documentar censura;
- explicar as variáveis;
- registrar o tratamento de valores ausentes.

### 6.4 Séries epidemiológicas — InfoDengue

**Uso:** notebooks 07 e 08.  
**Fonte:** API pública do InfoDengue.  
**Granularidade:** semana epidemiológica.  
**Doença padrão:** dengue.  
**Município padrão:** Niterói, código IBGE `3303302`.  
**Período padrão:** 2016–2025, evitando o ano corrente incompleto.

Documentação:

```text
https://info.dengue.mat.br/tutorial_api_python/locale-en
```

Endpoint:

```text
https://info.dengue.mat.br/api/alertcity
```

Parâmetros:

```python
params = {
    "geocode": 3303302,
    "disease": "dengue",
    "format": "csv",
    "ew_start": 1,
    "ew_end": 53,
    "ey_start": 2016,
    "ey_end": 2025,
}
```

Requisitos:

- usar `requests` com `timeout`;
- validar resposta HTTP e colunas;
- salvar cache na sessão;
- converter `data_iniSE` para data;
- ordenar cronologicamente;
- lidar explicitamente com semanas ausentes;
- não preencher ausências com zero sem justificativa;
- exibir data de download;
- informar que valores podem sofrer revisão;
- permitir alteração do município, período e doença;
- permitir fallback explícito para Rio de Janeiro quando Niterói não retornar dados;
- nunca substituir falha da API por dados sintéticos silenciosamente.

---

## 7. Decisões técnicas

### 7.1 Bibliotecas

- pandas;
- NumPy;
- matplotlib;
- seaborn;
- scikit-learn;
- SHAP;
- lifelines;
- medmnist;
- TensorFlow/Keras;
- requests;
- statsmodels, quando necessário;
- kneed, opcional.

### 7.2 Comparação low-code

O notebook 04 deverá usar funções próprias sobre scikit-learn, armazenadas em `src/model_selection.py`.

Interface desejada:

```python
leaderboard = compare_classifiers(
    X_train,
    y_train,
    cv=5,
    scoring=["roc_auc", "f1", "recall", "precision"],
)

best_model, tuning_results = tune_classifier(
    model_name=leaderboard.iloc[0]["model"],
    X=X_train,
    y=y_train,
    cv=5,
    n_iter=20,
)
```

Motivos:

- compatibilidade;
- transparência;
- poucas chamadas no notebook;
- menor dependência de APIs low-code em transição.

PyCaret poderá aparecer apenas como extensão opcional, não como dependência central.

### 7.3 Imagens

Preferir TensorFlow/Keras. A leitura poderá usar:

```python
X_train = train_data.imgs[..., None]
y_train = train_data.labels.ravel()
```

Modelo pequeno:

- normalização;
- dois ou três blocos convolucionais;
- `GlobalAveragePooling2D`;
- saída binária.

O Grad-CAM deverá ficar em `src/gradcam.py`.

### 7.4 Gráficos

- títulos em português;
- eixos identificados;
- legendas legíveis;
- evitar gráficos 3D;
- indicar número de observações;
- usar percentuais para categorias quando adequado;
- evitar excesso de casas decimais;
- mostrar baseline quando aplicável.

---

## 8. Estrutura do repositório

```text
aprendizado-maquina-saude-hands-on/
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements-colab.txt
├── pyproject.toml
├── .gitignore
├── .github/
│   └── workflows/
│       └── validate-notebooks.yml
├── notebooks/
│   ├── 01_estatistica_descritiva.ipynb
│   ├── 02_aprendizado_supervisionado.ipynb
│   ├── 03_aprendizado_nao_supervisionado.ipynb
│   ├── 04_comparacao_modelos_hiperparametros.ipynb
│   ├── 05_imagens_gradcam.ipynb
│   ├── 06_analise_sobrevivencia.ipynb
│   ├── 07_aprendizado_reforco.ipynb
│   └── 08_series_temporais.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loading.py
│   ├── visualization.py
│   ├── evaluation.py
│   ├── model_selection.py
│   ├── clustering.py
│   ├── gradcam.py
│   ├── survival_utils.py
│   ├── dengue_api.py
│   ├── reinforcement_env.py
│   └── time_series.py
├── tests/
│   ├── test_data_loading.py
│   ├── test_evaluation.py
│   ├── test_model_selection.py
│   ├── test_reinforcement_env.py
│   └── test_time_series.py
├── assets/
│   └── figures/
└── data/
    ├── README.md
    └── cache/
        └── .gitkeep
```

Não versionar as bases completas.

---

## 9. Padrão obrigatório dos notebooks

Cada notebook deverá conter:

1. título e número;
2. duração estimada;
3. objetivos;
4. pré-requisitos;
5. fonte e licença;
6. aviso de uso educacional;
7. botão **Open in Colab**;
8. preparação do ambiente;
9. pergunta orientadora;
10. obtenção dos dados;
11. inspeção;
12. preparação;
13. experimento;
14. avaliação;
15. interpretação;
16. limitações;
17. atividade;
18. três aprendizados principais;
19. referências;
20. versões das bibliotecas.

A célula inicial deverá detectar Colab, clonar ou atualizar o repositório, instalar apenas dependências ausentes e definir a semente.

Centralizar o repositório em:

```python
REPO = "SEU_USUARIO/aprendizado-maquina-saude-hands-on"
```

---

## 10. Botões do Google Colab

Modelo:

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](
https://colab.research.google.com/github/SEU_USUARIO/SEU_REPOSITORIO/blob/main/notebooks/01_estatistica_descritiva.ipynb
)
```

Requisitos:

- usar branch `main`;
- testar todos os links;
- colocar um botão no README e no início de cada notebook;
- documentar como trocar usuário e repositório.

---

# 11. Especificação dos experimentos

## 11.1 Notebook 01 — Estatística descritiva

### Título

**Conhecendo indicadores de saúde: estatística descritiva e visualização**

### Objetivos

- baixar uma base pública;
- inspecionar dimensões, tipos e qualidade;
- diferenciar variáveis numéricas, binárias e ordinais;
- calcular estatísticas descritivas;
- escolher gráficos adequados;
- produzir `pairplot`;
- discutir dados observacionais e autorrelatados.

### Fluxo mínimo

1. baixar com `ucimlrepo`;
2. unir atributos e alvo;
3. mostrar dimensões, primeiras linhas, tipos, ausências e duplicatas;
4. mostrar distribuição do alvo;
5. selecionar, por exemplo:
   - `BMI`;
   - `Age`;
   - `GenHlth`;
   - `PhysHlth`;
   - `MentHlth`;
   - `HighBP`;
   - `Diabetes_binary`;
6. apresentar tabela descritiva;
7. produzir:
   - histograma e boxplot para `BMI`;
   - barras proporcionais para `HighBP`;
   - gráfico ordinal para `GenHlth`;
   - prevalência do alvo;
8. gerar `pairplot` em amostra estratificada de 800–1.500 registros;
9. criar função que escolha gráfico conforme o tipo.

### Regras

- não executar `pairplot` na base inteira;
- explicar a amostragem;
- não chamar associação de causalidade;
- mostrar mediana e intervalo interquartil em distribuições assimétricas.

### Atividade

Escolher outro atributo, criar o gráfico apropriado e escrever:

1. o que o gráfico sugere;
2. o que não pode ser concluído.

### Aceitação

- CPU;
- até 4 minutos;
- quatro gráficos univariados;
- um `pairplot`;
- uma tabela descritiva;
- ao menos uma limitação.

---

## 11.2 Notebook 02 — Supervisionado, avaliação e explicabilidade

### Título

**Predição, desempenho e explicabilidade em classificação**

### Objetivos

- avaliar correlação numérica e visual;
- construir pipeline;
- separar treino e teste;
- usar cinco folds;
- avaliar matriz de confusão;
- calcular sensibilidade, especificidade, precisão e F1;
- analisar ROC-AUC e PR-AUC;
- aplicar SHAP;
- diferenciar explicação do modelo e causalidade.

### Preparação

- amostra estratificada configurável, padrão de 20–40 mil registros;
- teste separado antes de ajuste;
- `Pipeline`;
- `RANDOM_STATE = 42`.

### Correlação

Apresentar:

- matriz de Spearman;
- tabela com maiores correlações absolutas;
- heatmap;
- correlação com o alvo;
- ressalvas sobre codificação, não linearidade e causalidade.

### Modelo convencional

Regressão logística com:

```text
class_weight="balanced"
```

### Validação cruzada

```python
StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)
```

Métricas:

- ROC-AUC;
- F1;
- recall/sensibilidade;
- precisão;
- balanced accuracy;
- média e desvio-padrão.

### Teste final

Apresentar:

- matriz de confusão;
- acurácia;
- balanced accuracy;
- sensibilidade;
- especificidade;
- precisão;
- F1;
- ROC-AUC;
- PR-AUC;
- curva ROC;
- curva precisão-recall.

Criar:

```python
report = classification_report_health(
    y_test,
    y_pred,
    y_prob,
)
```

As fórmulas devem aparecer em Markdown.

### Explicabilidade

Treinar adicionalmente um `RandomForestClassifier` ou equivalente e apresentar:

- importância por permutação;
- SHAP em barras;
- beeswarm;
- dependência da variável principal;
- uma observação correta;
- uma observação incorreta.

Usar amostra SHAP de 200–500 registros.

### Regras contra vazamento

- scaler ajustado apenas no treino;
- seleção dentro da validação;
- teste usado somente ao final;
- nenhum hiperparâmetro escolhido pelo teste.

### Reflexões

- ROC-AUC é suficiente?
- qual erro é mais relevante?
- SHAP mostra causalidade?
- o que muda ao alterar o limiar?

### Aceitação

- cinco folds;
- matriz de confusão;
- ROC e precisão-recall;
- heatmap e tabela de correlação;
- ao menos duas visualizações de explicabilidade;
- interpretação de falso positivo e falso negativo.

---

## 11.3 Notebook 03 — K-means e PCA

### Título

**Descobrindo perfis: K-means, elbow e PCA**

### Objetivos

- compreender agrupamento;
- selecionar atributos;
- padronizar escalas;
- aplicar K-means;
- usar elbow e silhouette;
- visualizar com PCA;
- caracterizar clusters;
- evitar interpretação clínica indevida.

### Atributos sugeridos

- `BMI`;
- `Age`;
- `GenHlth`;
- `PhysHlth`;
- `MentHlth`;
- `Education`;
- `Income`.

O alvo não pode participar do agrupamento.

### Fluxo

1. selecionar atributos;
2. tratar ausências;
3. padronizar;
4. calcular K-means para `k=2` a `k=8`;
5. armazenar inércia e silhouette;
6. plotar elbow e silhouette;
7. escolher `k`, com `KneeLocator` e fallback transparente;
8. ajustar K-means final;
9. aplicar PCA com dois componentes;
10. mostrar variância explicada;
11. mostrar dispersão e centróides;
12. criar tabela de perfil;
13. analisar o alvo apenas depois, como avaliação externa;
14. criar heatmap de médias padronizadas.

### Cuidados

- PCA perde informação;
- clusters não são classes verdadeiras;
- K-means depende de escala e inicialização;
- clusters não devem ser chamados de fenótipos clínicos sem validação.

### Aceitação

- elbow;
- silhouette;
- K-means;
- PCA 2D;
- tabela de perfil;
- heatmap;
- alvo excluído do agrupamento.

---

## 11.4 Notebook 04 — Modelos e hiperparâmetros

### Título

**Comparando modelos sem escrever muito código**

### Objetivos

- comparar algoritmos na mesma validação;
- criar leaderboard;
- evitar seleção apenas por acurácia;
- buscar hiperparâmetros;
- preservar o teste;
- comparar antes e depois da otimização.

### Modelos mínimos

1. regressão logística;
2. árvore de decisão;
3. random forest;
4. histogram gradient boosting.

### Interface

```python
models = get_default_classifiers(random_state=42)

leaderboard = compare_classifiers(
    models=models,
    X=X_train,
    y=y_train,
    cv=5,
    scoring="roc_auc",
)
```

Depois:

```python
best_model, search = tune_classifier(
    model_name=leaderboard.iloc[0]["model"],
    X=X_train,
    y=y_train,
    cv=5,
    n_iter=20,
    scoring="roc_auc",
)
```

### Implementação de `compare_classifiers`

- mesma validação para todos;
- ROC-AUC;
- F1;
- recall;
- precision;
- balanced accuracy;
- tempo de ajuste;
- DataFrame ordenado;
- captura de falhas;
- nenhum acesso ao teste.

### Implementação de `tune_classifier`

- `RandomizedSearchCV`;
- espaços de busca pequenos;
- cinco folds;
- melhores parâmetros;
- tabela resumida;
- custo controlado.

### Visualizações

- leaderboard;
- gráfico de métricas;
- tempo;
- padrão versus ajustado;
- matriz de confusão final;
- ROC final.

### Aceitação

- quatro modelos;
- mesma validação;
- busca aleatória;
- teste intacto;
- leaderboard;
- melhores parâmetros;
- desempenho antes e depois.

---

## 11.5 Notebook 05 — Imagens e Grad-CAM

### Título

**Classificação de imagens médicas e Grad-CAM com CNN pequena**

### Objetivos

- carregar imagens;
- visualizar exemplos;
- usar treino, validação e teste oficiais;
- criar CNN pequena;
- avaliar classificação;
- gerar Grad-CAM;
- interpretar limites dos mapas de calor.

### Execução

- recomendar GPU;
- detectar GPU;
- continuar em CPU com aviso;
- 5–10 épocas;
- `EarlyStopping`;
- batches pequenos.

### Fluxo

1. instalar `medmnist`;
2. baixar os três conjuntos;
3. mostrar dimensões e classes;
4. exibir grade de imagens;
5. normalizar;
6. construir CNN;
7. treinar;
8. mostrar curvas de loss e AUC/accuracy;
9. avaliar:
   - matriz de confusão;
   - sensibilidade;
   - especificidade;
   - F1;
   - ROC-AUC;
10. localizar última camada convolucional;
11. produzir Grad-CAM para:
    - verdadeiro positivo;
    - verdadeiro negativo;
    - falso positivo, quando existir;
    - falso negativo, quando existir;
12. mostrar imagem, heatmap, sobreposição, probabilidade e rótulo.

### Função

```python
show_gradcam(
    model=model,
    image=X_test[index],
    last_conv_layer="nome_da_camada",
    class_index=0,
)
```

### Cuidados

- Grad-CAM mostra influência na rede, não justificativa clínica;
- mapas podem destacar artefatos;
- baixa resolução reduz interpretação;
- não afirmar detecção clínica real;
- mostrar pelo menos um erro.

### Aceitação

- download automático;
- CNN funcional;
- curvas;
- matriz de confusão;
- métricas;
- pelo menos três Grad-CAM;
- aviso de não uso clínico.

---

## 11.6 Notebook 06 — Sobrevivência

### Título

**Tempo até o evento: Kaplan–Meier e regressão de Cox**

### Objetivos

- compreender tempo, evento e censura;
- visualizar Kaplan–Meier;
- comparar grupos;
- executar log-rank;
- ajustar Cox;
- interpretar hazard ratio;
- verificar proporcionalidade;
- entender estratificação.

### Preparação

- baixar CSV;
- remover índice;
- recodificar `event`;
- mapear sexo;
- mostrar ausências;
- usar estratégia explícita;
- informar registros removidos.

### Sem estratificação

1. KM global;
2. intervalo de confiança;
3. mediana;
4. número em risco, quando viável;
5. Cox com idade, sexo e `ph.ecog`;
6. coeficiente, HR, IC e p-valor;
7. forest plot;
8. verificação de riscos proporcionais.

### Estratificação visual

- KM por sexo;
- log-rank;
- interpretação.

### Cox estratificado

```python
cph.fit(
    df_model,
    duration_col="time",
    event_col="event",
    strata=["sex"],
)
```

Comparar:

- coeficientes restantes;
- concordance index;
- log-likelihood;
- ausência de coeficiente único para o estrato.

### Cuidados

- hazard não é probabilidade;
- HR não é diferença de sobrevivência;
- significância não garante relevância clínica;
- não afirmar causalidade;
- base pequena.

### Aceitação

- KM global;
- KM por grupo;
- log-rank;
- Cox sem estratificação;
- Cox estratificado;
- forest plot;
- verificação de pressupostos.

---

## 11.7 Notebook 07 — Aprendizado por reforço

### Título

**Aprendizado por reforço para planejamento de estoque em vigilância epidemiológica**

### Contexto

Criar ambiente simplificado para decisão de estoque de kits ou insumos. O agente observa demanda recente e escolhe um nível de estoque.

Não simular tratamento ou decisão clínica.

### Objetivos

- compreender estado, ação, recompensa e episódio;
- diferenciar supervisionado e reforço;
- construir ambiente discreto;
- aplicar Q-learning;
- observar exploração e explotação;
- visualizar convergência;
- interpretar política;
- discutir a função de recompensa.

### Dados reais e ambiente simulado

A série de dengue será real. Ações e recompensas serão sintéticas e identificadas como tal.

### Estados

Combinar:

- demanda baixa, média ou alta;
- tendência caindo, estável ou subindo.

Total: 9 estados.

Limites calculados apenas no treino.

### Ações

- estoque baixo;
- estoque médio;
- estoque alto.

### Recompensa

```text
recompensa =
    - custo_de_excesso
    - custo_de_falta
    - custo_operacional
```

Falta terá custo maior, mas todos os valores devem ficar em configuração.

### Ambiente

```python
env = DengueInventoryEnv(
    demand_series=train_series,
    stock_levels=[q25, q50, q75],
)

state = env.reset()
next_state, reward, done, info = env.step(action)
```

### Q-learning

```python
q_table, rewards = train_q_learning(
    env,
    episodes=1000,
    alpha=0.1,
    gamma=0.95,
    epsilon_start=1.0,
    epsilon_end=0.05,
)
```

### Avaliação

Comparar com:

1. estoque sempre médio;
2. política aleatória;
3. regra baseada no último valor.

Apresentar:

- recompensa acumulada;
- custo de falta;
- custo de excesso;
- semanas com falta;
- política final;
- heatmap da Q-table;
- recompensa por episódio;
- evolução de epsilon.

### Separação temporal

- anos iniciais para treino;
- anos finais para teste;
- sem embaralhamento;
- quantis calculados somente no treino.

### Reflexões

- como a recompensa muda a política?
- maior recompensa significa melhor decisão pública?
- quais variáveis faltam?
- os dados mostram efeito causal das ações? Não.

### Aceitação

- InfoDengue;
- ambiente documentado;
- Q-learning;
- baseline;
- teste temporal;
- Q-table;
- curva de aprendizado;
- aviso de ambiente sintético.

---

## 11.8 Notebook 08 — Séries temporais

### Título

**Prevendo casos semanais de dengue com atributos de defasagem**

### Objetivos

- compreender ordem temporal;
- visualizar tendência e sazonalidade;
- criar lags;
- estabelecer baseline;
- usar divisão temporal;
- aplicar `TimeSeriesSplit`;
- avaliar previsão;
- reconhecer limites epidemiológicos.

### Alvo

Preferir `casos_est`, quando disponível. Permitir `casos` com explicação.

### Preparação

1. baixar e ordenar;
2. converter datas;
3. inspecionar semanas ausentes;
4. não preencher com zero automaticamente;
5. evitar ano parcial;
6. documentar qualquer interpolação.

### Análise

- série completa;
- média móvel de quatro semanas;
- padrão por mês ou semana epidemiológica;
- decomposição opcional;
- autocorrelação.

### Atributos

```python
features = make_lag_features(
    series,
    lags=[1, 2, 3, 4, 8, 12, 52],
    rolling_windows=[4, 8, 12],
)
```

Incluir:

- lags;
- médias móveis deslocadas;
- desvio-padrão móvel deslocado;
- seno e cosseno da semana;
- tendência.

Toda janela deve usar apenas o passado.

### Divisão

- treino: anos iniciais;
- validação: período intermediário ou `TimeSeriesSplit`;
- teste: último ano completo;
- nunca divisão aleatória.

### Baseline

```text
previsão da próxima semana = valor da semana anterior
```

### Modelo

Preferência:

```text
HistGradientBoostingRegressor
```

Alternativa:

```text
RandomForestRegressor
```

### Avaliação

- MAE;
- RMSE;
- WAPE ou sMAPE;
- comparação com baseline;
- real versus previsto;
- resíduos;
- erro por período;
- importância por permutação;
- previsão um passo à frente.

### Regras

- `TimeSeriesSplit(n_splits=5)`;
- nenhum futuro nos atributos;
- teste intacto;
- pré-processamento ajustado no treino.

### Interpretação

- prever não é explicar;
- notificações podem ser revisadas;
- mudanças estruturais afetam desempenho;
- sazonalidade pode mudar;
- desempenho passado não garante futuro;
- não orientar ação pública.

### Aceitação

- série real;
- baseline;
- lags;
- validação temporal;
- modelo;
- comparação visual;
- métricas;
- ausência de vazamento.

---

# 12. Funções auxiliares

## `src/data_loading.py`

```python
def load_cdc_diabetes(
    sample_size: int | None = None,
    random_state: int = 42,
    stratify: bool = True,
) -> tuple:
    """Baixa e prepara a base CDC Diabetes Health Indicators."""
```

## `src/visualization.py`

```python
def plot_variable(
    data,
    column: str,
    target: str | None = None,
    kind: str = "auto",
):
    """Escolhe uma visualização adequada ao tipo do atributo."""
```

## `src/evaluation.py`

```python
def classification_report_health(
    y_true,
    y_pred,
    y_prob=None,
):
    """Calcula métricas relevantes para classificação em saúde."""
```

Incluir cálculo explícito de especificidade.

## `src/model_selection.py`

```python
def compare_classifiers(...):
    """Compara modelos usando a mesma validação cruzada."""

def tune_classifier(...):
    """Executa RandomizedSearchCV sem acessar o teste."""
```

## `src/clustering.py`

```python
def evaluate_kmeans_range(
    X_scaled,
    k_values=range(2, 9),
):
    """Calcula inércia e silhouette."""
```

## `src/gradcam.py`

```python
def make_gradcam_heatmap(
    image,
    model,
    last_conv_layer_name: str,
):
    """Produz Grad-CAM para uma imagem."""
```

## `src/dengue_api.py`

```python
def fetch_infodengue(
    geocode: int,
    disease: str,
    start_year: int,
    end_year: int,
    cache: bool = True,
):
    """Baixa, valida e organiza dados do InfoDengue."""
```

## `src/reinforcement_env.py`

```python
class DengueInventoryEnv:
    """Ambiente didático de estoque baseado em demanda."""
```

## `src/time_series.py`

```python
def make_lag_features(...):
    """Cria atributos usando somente informações anteriores."""

def temporal_train_test_split(...):
    """Separa dados preservando ordem temporal."""
```

---

# 13. README

O README deverá conter:

- descrição;
- objetivos;
- tabela dos oito notebooks;
- botão Colab por notebook;
- nível e duração;
- bases utilizadas;
- execução;
- estrutura;
- licença;
- citação;
- aviso educacional;
- contribuição;
- compatibilidade;
- problemas conhecidos.

Tabela:

| Nº | Tema | Base | Duração | Colab |
|---:|---|---|---:|---|
| 01 | Estatística descritiva | CDC Diabetes | 45–60 min | botão |
| 02 | Supervisionado e SHAP | CDC Diabetes | 75–90 min | botão |
| 03 | K-means e PCA | CDC Diabetes | 60–75 min | botão |
| 04 | Modelos e hiperparâmetros | CDC Diabetes | 75–90 min | botão |
| 05 | Imagens e Grad-CAM | PneumoniaMNIST | 90 min | botão |
| 06 | Sobrevivência | NCCTG Lung | 75–90 min | botão |
| 07 | Reforço | InfoDengue | 75–90 min | botão |
| 08 | Séries temporais | InfoDengue | 75–90 min | botão |

Criar glossário:

- atributo;
- alvo;
- treino;
- validação;
- teste;
- fold;
- sensibilidade;
- especificidade;
- precisão;
- F1;
- ROC-AUC;
- explicabilidade;
- cluster;
- censura;
- hazard;
- estado;
- ação;
- recompensa;
- lag.

---

# 14. Dependências

Criar `requirements-colab.txt` com intervalos conservadores:

```text
ucimlrepo>=0.0.7,<1
shap>=0.45,<1
lifelines>=0.30,<1
medmnist>=3,<4
kneed>=0.8,<1
```

O Codex deverá:

1. testar no Colab atual;
2. registrar versões funcionais;
3. evitar pinagem rígida desnecessária;
4. não usar versões alfa como dependência obrigatória;
5. evitar reinicialização do runtime;
6. emitir erros claros.

---

# 15. Desempenho esperado

| Notebook | Ambiente | Meta |
|---|---|---:|
| 01 | CPU | até 4 min |
| 02 | CPU | até 8 min |
| 03 | CPU | até 5 min |
| 04 | CPU | até 10 min |
| 05 | GPU | até 12 min |
| 06 | CPU | até 4 min |
| 07 | CPU | até 4 min |
| 08 | CPU | até 6 min |

Criar `FAST_MODE=True` para testes. Ele poderá reduzir amostra, épocas, iterações e episódios, mas o notebook final deve preservar cinco folds onde exigido.

---

# 16. Testes

## 16.1 Unitários

Cobrir:

- carregamento da base;
- especificidade;
- formato do leaderboard;
- ausência de uso do teste na busca;
- criação de lags;
- ausência de lags futuros;
- transições do ambiente;
- recodificação do evento.

## 16.2 Smoke tests

Workflow para:

- validar JSON dos notebooks;
- executar importações;
- rodar fluxo principal em `FAST_MODE`;
- não treinar imagem completa em toda alteração;
- apresentar erros úteis.

## 16.3 Teste manual

1. abrir pelo botão Colab;
2. executar tudo;
3. confirmar ausência de upload;
4. confirmar término;
5. revisar gráficos e textos;
6. registrar data e versões.

---

# 17. Critérios globais de aceitação

- [ ] oito notebooks;
- [ ] todos abrem pelo Colab;
- [ ] download automático;
- [ ] nenhum token ou login;
- [ ] código visível simplificado;
- [ ] funções documentadas;
- [ ] fontes e licenças registradas;
- [ ] aviso educacional em todos;
- [ ] notebook 01 com estatística, gráficos e pairplot;
- [ ] notebook 02 com correlação, cinco folds, matriz, métricas e SHAP;
- [ ] notebook 03 com elbow, K-means e PCA;
- [ ] notebook 04 com comparação e hiperparâmetros;
- [ ] notebook 05 com imagens e Grad-CAM;
- [ ] notebook 06 com e sem estratificação;
- [ ] notebook 07 com Q-learning;
- [ ] notebook 08 com baseline, lags e validação temporal;
- [ ] teste não usado para ajuste;
- [ ] sem vazamento temporal;
- [ ] interpretação cautelosa;
- [ ] execução no Colab gratuito;
- [ ] README com oito botões;
- [ ] testes básicos aprovados.

---

# 18. Qualidade textual

- linguagem clara;
- termos definidos;
- parágrafos curtos;
- evitar jargão sem explicação;
- diferenciar observação, hipótese e conclusão;
- evitar “o modelo provou”;
- preferir “nesta amostra” e “neste experimento”;
- não chamar predição de diagnóstico;
- destacar inferências pedagógicas;
- títulos e legendas em português.

---

# 19. Tratamento de erros

Downloads devem:

- definir timeout;
- verificar status;
- validar colunas;
- emitir mensagem acionável;
- usar cache quando disponível;
- informar uso do cache;
- não ocultar exceções;
- nunca substituir dados reais por sintéticos silenciosamente.

Exemplo:

```text
Não foi possível acessar a API do InfoDengue.
Verifique conexão, período e código IBGE.
Nenhum dado sintético foi utilizado.
```

---

# 20. Ética e limitações

## Tabular

- autorrelato;
- representação de grupos;
- sexo, idade, renda e escolaridade;
- associação versus causalidade;
- desbalanceamento;
- generalização.

## Imagens

- origem da amostra;
- população pediátrica;
- resolução;
- artefatos;
- mudança de equipamento;
- shortcut learning;
- Grad-CAM não é validação clínica.

## Sobrevivência

- censura;
- tamanho amostral;
- proporcionalidade;
- confundimento;
- hazard versus risco absoluto.

## Reforço

- recompensa é escolha normativa;
- ambiente não representa a realidade integral;
- dados históricos não mostram efeito causal das ações simuladas.

## Séries temporais

- atraso e revisão;
- mudança de vigilância;
- sazonalidade;
- choques externos;
- incerteza;
- desempenho passado não garante futuro.

---

# 21. Ordem de implementação

1. criar estrutura;
2. criar configuração;
3. implementar carregamento CDC;
4. notebook 01;
5. métricas e notebook 02;
6. clustering e notebook 03;
7. comparação/tuning e notebook 04;
8. MedMNIST e Grad-CAM;
9. sobrevivência;
10. cliente InfoDengue;
11. ambiente de reforço;
12. funções temporais;
13. README e botões;
14. testes;
15. smoke tests;
16. revisão;
17. validação no Colab.

---

# 22. Instrução final ao Codex

Implemente o repositório completo. Não entregue apenas pseudocódigo ou trechos isolados.

- crie os oito `.ipynb`;
- mantenha pouco código por célula;
- escreva explicações em Markdown;
- mova complexidade repetitiva para `src/`;
- baixe dados diretamente das fontes;
- teste em ambiente equivalente ao Colab;
- não peça upload;
- não use dados privados;
- não use teste para seleção;
- não embaralhe séries temporais;
- não esconda decisões metodológicas;
- inclua atividades e interpretações;
- crie todos os botões Colab;
- documente para aluno e professor;
- registre limitações;
- valide os critérios de aceitação.

Quando uma biblioteca ou API tiver mudado, adapte a implementação usando documentação oficial atual, preservando os objetivos pedagógicos e a interface simples deste PRD.
