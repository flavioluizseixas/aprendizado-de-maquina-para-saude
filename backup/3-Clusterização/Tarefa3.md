# Tarefa 3

## Breast Cancer Wisconsin (Diagnostic) Dataset - UCI Machine Learning Repository

Este dataset contém 569 instâncias e 30 atributos numéricos que descrevem características extraídas de imagens digitalizadas de exames de tumores mamários. Esses atributos incluem:

- Radius: Média do raio (distância do centro aos pontos do perímetro)
Texture: Desvio padrão dos valores de cinza da superfície celular
- Perimeter: Perímetro médio
- Area: Área média
- Smoothness: Variação local nos comprimentos dos raios
- Compactness: (Perímetro² / Área - 1.0)
- Concavity: Severidade das concavidades na superfície celular
- Concave points: Número de pontos côncavos no contorno
- Symmetry: Simetria da célula
- Fractal dimension: Dimensão fractal ("aproximação" da irregularidade)

O objetivo será agrupar as instâncias com base nas características celulares para encontrar padrões entre diferentes tipos de tumores.

Link para o dataset:
[Breast Cancer Wisconsin (Diagnostic) Data Set](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29)

## Metodologia

Aplicar o algoritmo de K-Means para identificar padrões e similaridades entre tumores mamários a partir das características celulares fornecidas no dataset. O objetivo será agrupar os dados e explorar se os clusters resultantes correspondem a padrões de benignidade ou malignidade dos tumores.

1. Coleta e preparação de dados:
  - Carregar e explorar o dataset para compreender as variáveis e o formato dos dados.
  - Realizar o pré-processamento necessário, como normalização e tratamento de valores ausentes.

2. Aplicação do K-Means:
  - Utilizar o algoritmo K-Means para agrupar os tumores com base nas características celulares.
  - Avaliar diferentes números de clusters (valores de K) e interpretar os resultados.

3. Análise dos clusters:
  - Identificar padrões comuns nos clusters, como características celulares típicas de tumores malignos ou benignos.
  - Explorar a relação entre os clusters e a variável de saída (benigno/maligno) para validar os agrupamentos.

4. Visualização dos resultados:
  - Utilizar técnicas como PCA (Análise de Componentes Principais) para reduzir a dimensionalidade e visualizar os clusters em gráficos.

## Conclusões:

Discutir como os agrupamentos podem ajudar na estratificação dos pacientes e no entendimento dos fatores celulares que influenciam o risco de malignidade.