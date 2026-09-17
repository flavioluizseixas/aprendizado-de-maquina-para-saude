# Atividade 3 — Aprendizado não supervisionado

## K-means e PCA | Versão mínima

**Objetivo:** explorar grupos de pessoas com indicadores de saúde semelhantes, justificar a escolha do número de clusters e interpretar seus perfis e sua projeção em duas dimensões.

**Tempo estimado:** 40–50 minutos, incluindo a comparação final.

## Material e dados

Use o notebook [03_aprendizado_nao_supervisionado_versão_minima.ipynb](../notebooks/03_aprendizado_nao_supervisionado_vers%C3%A3o_minima.ipynb), com seis células de código. Abra o arquivo no Google Colab ou no Jupyter com pandas, matplotlib e scikit-learn instalados. O carregamento requer internet.

Fonte: [CDC Diabetes Health Indicators — UCI 891](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators). Consulte o dicionário e os termos de uso na fonte. Cada linha representa uma pessoa. O notebook seleciona 5.000 registros com random_state=42, após excluir eventuais ausências nos atributos usados.

- **BMI:** índice de massa corporal, em kg/m².
- **Age:** faixa etária codificada de 1 a 13; o código não é a idade em anos.
- **GenHlth:** saúde geral, de 1 (excelente) a 5 (ruim).
- **PhysHlth e MentHlth:** dias de saúde física e mental ruim nos últimos 30 dias.
- **Education e Income:** categorias ordenadas de escolaridade (1–6) e renda (1–8).

Age, GenHlth, Education e Income serão tratados como números: isso simplifica as distâncias entre categorias. ID é apenas identificador. Diabetes_binary (0 = sem diabetes; 1 = pré-diabetes/diabetes) será usado somente para descrever os grupos já formados, sem participar da padronização, da escolha de k, do K-means ou do PCA.

## Roteiro e questões

### 1. Dados e padronização

Execute as seções 1 e 2. Informe o tamanho da amostra e os atributos usados. Explique por que padronizar antes de calcular distâncias e por que excluir ID e Diabetes_binary do agrupamento. Aqui, a análise é exploratória na própria amostra, sem avaliação preditiva em um conjunto de teste.

### 2. Quantos grupos?

Execute a seção 3 para k de 2 a 6, com n_init=10 e random_state=42. Apresente a tabela e os gráficos de inércia e silhouette; este último usa uma subamostra fixa de 2.000 registros para reduzir o custo. Existe um cotovelo claro? Qual k apresenta o maior silhouette? O que um valor próximo de zero sugere?

### 3. Escolha e ajuste final

Execute a seção 4. O código começa pelo k com maior silhouette; você pode substituí-lo por outro entre 2 e 6, justificando a decisão pelos dois gráficos. Registre o k escolhido e o tamanho de cada cluster. A menor inércia, isoladamente, não define a melhor escolha.

### 4. Perfis dos grupos

Execute a seção 5 e compare as médias dos atributos na escala original. Descreva dois clusters usando pelo menos três atributos e seus tamanhos. Compare o percentual de pré-diabetes/diabetes observado em cada grupo. Explique por que essa diferença não demonstra causalidade nem transforma os clusters em diagnósticos. Os números dos clusters são rótulos arbitrários, sem ordem de gravidade.

### 5. Visualização com PCA

Execute a seção 6. Apresente o gráfico, a variância explicada por PC1 e PC2 e a soma das duas. O K-means usa todos os atributos padronizados; o PCA serve para visualizar os grupos. Comente a sobreposição no plano e a informação que fica fora desses dois eixos. A variância explicada não é uma medida de acurácia.

### 6. Pequena mudança no experimento

Guarde as tabelas e o gráfico da execução inicial. Retire Income da lista de atributos e execute novamente as seis células, mantendo a amostra de 5.000 registros, a semente e os mesmos critérios de escolha de k. Compare o k escolhido, o silhouette, os tamanhos e os perfis. A retirada do atributo altera as distâncias: um silhouette maior não basta para concluir que a nova solução é melhor. Se havia ausências, confirme que os IDs da amostra permaneceram os mesmos. Compare grupos pelos perfis, pois o número de um cluster pode mudar entre execuções.

## Entrega e critérios

Entregue um único arquivo .ipynb com identificação dos participantes, código executado, saídas das duas análises e respostas em células Markdown. Para preservar a primeira análise, duplique as seis células antes de alterar a lista de atributos na cópia. Conclua em 5–8 linhas, destacando um achado e duas limitações.

A avaliação considera execução reproduzível, justificativa de k, interpretação dos perfis e do PCA e comparação fundamentada entre as duas análises. Não é necessário obter grupos bem separados: resultados com sobreposição também devem ser discutidos.

Material com finalidade exclusivamente educacional. Os indicadores incluem autorrelato; os resultados descrevem esta amostra, não estimam prevalências populacionais e não devem orientar decisões clínicas.

## Referências de apoio

- [K-means — scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
- [Silhouette — scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)
- [PCA — scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
