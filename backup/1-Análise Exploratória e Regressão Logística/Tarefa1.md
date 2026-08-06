
# Tarefa 1

## Análise de Fatores de Risco para Doença Cardíaca Usando o Heart Disease Dataset

Neste exercício, você irá trabalhar com um conjunto de dados de saúde que contém informações detalhadas sobre fatores de risco para doenças cardíacas. O dataset inclui variáveis como idade, sexo, tipo de dor no peito, pressão arterial em repouso, colesterol sérico, e outras medições clínicas.

**Objetivo:** realizar uma análise exploratória e desenvolver um modelo preditivo para identificar a presença de doença cardíaca com base nesses fatores.


## Dataset

O dataset inclui as seguintes variáveis:

- age: Idade do paciente.
- sex: Sexo (1 = masculino; 0 = feminino).
- cp: Tipo de dor no peito (4 valores: 1 = angina típica; 2 = angina atípica; 3 = dor não anginosa; 4 = assintomática).
- trestbps: Pressão arterial em repouso (mm Hg).
- chol: Colesterol sérico em mg/dl.
- fbs: Açúcar no sangue em jejum > 120 mg/dl (1 = verdadeiro; 0 = falso).
- restecg: Resultados do eletrocardiograma em repouso (0 = normal; 1 = com anormalidade na onda ST-T; 2 = hipertrofia ventricular esquerda).
- thalach: Frequência cardíaca máxima atingida.
- exang: Angina induzida por exercício (1 = sim; 0 = não).
- oldpeak: Depressão do segmento ST induzida por exercício em relação ao repouso.
- slope: Inclinação do segmento ST no pico do exercício (1 = subida; 2 = plana; 3 = descendente).
- ca: Número de vasos principais (0-3) coloridos por fluoroscopia.
- thal: 0 = normal; 1 = defeito fixo; 2 = defeito reversível.
- target: Diagnóstico de doença cardíaca (1 = presença de doença; 0 = ausência de doença).


## Passos

1.	Leitura do Dataset

2. 	Análise Descritiva

- 	Explore as estatísticas descritivas das variáveis, como age, chol, trestbps, e thalach.

3. 	Visualização dos Dados

-	Crie gráficos para explorar a distribuição das variáveis como age, chol, trestbps, e thalach. Utilize histogramas, boxplots, e gráficos de dispersão.

4.	Teste de Correlação

- Realize testes de correlação para identificar a relação entre variáveis contínuas, como idade, colesterol, e frequência cardíaca máxima.

5.	Modelo Explicativo: Regressão Logística

- Construa um modelo de regressão logística para prever a presença de doença cardíaca (target) usando variáveis como age, sex, cp, chol, thalach, e ca.

6. 	Interpretação dos Resultados

- Interprete os coeficientes do modelo de regressão logística, focando nas variáveis significativas. Discuta como essas variáveis influenciam a probabilidade de presença de doença cardíaca.
- Calcule o AIC do modelo e discuta sua relevância na seleção do modelo.
	
7.	Conclusão

- Baseado na análise, conclua quais fatores de risco são mais relevantes para a previsão de doença cardíaca e como esses insights podem ser utilizados em prática clínica ou em futuros estudos.

## Download da base

[link](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset?resource=download)

