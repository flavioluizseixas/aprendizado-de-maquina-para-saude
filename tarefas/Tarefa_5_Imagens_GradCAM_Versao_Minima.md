# Atividade 5 — Classificação de imagens e Grad-CAM

## CNN pequena | Versão mínima

**Objetivo:** treinar uma rede convolucional simples, avaliar os erros de classificação e interpretar mapas Grad-CAM, distinguindo saída do modelo, explicação visual e evidência clínica.

**Tempo estimado:** 50–60 minutos, incluindo discussão; o tempo de treinamento varia conforme o hardware.

## Material e dados

Use o notebook [05_imagens_gradcam_versão_minima.ipynb](../notebooks/05_imagens_gradcam_vers%C3%A3o_minima.ipynb), com sete células de código. Execute em ordem no Colab ou Jupyter. O notebook informa as dependências e registra suas versões. A primeira execução requer internet; não é necessário clonar o repositório nem enviar arquivos. CPU é suficiente; GPU é opcional.

Fonte: [PneumoniaMNIST — MedMNIST](https://medmnist.com/), com radiografias pediátricas derivadas de Kermany et al., disponibilizado sob CC BY 4.0. Consulte também os [metadados oficiais](https://github.com/MedMNIST/MedMNIST/blob/main/medmnist/info.py).

- Imagens em tons de cinza, reduzidas para 64 × 64 pixels, com valores divididos por 255.
- Rótulos: 0 = normal; 1 = pneumonia, a classe positiva.
- Divisões oficiais: 4.708 imagens de treino, 524 de validação e 624 de teste. Não faça uma nova divisão.
- CNN com duas convoluções, até 30 épocas, batch size 64 e semente 42. Adam começa com taxa de aprendizado 0,001. Early stopping acompanha a AUC de validação, com paciência 5, e restaura os melhores pesos. Após duas épocas sem melhora suficiente da AUC de validação, ReduceLROnPlateau reduz a taxa pela metade, até o mínimo de 0,00001.
- Limiar previamente fixado em 0,5; Grad-CAM calculado para o escore de pneumonia antes da sigmoide, em todos os exemplos.

## Roteiro e questões

### 1. Dados e divisões

Execute as células 1 e 2. Apresente a quantidade de cada classe e o percentual de pneumonia no treino, na validação e no teste. Explique a função de cada divisão, o significado do canal único e a transformação dos pixels para o intervalo de 0 a 1. Por que a classe mais frequente pode tornar a acurácia insuficiente?

### 2. Modelo e treinamento

Execute as células 3 e 4. Explique, em linguagem própria, o papel das convoluções, do pooling e da sigmoide. Registre quantas épocas foram executadas, qual teve a maior AUC de validação e se houve redução da taxa de aprendizado. Compare a AUC de validação na quinta época com a melhor observada, se houver ao menos cinco épocas. Analise as curvas de erro e AUC: há sinais de diferença entre treino e validação? A melhor época coincidir com a última sugere que o limite pode ter sido atingido antes da estabilização, mas aumentar o limite não garante melhora nem ausência de sobreajuste. O teste não pode orientar a escolha da época, do modelo ou do limiar.

O treinamento pode terminar antes de 30 épocas por parada antecipada. A 11 segundos por época, o limite representa aproximadamente 5–6 minutos. Para começar do zero, execute a célula 3 antes da 4; repetir apenas a célula 4 continua a partir dos pesos atuais.

### 3. Desempenho no teste

Execute a célula 5 e registre verdadeiros negativos (VN), falsos positivos (FP), falsos negativos (FN) e verdadeiros positivos (VP). As linhas da matriz são os rótulos reais e as colunas, os previstos.

Apresente acurácia, sensibilidade, especificidade, precisão e F1 da classe pneumonia e ROC-AUC. No relatório, sensibilidade é recall de pneumonia e especificidade é recall de normal. Confira sensibilidade = VP/(VP+FN) e especificidade = VN/(VN+FP). Se não houver previsão positiva, informe que a precisão é indefinida; o código exibe zero por convenção.

Compare a acurácia da CNN com a regra de sempre prever a classe majoritária do treino. Qual tipo de erro é mais frequente? Por que ROC-AUC e acurácia não medem a mesma coisa? Não é necessário obter desempenho alto para concluir a atividade: um modelo limitado também deve ser analisado.

### 4. Grad-CAM em acertos e erros

Execute as células 6 e 7. Escolha um acerto e um erro entre os exemplos disponíveis e informe seus índices, rótulos reais, rótulos previstos e saídas P(pneumonia). Se faltar alguma categoria de erro ou acerto, registre a ausência e discuta os casos disponíveis, sem inventar exemplos.

Compare a distribuição espacial dos mapas e observe regiões difusas, bordas e possíveis artefatos. Todos os mapas explicam o escore de pneumonia, mesmo quando a previsão é normal. Eles não representam contornos de lesões. Um mapa nulo indica ausência de contribuição positiva no cálculo e não comprova ausência de doença. A escala é normalizada separadamente por imagem; a intensidade de cor não mede confiança entre casos.

### 5. Comparação de casos próximos do limiar

Preserve as saídas anteriores. Duplique somente a célula 7 e insira, na cópia, a linha **selecionados = proximos** imediatamente antes de **for i in selecionados:**. Execute a cópia para visualizar os dois índices mais próximos de 0,5, já informados pelo código. Não retreine o modelo nem altere o limiar.

Registre os índices, as probabilidades e suas distâncias até 0,5; ser o mais próximo não implica estar perto do limiar em termos absolutos. Compare os mapas e explique por que uma saída próxima de 0,5 e uma região colorida respondem a perguntas diferentes. A saída da sigmoide não foi calibrada como probabilidade clínica.

## Entrega e critérios

Entregue um único arquivo .ipynb com identificação dos participantes, as sete células executadas, suas saídas, a célula adicional de comparação e respostas em Markdown. Preserve o registro das versões e cite a fonte dos dados. Antes de entregar, reinicie o ambiente e execute tudo em ordem.

Conclua em 5–8 linhas com um achado e pelo menos duas limitações, considerando população pediátrica, resolução reduzida, diferenças entre instituições e limites da explicação visual. As imagens e os rótulos deste exercício não fornecem máscaras de lesão para validar a localização indicada pelo mapa.

A avaliação considera execução reproduzível, preservação das divisões oficiais, interpretação correta de métricas e erros, comparação dos exemplos e discussão dos limites do Grad-CAM. Não há exigência de desempenho mínimo nem de um mapa com aparência específica.

Material com finalidade exclusivamente educacional. Os resultados não devem orientar diagnósticos ou decisões clínicas. Grad-CAM não comprova causalidade, localização de doença ou validade clínica do modelo.

## Referências de apoio

- [MedMNIST v2 — Scientific Data](https://www.nature.com/articles/s41597-022-01721-8)
- [Grad-CAM — Selvaraju et al., ICCV 2017](https://openaccess.thecvf.com/content_ICCV_2017/html/Selvaraju_Grad-CAM_Visual_Explanations_ICCV_2017_paper.html)
- [Exemplo oficial de Grad-CAM — Keras](https://keras.io/examples/vision/grad_cam/)
- [EarlyStopping — Keras](https://keras.io/api/callbacks/early_stopping/)
- [ReduceLROnPlateau — Keras](https://keras.io/api/callbacks/reduce_lr_on_plateau/)
