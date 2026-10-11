# Atividade 8 — Orientações para o professor

Use com o [enunciado](Tarefa_8_Series_Temporais_Versao_Minima.md) e o [notebook mínimo](../notebooks/08_series_temporais_vers%C3%A3o_minima.ipynb). As questões abertas dependem da versão dos dados retornada pela API; não fixe antecipadamente um método vencedor ou valores das métricas.

## Condução sugerida

Peça que cada dupla calcule as defasagens e o MAE à mão antes de executar as células correspondentes. Distribua os papéis: uma pessoa executa e a outra explica de onde vem cada atributo; troquem os papéis na avaliação. Na discussão, convide duplas a justificar o resultado com números e a apontar uma limitação.

Se a rede estiver indisponível, um arquivo real já baixado pelo notebook pode ser colocado no mesmo caminho de cache dos computadores. Mantenha a fonte e a data de obtenção. Sem acesso ou cache, resolva os dois exemplos manuais e a discussão conceitual, deixando explícito que a parte prática com dados reais está pendente. Não substitua silenciosamente a base por dados simulados.

## Respostas e pontos de atenção

**1. Dados:** cada linha é uma semana, não uma pessoa. O alvo é uma estimativa semanal, não uma contagem definitiva. Confira município, período e ausências impressos. Um pico isolado não demonstra sazonalidade anual; padrões visuais sugerem hipóteses, cuja estabilidade requer investigação adicional.

**2. Sequência e RNN:** entrada antes da normalização = [10, 20, 30, 40]; lag_1 = 40; lag_2 = 30; lag_3 = 20; lag_4 = 10; media_4 = 25; repetir a última semana prevê 40. Para uma data t, a sequência usa t−28, t−21, t−14 e t−7 dias, nessa ordem. A forma (n, 4, 1) representa n exemplos, quatro passos e uma variável por passo. Em (n, 1, 4), haveria apenas um passo, sem a recorrência ao longo das quatro semanas. A SimpleRNN atualiza seu estado ao percorrer a janela; Dense(1) converte o último estado em uma correção sobre a última semana. A saída é inicializada com zeros: antes do treino, a rede reproduz exatamente a referência de persistência. O alvo de treinamento é alvo normalizado menos última semana normalizada; a previsão soma essa correção e desfaz a escala. Isso difere do resíduo de avaliação, observado menos previsto. O estado não é carregado de uma janela para outra. O alvo da nova semana não participa da entrada.

**3. Deslocamento:** shift(1) faz a janela terminar em t−1. Sem deslocamento, a média inclui o próprio alvo em t, indisponível no momento da previsão, causando vazamento de informação. Incluir a semana corrente é aceitável na curva descritiva histórica, cuja finalidade é resumir valores já observados.

A normalização também precisa respeitar o corte: aprender mínimo e máximo com o teste incorpora informação futura ao preparo do modelo. A escala é ajustada nos valores observados anteriores à validação e reaplicada sem ajuste; valores futuros podem sair de [0, 1]. A transformação inversa devolve a previsão à unidade de casos antes das métricas. A perda MSE impressa durante o treino está na escala normalizada. Previsões negativas são limitadas a zero por uma regra definida previamente.

**4. Divisão:** treino antecede validação, que antecede teste. Os pesos são ajustados no treino; a validação escolhe a época via EarlyStopping; o teste avalia a configuração fixada. Registre o número real de épocas e a época restaurada. A rede começa com a semente 42. A parada tem paciência 20 e limite 200; atingir o limite não prova convergência. As perdas de treino e validação estão na mesma escala, mas descrevem períodos diferentes. Não há retreinamento posterior. Um sorteio mistura o passado e o futuro e altera o problema avaliado. No horizonte de um passo, o valor observado em uma semana já encerrada pode ajudar a prever a próxima. Para prever todo o período no início, esses valores futuros ainda seriam desconhecidos; seria necessário um procedimento diferente. O uso retrospectivo de valores revisados também impede afirmar que se reproduziu o desempenho operacional da época.

**5. MAE:** erros absolutos = 2, 5 e 1; MAE = 8/3 ≈ 2,67 casos por semana. Para apoio, RMSE = raiz de ((4 + 25 + 1)/3) = raiz de 10 ≈ 3,16 casos por semana. O quadrado atribui maior peso a erros grandes antes de calcular a média.

**6. Comparação:** use os valores efetivamente exibidos. Redução do MAE = 100 × (MAE da última semana − MAE da RNN)/MAE da última semana. Positiva indica redução, negativa indica piora e zero indica empate; com baseline de MAE zero, a porcentagem é indefinida. Uma RNN pode perder para uma regra simples. A janela de quatro semanas não testa memória de longo alcance. Uma única semente e um único período não demonstram superioridade geral do modelo. Este teste não quantifica a incerteza da diferença nem demonstra desempenho futuro. Se MAE e RMSE indicarem preferências diferentes, discuta como erros grandes afetam o RMSE.

**7. Resíduos:** observado − previsto > 0 significa subestimação; < 0 significa superestimação. Confira se a conclusão da dupla combina com os números e o gráfico. Picos e mudanças rápidas podem estar associados a erros, mas este exercício não identifica suas causas. Um valor ausente excluído também não equivale a uma semana de zero casos.

**8. Conclusão:** deve citar um resultado concreto, responder à pergunta orientadora no período analisado e reconhecer duas limitações pertinentes. Prever não prova causalidade. Não se espera uma recomendação operacional de saúde pública.

## Escopo da simplificação

O roteiro retoma a RNN apresentada em aula: uma sequência de quatro semanas, SimpleRNN(16), Dense(1) inicializada com zeros, até 200 épocas, lotes de 16, Adam com taxa 0,001 e semente 42. São 305 parâmetros treináveis. A RNN aprende uma correção sobre a última observação; ela não recebe o valor da semana que prevê. A janela curta não representa diretamente uma sazonalidade anual. A validação ocupa as 52 semanas anteriores às 52 de teste. A normalização usa somente semanas de treino.

A parada antecipada e a previsão de correções são tentativas de melhorar generalização; não garantem vitória sobre as referências. Um teste já consultado não volta a ser independente ao mudar a configuração. Se a revisão foi motivada pelo resultado do teste, apresente os novos resultados como exploração e use outro período para confirmação. Prepare TensorFlow antes da aula; CPU é suficiente. Versões e hardware podem alterar resultados apesar da semente.

O notebook completo oferece outra abordagem com atributos tabulares e HistGradientBoostingRegressor, além de sazonalidade, autocorrelação e TimeSeriesSplit. Na versão mínima, a comparação final avalia a RNN previamente definida; não é necessário que ela vença as referências.

No desafio opcional, substitua SimpleRNN(16, ...) por SimpleRNN(8, ...). SimpleRNN(8) mais Dense(1) tem 89 parâmetros treináveis. Execute apenas a célula 4 para comparar pela validação, antes de abrir o teste. Após escolher, reexecute a célula 4 com a configuração escolhida e prossiga às células 5–6. Se o teste já foi visto, a análise é exploratória e requer outro período para confirmação. Não atribua pontos pela melhora numérica isolada.
