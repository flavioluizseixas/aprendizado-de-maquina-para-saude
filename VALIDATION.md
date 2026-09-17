# Registro de validação

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
