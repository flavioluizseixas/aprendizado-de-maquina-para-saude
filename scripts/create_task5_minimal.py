"""Gera o experimento 05 mínimo e o enunciado Word (requer python-docx)."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

import create_task3_minimal as template


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = "05_imagens_gradcam_versão_minima.ipynb"
TASK = ROOT / "tarefas" / "Tarefa_5_Imagens_GradCAM_Versao_Minima.md"
cell = template.cell


def build_notebook() -> dict:
    cells = [
        cell("markdown", f"""
            # 05 — Imagens e Grad-CAM: versão mínima

            [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)]({template.COLAB}/blob/main/notebooks/{quote(NOTEBOOK)})

            **Objetivo:** treinar uma CNN pequena, interpretar seus erros e investigar a saída pneumonia com Grad-CAM. Execute as sete células de código em ordem. Reserve 50–60 minutos; o treinamento depende do hardware.

            Use Colab ou Jupyter com Python 3.10–3.13, numpy, pandas, matplotlib, scikit-learn, requests, medmnist e TensorFlow 2.16 ou superior. Se faltar algum pacote, execute `%pip install numpy pandas matplotlib scikit-learn requests "medmnist>=3,<4" "tensorflow>=2.16,<3"` em uma célula adicional e reinicie o ambiente. Não é necessário clonar o repositório. A primeira execução requer internet; CPU é suficiente e GPU é opcional.

            ## Fonte e licença

            [PneumoniaMNIST — MedMNIST](https://medmnist.com/), derivado de radiografias pediátricas de Kermany et al.; licença CC BY 4.0. Usaremos imagens em tons de cinza de 64 × 64 pixels e as divisões oficiais: 4.708 para treino, 524 para validação e 624 para teste. [Metadados, URL e checksum oficiais](https://github.com/MedMNIST/MedMNIST/blob/main/medmnist/info.py).

            **Rótulos:** 0 = normal; 1 = pneumonia (classe positiva). São rótulos do conjunto de dados. Os pixels serão divididos por 255 para ficar entre 0 e 1; essa transformação fixa não aprende parâmetros no teste.

            Material com finalidade exclusivamente educacional. As imagens reduzidas e os mapas não devem orientar diagnósticos ou decisões clínicas.
        """),
        cell("markdown", """
            ## 1. Ambiente e dados

            O arquivo oficial é baixado com timeout e conferido por checksum antes da leitura. O cache evita novos downloads. Treino ajusta os pesos; validação escolhe a época; teste estima o desempenho final. Preserve essas divisões.
        """),
        cell("code", """
            import hashlib
            import platform
            from importlib.metadata import version
            from pathlib import Path

            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd
            import requests
            import tensorflow as tf
            from IPython.display import display
            from medmnist import INFO
            from sklearn.metrics import ConfusionMatrixDisplay, classification_report, roc_auc_score

            tf.keras.utils.set_random_seed(42)
            print("Python:", platform.python_version())
            print({name: version(name) for name in ["numpy", "pandas", "matplotlib", "scikit-learn", "requests", "tensorflow", "medmnist"]})
            print("GPU:", tf.config.list_physical_devices("GPU") or "não encontrada; usando CPU")
            info = INFO["pneumoniamnist"]
            assert info["label"] == {"0": "normal", "1": "pneumonia"}
            cache = Path("data/cache/medmnist")
            cache.mkdir(parents=True, exist_ok=True)
            arquivo = cache / "pneumoniamnist_64.npz"
            if not arquivo.exists() or hashlib.md5(arquivo.read_bytes()).hexdigest() != info["MD5_64"]:
                print("Baixando PneumoniaMNIST 64 × 64...", flush=True)
                resposta = requests.get(info["url_64"], timeout=(15, 60))
                resposta.raise_for_status()
                if hashlib.md5(resposta.content).hexdigest() != info["MD5_64"]:
                    raise ValueError("Checksum diferente do oficial; arquivo não será usado.")
                arquivo.write_bytes(resposta.content)
            with np.load(arquivo, allow_pickle=False) as dados:
                X_train, X_val, X_test = [dados[f"{s}_images"][..., None].astype("float32") / 255 for s in ["train", "val", "test"]]
                y_train, y_val, y_test = [dados[f"{s}_labels"].ravel().astype(int) for s in ["train", "val", "test"]]
            print("Dados oficiais carregados.")
        """),
        cell("markdown", """
            ## 2. Inspeção das imagens

            Observe quantidade, formato e proporção de pneumonia em cada divisão. As imagens abaixo pertencem somente ao treino. A dimensão final igual a 1 representa o canal de tons de cinza.
        """),
        cell("code", """
            resumo = []
            for nome, chave, X, y in [("treino", "train", X_train, y_train), ("validação", "val", X_val, y_val), ("teste", "test", X_test, y_test)]:
                assert X.shape == (info["n_samples"][chave], 64, 64, 1)
                assert len(X) == len(y) and set(np.unique(y)) == {0, 1}
                assert np.isfinite(X).all() and X.min() >= 0 and X.max() <= 1
                resumo.append({"divisão": nome, "n": len(y), "normal": int((y == 0).sum()), "pneumonia": int((y == 1).sum()), "% pneumonia": 100 * y.mean()})
            display(pd.DataFrame(resumo).round(1))
            nomes = ["normal", "pneumonia"]
            fig, eixos = plt.subplots(2, 4, figsize=(9, 5))
            for classe in [0, 1]:
                for eixo, i in zip(eixos[classe], np.flatnonzero(y_train == classe)[:4]):
                    eixo.imshow(X_train[i, ..., 0], cmap="gray", vmin=0, vmax=1)
                    eixo.set_title(nomes[classe])
                    eixo.axis("off")
            plt.tight_layout()
            plt.show()
        """),
        cell("markdown", """
            ## 3. Uma CNN pequena

            As convoluções aprendem filtros; o pooling reduz o tamanho espacial; a média global resume os mapas. A última camada produz um escore (logit), convertido pela sigmoide em uma saída entre 0 e 1. Essa saída não foi calibrada como probabilidade clínica.
        """),
        cell("code", """
            tf.keras.backend.clear_session()
            tf.keras.utils.set_random_seed(42)
            entrada = tf.keras.Input(shape=(64, 64, 1))
            x = tf.keras.layers.Conv2D(16, 3, padding="same", activation="relu")(entrada)
            x = tf.keras.layers.MaxPooling2D()(x)
            x = tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu", name="last_conv")(x)
            x = tf.keras.layers.GlobalAveragePooling2D()(x)
            logit = tf.keras.layers.Dense(1, name="logit")(x)
            saida = tf.keras.layers.Activation("sigmoid")(logit)
            modelo = tf.keras.Model(entrada, saida)
            modelo.compile(optimizer="adam", loss="binary_crossentropy", metrics=[tf.keras.metrics.AUC(name="auc")])
            modelo.summary()
        """),
        cell("markdown", """
            ## 4. Treinamento e validação

            Use todos os exemplos de treino e até cinco épocas. Early stopping acompanha a AUC de validação e restaura os pesos da melhor época. A AUC exibida durante o treinamento é uma aproximação do TensorFlow. O teste não participa desta escolha. Diferenças entre hardware e versões podem mudar os resultados mesmo com semente fixa.
        """),
        cell("code", """
            parada = tf.keras.callbacks.EarlyStopping(monitor="val_auc", mode="max", patience=2, restore_best_weights=True)
            historico = modelo.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=5, batch_size=64, callbacks=[parada], verbose=2)
            curvas = pd.DataFrame(historico.history)
            curvas.index = np.arange(1, len(curvas) + 1)
            print("Melhor época pela AUC de validação:", int(curvas["val_auc"].idxmax()))
            fig, eixos = plt.subplots(1, 2, figsize=(10, 3))
            curvas[["loss", "val_loss"]].plot(ax=eixos[0], title="Erro (entropia cruzada)")
            curvas[["auc", "val_auc"]].plot(ax=eixos[1], title="AUC")
            for eixo in eixos:
                eixo.set_xlabel("Época")
                eixo.set_xticks(curvas.index)
            plt.tight_layout()
            plt.show()
        """),
        cell("markdown", """
            ## 5. Avaliação no teste oficial

            O limiar foi fixado previamente em 0,5. Recall de pneumonia é a sensibilidade; recall de normal é a especificidade. A ROC-AUC usa as saídas contínuas, enquanto a matriz depende do limiar. Compare também com a regra de prever sempre a classe majoritária **do treino**. Não ajuste o modelo ou o limiar para melhorar os resultados neste teste.
        """),
        cell("code", """
            probabilidades = modelo.predict(X_test, batch_size=128, verbose=0).ravel()
            predicoes = (probabilidades >= 0.5).astype(int)
            print(classification_report(y_test, predicoes, labels=[0, 1], target_names=nomes, digits=3, zero_division=0))
            print(f"ROC-AUC: {roc_auc_score(y_test, probabilidades):.3f}")
            majoritaria = int(np.bincount(y_train).argmax())
            print(f"Referência: sempre {nomes[majoritaria]} → acurácia {(y_test == majoritaria).mean():.3f}")
            ConfusionMatrixDisplay.from_predictions(y_test, predicoes, labels=[0, 1], display_labels=nomes, cmap="Blues")
            plt.title("Teste oficial — limiar 0,5")
            plt.show()
        """),
        cell("markdown", """
            ## 6. Como calcular o Grad-CAM

            A função abaixo calcula o gradiente do **escore de pneumonia antes da sigmoide** em relação à última convolução. Usa a média dos gradientes como peso dos mapas, mantém as contribuições positivas e normaliza entre 0 e 1. Assim, todos os exemplos explicam a mesma classe, inclusive os previstos como normal. Um mapa nulo significa ausência de contribuição positiva neste cálculo; não comprova ausência de doença. A normalização é por imagem: intensidade de cor não permite comparar confiança entre casos.
        """),
        cell("code", """
            modelo_grad = tf.keras.Model(modelo.inputs[0], [modelo.get_layer("last_conv").output, modelo.get_layer("logit").output])

            def gradcam(imagem):
                with tf.GradientTape() as fita:
                    mapas, escore = modelo_grad(imagem[None, ...], training=False)
                    alvo = escore[:, 0]  # Sempre a classe pneumonia.
                gradientes = fita.gradient(alvo, mapas)
                pesos = tf.reduce_mean(gradientes, axis=(0, 1, 2))
                mapa = tf.nn.relu(tf.reduce_sum(mapas[0] * pesos, axis=-1))
                mapa = tf.math.divide_no_nan(mapa, tf.reduce_max(mapa))
                return tf.image.resize(mapa[None, ..., None], (64, 64))[0, ..., 0].numpy()

            print("Grad-CAM pronto: alvo fixo = escore de pneumonia.")
        """),
        cell("markdown", """
            ## 7. Acertos, erros e mapas

            Mostramos o primeiro índice disponível de cada tipo de resultado; categorias ausentes são informadas. É uma seleção ilustrativa, sem estimar a qualidade geral dos mapas. Cada linha apresenta imagem, mapa e sobreposição na mesma escala de cores.
        """),
        cell("code", """
            categorias = {
                "falso positivo": (y_test == 0) & (predicoes == 1),
                "falso negativo": (y_test == 1) & (predicoes == 0),
                "verdadeiro positivo": (y_test == 1) & (predicoes == 1),
                "verdadeiro negativo": (y_test == 0) & (predicoes == 0),
            }
            selecionados = []
            for nome, mascara in categorias.items():
                indices = np.flatnonzero(mascara)
                if len(indices):
                    selecionados.append(int(indices[0]))
                else:
                    print(f"Sem {nome} neste teste.")
            # Para a questão final, substitua somente a lista acima pelos dois índices impressos abaixo.
            proximos = np.argsort(np.abs(probabilidades - 0.5), kind="stable")[:2].tolist()
            print("Dois índices mais próximos de 0,5:", proximos)
            for i in selecionados:
                mapa = gradcam(X_test[i])
                fig, eixos = plt.subplots(1, 3, figsize=(9, 3))
                eixos[0].imshow(X_test[i, ..., 0], cmap="gray", vmin=0, vmax=1)
                eixos[1].imshow(mapa, cmap="jet", vmin=0, vmax=1)
                eixos[2].imshow(X_test[i, ..., 0], cmap="gray", vmin=0, vmax=1)
                eixos[2].imshow(mapa, cmap="jet", vmin=0, vmax=1, alpha=0.4)
                for eixo, titulo in zip(eixos, ["Imagem", "Grad-CAM: pneumonia", "Sobreposição"]):
                    eixo.set_title(titulo)
                    eixo.axis("off")
                fig.suptitle(f"Índice {i} | real: {nomes[y_test[i]]} | previsto: {nomes[predicoes[i]]} | P(pneumonia)={probabilidades[i]:.3f}")
                plt.tight_layout()
                plt.show()
        """),
        cell("markdown", """
            ## Atividade e entrega

            1. Informe as contagens e a proporção de pneumonia em cada divisão. Explique suas funções e o desbalanceamento.
            2. Identifique a melhor época pela validação e comente as curvas. O que elas permitem dizer sobre sobreajuste em apenas cinco épocas?
            3. Registre VN, FP, FN, VP, sensibilidade, especificidade, precisão, F1, acurácia e ROC-AUC. Compare a acurácia com a referência majoritária. Qual erro o modelo comete mais?
            4. Compare os mapas de um acerto e um erro, quando disponíveis. Informe índice, rótulos e saída do modelo. Discuta bordas, regiões difusas e possíveis atalhos sem afirmar localização de lesão.
            5. Duplique a célula 7 e, na cópia, insira `selecionados = proximos` imediatamente antes de `for i in selecionados:`. Compare os dois casos mais próximos de 0,5 e suas distâncias ao limiar. Eles podem ainda estar longe de 0,5. Explique por que cor do mapa e saída probabilística respondem a perguntas diferentes. Não retreine o modelo.

            **Entrega:** um `.ipynb` com identificação, as sete células executadas, as saídas originais e da comparação final e respostas em Markdown. Conclua em 5–8 linhas com um achado e duas limitações. O [enunciado completo](../tarefas/Tarefa_5_Imagens_GradCAM_Versao_Minima.md) detalha os critérios.

            **Limites:** população pediátrica, perda de detalhes em 64 × 64 e possíveis diferenças entre instituições. Grad-CAM investiga o escore da rede; não confirma doença, causalidade ou validade clínica. O conjunto não contém máscaras de lesão para validar localização neste exercício.

            **Referências:** [MedMNIST v2](https://www.nature.com/articles/s41597-022-01721-8), [Grad-CAM — artigo original](https://openaccess.thecvf.com/content_ICCV_2017/html/Selvaraju_Grad-CAM_Visual_Explanations_ICCV_2017_paper.html) e [exemplo oficial Keras](https://keras.io/examples/vision/grad_cam/).
        """),
    ]
    for i, entry in enumerate(cells):
        entry["id"] = f"atividade5-{i:02d}"
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
    document = template.build_document(TASK, "Atividade 5 — Imagens e Grad-CAM | Versão mínima")
    document.save(TASK.with_suffix(".docx"))
    print(notebook_path)
    print(TASK.with_suffix(".docx"))


if __name__ == "__main__":
    main()
