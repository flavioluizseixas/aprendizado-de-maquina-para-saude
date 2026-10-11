# Atividade 8 — Previsão semanal de casos de dengue

## Séries temporais com RNN | Versão mínima

**Enunciado:** uma equipe de estudo quer investigar se os casos das semanas anteriores ajudam a prever os casos da semana seguinte em Niterói. Sua dupla deverá organizar a série em ordem temporal, construir sequências de quatro semanas e comparar uma rede neural recorrente (SimpleRNN) com duas regras simples: repetir a última semana e calcular a média das quatro semanas anteriores. Ao final, apresente evidências sobre o desempenho e explique os limites dessa comparação. O cenário é educacional; não representa uma ferramenta de decisão de saúde pública.

**Pergunta orientadora:** usar informações das semanas anteriores melhora a previsão de uma semana em relação a repetir o último valor?

**Objetivos:** reconhecer uma série temporal; interpretar sequências, defasagens e médias móveis; retomar a RNN apresentada em aula; evitar informação futura nas entradas e na normalização; separar treino, validação e teste cronologicamente; calcular e interpretar erros de previsão.

**Organização:** duplas, 45–60 minutos. Pré-requisitos: noções de DataFrame, gráficos, média, treino/teste e redes recorrentes. A preparação de download já está pronta; concentre-se no raciocínio temporal e na interpretação. Prepare o ambiente com TensorFlow antes da aula; a instalação não está incluída nesse tempo.

## Material e dados

Use [08_series_temporais_versão_minima.ipynb](../notebooks/08_series_temporais_vers%C3%A3o_minima.ipynb), com seis células de código, no Colab ou Jupyter. Execute em ordem. O primeiro download requer internet; as próximas execuções podem usar o cache. O notebook funciona sem clonar o repositório e informa bibliotecas, fonte, período e registro de acesso.

São necessários pandas, numpy, matplotlib, requests, scikit-learn e TensorFlow (Keras). A instalação está indicada no notebook. Pode executar em CPU, sem GPU.

Fonte: [API pública do InfoDengue](https://info.dengue.mat.br/tutorial_api_python/locale-en). Município: Niterói (RJ), código IBGE 3303302. Consulta: semanas epidemiológicas de 2016–2025; registre o período efetivamente retornado. Consulte os termos de uso e as orientações de citação da fonte.

- Cada linha corresponde a uma semana epidemiológica; data_iniSE indica seu domingo inicial.
- O alvo casos_est é a estimativa de casos semanais por nowcasting, que considera atrasos de notificação; os valores podem ser revistos.
- As últimas 52 semanas do calendário retornado são reservadas ao teste; as 52 anteriores são validação; as anteriores a ambas formam o treino. Esses intervalos não necessariamente coincidem com anos civis.
- Semanas ausentes não viram zero. Linhas sem alvo ou atributos completos são excluídas e contabilizadas. O teste pode ter menos de 52 linhas utilizáveis.
- A entrada da RNN é [lag_4, lag_3, lag_2, lag_1], do mais antigo ao mais recente. O formato é (amostras, 4 passos de tempo, 1 variável). A média media_4 serve apenas como referência de comparação.
- A rede usa SimpleRNN(16), ativação tanh e estado reiniciado entre janelas, seguida de Dense(1) com saída linear. São 305 parâmetros treináveis. Ela aprende uma correção: **previsão = última semana + correção da RNN**. A saída começa com pesos e viés zero, portanto a previsão inicial coincide com repetir a última semana. Uma correção pode aumentar ou diminuir a previsão.
- A rede treina por até 200 épocas, lotes de 16, Adam (taxa 0,001), perda MSE, sem embaralhar e semente 42. EarlyStopping monitora a perda de validação, espera 20 épocas sem melhora e restaura os melhores pesos. O teste não escolhe a época. Atingir o limite de 200 épocas não demonstra convergência. Não há retreinamento após selecionar a época.
- MinMaxScaler aprende a escala somente com valores anteriores à validação. O alvo da rede é a diferença entre alvo normalizado e última semana normalizada. Somamos a correção prevista à última semana normalizada, desfazemos a escala e limitamos previsões negativas a zero antes das métricas. Validação e teste não reajustam a escala, mesmo com valores fora de [0, 1]. A perda de treino está na escala normalizada; MAE e RMSE finais estão em casos por semana.

**Horizonte de avaliação:** uma semana por vez. Após cada semana, seu valor observado pode compor os atributos da próxima. Os pesos são ajustados apenas no treino; a validação seleciona a época e o teste avalia o modelo fixado. Como usamos dados históricos obtidos hoje, sujeitos a revisões, essa avaliação retrospectiva não reproduz exatamente a informação disponível na época.

## Roteiro para a aula

**Abertura — 5 minutos:** leia o cenário, discuta a pergunta orientadora e faça os cálculos do exemplo de defasagens antes de executar o código.

**Exploração — 10 minutos:** execute as células 1 e 2; confira a fonte, o período, as ausências e o comportamento do gráfico anterior ao teste.

**Construção e treino — 10–15 minutos:** execute as células 3 e 4; interprete uma sequência, a forma (n, 4, 1), a normalização e as datas de treino, validação e teste. Observe o resumo da rede, as curvas de perda, a melhor época e a tabela de validação. A rede prevê uma correção; explique como ela se converte em casos.

**Avaliação — 10–15 minutos:** execute as células 5 e 6; compare os erros e investigue uma semana com erro grande.

**Discussão e entrega — 10–15 minutos:** responda às questões e escreva a conclusão. Uma dupla apresenta um resultado e outra aponta uma limitação da interpretação.

## Perguntas

### 1. Entender os dados

O que representa cada linha? Informe município, alvo, período efetivamente retornado e número de semanas/valores ausentes. No gráfico anterior ao teste, descreva um pico ou uma mudança ao longo do tempo. É possível afirmar apenas com esse gráfico que existe uma sazonalidade anual estável? Justifique.

### 2. Construir a sequência para a RNN

Nas quatro semanas anteriores ocorreram 10, 20, 30 e 40 casos, nessa ordem. Escreva a sequência que a RNN recebe, antes da normalização, e calcule lag_1, lag_2, lag_3, lag_4, media_4 e a previsão de repetir a última semana. O alvo dessa nova semana ainda é desconhecido. Escolha uma linha da tabela real e indique as quatro datas de entrada em ordem. O que significa (n, 4, 1)? Por que quatro passos com uma variável diferem de um passo com quatro variáveis? Como o estado recorrente participa da previsão?

### 3. Evitar informação indisponível

Explique por que usamos shift(1).rolling(4).mean() na referência de média móvel. O que aconteceria se usássemos rolling(4).mean() diretamente para prever o alvo da mesma linha? Qual é a diferença entre a média descritiva do gráfico e a média usada na previsão? Por que o normalizador deve aprender apenas com o treino, sem incluir a validação? Por que desfazemos a normalização antes de calcular MAE e RMSE?

### 4. Preservar a ordem temporal

Informe quantidades e datas de treino, validação e teste após a exclusão de linhas incompletas. Registre as épocas executadas e a melhor época. Como EarlyStopping usa a validação? Por que não pode usar o teste? Se a correção da RNN for zero, qual é a previsão? Por que sortear aleatoriamente as semanas não representa a previsão de semanas posteriores? Por que o valor de uma semana anterior do teste pode entrar como lag para prever a seguinte? Isso seria compatível com prever todas as 52 semanas de uma só vez no início do teste?

### 5. Calcular um erro de previsão

Considere valores reais 20, 30 e 40 e previsões 18, 35 e 39. Calcule os erros absolutos e o MAE. Explique sua unidade. Por que o RMSE é mais afetado por um erro muito grande?

### 6. Comparar os métodos

Registre MAE e RMSE dos três métodos: última semana, média de quatro semanas e RNN. Qual teve menor MAE? A RNN melhorou as duas referências? Interprete a redução percentual exibida, inclusive se for negativa. Uma diferença pequena neste teste demonstra superioridade em outros períodos? Não há exigência de que a RNN vença as referências.

### 7. Investigar um erro grande

Escolha uma das três semanas da tabela de maiores erros da RNN. Registre data, observado, previsão, resíduo e erro absoluto. O modelo subestimou ou superestimou os casos? Relacione o resultado ao gráfico. O erro ocorreu durante uma subida, uma descida ou um pico? Descreva a associação observada sem atribuir uma causa epidemiológica.

### 8. Concluir com responsabilidade

Em 5–8 linhas, responda à pergunta orientadora com base nos resultados e apresente pelo menos duas limitações. Considere atrasos e revisões das notificações, semanas excluídas, mudanças de padrão, avaliação em um único período e ausência de intervalos de previsão. Se você modificou o modelo após observar o teste, explique por que essa comparação passou a ser exploratória e exige outro período para confirmação. Uma boa previsão demonstra causalidade? Essa análise basta para orientar ações de saúde pública?

## Entrega e avaliação

Entregue um único arquivo .ipynb com identificação da dupla, as seis células executadas, saídas e respostas em Markdown. Registre a fonte e preserve a tabela dos três métodos. Antes de entregar, reinicie o ambiente e execute tudo em ordem.

- Dados e leitura do gráfico: 2 pontos.
- Sequências da RNN, normalização e prevenção de informação futura: 2 pontos.
- Divisão temporal e entendimento do horizonte: 2 pontos.
- Cálculo, comparação dos erros e análise de uma semana: 2 pontos.
- Conclusão fundamentada, limites e execução reproduzível: 2 pontos.

O critério central é explicar as escolhas e interpretar os resultados. A nota não depende de obter um MAE baixo ou de a RNN superar os métodos simples.

## Desafio opcional — mais 10 minutos

Antes de executar a célula 5, preserve os resultados de validação da rede de 16 unidades. Em uma cópia, substitua SimpleRNN(16, ...) por SimpleRNN(8, ...) e execute apenas a célula 4. Compare o número de parâmetros, a melhor época e o MAE de validação. Escolha pela validação, execute novamente a célula 4 com essa configuração e só então as células 5–6.

Se já tiver observado o teste, a comparação é exploratória. Não escolha uma configuração para fazer a RNN vencer no teste: reserve outro período para confirmação independente. Uma redução do erro de treino não garante menor erro em semanas posteriores.

Material com finalidade exclusivamente educacional. Os resultados não devem orientar diagnósticos ou decisões de saúde pública. Previsão e associação temporal não demonstram causalidade.

## Referências de apoio

- [InfoDengue — API, dicionário e acesso](https://info.dengue.mat.br/tutorial_api_python/locale-en)
- [Keras — SimpleRNN](https://keras.io/api/layers/recurrent_layers/simple_rnn/)
- [TensorFlow — previsão de séries temporais](https://www.tensorflow.org/tutorials/structured_data/time_series)
- [scikit-learn — MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)
- [scikit-learn — lags e avaliação temporal](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html)

- [Keras — EarlyStopping](https://keras.io/api/callbacks/early_stopping/)
