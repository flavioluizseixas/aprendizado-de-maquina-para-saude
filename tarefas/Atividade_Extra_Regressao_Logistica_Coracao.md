# Atividade em grupos — Regressão logística e doença cardíaca

## Proposta

Como avaliar um modelo de classificação e interpretar o que seus coeficientes dizem sobre as odds de doença cardíaca? Cada grupo executará um código pronto, analisará o desempenho no teste e explicará associações estimadas pelo modelo.

**Organização sugerida:** grupos de 3–4 alunos; 60–75 minutos. Distribuam as funções de execução, conferência dos cálculos, interpretação e apresentação. Todos devem participar das respostas.

**Material:** [notebook pronto em Python](../notebooks/extra_regressao_logistica_coracao.ipynb). São seis células de código, executáveis no Colab ou no Jupyter com numpy, pandas e scikit-learn. O carregamento requer internet; não é necessário clonar o repositório.

## Base e modelo

Usaremos [Heart Disease — Cleveland, UCI](https://archive.ics.uci.edu/dataset/45/heart+disease), de Janosi, Steinbrunn, Pfisterer e Detrano (1989), sob licença CC BY 4.0. A base tem 303 registros. O desfecho representa presença de doença registrada na base, não o risco de desenvolver doença no futuro: y=0 quando num=0; y=1 quando num é maior que zero.

O modelo usará apenas cinco atributos, escolhidos previamente para facilitar a interpretação:

- **age:** idade, em anos.
- **trestbps:** pressão arterial de repouso na admissão, em mmHg.
- **chol:** colesterol sérico, em mg/dL.
- **thalach:** frequência cardíaca máxima atingida no exame, em batimentos por minuto.
- **exang:** angina induzida por exercício, 0 = não e 1 = sim.

A base possui ausências em outros atributos; o notebook verifica apenas os cinco usados e o desfecho. Mantém divisão estratificada de 75% para treino e 25% para teste, semente 42, padronização ajustada no treino e regressão logística com regularização L2 (C=1). Todos os grupos usam a mesma configuração e limiar 0,5. Não alterem o modelo com base no resultado do teste.

## Parte comum — todos os grupos

### 1. Dados e treinamento

Execute as células 1 e 2. Informe quantos registros e quantos casos positivos há no treino e no teste. Explique a estratificação e por que a padronização é ajustada apenas no treino. Onde estão armazenados os coeficientes estimados?

### 2. Desempenho no teste

Execute a célula 3. Registre verdadeiros positivos, verdadeiros negativos, falsos positivos e falsos negativos. Apresente acurácia, sensibilidade, especificidade, precisão, F1 e ROC-AUC. Confira manualmente sensibilidade e especificidade usando a matriz. Compare a acurácia com a de um classificador que sempre prevê a classe mais frequente do treino. O que a acurácia isolada esconderia? ROC-AUC mede ordenação, não garante probabilidades bem calibradas.

### 3. Coeficientes

Execute a célula 4. Escolha um coeficiente positivo e um negativo, se houver, e explique sua direção em relação à classe 1. Diferencie escala padronizada e escala original. Por que é preciso converter também o intercepto? Compare coeficientes sempre considerando as unidades; os atributos podem estar correlacionados.

### 4. Odds e probabilidades

Execute a célula 5. Escolha um dos cinco registros apresentados e informe sua probabilidade e suas odds estimadas. Confira odds=p/(1−p) e p=odds/(1+odds). Por que odds não são porcentagens? A probabilidade reconstruída pelos coeficientes coincide com predict_proba?

### 5. Odds ratios

Execute a célula 6. Interprete uma OR para atributo contínuo e a OR de exang, sempre mantendo os demais atributos constantes. Use o incremento indicado na tabela. Complete: “Segundo este modelo, [contraste] está associado a odds de doença multiplicadas por [OR], mantendo os demais atributos constantes”. OR próxima de 1 não permite concluir ausência de associação estatística: este roteiro não calcula testes de significância.

## Foco de discussão de cada grupo

Todos completam a parte comum; distribua os focos A–D entre os grupos. Se houver mais grupos, repita os focos para comparar interpretações.

- **A — Erros e desempenho:** explique um falso negativo e um falso positivo neste contexto. Se o limiar diminuísse, qual mudança seria esperada na sensibilidade e na especificidade? Discuta sem procurar o melhor limiar no teste.
- **B — Idade e pressão:** interprete as OR para +10 anos e +10 mmHg. Calcule também a OR para +20 anos usando o coeficiente de age e confira a relação com a OR para +10 anos.
- **C — Colesterol e frequência cardíaca:** interprete as OR para +20 mg/dL de colesterol e +10 batimentos/minuto. Um coeficiente negativo demonstra que aumentar essa variável protege uma pessoa? Discuta associação, correlação entre atributos e seleção da amostra.
- **D — Angina, odds e probabilidade:** interprete exang=1 versus exang=0. Para um perfil hipotético com exang=0 e probabilidade p₀=0,20, use a OR de exang para obter odds₁=OR×p₀/(1−p₀) e p₁=odds₁/(1+odds₁), mantendo os demais atributos constantes. Compare p₁ com OR×p₀ e explique a diferença. O cálculo é um contraste do modelo, não efeito de uma intervenção.

## Entrega e fechamento

Entregue um .ipynb por grupo com nomes, saídas das seis células, respostas da parte comum e do foco atribuído. Prepare uma apresentação de três minutos com uma métrica, uma OR interpretada e uma limitação. Antes de entregar, reinicie o ambiente e execute todas as células em sequência.

Critérios: execução reproduzível, leitura correta da matriz, distinção entre probabilidade e odds, interpretação da OR com seu incremento e discussão dos limites. Os coeficientes e OR pertencem ao mesmo modelo regularizado; não são estimativas causais. A amostra pequena e histórica e a ausência de validação externa limitam a generalização. Material com finalidade exclusivamente educacional, sem uso em decisões clínicas.

## Referências de apoio

- [Regressão logística — scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
- [Padronização — scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)
