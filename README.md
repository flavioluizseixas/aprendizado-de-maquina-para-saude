# Aprendizado de Máquina para Saúde — hands-on

Coleção de oito experimentos progressivos, em português, para estudar aprendizado de máquina aplicado à saúde no Python e no Google Colab. Os notebooks baixam bases públicas diretamente das fontes, evitam upload manual e separam a complexidade repetitiva em funções documentadas em `src/`.

> **Aviso:** este material tem finalidade exclusivamente educacional. Os resultados não devem ser usados para diagnóstico, prognóstico, tratamento, gestão assistencial ou decisão de saúde pública sem validação adequada, análise de contexto e supervisão de profissionais qualificados.

## Notebooks

| Nº | Tema | Base | Duração | Colab |
|---:|---|---|---:|---|
| 01 | Estatística descritiva | CDC Diabetes | 45–60 min | [Abrir](https://colab.research.google.com/github/flavioluizseixas/aprendizado-de-maquina-para-saude/blob/main/notebooks/01_estatistica_descritiva.ipynb) |
| 02 | Supervisionado e SHAP | CDC Diabetes | 75–90 min | [Abrir](https://colab.research.google.com/github/flavioluizseixas/aprendizado-de-maquina-para-saude/blob/main/notebooks/02_aprendizado_supervisionado.ipynb) |
| 03 | K-means e PCA | CDC Diabetes | 60–75 min | [Abrir](https://colab.research.google.com/github/flavioluizseixas/aprendizado-de-maquina-para-saude/blob/main/notebooks/03_aprendizado_nao_supervisionado.ipynb) |
| 04 | Modelos e hiperparâmetros | CDC Diabetes | 75–90 min | [Abrir](https://colab.research.google.com/github/flavioluizseixas/aprendizado-de-maquina-para-saude/blob/main/notebooks/04_comparacao_modelos_hiperparametros.ipynb) |
| 05 | Imagens e Grad-CAM | PneumoniaMNIST | 90 min | [Abrir](https://colab.research.google.com/github/flavioluizseixas/aprendizado-de-maquina-para-saude/blob/main/notebooks/05_imagens_gradcam.ipynb) |
| 06 | Sobrevivência | NCCTG Lung | 75–90 min | [Abrir](https://colab.research.google.com/github/flavioluizseixas/aprendizado-de-maquina-para-saude/blob/main/notebooks/06_analise_sobrevivencia.ipynb) |
| 07 | Reforço | InfoDengue | 75–90 min | [Abrir](https://colab.research.google.com/github/flavioluizseixas/aprendizado-de-maquina-para-saude/blob/main/notebooks/07_aprendizado_reforco.ipynb) |
| 08 | Séries temporais | InfoDengue | 75–90 min | [Abrir](https://colab.research.google.com/github/flavioluizseixas/aprendizado-de-maquina-para-saude/blob/main/notebooks/08_series_temporais.ipynb) |

## O que você aprenderá

- exploração e visualização responsável de dados observacionais;
- classificação, validação cruzada, métricas e explicabilidade;
- agrupamento, elbow, silhouette e PCA;
- comparação de modelos e busca de hiperparâmetros sem tocar no teste;
- CNN pequena e Grad-CAM em imagens médicas pré-processadas;
- Kaplan–Meier, log-rank, Cox e estratificação;
- Q-learning em um ambiente operacional simulado;
- previsão temporal com lags, baseline e validação cronológica.

## Bases públicas

- **CDC Diabetes Health Indicators**, disponibilizada pela [UCI](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators), nos notebooks 01–04. Os indicadores vêm do BRFSS e incluem autorrelato.
- **PneumoniaMNIST**, do [MedMNIST](https://medmnist.com/), no notebook 05. As radiografias pediátricas foram reduzidas e pré-processadas; o conjunto não se destina a uso clínico.
- **NCCTG Lung Cancer**, do pacote R `survival`, via [Rdatasets](https://vincentarelbundock.github.io/Rdatasets/doc/survival/lung.html), no notebook 06.
- **InfoDengue**, pela [API pública](https://info.dengue.mat.br/tutorial_api_python/locale-en), nos notebooks 07–08. Os valores epidemiológicos podem ser revistos.

Cada fonte mantém seus próprios termos, licença e regras de citação; a licença deste repositório não substitui as licenças das bases.

## Execução

O caminho recomendado é clicar em **Abrir** na tabela e escolher `Executar tudo` no Colab. A primeira célula clona ou atualiza o repositório, instala somente os pacotes ausentes e fixa a semente aleatória. Nenhum notebook pede arquivo local, token ou login.

Para executar localmente:

```bash
git clone https://github.com/flavioluizseixas/aprendizado-de-maquina-para-saude.git
cd aprendizado-de-maquina-para-saude
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux/macOS
source .venv/bin/activate
```

Instale o projeto com todas as dependências dos notebooks e inicie o Jupyter a partir da raiz do repositório:

```bash
python -m pip install -e ".[dev,notebooks]"
jupyter lab
```

Não é necessário editar os notebooks: a célula de preparação detecta a execução fora do Colab, localiza a raiz do projeto e instala somente os pacotes que ainda estejam ausentes no ambiente do kernel.

Os notebooks têm `FAST_MODE = True` por padrão para uma primeira execução econômica. Desative-o para aumentar amostras, épocas, iterações ou episódios; as validações obrigatórias continuam usando cinco folds.

### Usar um fork

Altere `REPO` e `REPO_URL` em `src/config.py` e as constantes no início de `scripts/build_notebooks.py`; depois rode `python scripts/build_notebooks.py`. Os links usam a branch `main`.

## Estrutura

```text
notebooks/       oito roteiros executáveis
src/             carregamento, avaliação e algoritmos reutilizáveis
tests/           testes unitários sem downloads reais
data/cache/      cache local ignorado pelo Git
assets/figures/  figuras permanentes, quando houver
scripts/         geração reproduzível dos notebooks
```

O conteúdo didático anterior foi preservado em `backup/` e não é necessário para os novos notebooks.

## Glossário rápido

- **atributo:** variável usada como entrada; **alvo:** resultado que se deseja prever;
- **treino / validação / teste:** dados usados, respectivamente, para aprender, escolher e estimar o desempenho final;
- **fold:** uma partição da validação cruzada;
- **sensibilidade:** proporção de positivos detectados; **especificidade:** proporção de negativos detectados;
- **precisão:** proporção das previsões positivas que eram positivas; **F1:** média harmônica entre precisão e sensibilidade;
- **ROC-AUC:** capacidade de ordenação entre classes ao variar o limiar;
- **explicabilidade:** técnicas para investigar como um modelo produziu saídas, sem implicar causalidade;
- **cluster:** grupo criado por semelhança matemática, não uma classe clínica verdadeira;
- **censura:** evento não observado durante o acompanhamento; **hazard:** taxa instantânea condicionada à sobrevivência;
- **estado / ação / recompensa:** descrição do contexto, escolha do agente e retorno numérico no reforço;
- **lag:** valor passado usado como atributo temporal.

## Qualidade, testes e contribuição

Execute `python -m pytest` para os testes unitários e `python scripts/validate_notebooks.py` para validar estrutura e sintaxe das células. Pull requests devem preservar a separação treino/teste, a ordem temporal, os avisos éticos e a execução sem credenciais.

## Compatibilidade e problemas conhecidos

O alvo principal é o Colab atual, com Python 3.10–3.13. Downloads dependem da disponibilidade da UCI, MedMNIST, Rdatasets e InfoDengue. A API do InfoDengue pode ficar indisponível ou não retornar um município/período; a falha é exibida e nunca é substituída silenciosamente por dados sintéticos. O notebook de imagens é mais rápido com GPU e resultados exatos podem variar entre aceleradores.

O Rdatasets atualmente publica o NCCTG Lung no arquivo `survival/cancer.csv` (alias histórico documentado pelo pacote `survival`); `survival/lung.csv` passou a apontar para outra tabela. O notebook valida as colunas antes de prosseguir.

## Licença e citação

Código e textos estão sob a licença MIT; consulte [LICENSE](LICENSE). Para citar o material, use os metadados de [CITATION.cff](CITATION.cff) e cite também as bases e artigos indicados em cada notebook.
