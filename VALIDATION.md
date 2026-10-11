# Registro de validação

## 10 de outubro de 2026 — comparação SimpleRNN e GRU na atividade 8

- Preservada a SimpleRNN revisada e acrescentada GRU(16, reset_after=True), ambas seguidas de Dense(1) inicialmente zerada para prever correções sobre a última semana. Mesmas sequências de quatro semanas, escala, alvo, divisões 414/52/52, semente 42 reiniciada por rede, Adam 0,001, lotes 16, MSE, limite 200 épocas e EarlyStopping com paciência 20 e restauração dos melhores pesos. Modelos, otimizadores e callbacks independentes. Nenhum ajuste após observar o resultado da GRU no teste.
- Executadas as seis células em CPU com TensorFlow 2.21.0. SimpleRNN: 305 parâmetros, 200 épocas executadas, melhor época 200, MAE de validação 15,3387. GRU: 929 parâmetros, 200 épocas executadas, melhor época 181, MAE de validação 14,9855. Ambas atingiram o limite; não se infere convergência. A GRU restaurou os pesos da época 181.
- Teste: última semana MAE 3,9231 / RMSE 5,0763; média móvel MAE 3,3029 / RMSE 4,7021; SimpleRNN MAE 3,8765 / RMSE 5,1102; GRU MAE 4,0041 / RMSE 5,1518. Confirmado numericamente que a SimpleRNN preserva o desempenho anterior. A pequena vantagem da GRU na validação não se repetiu no teste. A média móvel continua melhor neste período. A comparação permanece exploratória por usar um teste já consultado.
- Conferidos modelos e otimizadores distintos, parâmetros, formas das entradas e saídas, ausência de valores não finitos, normalização restrita ao treino, reconstrução da correção, perdas dos pesos restaurados iguais às melhores perdas de validação, quatro linhas de métricas, resíduos e três maiores erros de cada rede. Inspecionado o gráfico conjunto. Igual número de unidades não iguala capacidade; o material explicita essa diferença e o fato de GRU também ser uma RNN.
- Notebook, gerador, README, enunciados Markdown/Word e orientações atualizados, preservando seis células. Geração reproduzível, conteúdo do DOCX, estrutura dos 14 notebooks e `git diff --check` aprovados. Sem saídas versionadas, renderização no Word ou nova validação pela interface do Colab.

## 10 de outubro de 2026 — revisão da RNN por validação temporal

- O TensorFlow 2.21.0 passou a importar no ambiente local. Reproduzida integralmente a versão anterior, em CPU, com o mesmo cache real e semente 42: RNN com MAE 4,9811 e RMSE 6,2049; última semana com 3,9231 e 5,0763; média móvel com 3,3029 e 4,7021. Os valores reproduzem a captura apresentada pelo usuário.
- Antes de reavaliar o teste, comparadas quatro variantes na validação: previsão direta com escala original (MAE 17,2797), direta com log1p (26,0149), correção da última semana com escala original (15,3387), correção com log1p (18,1171). Todas usaram SimpleRNN(16), Adam 0,001, semente 42, lotes 16, limite 200 épocas, EarlyStopping por val_loss com paciência 20 e restauração dos melhores pesos. A escala foi aprendida somente antes da validação. Não houve ajuste de arquitetura ou hiperparâmetros após observar o novo teste.
- Escolhida pela validação a previsão de correções, com saída Dense(1) inicialmente zerada. Divisão final: 414 janelas de treino (2016-01-31 a 2023-12-31), 52 de validação (2024-01-07 a 2024-12-29), 52 de teste (2025-01-05 a 2025-12-28). Sem retreinamento posterior. A melhor época foi 200; o limite foi atingido, portanto não houve parada antecipada nesta execução nem comprovação de convergência.
- No teste, a nova RNN obteve MAE **3,8765** e RMSE **5,1102**: melhora frente à versão anterior, mas a média móvel permanece melhor nas duas métricas. A comparação antes/depois envolve tanto a forma de previsão quanto o procedimento de treino; não isola o efeito de uma única mudança. Como a revisão foi motivada pelo teste já consultado, esses resultados são exploratórios, não uma confirmação independente de generalização.
- Executadas integralmente as seis células da versão anterior e da revisada. Conferidos formato das sequências, 305 parâmetros, previsões finitas e não negativas, escala restrita ao treino, reconstrução do alvo a partir da correção e perda dos pesos restaurados igual à melhor val_loss. Inspecionado o gráfico de previsões e resíduos. Enunciados e orientações atualizados para ensinar validação temporal, correções e seleção de épocas; desafio de oito unidades compara pela validação antes do teste.
- Validador do repositório: 14 notebooks aprovados; 3 testes de séries temporais aprovados. Geração reproduzível, conteúdo atualizado do DOCX e `git diff --check` conferidos. Notebook sem saídas versionadas. Sem nova validação pela interface do Colab nem renderização do Word.

## 10 de outubro de 2026 — atividade 8 mínima com RNN

- Substituída a árvore por SimpleRNN(16) e Dense(1), com sequências das quatro semanas anteriores em ordem cronológica, escala aprendida somente antes do teste, 50 épocas fixas e comparação com última semana e média móvel. Atualizados gerador, notebook, enunciados Markdown/Word, orientações do professor, README e dependência TensorFlow do extra `time-series`.
- Conferido o preparo com o cache real de Niterói: 522 semanas, sem ausências; 466 sequências de treino e 52 de teste. Verificados formato `(n, 4, 1)`, correspondência de cada passo com sua data, transformação inversa, divisão cronológica e ajuste da escala. Exemplos pequenos adicionais verificaram exclusão de janelas incompletas e invariância das entradas passadas quando o futuro muda.
- `python scripts/validate_notebooks.py`: 14 notebooks aprovados. `nbformat.validate`, geração reproduzível, conteúdo do DOCX e `git diff --check` aprovados. `python -m pytest tests/test_time_series.py -q -p no:cacheprovider`: 3 testes aprovados. Notebook salvo sem saídas; renderização visual do Word não verificada.
- **Limite da validação:** o import do TensorFlow instalado falhou em `_pywrap_tf2` por bloqueio de DLL pelo Controle de Aplicativo do Windows, inclusive fora do sandbox. Para verificar o preparo, somente esse import foi omitido na execução de conferência, sem alterar o notebook entregue. Treinamento, previsões, métricas finais e desafio de oito unidades ainda não foram executados nesta revisão. Nenhum desempenho da RNN foi presumido; falta executar integralmente em ambiente funcional, como o Colab.

## 3 de outubro de 2026 — treinamento ampliado do experimento 05 mínimo

- Mantidas as sete células, a arquitetura de 4.833 parâmetros, as divisões oficiais, a semente 42 e o limiar 0,5. Limite ampliado de 5 para 30 épocas; Adam com taxa inicial explícita de 0,001; EarlyStopping pela AUC de validação com paciência 5 e restauração dos melhores pesos; ReduceLROnPlateau pela mesma métrica, fator 0,5, paciência 2 e mínimo 0,00001. Notebook, gerador e enunciados Markdown/Word atualizados.
- O ajuste foi conferido primeiro usando apenas treino e validação. Na mesma execução local, a AUC de validação passou de 0,8369 na época 5 para 0,9454 na época 30; a perda de validação caiu de 0,4688 para 0,2661. A taxa foi reduzida ao fim das épocas 24 e 26. O limite de 30 foi atingido, sem parada antecipada; isso não demonstra convergência. A restauração dos pesos foi conferida pela reavaliação da AUC de validação.
- Após fixar a configuração, executadas as sete células e o exercício adicional de Grad-CAM em CPU, com o mesmo ambiente descrito abaixo. No teste: VN=142, FP=92, FN=22 e VP=368; acurácia=0,817, sensibilidade=0,944, especificidade=0,607 e ROC-AUC=0,919. Não houve ajuste posterior pelo teste. Resultados podem variar com hardware e versões.
- Conferidos mapas finitos em [0, 1], dimensões 64 × 64, geração reproduzível do notebook e integridade/conteúdo atualizado do Word. `python scripts/validate_notebooks.py`: 13 notebooks aprovados; `nbformat.validate` e `git diff --check` aprovados. Notebook salvo sem saídas. Execução local, sem nova validação na interface do Colab.

## 3 de outubro de 2026 — experimento 05 e versão mínima

- Reexecutado integralmente `05_imagens_gradcam.ipynb`, com `FAST_MODE=True`, em CPU: treinamento, avaliação e quatro mapas Grad-CAM concluídos. No teste oficial: VN=13, FP=221, FN=17 e VP=373; acurácia=0,619 e ROC-AUC=0,744.
- Criado `05_imagens_gradcam_versão_minima.ipynb`, com sete células de código, sem imports de `src/` ou clonagem do repositório. Usa os 4.708 exemplos de treino, 524 de validação e 624 de teste, com pixels em [0, 1], cinco épocas como limite e early stopping pela AUC de validação. Limiar fixado previamente em 0,5.
- As sete células e a comparação adicional dos dois casos mais próximos de 0,5 foram executadas. Na versão mínima, a melhor época foi a quinta: VN=12, FP=222, FN=9 e VP=381; acurácia=0,630, sensibilidade=0,977, especificidade=0,051, precisão=0,632, F1=0,767 e ROC-AUC=0,799. A referência de sempre prever a classe majoritária do treino teve acurácia=0,625. Esses resultados evidenciam as limitações da CNN curta; não foi feita seleção de modelo ou limiar pelo teste.
- Grad-CAM da versão mínima explica sempre o logit de pneumonia, inclusive em previsões normais. Conferidos formato 64 × 64, valores finitos em [0, 1] e equivalência numérica com o CAM calculado diretamente pelos pesos da camada linear após a média global, com tolerância absoluta de 1e-5. Corrigida a estrutura de entrada do modelo auxiliar para evitar aviso no Keras. Inspecionadas visualmente as curvas e uma figura com imagem, mapa e sobreposição.
- Ambiente: Windows, CPU, Python 3.13.12, TensorFlow 2.21.0, MedMNIST 3.0.2, NumPy 2.4.3, pandas 2.3.3, Matplotlib 3.11.1, scikit-learn 1.9.0 e requests 2.32.5. A execução do TensorFlow precisou ocorrer fora do sandbox devido ao bloqueio de uma DLL pelo controle de aplicativo do Windows. Usado arquivo oficial já em cache, com checksum validado; não foi refeito o download nesta rodada.
- `python -m pytest -q`: 18 testes aprovados; avisos sobre classe ausente em teste específico e permissão para o cache do pytest. `python scripts/validate_notebooks.py`: 13 notebooks aprovados, sem saídas versionadas. Novo notebook também aprovado em `nbformat.validate`; geração reproduzível conferida.
- Enunciado em Markdown e Word com objetivos, cinco etapas, entrega e critérios. Verificados integridade do DOCX, seções, links locais e compatibilidade do gerador anterior da tarefa 3. A renderização das páginas no Word não foi verificada. Regeneração: `python scripts/create_task5_minimal.py` (requer `python-docx`).
- Ainda depende de publicação na branch `main` para validar o botão Colab pela interface. A validação desta rodada foi local; não houve publicação.

## 17 de setembro de 2026 — regressão logística em grupos

- Novo `extra_regressao_logistica_coracao.ipynb`: seis células executadas sequencialmente, com os dados Heart Disease baixados da UCI. Na conferência local, apenas a URL foi substituída pelo caminho do CSV baixado. Ambiente: Python 3.13.12, NumPy 2.4.3, pandas 2.3.3 e scikit-learn 1.9.0.
- Cinco atributos sem ausências; 303 registros, sendo 227 de treino e 76 de teste. Ajuste convergiu sem avisos. Conferidas a separação dos índices e a padronização aprendida exclusivamente no treino.
- Matriz de confusão: VN=32, FP=9, FN=11 e VP=24. Acurácia=0,737, sensibilidade=0,686, especificidade=0,780, precisão=0,727, F1=0,706 e ROC-AUC=0,843. Referência da classe majoritária: acurácia=0,539.
- Verificada equivalência entre os escores/probabilidades do pipeline e sua reconstrução pelos coeficientes e intercepto na escala original. Cada OR foi conferida pela razão das odds calculadas diretamente pelo modelo em dois perfis com o contraste solicitado.
- Conferidos os exercícios: OR para +20 anos igual ao quadrado da OR para +10 anos; com OR de exang aproximadamente 4,126 e p₀=0,20, o exemplo hipotético produz p₁ aproximadamente 0,508.
- Novo notebook aprovado em `nbformat.validate`; 12 notebooks aprovados no validador do repositório. Word verificado quanto à integridade, seções e links locais. Notebook salvo sem saídas; o botão Colab passa a funcionar após publicação na branch `main`.

## 17 de setembro de 2026 — atividade 3 mínima

- `python scripts/validate_notebooks.py`: 11 notebooks aprovados, incluindo a nova versão mínima, sem saídas versionadas; o novo notebook também passou em `nbformat.validate`.
- As seis células da versão mínima foram executadas sequencialmente em Python 3.13.12, com pandas 2.3.3, NumPy 2.4.3, scikit-learn 1.9.0 e Matplotlib 3.11.1. O CSV foi baixado da UCI nesta validação; na execução local, somente a URL de entrada foi substituída pelo caminho do arquivo baixado. As figuras foram salvas para inspeção com backend Agg.
- Na amostra de 5.000 registros e sete atributos, a escolha padrão foi k=2, silhouette de aproximadamente 0,331 e variância acumulada de aproximadamente 50,4% nos dois componentes.
- O exercício sem `Income` também executou todas as células: preservou os mesmos IDs, escolheu k=2 e produziu silhouette de aproximadamente 0,401. A comparação usa outro espaço de atributos e não comprova superioridade da solução.
- Conferidos: exclusão de ID e Diabetes_binary da matriz de entrada, padronização, contagens dos clusters, percentuais e gráficos. Enunciado Word verificado quanto à integridade do arquivo, presença das seções e links; a renderização no Word não foi validada, pois a automação local não concluiu.
- Notebook e Word regeneráveis com `python scripts/create_task3_minimal.py`. O botão Colab depende da publicação do novo arquivo na branch `main`.

## 5 de agosto de 2026

Ambiente equivalente local: Windows, Python 3.13.12, CPU. Os oito notebooks foram executados integralmente em kernels limpos com `FAST_MODE=True`, sem salvar saídas no Git.

| Verificação | Resultado |
|---|---|
| JSON, sintaxe, aviso educacional, botão Colab e seções finais | aprovado, 8/8 |
| Testes unitários | aprovado, 18 testes |
| Smoke test interno (classificação, clustering, reforço e tempo) | aprovado |
| Download UCI CDC 891 | aprovado |
| Download Rdatasets NCCTG Lung (`survival/cancer.csv`) | aprovado |
| Download InfoDengue para Niterói | aprovado |
| PneumoniaMNIST 64 × 64 e checksum oficial | aprovado |
| Notebooks 01–08 em `FAST_MODE` | aprovados |
| CNN e Grad-CAM com Keras 3 | aprovado em CPU |

Versões observadas:

```text
numpy 2.4.3
pandas 2.3.3
scikit-learn 1.9.0
matplotlib 3.11.1
seaborn 0.13.2
ucimlrepo 0.0.7
shap 0.52.0
lifelines 0.30.3
medmnist 3.0.2
kneed 0.8.6
statsmodels 0.14.6
tensorflow 2.21.0
requests 2.32.5
```

### Adaptações confirmadas

- O arquivo `survival/lung.csv` do Rdatasets não contém mais a tabela NCCTG esperada. O alias histórico oficial `survival/cancer.csv` contém as 228 linhas e 10 variáveis documentadas; o notebook usa essa URL e valida as colunas.
- O downloader do MedMNIST 3 usa `torchvision` internamente. Para evitar uma dependência desnecessária no experimento TensorFlow, `ensure_medmnist_download` baixa a URL oficial publicada pelo próprio MedMNIST, usa timeout, confirma MD5 e só então abre as divisões oficiais.
- O Grad-CAM usa `model.outputs[0]`, compatível com Keras 3, e redimensiona o mapa antes da sobreposição.
- Lacunas da série temporal usam somente a última observação passada; não há interpolação com valores futuros nem preenchimento com zero.

### Validação manual ainda necessária após publicação

Depois que os arquivos forem commitados e enviados à branch `main`, abrir cada botão no Google Colab e confirmar o fluxo pela interface. Os URLs já usam o repositório e a branch corretos, mas um link só pode servir arquivos que estejam publicados no GitHub.
