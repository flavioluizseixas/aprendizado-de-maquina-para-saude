# Redução de Dimensões Usando PCA

Vamos estender o exemplo numérico para um conjunto de dados em 4 dimensões, com o objetivo de reduzir para 2 dimensões usando o **PCA**. Essa redução é útil para visualizar clusters que foram gerados por algoritmos como **K-means**.

## Exemplo Numérico em 4 Dimensões

Suponha que temos o seguinte conjunto de dados com 5 amostras em 4 dimensões:

$$
X = \begin{bmatrix}
2 & 4 & 1 & 3 \\
6 & 8 & 2 & 5 \\
7 & 10 & 3 & 6 \\
13 & 14 & 7 & 9 \\
18 & 20 & 9 & 12
\end{bmatrix}
$$

### Passo 1: Centralização dos Dados

Primeiro, vamos centralizar os dados subtraindo a média de cada coluna (dimensão):

1. **Cálculo da média** para cada dimensão:

$$
\text{Média} = \begin{bmatrix}
9.2 \\
11.2 \\
4.4 \\
7
\end{bmatrix}
$$

2. **Centralização dos dados**:

$$
X_{centralizado} = X - \text{Média}
$$

Subtraindo a média de cada amostra:

$$
X_{centralizado} = \begin{bmatrix}
2-9.2 & 4-11.2 & 1-4.4 & 3-7 \\
6-9.2 & 8-11.2 & 2-4.4 & 5-7 \\
7-9.2 & 10-11.2 & 3-4.4 & 6-7 \\
13-9.2 & 14-11.2 & 7-4.4 & 9-7 \\
18-9.2 & 20-11.2 & 9-4.4 & 12-7
\end{bmatrix}
$$

$$
X_{centralizado} = \begin{bmatrix}
-7.2 & -7.2 & -3.4 & -4 \\
-3.2 & -3.2 & -2.4 & -2 \\
-2.2 & -1.2 & -1.4 & -1 \\
3.8 & 2.8 & 2.6 & 2 \\
8.8 & 8.8 & 4.6 & 5
\end{bmatrix}
$$

### Passo 2: Cálculo da Matriz de Covariância

A matriz de covariância é dada por:

$$
\text{Cov}(X) = \frac{1}{n-1} (X_{centralizado}^T X_{centralizado})
$$

Calculando a matriz de covariância:

$$
\text{Cov}(X) = \begin{bmatrix}
40.7 & 37.7 & 18.7 & 21.5 \\
37.7 & 35.7 & 17.7 & 20.5 \\
18.7 & 17.7 & 9.7 & 11.5 \\
21.5 & 20.5 & 11.5 & 13
\end{bmatrix}
$$

### Passo 3: Cálculo dos Autovalores e Autovetores

Após calcular os autovalores e autovetores da matriz de covariância, obtemos:

- **Autovalores**: \( $\lambda_1$ = 96.7, $\lambda_2$ = 1.2, $\lambda_3$ = 0.4, $\lambda_4$ = 0.1 \)
- **Autovetores**:

$$
v_1 = \begin{bmatrix} 0.6 \\ 0.6 \\ 0.3 \\ 0.4 \end{bmatrix}, \quad v_2 = \begin{bmatrix} -0.7 \\ 0.7 \\ 0 \\ 0.1 \end{bmatrix}
$$

### Passo 4: Seleção dos Principais Componentes

Selecionamos os dois maiores autovalores e seus autovetores correspondentes. Neste caso, temos \( v_1 \) e \( v_2 \).

### Passo 5: Projeção dos Dados

Finalmente, projetamos os dados originais no espaço reduzido usando os autovetores selecionados:

$$
X_{reduzido} = X_{centralizado} \cdot \begin{bmatrix}
v_1 & v_2
\end{bmatrix}
$$

Vamos calcular a projeção:

$$
X_{reduzido} = \begin{bmatrix}
-7.2 & -7.2 & -3.4 & -4 \\
-3.2 & -3.2 & -2.4 & -2 \\
-2.2 & -1.2 & -1.4 & -1 \\
3.8 & 2.8 & 2.6 & 2 \\
8.8 & 8.8 & 4.6 & 5
\end{bmatrix} \cdot \begin{bmatrix}
0.6 & -0.7 \\
0.6 & 0.7 \\
0.3 & 0 \\
0.4 & 0.1
\end{bmatrix}
$$

O resultado da projeção será um conjunto de dados em 2 dimensões:

$$
X_{reduzido} = \begin{bmatrix}
-10.08 & 0.0 \\
-5.12 & -1.68 \\
-2.72 & -1.44 \\
6.32 & 0.96 \\
11.6 & 2.16
\end{bmatrix}
$$

### Resultados Finais

Os dados em 2 dimensões são:

| Amostra | Dimensão 1 | Dimensão 2 |
|---------|------------|------------|
| 1       | -10.08     | 0.0        |
| 2       | -5.12      | -1.68      |
| 3       | -2.72      | -1.44      |
| 4       | 6.32       | 0.96       |
| 5       | 11.6       | 2.16       |

## Conclusão

Esse processo de PCA reduz a dimensionalidade dos dados de 4 para 2 dimensões, facilitando a visualização de clusters gerados por algoritmos como K-means. A visualização é crucial para entender como os dados estão agrupados e se os clusters são significativos.
