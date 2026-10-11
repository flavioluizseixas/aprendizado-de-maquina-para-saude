"""Gera o notebook mínimo de séries temporais e seu enunciado em Word."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

import create_task3_minimal as template


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = "08_series_temporais_versão_minima.ipynb"
TASK = ROOT / "tarefas" / "Tarefa_8_Series_Temporais_Versao_Minima.md"
cell = template.cell


def build_notebook() -> dict:
    cells = [
        cell("markdown", f"""
            # 08 — Séries temporais com RNN: versão mínima

            [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)]({template.COLAB}/blob/main/notebooks/{quote(NOTEBOOK)})

            **Pergunta orientadora:** os casos das semanas anteriores ajudam a prever os casos de uma semana melhor do que simplesmente repetir o último valor?

            **Objetivos:** reconhecer a ordem temporal, construir sequências com o passado, treinar uma rede neural recorrente (RNN), separar treino, validação e teste cronologicamente e interpretar MAE e RMSE. Atividade em duplas, com seis células de código, para 45–60 minutos. Retoma as noções de RNN apresentadas em aula.

            Use Colab ou Jupyter com pandas, numpy, matplotlib, requests, scikit-learn e TensorFlow. Se necessário, execute `%pip install pandas numpy matplotlib requests scikit-learn "tensorflow>=2.16,<3"` em uma célula adicional e reinicie o kernel. A versão do TensorFlow deve ser compatível com o Python do ambiente; no Colab, use o ambiente padrão. Não é necessária GPU. Execute as seis células em ordem. O primeiro download requer internet; não é necessário clonar o repositório. A célula 1 mantém um cache local dos dados.

            ## Fonte e licença

            Série semanal de Niterói (RJ; código IBGE 3303302), consultada para 2016–2025 na [API pública do InfoDengue](https://info.dengue.mat.br/tutorial_api_python/locale-en). Consulte os termos e as orientações de citação da fonte. Cada linha representa uma semana epidemiológica.

            **Dicionário:** `data_iniSE` é o domingo que inicia a semana; `casos_est` é a estimativa semanal por nowcasting, que considera atrasos de notificação. Esses valores podem ser revistos retrospectivamente. Mantemos o mesmo alvo principal do notebook completo.

            Material com finalidade exclusivamente educacional. A avaliação usa a versão histórica disponível no download; ela não reproduz exatamente os dados que estavam disponíveis em cada semana passada. Os resultados não devem orientar decisões de saúde pública.
        """),
        cell("markdown", """
            ## 1. Carregar e conferir a série

            **Se houver erro ao importar pandas:** confira o ambiente selecionado no kernel do notebook. No Windows, uma mensagem como “DLL load failed” e “Controle de Aplicativo bloqueou este arquivo”, mencionando `pyarrow._compute`, indica um bloqueio na instalação do PyArrow desse ambiente. Esta atividade não usa PyArrow diretamente. Selecione um ambiente em que pandas funcione (por exemplo, o ambiente `base` do Conda, se disponível), reinicie o kernel e execute tudo novamente. O Colab também é uma opção. Confira o caminho Python impresso pela célula. PyArrow pode ser exigido por outros programas do mesmo ambiente; confira essas dependências antes de removê-lo. Consulte as [dependências opcionais do pandas](https://pandas.pydata.org/docs/getting_started/install.html#optional-dependencies).

            A preparação técnica abaixo confere datas, valores e semanas ausentes. Não é necessário decorar esse código. Uma semana ausente permanece ausente: não será tratada como zero nem preenchida.

            **Progresso:** a célula anuncia cada importação e as etapas de leitura/download, validação e organização da série. Exibe a duração de cada etapa e repete o estado a cada 5 segundos enquanto aguarda. O caminho completo do cache aparece na saída; dentro deste projeto, o mesmo cache é usado ao abrir o notebook pela raiz ou pela pasta `notebooks`. No download, os limites são 15 segundos para conexão e 60 segundos de espera por dados em cada operação de leitura; não representam um limite total da célula. Se nem a mensagem inicial aparecer, o kernel pode ainda estar iniciando ou ocupado com outra execução; confira seu estado antes de executar novamente.
        """),
        cell("code", """
            import sys
            from contextlib import contextmanager
            from datetime import datetime, timezone
            from importlib.metadata import version
            from io import StringIO
            from pathlib import Path
            from threading import Event, Thread
            from time import perf_counter

            inicio_celula = perf_counter()
            print("Célula 1 iniciada.", flush=True)
            print("Python do kernel:", sys.executable, flush=True)

            @contextmanager
            def progresso(etapa):
                inicio = perf_counter()
                print(f"{etapa}...", flush=True)
                parar = Event()

                def avisar():
                    while not parar.wait(5):
                        print(f"  {etapa}: ainda executando ({perf_counter() - inicio:.1f}s).", flush=True)

                aviso = Thread(target=avisar, daemon=True)
                aviso.start()
                try:
                    yield
                finally:
                    parar.set()
                    aviso.join()
                print(f"  Concluído em {perf_counter() - inicio:.2f}s.", flush=True)

            with progresso("[1/4] Importando numpy"):
                import numpy as np
            with progresso("[1/4] Importando pandas"):
                import pandas as pd
            with progresso("[1/4] Importando matplotlib"):
                import matplotlib.pyplot as plt
            with progresso("[1/4] Importando requests"):
                import requests
            with progresso("[1/4] Importando scikit-learn e ferramentas de exibição"):
                from sklearn.metrics import mean_absolute_error, mean_squared_error
                from sklearn.preprocessing import MinMaxScaler
                from IPython.display import display
                versoes = {nome: version(nome) for nome in ["pandas", "numpy", "matplotlib", "requests", "scikit-learn"]}
            print("Versões:", versoes, flush=True)
            with progresso("[1/4] Importando TensorFlow/Keras"):
                import tensorflow as tf
            print("TensorFlow:", tf.__version__, flush=True)
            url = "https://info.dengue.mat.br/api/alertcity"
            parametros = dict(geocode=3303302, disease="dengue", format="csv",
                              ew_start=1, ew_end=53, ey_start=2016, ey_end=2025)
            raiz = next((p for p in [Path.cwd(), Path.cwd().parent]
                         if (p / "notebooks").is_dir() and (p / "src").is_dir()), Path.cwd())
            arquivo = raiz / "data/cache/infodengue_3303302_dengue_2016_2025.csv"
            print("Cache:", arquivo.resolve(), flush=True)
            if arquivo.exists():
                with progresso("[2/4] Lendo o cache local (sem download)"):
                    dados = pd.read_csv(arquivo)
                origem = "cache local"
            else:
                print("Cache não encontrado. A API pode demorar para responder.", flush=True)
                try:
                    with progresso("[2/4] Consultando a API InfoDengue e lendo o CSV"):
                        resposta = requests.get(url, params=parametros, timeout=(15, 60))
                        resposta.raise_for_status()
                        print(f"  Resposta recebida: HTTP {resposta.status_code} | {len(resposta.content):,} bytes.", flush=True)
                        dados = pd.read_csv(StringIO(resposta.text))
                except (requests.RequestException, pd.errors.ParserError, ValueError) as erro:
                    raise RuntimeError("Falha no download do InfoDengue. Confira a conexão e tente novamente. Nenhum dado simulado foi usado.") from erro
                origem = "API InfoDengue"

            with progresso("[3/4] Validando datas e valores"):
                if dados.empty or not {"data_iniSE", "casos_est"}.issubset(dados.columns):
                    raise ValueError("A resposta deve conter datas e casos_est; confira município e período.")
                datas = pd.to_datetime(dados["data_iniSE"], errors="coerce")
                valores = pd.to_numeric(dados["casos_est"], errors="coerce")
                if datas.isna().any() or datas.duplicated().any() or (datas.dt.dayofweek != 6).any():
                    raise ValueError("Datas inválidas, duplicadas ou fora do início semanal esperado.")
                if np.isinf(valores).any() or (valores.dropna() < 0).any():
                    raise ValueError("Há estimativas de casos inválidas.")
            with progresso("[4/4] Organizando a série semanal e conferindo o cache"):
                serie = pd.Series(valores.to_numpy(), index=datas, name="casos_est").sort_index()
                serie = serie.reindex(pd.date_range(serie.index.min(), serie.index.max(), freq="W-SUN"))
                serie.index.name = "Semana"
                if len(serie) < 160:
                    raise ValueError("São necessárias ao menos 160 semanas para treino, validação, teste e janela inicial.")
                if not arquivo.exists():
                    arquivo.parent.mkdir(parents=True, exist_ok=True)
                    dados.to_csv(arquivo, index=False)
            consulta = datetime.now(timezone.utc).isoformat()
            modificado = datetime.fromtimestamp(arquivo.stat().st_mtime, timezone.utc).isoformat()
            print("Fonte:", url, "| Município: Niterói (RJ) | Origem:", origem)
            print("Consulta (UTC):", consulta, "| Arquivo salvo/modificado (UTC):", modificado)
            print(f"Período retornado: {serie.index.min().date()} a {serie.index.max().date()}")
            print(f"Semanas: {len(serie)} | Semanas/valores ausentes: {serie.isna().sum()}")
            display(serie.head(8).to_frame())
            print(f"Pronto! Célula 1 concluída em {perf_counter() - inicio_celula:.2f}s.", flush=True)
        """),
        cell("markdown", """
            ## 2. Observar o passado

            Reservamos as últimas 52 semanas do calendário retornado para o teste. O gráfico inicial mostra somente o período anterior. A média móvel suaviza oscilações; neste gráfico descritivo ela inclui a semana corrente. Na célula 3, a média usada para prever será deslocada para usar apenas semanas anteriores.

            **Antes de executar:** uma série de casos que apresenta picos todos os anos necessariamente manterá o mesmo padrão no ano seguinte? Registre uma hipótese e observe o gráfico.
        """),
        cell("code", """
            inicio_teste = serie.index[-52]
            passado = serie.loc[serie.index < inicio_teste]
            fig, eixo = plt.subplots(figsize=(11, 4))
            passado.plot(ax=eixo, alpha=0.6, label="Casos estimados")
            passado.rolling(4).mean().plot(ax=eixo, label="Média móvel de 4 semanas")
            eixo.set(title="Dengue em Niterói — período anterior ao teste",
                     xlabel="Semana", ylabel="Casos estimados")
            eixo.legend()
            plt.tight_layout()
            plt.show()
            print("Início do período reservado para teste:", inicio_teste.date())
        """),
        cell("markdown", """
            ## 3. Transformar o passado em sequências

            Para prever a semana **t**, a RNN recebe os casos em **[t−4, t−3, t−2, t−1]**, do mais antigo ao mais recente. Cada passo contém uma variável: casos estimados. As colunas `lag_4`, `lag_3`, `lag_2` e `lag_1` permitem conferir a sequência antes de convertê-la para o formato **(amostras, passos de tempo, variáveis)**, aqui `(n, 4, 1)`. A rede atualiza seu estado interno a cada passo; o último estado alimenta uma camada que prevê uma correção sobre o último valor observado. O estado é reiniciado entre janelas (`stateful=False`).

            **Previsão = última semana + correção da RNN.** Se a correção for zero, a rede repete a última semana. Inicializamos a camada de saída com zeros para começar exatamente nessa referência. A correção pode ser positiva ou negativa e é aprendida no treino. Ela não é o resíduo de avaliação (observado − previsto), que só calculamos depois.

            `media_4` = média de t−1 a t−4 é uma referência simples, não uma entrada adicional da rede. `shift(1)` desloca os valores uma linha para que a média não inclua o alvo da própria semana.

            **Exercício antes do código:** nas quatro semanas anteriores ocorreram 10, 20, 30 e 40 casos, nessa ordem. Escreva a sequência recebida pela RNN, calcule `lag_1`, `lag_2`, `lag_3`, `lag_4`, `media_4` e a previsão de repetir a última semana. O alvo da semana seguinte ainda é desconhecido. Por que quatro passos com uma variável diferem de um passo com quatro variáveis?

            A grade semanal foi regularizada antes dos lags. Removemos linhas cujo alvo ou algum atributo esteja ausente; as contagens serão exibidas. Assim, as comparações usam as mesmas semanas com informação completa.
        """),
        cell("code", """
            tabela = pd.DataFrame({"alvo": serie})
            tabela["lag_1"] = serie.shift(1)
            tabela["lag_2"] = serie.shift(2)
            tabela["lag_3"] = serie.shift(3)
            tabela["lag_4"] = serie.shift(4)
            tabela["media_4"] = serie.shift(1).rolling(4).mean()
            antes = len(tabela)
            tabela = tabela.dropna()
            print(f"Linhas utilizáveis: {len(tabela)} | Removidas: {antes - len(tabela)}")
            display(tabela.head(6).round(2))
        """),
        cell("markdown", """
            ## 4. Separar treino, validação e teste e treinar

            As últimas 52 semanas são o teste; as 52 anteriores são a validação; o restante é treino. Não embaralhamos as linhas. Usamos `SimpleRNN(16)` seguida de `Dense(1)` para prever a correção sobre a última semana, com **305 parâmetros treináveis**.

            Reiniciamos a semente em 42 e treinamos por **até 200 épocas**, com lotes de 16, Adam com taxa 0,001 e perda MSE. `EarlyStopping` monitora a perda de validação, espera 20 épocas sem melhora e restaura os melhores pesos. O teste não decide a época de parada. Atingir 200 épocas não demonstra convergência.

            Ajustamos `MinMaxScaler` **somente nos valores anteriores à validação**. O alvo da rede é `alvo_normalizado − última_semana_normalizada`. Somamos a correção prevista à última semana normalizada e desfazemos a transformação para avaliar em casos por semana. Valores posteriores podem ficar fora de [0, 1]; não reajustamos a escala com eles. A entrada tem forma `(n, 4, 1)`, não `(n, 1, 4)`. A perda impressa está na escala normalizada, não em casos.

            Os pesos são ajustados apenas no treino; a validação escolhe a época. Não retreinamos depois dessa escolha. O gráfico de perdas permite discutir o treinamento, e a tabela de validação permite comparar os métodos antes do teste. A semente facilita a reprodução, mas versões e hardware podem alterar os resultados. Se já observamos o teste e depois modificamos o modelo, a nova comparação nesse mesmo teste é exploratória; uma confirmação independente exige outro período.
        """),
        cell("code", """
            passos = ["lag_4", "lag_3", "lag_2", "lag_1"]  # antigo -> recente
            inicio_validacao = passado.index[-52]
            treino = tabela.loc[tabela.index < inicio_validacao]
            validacao = tabela.loc[(tabela.index >= inicio_validacao) & (tabela.index < inicio_teste)]
            teste = tabela.loc[tabela.index >= inicio_teste]
            if len(treino) < 52 or validacao.empty or teste.empty:
                raise ValueError("Há poucas semanas completas em treino, validação ou teste; confira as ausências.")
            assert treino.index.max() < validacao.index.min() <= validacao.index.max() < teste.index.min()
            print(f"Treino: {len(treino)} semanas | {treino.index.min().date()} a {treino.index.max().date()}")
            print(f"Validação: {len(validacao)} de 52 semanas | {validacao.index.min().date()} a {validacao.index.max().date()}")
            print(f"Teste: {len(teste)} de 52 semanas reservadas | {teste.index.min().date()} a {teste.index.max().date()}")
            escala = MinMaxScaler()
            valores_treino = serie.loc[serie.index < inicio_validacao].dropna()
            escala.fit(valores_treino.to_numpy().reshape(-1, 1))

            def sequencias_normalizadas(quadro):
                valores = quadro[passos].to_numpy()
                return escala.transform(valores.reshape(-1, 1)).reshape(-1, 4, 1).astype("float32")

            X_treino = sequencias_normalizadas(treino)
            X_validacao = sequencias_normalizadas(validacao)
            X_teste = sequencias_normalizadas(teste)
            y_treino = escala.transform(treino[["alvo"]].to_numpy()).astype("float32")
            y_validacao = escala.transform(validacao[["alvo"]].to_numpy()).astype("float32")
            correcao_treino = y_treino - X_treino[:, -1, :]
            correcao_validacao = y_validacao - X_validacao[:, -1, :]
            print("Entrada da RNN (amostras, passos, variáveis):", X_treino.shape)
            tf.keras.backend.clear_session()
            tf.keras.utils.set_random_seed(42)
            modelo = tf.keras.Sequential([
                tf.keras.Input(shape=(4, 1)),
                tf.keras.layers.SimpleRNN(16, activation="tanh", stateful=False),
                tf.keras.layers.Dense(1, kernel_initializer="zeros", bias_initializer="zeros"),
            ])
            modelo.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss="mse")
            modelo.summary()
            parada = tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=20, restore_best_weights=True)
            historico = modelo.fit(
                X_treino, correcao_treino,
                validation_data=(X_validacao, correcao_validacao),
                epochs=200, batch_size=16, shuffle=False, verbose=2, callbacks=[parada])
            melhor_epoca = int(np.argmin(historico.history["val_loss"]) + 1)
            print(f"Épocas executadas: {len(historico.history['loss'])} | Melhor época de validação: {melhor_epoca}")

            def prever_casos(X):
                correcao = modelo.predict(X, verbose=0)
                previsao_normalizada = X[:, -1, :] + correcao
                return np.maximum(escala.inverse_transform(previsao_normalizada).ravel(), 0)

            previsao_validacao = prever_casos(X_validacao)
            display(pd.DataFrame({"MAE de validação (casos)": {
                "Última semana": mean_absolute_error(validacao["alvo"], validacao["lag_1"]),
                "Média de 4 semanas": mean_absolute_error(validacao["alvo"], validacao["media_4"]),
                "RNN": mean_absolute_error(validacao["alvo"], previsao_validacao),
            }}).round(2))
            pd.DataFrame({"Treino": historico.history["loss"],
                          "Validação": historico.history["val_loss"]},
                         index=np.arange(1, len(historico.history["loss"]) + 1)).plot(
                             title="Treinamento da RNN", xlabel="Época", ylabel="MSE normalizado")
            plt.tight_layout()
            plt.show()
        """),
        cell("markdown", """
            ## 5. Comparar com duas regras simples

            Comparamos três métodos: **repetir a última semana**, **média das quatro semanas anteriores** e **RNN (SimpleRNN)**. Menor erro indica melhor desempenho neste teste. A rede aprende uma correção; após somá-la à última semana e voltar à escala original, limitamos previsões negativas a zero. As mesmas semanas são avaliadas nos três métodos. Não escolhemos épocas ou configurações pelo teste.

            **MAE:** média dos erros absolutos, em casos por semana. **RMSE:** raiz da média dos erros ao quadrado, também em casos por semana; dá mais peso a erros grandes. Exemplo: para valores reais 20, 30 e 40 e previsões 18, 35 e 39, os erros absolutos são 2, 5 e 1. Calcule o MAE antes de executar.

            **Horizonte:** avaliamos previsões de uma semana por vez. Para prever cada semana do teste, usamos os valores observados nas semanas anteriores, inclusive quando elas já pertencem ao período de teste. Os pesos são ajustados apenas no treino, com a época selecionada pela validação. Não estamos prevendo as 52 semanas de uma só vez. Como os valores foram obtidos retrospectivamente, revisões e atrasos limitam a simulação de uso real.
        """),
        cell("code", """
            previsao_rnn = prever_casos(X_teste)
            comparacao = pd.DataFrame({
                "Observado": teste["alvo"],
                "Última semana": teste["lag_1"],
                "Média de 4 semanas": teste["media_4"],
                "RNN": previsao_rnn,
            }, index=teste.index)
            resultados = pd.DataFrame([
                {"Método": nome,
                 "MAE": mean_absolute_error(comparacao["Observado"], comparacao[nome]),
                 "RMSE": np.sqrt(mean_squared_error(comparacao["Observado"], comparacao[nome]))}
                for nome in comparacao.columns[1:]
            ]).set_index("Método")
            display(resultados.round(2))
            mae_base = resultados.loc["Última semana", "MAE"]
            if mae_base > 0:
                ganho = 100 * (mae_base - resultados.loc["RNN", "MAE"]) / mae_base
                print(f"Redução do MAE da RNN frente à última semana: {ganho:.1f}%")
                print("Resultado positivo = redução do erro; negativo = aumento do erro.")
            else:
                print("Baseline com MAE zero: redução percentual indefinida.")
        """),
        cell("markdown", """
            ## 6. Investigar onde ocorrem os erros

            Observe se as previsões acompanham subidas, descidas e picos. O resíduo é **observado − previsto**: positivo indica subestimação; negativo indica superestimação. Exibimos os resíduos e as três semanas com maior erro absoluto da RNN. Um MAE menor não garante menor erro em todas as semanas.
        """),
        cell("code", """
            fig, eixos = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
            comparacao.plot(ax=eixos[0], title="Uma semana por vez — período de teste")
            eixos[0].set_ylabel("Casos estimados")
            residuo = comparacao["Observado"] - comparacao["RNN"]
            residuo.plot(ax=eixos[1], color="C3", label="Resíduo da RNN")
            eixos[1].axhline(0, color="black", linewidth=1)
            eixos[1].set(xlabel="Semana", ylabel="Observado − previsto")
            eixos[1].legend()
            plt.tight_layout()
            plt.show()
            maiores_erros = comparacao.assign(residuo=residuo, erro_absoluto=residuo.abs())
            display(maiores_erros.nlargest(3, "erro_absoluto").round(2))
        """),
        cell("markdown", """
            ## Atividade e perguntas

            1. O que representa cada linha? Informe o município, o alvo, o período retornado e as ausências. No gráfico anterior ao teste, descreva um pico ou uma mudança ao longo do tempo. O gráfico permite afirmar uma sazonalidade anual estável?
            2. Resolva o exemplo de 10, 20, 30 e 40 casos da célula 3. Escolha também uma linha da tabela real e explique a ordem das quatro semanas. O que significa a forma `(n, 4, 1)`?
            3. Por que usamos `shift(1).rolling(4).mean()`? O que ocorreria se calculássemos `rolling(4).mean()` diretamente para prever a mesma semana? Por que ajustamos a normalização apenas no treino e a desfazemos antes de calcular os erros?
            4. Registre as datas e quantidades de treino, validação e teste. Qual foi a melhor época? Explique o papel de cada divisão e por que não usamos o teste no EarlyStopping. Por que podemos usar uma semana anterior do teste como lag para a seguinte? Se a correção da RNN for zero, qual é sua previsão?
            5. Calcule o MAE do exemplo da célula 5 e explique sua unidade. Por que o RMSE é mais afetado por um erro muito grande?
            6. Registre MAE e RMSE dos três métodos. Qual teve menor MAE? A RNN melhorou as referências? Interprete a redução percentual, inclusive se negativa. Uma diferença pequena demonstra superioridade em períodos futuros?
            7. Escolha uma das três semanas da tabela de maiores erros. Registre data, observado, previsão, resíduo e erro absoluto. Houve subestimação ou superestimação? Relacione o erro com o gráfico, sem afirmar uma causa epidemiológica.
            8. Conclua em 5–8 linhas: responda à pergunta orientadora com os resultados obtidos e apresente duas limitações. Considere revisões, atrasos, semanas excluídas, mudanças de padrão, teste único e ausência de intervalos de previsão.

            **Entrega:** um `.ipynb` com nomes da dupla, seis células executadas, saídas e respostas em Markdown. Antes de entregar, reinicie o ambiente e execute tudo em ordem. Preserve a tabela dos três métodos. A avaliação considera a interpretação e a preservação da ordem temporal; não exige que a RNN vença as referências.

            **Desafio opcional (+10 minutos):** antes de executar a célula 5, preserve os resultados de validação da rede de 16 unidades. Em uma cópia, substitua `SimpleRNN(16, ...)` por `SimpleRNN(8, ...)` e execute apenas a célula 4. Compare parâmetros, melhor época e MAE de validação. Escolha pela validação, reexecute a célula 4 com a configuração escolhida e só então as células 5–6. Se já tiver observado o teste, trate a comparação como exploração e reserve outro período para confirmação independente.

            **Três aprendizados principais:** fornecer sequências em ordem à RNN; preservar a divisão temporal e normalizar só pelo treino; comparar com regras simples e interpretar os limites dos erros.

            **Apoio:** [API e dicionário InfoDengue](https://info.dengue.mat.br/tutorial_api_python/locale-en), [Keras — SimpleRNN](https://keras.io/api/layers/recurrent_layers/simple_rnn/) e [exemplo oficial de lags e divisão temporal](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html).
        """),
    ]
    for index, entry in enumerate(cells):
        entry["id"] = f"atividade8-{index:02d}"
    return {
        "cells": cells,
        "metadata": {
            "colab": {"name": NOTEBOOK, "provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    notebook_path = ROOT / "notebooks" / NOTEBOOK
    notebook_path.write_text(json.dumps(build_notebook(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    document = template.build_document(TASK, "Atividade 8 — Séries temporais | Versão mínima")
    document.save(TASK.with_suffix(".docx"))
    print(notebook_path)
    print(TASK.with_suffix(".docx"))


if __name__ == "__main__":
    main()
