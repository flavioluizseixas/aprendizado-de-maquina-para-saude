# Registro de validação

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
