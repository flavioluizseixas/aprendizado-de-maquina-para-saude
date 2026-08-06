# Cálculo de Autovalores e Autovetores

O cálculo de **autovalores** e **autovetores** é uma parte fundamental do **PCA** e de muitas outras técnicas em álgebra linear. Aqui está uma explicação passo a passo do cálculo:

## 1. Definição de Autovalores e Autovetores

Para uma matriz quadrada \( A \), um vetor \( v \) é chamado de **autovetor** de \( A \) se ele satisfaz a seguinte equação:

$$
A v = \lambda v
$$

Onde:
- \( A \) é uma matriz quadrada (por exemplo, a matriz de covariância no PCA).
- \( v \) é o **autovetor**, um vetor não nulo.
- \( \lambda \) é o **autovalor** associado ao autovetor \( v \).

Isso significa que, quando a matriz \( A \) atua sobre o vetor \( v \), o resultado é simplesmente o vetor \( v \) escalado por um valor \( \lambda \).

## 2. Como calcular os Autovalores $ (\lambda) $

Os autovalores de uma matriz \( A \) são encontrados resolvendo o **polinômio característico**, que é dado pela seguinte equação:

$$
\det(A - \lambda I) = 0
$$

Onde:
- \( \det \) é o **determinante** da matriz.
- \( I \) é a **matriz identidade** do mesmo tamanho que \( A \).
- \( \lambda \) são os autovalores.

### Etapas para calcular os autovalores:

1. **Subtração de $ \lambda I $ de \( A \)**:
   $$
   A - \lambda I
   $$
   Isso resulta em uma nova matriz.

2. **Determinante**: Calcule o determinante da matriz \( A - \lambda I \). Isso resulta em um polinômio em \( \lambda \).

3. **Resolver o polinômio**: Resolva o polinômio característico \( \det(A - \lambda I) = 0 \) para encontrar os valores de \( \lambda \), que são os **autovalores**.

### Exemplo:

Considere uma matriz simples \( A \) de \( 2 \times 2 \):

$$
A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}
$$

O polinômio característico será:

$$
\det(A - \lambda I) = \det \begin{bmatrix} 4 - \lambda & 1 \\ 2 & 3 - \lambda \end{bmatrix} = 0
$$

O determinante de uma matriz \( 2 $\times$ 2 \) é calculado como:

$$
(4 - \lambda)(3 - \lambda) - (2)(1) = 0
$$

Expandindo a equação:

$$
(4 - \lambda)(3 - \lambda) - 2 = 0
$$

$$
12 - 7\lambda + \lambda^2 - 2 = 0
$$

$$
\lambda^2 - 7\lambda + 10 = 0
$$

Agora resolvemos essa equação quadrática para \( \lambda \). Usando a fórmula quadrática:

$$
\lambda = \frac{-(-7) \pm \sqrt{(-7)^2 - 4(1)(10)}}{2(1)}
$$

$$
\lambda = \frac{7 \pm \sqrt{49 - 40}}{2} = \frac{7 \pm \sqrt{9}}{2}
$$

$$
\lambda_1 = 5, \quad \lambda_2 = 2
$$

Os autovalores de \( A \) são \( 5 \) e \( 2 \).

## 3. Como calcular os Autovetores

Depois de encontrar os autovalores, podemos calcular os autovetores correspondentes para cada \( \lambda \).

### Etapas para calcular os autovetores:

1. Para cada autovalor \( \lambda \), substituímos o valor na equação \( A v = \lambda v \), ou seja, resolvemos o sistema:

$$
(A - \lambda I) v = 0
$$

2. Esse sistema de equações geralmente resulta em um sistema homogêneo linear. Encontramos os **autovetores** resolvendo para \( v \) (normalmente por métodos algébricos como eliminação de Gauss).

### Exemplo de autovetor:

Para o autovalor \( \lambda_1 = 5 \), vamos resolver \( (A - 5I)v = 0 \).

$$
A - 5I = \begin{bmatrix} 4 - 5 & 1 \\ 2 & 3 - 5 \end{bmatrix} = \begin{bmatrix} -1 & 1 \\ 2 & -2 \end{bmatrix}
$$

Agora resolvemos o sistema:

$$
\begin{bmatrix} -1 & 1 \\ 2 & -2 \end{bmatrix} \begin{bmatrix} v_1 \\ v_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
$$

Isso nos dá a equação:

$$
-1v_1 + v_2 = 0 \quad \text{ou} \quad v_1 = v_2
$$

Então, um autovetor correspondente a \( \lambda_1 = 5 \) é:

$$
v = \begin{bmatrix} 1 \\ 1 \end{bmatrix}
$$

Para o autovalor \( \lambda_2 = 2 \), o sistema é:

$$
A - 2I = \begin{bmatrix} 4 - 2 & 1 \\ 2 & 3 - 2 \end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 2 & 1 \end{bmatrix}
$$

Resolvendo o sistema:

$$
2v_1 + v_2 = 0 \quad \text{ou} \quad v_2 = -2v_1
$$

Então, um autovetor correspondente a \( \lambda_2 = 2 \) é:

$$
v = \begin{bmatrix} 1 \\ -2 \end{bmatrix}
$$

## Resumo

1. Para encontrar os **autovalores**, resolvemos o polinômio característico \( \det(A - \lambda I) = 0 \).
2. Para encontrar os **autovetores**, resolvemos o sistema \( (A - \lambda I)v = 0 \) para cada autovalor \( \lambda \).

Esses passos são usados em muitas aplicações, como o **PCA**, para encontrar as direções de maior variância nos dados.
