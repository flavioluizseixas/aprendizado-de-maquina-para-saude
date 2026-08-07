"""Gera os oito notebooks a partir de fontes de texto revisáveis.

Execute novamente após alterar REPO ou algum roteiro. Os notebooks são salvos sem
saídas, de modo que o Git registre somente código e texto pedagógico.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"
REPO = "flavioluizseixas/aprendizado-de-maquina-para-saude"
UCI_DIABETES_URL = "https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators"
MEDMNIST_INFO_URL = "https://github.com/MedMNIST/MedMNIST/blob/main/medmnist/info.py"
RDATASETS_LUNG_URL = "https://vincentarelbundock.github.io/Rdatasets/doc/survival/lung.html"
INFODENGUE_API_URL = "https://info.dengue.mat.br/tutorial_api_python/locale-en"
NOTICE = (
    "Este material tem finalidade exclusivamente educacional. Os resultados não "
    "devem ser usados para diagnóstico, prognóstico, tratamento, gestão assistencial "
    "ou decisão de saúde pública sem validação adequada, análise de contexto e "
    "supervisão de profissionais qualificados."
)


def clean(source: str) -> str:
    return textwrap.dedent(source).strip()


def markdown(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": clean(source)}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": clean(source),
    }


def header(
    number: str,
    title: str,
    filename: str,
    duration: str,
    objectives: list[str],
    prerequisites: str,
    source: str,
    license_note: str,
) -> list[dict]:
    goals = "\n".join(f"- {goal}" for goal in objectives)
    colab = (
        f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{filename}"
    )
    return [
        markdown(
            f"# {number} — {title}\n\n"
            f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})\n\n"
            f"**Duração estimada:** {duration}  \n"
            f"**Pré-requisitos:** {prerequisites}\n\n"
            f"## Objetivos\n\n{goals}\n\n"
            f"## Fonte e licença\n\n{source}\n\n{license_note}\n\n"
            f"> **Uso responsável:** {NOTICE}"
        )
    ]


PACKAGE_SPECS = {
    "numpy": "numpy>=1.26,<3",
    "pandas": "pandas>=2.1,<4",
    "matplotlib": "matplotlib>=3.8,<4",
    "seaborn": "seaborn>=0.13,<1",
    "sklearn": "scikit-learn>=1.4,<2",
    "scipy": "scipy>=1.11,<2",
    "requests": "requests>=2.31,<3",
    "ucimlrepo": "ucimlrepo>=0.0.7,<1",
    "shap": "shap>=0.45,<1",
    "kneed": "kneed>=0.8,<1",
    "medmnist": "medmnist>=3,<4",
    "tensorflow": "tensorflow>=2.16,<3",
    "lifelines": "lifelines>=0.30,<1",
    "statsmodels": "statsmodels>=0.14,<1",
}


def environment(extra_modules: list[str]) -> dict:
    base_modules = ["numpy", "pandas", "matplotlib", "seaborn", "sklearn", "requests"]
    specifications = {
        name: PACKAGE_SPECS[name] for name in [*base_modules, *extra_modules]
    }
    return code(
        f"""
        # Preparação reproduzível do ambiente (a instalação ocorre só se faltar pacote).
        import importlib.util
        import os
        import subprocess
        import sys
        from pathlib import Path

        REPO = "{REPO}"
        REPO_DIR = Path("/content") / REPO.split("/")[-1]
        IN_COLAB = "google.colab" in sys.modules
        if IN_COLAB:
            command = ["git", "clone", f"https://github.com/{{REPO}}.git", str(REPO_DIR)]
            if REPO_DIR.exists():
                command = ["git", "-C", str(REPO_DIR), "pull", "--ff-only"]
            subprocess.run(command, check=True)
            os.chdir(REPO_DIR)
        else:
            candidates = [Path.cwd(), Path.cwd().parent]
            project = next((p for p in candidates if (p / "src").exists()), Path.cwd())
            os.chdir(project)

        packages = {specifications!r}
        missing = [spec for module, spec in packages.items() if importlib.util.find_spec(module) is None]
        if missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *missing])

        from src.config import RANDOM_STATE, seed_everything
        seed_everything(RANDOM_STATE)
        print(f"Ambiente pronto em {{Path.cwd()}} | Colab={{IN_COLAB}} | semente={{RANDOM_STATE}}")
        """
    )


def execution_guide(filename: str, extra: str, local_note: str = "") -> dict:
    note = f"\n\n{local_note}" if local_note else ""
    return markdown(
        f"""
        ## Onde executar

        ### Google Colab

        Use o botão **Open In Colab** no início do notebook e escolha **Executar tudo**. A célula de preparação clona ou atualiza o repositório em `/content`, instala somente as dependências ausentes e fixa a semente aleatória.

        ### Computador local

        Requisitos: Git e Python 3.10–3.13. No terminal, clone o projeto e crie um ambiente virtual:

        ```bash
        git clone https://github.com/{REPO}.git
        cd aprendizado-de-maquina-para-saude
        python -m venv .venv
        ```

        Ative-o no Windows PowerShell com `.\\.venv\\Scripts\\Activate.ps1` ou, no Linux/macOS, com `source .venv/bin/activate`.

        Instale somente as dependências deste encontro e abra o notebook a partir da raiz do repositório:

        ```bash
        python -m pip install -e ".[{extra}]"
        jupyter lab notebooks/{filename}
        ```

        Não é necessário alterar caminhos nem fazer upload de arquivos. Fora do Colab, a próxima célula usa o repositório local e o mesmo ambiente Python selecionado como kernel do Jupyter.{note}
        """
    )


def footer(
    limitations: list[str],
    activity: str,
    learnings: list[str],
    references: list[str],
    packages: tuple[str, ...],
) -> list[dict]:
    limitations_text = "\n".join(f"- {item}" for item in limitations)
    learnings_text = "\n".join(f"{i}. {item}" for i, item in enumerate(learnings, 1))
    references_text = "\n".join(f"- {item}" for item in references)
    return [
        markdown(f"## Limitações e responsabilidade\n\n{limitations_text}"),
        markdown(f"## Atividade\n\n{activity}"),
        markdown(f"## Três aprendizados principais\n\n{learnings_text}"),
        markdown(f"## Referências\n\n{references_text}"),
        markdown("## Versões das bibliotecas\n\nRegistre o ambiente junto ao resultado."),
        code(
            "from src.config import library_versions\n"
            f"library_versions({packages!r})"
        ),
    ]


def notebook_01() -> list[dict]:
    filename = "01_estatistica_descritiva.ipynb"
    cells = header(
        "01",
        "Conhecendo indicadores de saúde: estatística descritiva e visualização",
        filename,
        "60–75 minutos",
        [
            "baixar e inspecionar uma base pública",
            "distinguir variáveis numéricas, binárias e ordinais",
            "resumir distribuições e escolher gráficos adequados",
            "comparar pares de variáveis com visualizações e medidas de associação",
            "discutir autorrelato, associação e limites de generalização",
        ],
        "Python inicial, pandas e leitura de gráficos.",
        f"[CDC Diabetes Health Indicators — descrição das variáveis]({UCI_DIABETES_URL}), "
        "conjunto 891 da UCI, derivado do BRFSS. Consulte a tabela de variáveis para "
        "interpretar os códigos dos atributos, como 0 e 1.",
        "Consulte a licença CC BY 4.0 e a citação exibidas na página da UCI.",
    )
    cells += [
        markdown("## Preparação do ambiente\n\n> Como tornar a execução repetível e sem upload manual?"),
        environment(["ucimlrepo", "scipy", "statsmodels"]),
        code(
            """
            import matplotlib.pyplot as plt
            import pandas as pd
            import seaborn as sns
            from scipy.stats import chi2_contingency, pointbiserialr
            from sklearn.model_selection import train_test_split
            from statsmodels.graphics.mosaicplot import mosaic

            from src.data_loading import load_cdc_diabetes
            from src.visualization import plot_variable

            FAST_MODE = True
            SAMPLE_SIZE = 20_000 if FAST_MODE else None  # None preserva a base completa
            sns.set_theme(style="whitegrid")
            """
        ),
        markdown(
            "## Pergunta orientadora\n\n> Como se distribuem indicadores autorrelatados de saúde nesta amostra, e quais conclusões eles não sustentam?"
        ),
        markdown("## Obtenção dos dados\n\n> A fonte e a amostragem ficaram registradas?"),
        code(
            """
            data, metadata = load_cdc_diabetes(SAMPLE_SIZE, random_state=RANDOM_STATE)
            print({key: metadata.get(key) for key in ["name", "uci_id", "target", "sample_size"]})
            print(metadata["feature_types"])
            """
        ),
        markdown(
            "### Como ler os códigos usados neste encontro\n\n"
            "Os números de variáveis categóricas são **rótulos**, não quantidades. Por exemplo, "
            "`GenHlth=4` identifica uma categoria e não significa o dobro de `GenHlth=2`. "
            "Os nomes legíveis abaixo serão reutilizados nas tabelas, eixos e legendas."
        ),
        code(
            """
            outcome_labels = {0: "0 Sem diabetes", 1: "1 Pré-diabetes/diabetes"}
            high_bp_labels = {0: "0 Sem pressão alta", 1: "1 Com pressão alta"}
            health_labels = {
                1: "1 Excelente", 2: "2 Muito boa", 3: "3 Boa",
                4: "4 Regular", 5: "5 Ruim",
            }
            age_labels = {
                1: "18–24", 2: "25–29", 3: "30–34", 4: "35–39", 5: "40–44",
                6: "45–49", 7: "50–54", 8: "55–59", 9: "60–64", 10: "65–69",
                11: "70–74", 12: "75–79", 13: "80 ou mais",
            }

            label_dictionary = pd.DataFrame({
                "Variável": ["Diabetes_binary", "HighBP", "GenHlth", "Age"],
                "Significado dos códigos": [
                    "; ".join(outcome_labels.values()),
                    "; ".join(high_bp_labels.values()),
                    "; ".join(health_labels.values()),
                    "; ".join(f"{code}={label}" for code, label in age_labels.items()),
                ],
            })
            display(label_dictionary.style.hide(axis="index"))
            """
        ),
        markdown("## Inspeção\n\n> Qual é o tamanho, o tipo e a qualidade aparente da tabela?"),
        code(
            """
            display(data.head())
            print("Dimensão:", data.shape)
            display(data.dtypes.rename("tipo").to_frame().T)
            display(data.isna().sum().rename("ausências").to_frame().T)
            print("Linhas duplicadas:", data.duplicated().sum())
            """
        ),
        code(
            """
            target_percent = data["Diabetes_binary"].value_counts(normalize=True).sort_index() * 100
            target_percent.index = target_percent.index.map(outcome_labels)
            display(target_percent.rename("percentual").round(1).to_frame())
            ax = target_percent.plot.bar(
                title=f"Indicador de diabetes/pré-diabetes (n={len(data):,})",
                color=["#4C78A8", "#E45756"],
            )
            ax.set(ylabel="Percentual (%)", xlabel="")
            ax.tick_params(axis="x", rotation=0)
            plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nA barra descreve a prevalência do **indicador-alvo na amostra**. Ela não mede o desempenho de um diagnóstico e não explica por que o desfecho ocorreu."
        ),
        markdown("## Preparação\n\n> Quais resumos são adequados para distribuições possivelmente assimétricas?"),
        code(
            """
            selected = ["BMI", "Age", "GenHlth", "PhysHlth", "MentHlth", "HighBP", "Diabetes_binary"]
            description = data[selected].describe(percentiles=[0.25, 0.5, 0.75]).T
            description["IQR"] = description["75%"] - description["25%"]
            display(description[["count", "mean", "std", "25%", "50%", "75%", "IQR"]].round(2))
            """
        ),
        markdown("## Experimento\n\n> Qual gráfico responde melhor a cada tipo de variável?"),
        code(
            """
            bmi_plot_data = data.assign(**{"Índice de massa corporal (BMI)": data["BMI"]})
            plot_variable(bmi_plot_data, "Índice de massa corporal (BMI)")
            plt.show()
            """
        ),
        code(
            """
            high_bp_plot_data = data.assign(
                **{"Pressão arterial elevada": data["HighBP"].map(high_bp_labels)}
            )
            plot_variable(high_bp_plot_data, "Pressão arterial elevada", kind="categorical")
            plt.xticks(rotation=0)
            plt.show()
            """
        ),
        code(
            """
            health_plot_data = data.assign(
                **{"Saúde geral autorrelatada": data["GenHlth"].map(health_labels)}
            )
            plot_variable(health_plot_data, "Saúde geral autorrelatada", kind="ordinal")
            plt.xticks(rotation=25, ha="right")
            plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nPara BMI, mediana e IQR são resistentes a extremos. Para variáveis binárias e ordinais, percentuais preservam uma leitura mais direta. Diferenças entre grupos são associações descritivas, não efeitos causais."
        ),
        markdown("## Avaliação visual conjunta\n\n> É possível observar relações sem desenhar 250 mil pontos?"),
        code(
            """
            pair_frame = pd.DataFrame({
                "IMC": data["BMI"],
                "Saúde física ruim (dias/30)": data["PhysHlth"],
                "Saúde mental ruim (dias/30)": data["MentHlth"],
                "Indicador de diabetes": data["Diabetes_binary"].map(outcome_labels),
            })
            pair_n = min(1_000, len(data) - 1)
            pair_sample, _ = train_test_split(
                pair_frame, train_size=pair_n,
                stratify=data["Diabetes_binary"], random_state=RANDOM_STATE,
            )
            sns.pairplot(
                pair_sample, hue="Indicador de diabetes", corner=True,
                plot_kws={"alpha": 0.35, "s": 18},
            )
            plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nA amostra estratificada de até 1.000 linhas torna o `pairplot` legível e rápido, preservando aproximadamente as classes. Os eixos contêm apenas medidas numéricas; a categoria aparece na legenda com seu significado. Sobreposição indica que um atributo isolado dificilmente separa perfeitamente os grupos."
        ),
        markdown(
            "## Comparações bivariadas adequadas ao tipo\n\n"
            "O `pairplot` é útil para variáveis numéricas, mas códigos de categorias não devem ser "
            "interpretados como medidas contínuas. As estratégias seguintes preservam a natureza "
            "das variáveis.\n\n"
            "### Duas variáveis categóricas\n\n"
            "Vamos comparar a saúde geral autorrelatada (`GenHlth`) com o indicador binário "
            "`Diabetes_binary`. Percentuais condicionais evitam que o tamanho desigual das "
            "categorias domine a leitura."
        ),
        code(
            """
            health_order = list(health_labels.values())
            outcome_order = list(outcome_labels.values())

            comparison = data.assign(
                GenHlth_label=data["GenHlth"].map(health_labels),
                outcome_label=data["Diabetes_binary"].map(outcome_labels),
            )
            comparison["GenHlth_label"] = pd.Categorical(
                comparison["GenHlth_label"], categories=health_order, ordered=True
            )
            comparison["outcome_label"] = pd.Categorical(
                comparison["outcome_label"], categories=outcome_order, ordered=True
            )

            contingency = pd.crosstab(
                comparison["GenHlth_label"], comparison["outcome_label"], dropna=False
            )
            row_percent = contingency.div(contingency.sum(axis=1), axis=0) * 100
            display(contingency.rename_axis("Saúde geral"))
            display(row_percent.rename_axis("Saúde geral").round(1))
            """
        ),
        code(
            """
            fig, axes = plt.subplots(1, 2, figsize=(15, 5), constrained_layout=True)
            sns.heatmap(
                row_percent, annot=True, fmt=".1f", cmap="Blues", ax=axes[0],
                cbar_kws={"label": "% dentro da categoria de saúde geral"},
            )
            axes[0].set_title("Heatmap de percentuais condicionais")
            axes[0].set_xlabel("Indicador-alvo")
            axes[0].set_ylabel("Saúde geral autorrelatada")

            row_percent.plot.bar(
                stacked=True, ax=axes[1], color=["#4C78A8", "#E45756"], width=0.8
            )
            axes[1].set(title="Barras 100% empilhadas", xlabel="Saúde geral autorrelatada", ylabel="Percentual (%)")
            axes[1].set_ylim(0, 100)
            axes[1].legend(title="Indicador-alvo", bbox_to_anchor=(1.02, 1), loc="upper left")
            plt.show()
            """
        ),
        code(
            """
            outcome_by_health = (
                comparison.groupby("GenHlth_label", observed=False)["Diabetes_binary"]
                .agg(n="size", proporcao="mean")
            )
            outcome_by_health["percentual_desfecho"] = 100 * outcome_by_health["proporcao"]
            display(outcome_by_health[["n", "percentual_desfecho"]].round(1))

            ax = outcome_by_health["percentual_desfecho"].plot.bar(
                color="#E45756", figsize=(8, 4), title="Proporção do desfecho por categoria"
            )
            ax.set(xlabel="Saúde geral autorrelatada", ylabel="Pré-diabetes/diabetes (%)")
            ax.set_ylim(0, max(5, outcome_by_health["percentual_desfecho"].max() * 1.12))
            plt.show()
            """
        ),
        code(
            """
            mosaic_data = comparison.rename(columns={
                "GenHlth_label": "Saúde geral",
                "outcome_label": "Indicador de diabetes",
            })
            fig, _ = mosaic(
                mosaic_data.dropna(subset=["Saúde geral", "Indicador de diabetes"]),
                ["Saúde geral", "Indicador de diabetes"],
                title="Mosaico: saúde geral × indicador de diabetes",
            )
            fig.set_size_inches(11, 6)
            plt.show()
            """
        ),
        code(
            """
            chi2, p_value, degrees_freedom, expected = chi2_contingency(contingency)
            n_observations = contingency.to_numpy().sum()
            min_dimension = min(contingency.shape[0] - 1, contingency.shape[1] - 1)
            cramers_v = (chi2 / (n_observations * min_dimension)) ** 0.5

            categorical_association = pd.Series({
                "qui_quadrado": chi2,
                "graus_de_liberdade": degrees_freedom,
                "p_valor": p_value,
                "V_de_Cramer": cramers_v,
                "menor_frequencia_esperada": expected.min(),
            })
            display(categorical_association.to_frame("valor").round(4))
            """
        ),
        markdown(
            "O heatmap e as barras usam percentuais **dentro de cada categoria de saúde geral**. "
            "O mosaico acrescenta o tamanho relativo das categorias pela área dos retângulos. "
            "O teste qui-quadrado avalia incompatibilidade com independência; o V de Cramér "
            "resume a magnitude da associação entre 0 e 1. Com amostras grandes, um p-valor "
            "pequeno pode acompanhar uma associação fraca, por isso gráficos e tamanho de efeito "
            "devem ser examinados juntos."
        ),
        markdown(
            "### Uma variável categórica e uma numérica\n\n"
            "Agora comparamos o indicador categórico `Diabetes_binary` e a variável numérica "
            "`BMI`. Resumos por grupo e gráficos de distribuição são mais informativos do que "
            "uma nuvem de pontos com categorias codificadas como números."
        ),
        code(
            """
            bmi_summary = (
                comparison.groupby("outcome_label", observed=False)["BMI"]
                .agg(
                    n="size", media="mean", mediana="median", desvio_padrao="std",
                    q1=lambda values: values.quantile(0.25),
                    q3=lambda values: values.quantile(0.75),
                )
            )
            bmi_summary["IQR"] = bmi_summary["q3"] - bmi_summary["q1"]
            display(bmi_summary.round(2))

            fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
            sns.boxplot(data=comparison, x="outcome_label", y="BMI", order=outcome_order, ax=axes[0])
            axes[0].set(title="Boxplot por grupo", xlabel="Indicador-alvo", ylabel="BMI")
            sns.violinplot(
                data=comparison, x="outcome_label", y="BMI", order=outcome_order,
                inner="quartile", cut=0, ax=axes[1],
            )
            axes[1].set(title="Distribuição e quartis", xlabel="Indicador-alvo", ylabel="BMI")
            plt.show()
            """
        ),
        code(
            """
            valid_bmi = comparison[["Diabetes_binary", "BMI"]].dropna()
            r_point_biserial, p_point_biserial = pointbiserialr(
                valid_bmi["Diabetes_binary"], valid_bmi["BMI"]
            )
            grouped_bmi = valid_bmi.groupby("Diabetes_binary")["BMI"].agg(["size", "mean", "var"])
            pooled_variance = (
                ((grouped_bmi["size"] - 1) * grouped_bmi["var"]).sum()
                / (grouped_bmi["size"].sum() - len(grouped_bmi))
            )
            standardized_mean_difference = (
                (grouped_bmi.loc[1, "mean"] - grouped_bmi.loc[0, "mean"])
                / pooled_variance ** 0.5
            )

            numeric_association = pd.Series({
                "diferenca_das_medias_BMI": grouped_bmi.loc[1, "mean"] - grouped_bmi.loc[0, "mean"],
                "r_ponto_bisserial": r_point_biserial,
                "p_valor_r": p_point_biserial,
                "eta_quadrado": r_point_biserial ** 2,
                "diferenca_padronizada_medias": standardized_mean_difference,
            })
            display(numeric_association.to_frame("valor").round(4))
            """
        ),
        markdown(
            "A correlação ponto-bisserial quantifica a associação entre uma categoria binária e "
            "uma medida numérica; η² é seu quadrado neste caso e resume a fração da variabilidade "
            "amostral situada entre os dois grupos. A diferença padronizada de médias facilita a "
            "comparação de magnitude na escala do desvio-padrão. Sinal, p-valor e tamanho de efeito "
            "dependem da codificação e não controlam confundimento nem demonstram causalidade."
        ),
    ]
    cells += footer(
        [
            "Os indicadores do BRFSS incluem autorrelato, sujeito a memória e classificação incorreta.",
            "Amostragem, representação de grupos e desbalanceamento limitam a generalização.",
            "Uma associação visual não estabelece causalidade nem substitui avaliação clínica.",
        ],
        "Escolha uma variável categórica diferente de `GenHlth` e repita a comparação com o desfecho. Depois escolha uma variável numérica diferente de `BMI`, compare os grupos e relate: (1) percentuais condicionais; (2) tamanho de efeito; (3) o que não pode ser concluído.",
        [
            "O tipo da variável orienta o resumo e o gráfico.",
            "Percentuais condicionais e distribuições por grupo evitam tratar códigos como medidas contínuas.",
            "Gráficos, testes e tamanhos de efeito descrevem associação, mas não provam causalidade.",
        ],
        [
            "[UCI — CDC Diabetes Health Indicators](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)",
            "[CDC — BRFSS](https://www.cdc.gov/brfss/)",
            "[statsmodels — mosaic plot](https://www.statsmodels.org/stable/generated/statsmodels.graphics.mosaicplot.mosaic.html)",
            "[SciPy — chi2_contingency](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.contingency.chi2_contingency.html)",
        ],
        ("numpy", "pandas", "matplotlib", "seaborn", "scipy", "scikit-learn", "statsmodels", "ucimlrepo"),
    )
    return cells


def notebook_02() -> list[dict]:
    filename = "02_aprendizado_supervisionado.ipynb"
    cells = header(
        "02",
        "Predição, desempenho e explicabilidade em classificação",
        filename,
        "90–110 minutos",
        [
            "construir um pipeline sem vazamento",
            "avaliar regressão logística e Random Forest somente no teste reservado",
            "interpretar sensibilidade, especificidade, ROC-AUC e PR-AUC",
            "interpretar odds ratios ajustadas com IC95% e SHAP na regressão logística",
            "investigar uma Random Forest separadamente com permutação e SHAP",
        ],
        "Notebook 01 ou noções de pandas e classificação binária.",
        f"[CDC Diabetes Health Indicators — descrição das variáveis]({UCI_DIABETES_URL}), "
        "conjunto 891 da UCI, derivado do BRFSS. Consulte a tabela de variáveis para "
        "interpretar os códigos dos atributos, como 0 e 1.",
        "Fonte UCI sob CC BY 4.0; cite o conjunto e sua publicação.",
    )
    cells += [
        execution_guide(filename, "supervised"),
        markdown("## Preparação do ambiente\n\n> Como fixar dependências e semente?"),
        environment(["ucimlrepo", "shap", "statsmodels"]),
        code(
            """
            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd
            import seaborn as sns
            import shap
            import statsmodels.api as sm
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.inspection import permutation_importance
            from sklearn.impute import SimpleImputer
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import ConfusionMatrixDisplay
            from sklearn.model_selection import train_test_split
            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import StandardScaler
            from src.data_loading import load_cdc_diabetes
            from src.evaluation import classification_report_health, plot_classification_curves, report_frame
            """
        ),
        code(
            """
            FAST_MODE = True
            SAMPLE_SIZE = 30_000 if FAST_MODE else 40_000

            TARGET_NAME = "Indicador de diabetes"
            target_labels = {0: "0 Sem diabetes", 1: "1 Pré-diabetes/diabetes"}
            feature_labels = {
                "HighBP": "Pressão alta",
                "HighChol": "Colesterol alto",
                "CholCheck": "Verificação de colesterol (5 anos)",
                "BMI": "IMC",
                "Smoker": "Fumou ao menos 100 cigarros",
                "Stroke": "Histórico de AVC",
                "HeartDiseaseorAttack": "Doença cardíaca ou infarto",
                "PhysActivity": "Atividade física (30 dias)",
                "Fruits": "Consumo diário de frutas",
                "Veggies": "Consumo diário de vegetais",
                "HvyAlcoholConsump": "Consumo elevado de álcool",
                "AnyHealthcare": "Cobertura de saúde",
                "NoDocbcCost": "Sem consulta por custo",
                "GenHlth": "Saúde geral (1 excelente–5 ruim)",
                "MentHlth": "Saúde mental ruim (dias/30)",
                "PhysHlth": "Saúde física ruim (dias/30)",
                "DiffWalk": "Dificuldade para caminhar",
                "Sex": "Sexo",
                "Age": "Faixa etária",
                "Education": "Escolaridade",
                "Income": "Faixa de renda",
            }

            data, metadata = load_cdc_diabetes(SAMPLE_SIZE, random_state=RANDOM_STATE)
            X = data.drop(columns="Diabetes_binary").rename(columns=feature_labels)
            y = data["Diabetes_binary"].astype(int)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
            )
            print("Treino:", X_train.shape, "| teste reservado:", X_test.shape)
            """
        ),
        markdown(
            """
            ### Dicionário de variáveis e rótulos

            A classe positiva (`1`) reúne **pré-diabetes ou diabetes**; portanto, o modelo não separa essas duas condições. Nos atributos binários, `0` e `1` representam categorias documentadas na fonte, não intensidades. Variáveis como saúde geral, idade, escolaridade e renda usam códigos ordinais.

            A tabela seguinte vem diretamente dos metadados da UCI. Consulte também a [página da base](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators) antes de interpretar qualquer atributo.
            """
        ),
        code(
            """
            coding_summary = pd.DataFrame({
                "Grupo": [
                    "Desfecho", "Indicadores binários", "Sexo", "Saúde geral", "Demográficos ordinais"
                ],
                "Como interpretar": [
                    "0=sem diabetes; 1=pré-diabetes ou diabetes",
                    "0=não/ausente; 1=sim/presente (exceto a variável Sex)",
                    "Sex: 0=feminino; 1=masculino",
                    "1=excelente; 2=muito boa; 3=boa; 4=regular; 5=ruim",
                    "Age, Education e Income são faixas ordenadas; consulte os níveis na fonte",
                ],
            })
            display(coding_summary.style.hide(axis="index"))

            variable_dictionary = metadata.get("variables")
            if isinstance(variable_dictionary, pd.DataFrame):
                dictionary_columns = [
                    column for column in ["name", "role", "type", "description", "units"]
                    if column in variable_dictionary.columns
                ]
                variable_dictionary = variable_dictionary[dictionary_columns].copy()
                translated_names = {**feature_labels, "Diabetes_binary": TARGET_NAME}
                if "name" in variable_dictionary:
                    variable_dictionary.insert(
                        1, "nome_no_notebook",
                        variable_dictionary["name"].map(translated_names).fillna(variable_dictionary["name"]),
                    )
                display(variable_dictionary.rename(columns={
                    "name": "nome_original", "role": "papel", "type": "tipo",
                    "description": "descrição_UCI", "units": "unidade",
                }))

            class_distribution = pd.DataFrame({
                "n": y.value_counts().sort_index(),
                "percentual": 100 * y.value_counts(normalize=True).sort_index(),
            })
            class_distribution.index = class_distribution.index.map(target_labels)
            display(class_distribution.round(1).rename_axis("classe do desfecho"))
            """
        ),
        markdown(
            "## Pergunta orientadora\n\n> Um modelo consegue ordenar pessoas com e sem o indicador-alvo, e quais erros aparecem quando escolhemos um limiar?"
        ),
        markdown("## Inspeção de correlações\n\n> Quais associações monotônicas merecem atenção antes do modelo?"),
        code(
            """
            modeling_data = X.assign(**{TARGET_NAME: y})
            corr = modeling_data.corr(method="spearman", numeric_only=True)
            target_corr = corr[TARGET_NAME].drop(TARGET_NAME)
            top_corr = target_corr.abs().sort_values(ascending=False).head(12).index
            display(target_corr.loc[top_corr].sort_values(key=abs, ascending=False).rename("Spearman").to_frame())
            plt.figure(figsize=(10, 7))
            sns.heatmap(corr.loc[[*top_corr, TARGET_NAME], [*top_corr, TARGET_NAME]], cmap="vlag", center=0)
            plt.title("Correlação de Spearman entre os principais atributos")
            plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nSpearman resume associação monotônica. Códigos ordinais, não linearidade e variáveis omitidas afetam a leitura; correlação não demonstra causalidade."
        ),
        markdown(
            """
            ## Modelo preditivo de regressão logística

            > Como ajustar o pré-processamento somente no treinamento e avaliar apenas no teste reservado?

            O conjunto de treinamento serve para ajustar o classificador. Nenhuma medida de desempenho de re-substituição no treinamento será exibida, pois ela tende a ser otimista. Todas as métricas seguintes serão calculadas exclusivamente no teste.
            """
        ),
        code(
            """
            pipeline = Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1_000, class_weight="balanced", random_state=RANDOM_STATE)),
            ])
            """
        ),
        markdown(
            """
            ## Avaliação da regressão logística no teste

            > O que acontece no conjunto que não participou do ajuste?

            Para positivos (VP), negativos (VN), falsos positivos (FP) e falsos negativos (FN):

            - sensibilidade = VP / (VP + FN);
            - especificidade = VN / (VN + FP);
            - precisão = VP / (VP + FP);
            - F1 = 2 × precisão × sensibilidade / (precisão + sensibilidade).
            """
        ),
        code(
            """
            pipeline.fit(X_train, y_train)
            y_prob = pipeline.predict_proba(X_test)[:, 1]
            y_pred = (y_prob >= 0.5).astype(int)
            report = classification_report_health(y_test, y_pred, y_prob)
            display(report_frame(report).round(3))
            ConfusionMatrixDisplay.from_predictions(
                y_test, y_pred,
                display_labels=[target_labels[0], target_labels[1]], cmap="Blues",
            )
            plt.title("Matriz de confusão — teste")
            plt.show()
            plot_classification_curves(y_test, y_prob); plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nUm falso negativo é um positivo no conjunto que o limiar não sinalizou; um falso positivo é um negativo sinalizado. O custo de cada erro depende do contexto — não é decidido pela ROC-AUC. Alterar 0,5 muda esse equilíbrio."
        ),
        markdown(
            """
            ## Explicabilidade da regressão logística

            > Quais associações condicionais o modelo estima e como elas aparecem em uma previsão individual?

            O pipeline anterior tem finalidade **preditiva**: usa regularização, pesos de classe e padronização. Esses recursos são úteis para previsão, mas seus coeficientes não devem ser apresentados como estimativas epidemiológicas clássicas.

            Para estimar *odds ratios* ajustadas, ajustaremos um segundo modelo logístico, agora inferencial:

            - sem `class_weight` e sem penalização;
            - variáveis binárias mantidas como 0/1, com 0 como referência;
            - IMC e dias de saúde ruim mantidos nas unidades originais;
            - saúde geral, idade, escolaridade e renda tratadas como categorias, sem supor distâncias iguais entre os níveis;
            - nível 1 usado como referência nas variáveis categóricas;
            - IC95% robustos HC3 para representar a incerteza amostral sob as hipóteses declaradas.

            Como o objetivo aqui é estimar associações, e não medir generalização preditiva, o modelo usa toda a amostra analítica. Cada OR é ajustada simultaneamente pelas demais variáveis do quadro.
            """
        ),
        code(
            """
            binary_features = [
                "Pressão alta", "Colesterol alto", "Verificação de colesterol (5 anos)",
                "Fumou ao menos 100 cigarros", "Histórico de AVC",
                "Doença cardíaca ou infarto", "Atividade física (30 dias)",
                "Consumo diário de frutas", "Consumo diário de vegetais",
                "Consumo elevado de álcool", "Cobertura de saúde", "Sem consulta por custo",
                "Dificuldade para caminhar", "Sexo",
            ]
            continuous_features = [
                "IMC", "Saúde mental ruim (dias/30)", "Saúde física ruim (dias/30)",
            ]
            category_levels = {
                "Saúde geral (1 excelente–5 ruim)": list(range(1, 6)),
                "Faixa etária": list(range(1, 14)),
                "Escolaridade": list(range(1, 7)),
                "Faixa de renda": list(range(1, 9)),
            }

            epidemiology_data = X.assign(**{TARGET_NAME: y}).dropna().copy()
            print(
                f"Amostra analítica completa: {len(epidemiology_data):,} de {len(X):,} participantes; "
                f"eventos: {epidemiology_data[TARGET_NAME].sum():,}."
            )

            epi_predictors = epidemiology_data[continuous_features + binary_features].astype(float).copy()
            for feature, levels in category_levels.items():
                observed = set(epidemiology_data[feature].astype(int).unique())
                unexpected = observed.difference(levels)
                if unexpected:
                    raise ValueError(f"Códigos inesperados em {feature}: {sorted(unexpected)}")
                coded = pd.Series(
                    pd.Categorical(
                        epidemiology_data[feature].astype(int),
                        categories=levels,
                        ordered=True,
                    ),
                    index=epidemiology_data.index,
                    name=feature,
                )
                dummies = pd.get_dummies(
                    coded, prefix=feature, prefix_sep=" = ", drop_first=True, dtype=float
                )
                epi_predictors = pd.concat([epi_predictors, dummies], axis=1)

            epi_design = sm.add_constant(epi_predictors, has_constant="add").astype(float)
            epi_outcome = epidemiology_data[TARGET_NAME].astype(int)
            epi_result = sm.GLM(
                epi_outcome, epi_design, family=sm.families.Binomial()
            ).fit(cov_type="HC3")

            references = pd.DataFrame({
                "variáveis": [
                    "Binárias (exceto Sexo)", "Sexo", "Saúde geral",
                    "Faixa etária", "Escolaridade", "Faixa de renda", "Contínuas",
                ],
                "contraste da OR": [
                    "1 (sim/presente) versus 0 (não/ausente)",
                    "1 (masculino) versus 0 (feminino)",
                    "cada nível versus 1 (excelente)",
                    "cada faixa versus faixa 1", "cada nível versus nível 1",
                    "cada faixa versus faixa 1", "aumento de uma unidade original",
                ],
            })
            display(references.style.hide(axis="index"))
            """
        ),
        code(
            """
            confidence = epi_result.conf_int()
            epi_or = pd.DataFrame({
                "coeficiente (log-odds)": epi_result.params,
                "OR ajustada": np.exp(epi_result.params),
                "IC95% inferior": np.exp(confidence[0]),
                "IC95% superior": np.exp(confidence[1]),
                "valor-p": epi_result.pvalues,
            }).drop(index="const")
            epi_or.index.name = "atributo ou contraste (referência omitida)"
            display(epi_or.round({
                "coeficiente (log-odds)": 3, "OR ajustada": 3,
                "IC95% inferior": 3, "IC95% superior": 3, "valor-p": 4,
            }))

            or_plot = (
                epi_or.assign(distancia_de_OR_1=np.abs(epi_or["coeficiente (log-odds)"]))
                .nlargest(15, "distancia_de_OR_1")
                .sort_values("OR ajustada")
            )
            y_positions = np.arange(len(or_plot))
            plt.figure(figsize=(10, 7))
            plt.errorbar(
                or_plot["OR ajustada"], y_positions,
                xerr=np.vstack([
                    or_plot["OR ajustada"] - or_plot["IC95% inferior"],
                    or_plot["IC95% superior"] - or_plot["OR ajustada"],
                ]),
                fmt="o", capsize=3,
            )
            plt.yticks(y_positions, or_plot.index)
            plt.axvline(1, color="black", linestyle="--", linewidth=1)
            plt.xscale("log")
            plt.xlabel("Odds ratio ajustada (escala logarítmica) e IC95% robusto")
            plt.title("Associações condicionais mais distantes de OR = 1")
            plt.tight_layout()
            plt.show()
            """
        ),
        markdown(
            """
            ### Como interpretar as odds ratios

            `exp(coeficiente)` é a razão de *odds* associada ao contraste indicado, mantendo as demais variáveis constantes. OR = 1,25 representa *odds* 25% maiores; não significa probabilidade ou risco 25% maior. Se o IC95% inclui 1, os dados são compatíveis também com ausência de associação nesse nível de incerteza.

            Os valores-p são exibidos para transparência, mas magnitude, intervalo de confiança, plausibilidade e pergunta científica devem orientar a leitura — não uma regra automática de significância.
            """
        ),
        markdown(
            """
            ### SHAP da regressão logística

            SHAP complementa a OR: a OR resume um contraste global do modelo, enquanto SHAP mostra quanto o valor observado de cada atributo desloca uma previsão em relação à saída média. No modelo logístico linear, essas contribuições são aditivas em **log-odds**. Valores SHAP positivos aumentam a log-odds estimada da classe 1; valores negativos a reduzem.
            """
        ),
        code(
            """
            epi_features = epi_design.drop(columns="const")
            epi_background = epi_features.sample(
                min(500, len(epi_features)), random_state=RANDOM_STATE
            )
            epi_masker = shap.maskers.Independent(
                epi_background, max_samples=len(epi_background)
            )
            epi_shap_sample = epi_features.sample(
                min(300, len(epi_features)), random_state=RANDOM_STATE + 1
            )
            epi_explainer = shap.LinearExplainer(
                (
                    epi_result.params[epi_features.columns].to_numpy(),
                    float(epi_result.params["const"]),
                ),
                epi_masker,
            )
            epi_shap_values = epi_explainer(epi_shap_sample)
            shap.plots.bar(epi_shap_values, max_display=12)
            shap.plots.beeswarm(epi_shap_values, max_display=12)
            """
        ),
        markdown(
            """
            A OR e o SHAP descrevem o mesmo modelo por ângulos diferentes. Nenhum deles identifica efeito causal. Variáveis correlacionadas podem dividir ou deslocar contribuições, e as dummies devem ser interpretadas contra a categoria de referência omitida.

            ## Random Forest: avaliação preditiva no teste

            > Como o segundo classificador se comporta em dados que não participaram do ajuste?

            A Random Forest abaixo é um **segundo modelo**. Primeiro ela é ajustada somente no treinamento e avaliada no teste reservado. Assim como na regressão logística, não exibiremos desempenho no conjunto usado para o ajuste.
            """
        ),
        code(
            """
            forest_imputer = SimpleImputer(strategy="median")
            X_train_i = pd.DataFrame(
                forest_imputer.fit_transform(X_train), columns=X.columns, index=X_train.index
            )
            X_test_i = pd.DataFrame(
                forest_imputer.transform(X_test), columns=X.columns, index=X_test.index
            )
            forest_evaluation = RandomForestClassifier(
                n_estimators=150,
                class_weight="balanced_subsample",
                n_jobs=-1,
                random_state=RANDOM_STATE,
            )
            forest_evaluation.fit(X_train_i, y_train)
            forest_test_prob = forest_evaluation.predict_proba(X_test_i)[:, 1]
            forest_test_pred = (forest_test_prob >= 0.5).astype(int)
            forest_test_report = classification_report_health(
                y_test, forest_test_pred, forest_test_prob
            )
            display(report_frame(forest_test_report).round(3))
            ConfusionMatrixDisplay.from_predictions(
                y_test, forest_test_pred,
                display_labels=[target_labels[0], target_labels[1]], cmap="Greens",
            )
            plt.title("Random Forest: matriz de confusão — teste")
            plt.show()
            plot_classification_curves(y_test, forest_test_prob)
            plt.show()
            """
        ),
        markdown(
            """
            ### Como interpretar o desempenho

            As medidas, a matriz de confusão e as curvas acima usam **somente o teste reservado**. Elas podem ser comparadas às da regressão logística porque os dois classificadores receberam a mesma divisão. Nenhuma métrica de desempenho do treinamento é mostrada.

            ### Importância por permutação no teste

            A permutação usa a Random Forest ajustada no treinamento e o teste reservado. Assim, mede quanto cada atributo contribui para a capacidade de generalização observada, sem reutilizar os dados de ajuste.
            """
        ),
        code(
            """
            importance = permutation_importance(
                forest_evaluation, X_test_i, y_test,
                scoring="roc_auc", n_repeats=3,
                random_state=RANDOM_STATE, n_jobs=-1,
            )
            permutation = pd.Series(importance.importances_mean, index=X.columns).nlargest(12)
            permutation.sort_values().plot.barh(
                title="Importância por permutação no teste (ROC-AUC)"
            )
            plt.xlabel("Queda média na ROC-AUC do teste")
            plt.show()
            """
        ),
        markdown(
            """
            ### SHAP do modelo final reajustado

            Depois de concluir a avaliação, a Random Forest e o imputador são reajustados na amostra completa. O SHAP abaixo descreve esse **modelo final**, que é diferente do modelo usado para obter as métricas e a importância por permutação no teste. Não calculamos novas medidas de desempenho na amostra completa.
            """
        ),
        code(
            """
            full_imputer = SimpleImputer(strategy="median")
            X_full_i = pd.DataFrame(
                full_imputer.fit_transform(X), columns=X.columns, index=X.index
            )
            forest = RandomForestClassifier(
                n_estimators=150,
                class_weight="balanced_subsample",
                n_jobs=-1,
                random_state=RANDOM_STATE,
            )
            forest.fit(X_full_i, y)

            shap_sample = X_full_i.sample(min(300, len(X_full_i)), random_state=RANDOM_STATE)
            shap_background = X_full_i.sample(
                min(100, len(X_full_i)), random_state=RANDOM_STATE + 1
            )
            explainer = shap.Explainer(forest, shap_background)
            shap_values = explainer(shap_sample)
            if shap_values.values.ndim == 3:  # saída por classe em versões recentes
                shap_values = shap_values[..., 1]
            shap.plots.bar(shap_values, max_display=12)
            shap.plots.beeswarm(shap_values, max_display=12)
            """
        ),
        code(
            """
            mean_absolute_shap = np.abs(shap_values.values).mean(axis=0)
            main_feature = shap_values.feature_names[int(np.argmax(mean_absolute_shap))]
            shap.plots.scatter(shap_values[:, main_feature])
            """
        ),
        markdown(
            "### Como interpretar a explicabilidade\n\nA permutação descreve a dependência da ROC-AUC no teste em relação a cada atributo. O SHAP decompõe as saídas da Random Forest final, reajustada na amostra completa. As duas análises respondem a perguntas diferentes e nenhuma delas diz que mudar o atributo causará mudança de saúde."
        ),
    ]
    cells += footer(
        [
            "O alvo e os atributos incluem autorrelato e não representam um diagnóstico produzido pelo notebook.",
            "Desbalanceamento, limiar, subgrupos e mudança de população alteram os erros.",
            "As OR são associações condicionais: ajustar todas as variáveis não substitui uma pergunta causal, um DAG e a definição prévia de confundidores.",
            "Os IC95% HC3 não incorporam pesos, estratos ou conglomerados do desenho amostral complexo do BRFSS; não são estimativas populacionais nacionais.",
            "O modelo supõe efeito linear na log-odds para IMC e dias de saúde ruim e não inclui interações; essas hipóteses precisam ser avaliadas em uma análise epidemiológica real.",
            "A importância por permutação no teste descreve a dependência do desempenho do modelo avaliado e pode subestimar atributos correlacionados.",
            "SHAP pode refletir correlações, vieses e atalhos do modelo; não é explicação causal.",
        ],
        "Escolha uma exposição, interprete sua OR ajustada e IC95%, e compare essa leitura global com sua distribuição no gráfico SHAP. Depois teste limiares 0,3; 0,5; 0,7 no modelo preditivo e compare sensibilidade e especificidade.",
        [
            "O pipeline protege o teste durante o ajuste; ROC-AUC não substitui matriz de confusão nem PR-AUC.",
            "Desempenho e permutação da Random Forest usam o teste; a amostra completa é usada no GLM epidemiológico e no SHAP do modelo final reajustado.",
            "OR e SHAP respondem a perguntas diferentes, a Random Forest é um modelo separado e nenhuma dessas explicações demonstra causalidade.",
        ],
        [
            "[UCI — CDC Diabetes Health Indicators](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)",
            "[statsmodels — Generalized Linear Models](https://www.statsmodels.org/stable/glm.html)",
            "[SHAP — LinearExplainer](https://shap.readthedocs.io/en/stable/generated/shap.LinearExplainer.html)",
            "[scikit-learn — model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)",
        ],
        ("numpy", "pandas", "scikit-learn", "matplotlib", "seaborn", "shap", "statsmodels", "ucimlrepo"),
    )
    return cells


def notebook_03() -> list[dict]:
    filename = "03_aprendizado_nao_supervisionado.ipynb"
    cells = header(
        "03",
        "Descobrindo perfis: K-means, elbow e PCA",
        filename,
        "60–75 minutos",
        [
            "padronizar atributos e aplicar K-means",
            "comparar elbow e silhouette",
            "projetar os grupos em dois componentes principais",
            "caracterizar clusters sem chamá-los de fenótipos clínicos",
        ],
        "Notebook 01 e noções de distância.",
        f"[CDC Diabetes Health Indicators — descrição das variáveis]({UCI_DIABETES_URL}), "
        "conjunto 891 da UCI. Consulte a tabela de variáveis para interpretar os códigos "
        "dos atributos, como 0 e 1. O alvo será excluído do agrupamento.",
        "Fonte UCI sob CC BY 4.0; cite o conjunto e sua publicação.",
    )
    cells += [
        execution_guide(filename, "clustering"),
        markdown("## Preparação do ambiente\n\n> Como garantir a mesma inicialização?"),
        environment(["ucimlrepo", "kneed"]),
        code(
            """
            import matplotlib.pyplot as plt
            import pandas as pd
            import seaborn as sns
            from sklearn.cluster import KMeans
            from sklearn.decomposition import PCA
            from sklearn.impute import SimpleImputer
            from sklearn.preprocessing import StandardScaler

            from src.clustering import choose_k, evaluate_kmeans_range
            from src.data_loading import load_cdc_diabetes

            FAST_MODE = True
            attributes = ["BMI", "Age", "GenHlth", "PhysHlth", "MentHlth", "Education", "Income"]
            feature_labels = {
                "BMI": "IMC",
                "Age": "Faixa etária (1–13)",
                "GenHlth": "Saúde geral (1 excelente–5 ruim)",
                "PhysHlth": "Saúde física ruim (dias/30)",
                "MentHlth": "Saúde mental ruim (dias/30)",
                "Education": "Escolaridade (1–6)",
                "Income": "Faixa de renda (1–8)",
            }
            TARGET_NAME = "Indicador de diabetes"
            target_labels = {0: "0 Sem diabetes", 1: "1 Pré-diabetes/diabetes"}
            data, metadata = load_cdc_diabetes(
                15_000 if FAST_MODE else 40_000, random_state=RANDOM_STATE
            )
            """
        ),
        markdown(
            """
            ### Dicionário das variáveis usadas

            O agrupamento usa sete atributos e exclui `Diabetes_binary`. `Age`, `GenHlth`, `Education` e `Income` são códigos ordinais; as distâncias entre níveis são uma simplificação analítica. O desfecho só será consultado depois, para descrição externa.
            """
        ),
        code(
            """
            coding_summary = pd.DataFrame({
                "atributo_no_notebook": list(feature_labels.values()) + [TARGET_NAME],
                "nome_original": attributes + ["Diabetes_binary"],
                "interpretação": [
                    "Índice de massa corporal",
                    "Faixa etária ordenada de 1 a 13",
                    "1=excelente; 2=muito boa; 3=boa; 4=regular; 5=ruim",
                    "Número de dias de saúde física ruim nos últimos 30 dias",
                    "Número de dias de saúde mental ruim nos últimos 30 dias",
                    "Faixa de escolaridade ordenada de 1 a 6",
                    "Faixa de renda ordenada de 1 a 8",
                    "0=sem diabetes; 1=pré-diabetes ou diabetes (avaliação externa)",
                ],
            })
            display(coding_summary.style.hide(axis="index"))

            variable_dictionary = metadata.get("variables")
            if isinstance(variable_dictionary, pd.DataFrame) and "name" in variable_dictionary:
                selected_dictionary = variable_dictionary[
                    variable_dictionary["name"].isin(attributes + ["Diabetes_binary"])
                ].copy()
                available = [
                    column for column in ["name", "role", "type", "description", "units"]
                    if column in selected_dictionary
                ]
                display(selected_dictionary[available].rename(columns={
                    "name": "nome_original", "role": "papel", "type": "tipo",
                    "description": "descrição_UCI", "units": "unidade",
                }))
            """
        ),
        markdown(
            "## Pergunta orientadora\n\n> Existem agrupamentos matemáticos estáveis nesses indicadores, e como descrevê-los sem transformá-los em classes clínicas?"
        ),
        markdown("## Inspeção e preparação\n\n> O alvo entrou por engano no agrupamento? As escalas são comparáveis?"),
        code(
            """
            assert "Diabetes_binary" not in attributes
            X = data[attributes].rename(columns=feature_labels)
            imputer = SimpleImputer(strategy="median")
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(imputer.fit_transform(X))
            print("Matriz do agrupamento:", X_scaled.shape, "| alvo excluído:", "Diabetes_binary" not in attributes)
            """
        ),
        markdown("## Experimento: quantos clusters?\n\n> O cotovelo e o silhouette apontam para a mesma escolha?"),
        code(
            """
            results = evaluate_kmeans_range(X_scaled, range(2, 9), random_state=RANDOM_STATE)
            chosen_k, criterion = choose_k(results)
            display(results.round(3))
            print(f"k escolhido = {chosen_k} ({criterion})")
            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            results.plot(x="k", y="inércia", marker="o", ax=axes[0], legend=False, title="Elbow")
            results.plot(x="k", y="silhouette", marker="o", ax=axes[1], legend=False, title="Silhouette")
            plt.tight_layout(); plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nInércia sempre cai quando k cresce; buscamos uma mudança de inclinação. Silhouette favorece grupos compactos e separados. A escolha continua sendo uma decisão analítica, não uma descoberta de doenças."
        ),
        markdown("## PCA e visualização\n\n> Quanta informação dois eixos preservam?"),
        code(
            """
            kmeans = KMeans(n_clusters=chosen_k, n_init=10, random_state=RANDOM_STATE)
            clusters = kmeans.fit_predict(X_scaled)
            pca = PCA(n_components=2, random_state=RANDOM_STATE)
            coordinates = pca.fit_transform(X_scaled)
            centers_2d = pca.transform(kmeans.cluster_centers_)
            print("Variância explicada:", pca.explained_variance_ratio_.round(3), "| total:", pca.explained_variance_ratio_.sum().round(3))
            """
        ),
        code(
            """
            plot_data = pd.DataFrame(coordinates, columns=["PC1", "PC2"])
            plot_data["Cluster"] = [f"Cluster {value}" for value in clusters]
            sample = plot_data.sample(min(5_000, len(plot_data)), random_state=RANDOM_STATE)
            sns.scatterplot(data=sample, x="PC1", y="PC2", hue="Cluster", alpha=0.45, s=18, palette="tab10")
            plt.scatter(centers_2d[:, 0], centers_2d[:, 1], marker="X", s=180, c="black", label="centróides")
            plt.title(f"PCA dos clusters (amostra visual; n total={len(data):,})")
            plt.legend(); plt.show()
            """
        ),
        markdown("## Avaliação e perfis\n\n> O que caracteriza cada grupo na escala original e padronizada?"),
        code(
            """
            profiled = X.copy()
            profiled[TARGET_NAME] = data["Diabetes_binary"].to_numpy()
            profiled["Cluster"] = [f"Cluster {value}" for value in clusters]
            profile = profiled.groupby("Cluster")[list(X.columns)].mean()
            prevalence = profiled.groupby("Cluster")[TARGET_NAME].agg(["mean", "count"])
            prevalence["mean"] *= 100
            display(profile.round(2))
            display(prevalence.rename(columns={"mean": "prevalência externa (%)", "count": "n"}).round(1))
            standardized_profile = (
                pd.DataFrame(X_scaled, columns=X.columns)
                .assign(Cluster=[f"Cluster {value}" for value in clusters])
                .groupby("Cluster").mean()
            )
            sns.heatmap(standardized_profile, cmap="vlag", center=0, annot=True, fmt=".1f")
            plt.title("Perfil médio padronizado por cluster"); plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nO alvo foi consultado **depois** apenas como avaliação externa. Diferenças de prevalência não tornam o cluster um diagnóstico. PCA perde informação, portanto separação ou sobreposição no plano não resume todo o espaço."
        ),
    ]
    cells += footer(
        [
            "K-means depende de escala, inicialização, forma aproximadamente esférica e escolha de k.",
            "PCA com dois componentes omite parte da variabilidade.",
            "Clusters são construções matemáticas nesta amostra; chamá-los de fenótipos exigiria validação clínica externa.",
        ],
        "Remova um atributo, repita elbow/silhouette e compare os perfis. Explique por que a solução mudou ou permaneceu semelhante.",
        [
            "Padronizar evita que uma unidade domine as distâncias.",
            "Elbow e silhouette oferecem evidências complementares, não uma verdade única.",
            "O alvo só pode entrar depois, como descrição externa.",
        ],
        [
            "[UCI — CDC Diabetes Health Indicators](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)",
            "[scikit-learn — clustering](https://scikit-learn.org/stable/modules/clustering.html)",
            "[scikit-learn — PCA](https://scikit-learn.org/stable/modules/decomposition.html#pca)",
        ],
        ("numpy", "pandas", "scikit-learn", "matplotlib", "seaborn", "kneed", "ucimlrepo"),
    )
    return cells


def notebook_04() -> list[dict]:
    filename = "04_comparacao_modelos_hiperparametros.ipynb"
    cells = header(
        "04",
        "Comparando modelos sem escrever muito código",
        filename,
        "75–90 minutos",
        [
            "comparar quatro algoritmos nas mesmas partições",
            "construir um leaderboard com múltiplas métricas e tempo",
            "ajustar hiperparâmetros somente no treino",
            "comparar o modelo padrão e ajustado no teste intacto",
        ],
        "Notebook 02 e noções de validação cruzada.",
        f"[CDC Diabetes Health Indicators — descrição das variáveis]({UCI_DIABETES_URL}), "
        "conjunto 891 da UCI. Consulte a tabela de variáveis para interpretar os códigos "
        "dos atributos, como 0 e 1.",
        "Fonte UCI sob CC BY 4.0; cite o conjunto e sua publicação.",
    )
    cells += [
        execution_guide(filename, "model-comparison"),
        markdown("## Preparação do ambiente\n\n> Como reutilizar uma interface pequena e transparente?"),
        environment(["ucimlrepo"]),
        code(
            """
            import matplotlib.pyplot as plt
            import pandas as pd
            from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay
            from sklearn.model_selection import train_test_split

            from src.data_loading import load_cdc_diabetes
            from src.evaluation import classification_report_health
            from src.model_selection import (
                compare_classifiers, get_default_classifiers,
                tune_classifier, tuning_results_frame,
            )

            FAST_MODE = True
            TARGET_NAME = "Indicador de diabetes"
            target_labels = {0: "0 Sem diabetes", 1: "1 Pré-diabetes/diabetes"}
            feature_labels = {
                "HighBP": "Pressão alta", "HighChol": "Colesterol alto",
                "CholCheck": "Verificação de colesterol (5 anos)", "BMI": "IMC",
                "Smoker": "Fumou ao menos 100 cigarros", "Stroke": "Histórico de AVC",
                "HeartDiseaseorAttack": "Doença cardíaca ou infarto",
                "PhysActivity": "Atividade física (30 dias)",
                "Fruits": "Consumo diário de frutas", "Veggies": "Consumo diário de vegetais",
                "HvyAlcoholConsump": "Consumo elevado de álcool",
                "AnyHealthcare": "Cobertura de saúde", "NoDocbcCost": "Sem consulta por custo",
                "GenHlth": "Saúde geral (1 excelente–5 ruim)",
                "MentHlth": "Saúde mental ruim (dias/30)",
                "PhysHlth": "Saúde física ruim (dias/30)",
                "DiffWalk": "Dificuldade para caminhar", "Sex": "Sexo",
                "Age": "Faixa etária", "Education": "Escolaridade", "Income": "Faixa de renda",
            }
            data, metadata = load_cdc_diabetes(
                20_000 if FAST_MODE else 40_000, random_state=RANDOM_STATE
            )
            """
        ),
        code(
            """
            X = data.drop(columns="Diabetes_binary").rename(columns=feature_labels)
            y = data["Diabetes_binary"].astype(int)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
            )
            print("O teste foi reservado antes de qualquer comparação:", X_test.shape)
            """
        ),
        markdown(
            """
            ### Dicionário de variáveis, desfecho e modelos

            A classe `1` reúne pré-diabetes ou diabetes. Os quatro algoritmos recebem os mesmos atributos com nomes em português e as mesmas partições; os rótulos “padrão” e “ajustado” indicam configurações do modelo, não categorias de pacientes.
            """
        ),
        code(
            """
            coding_summary = pd.DataFrame({
                "item": ["Classe 0", "Classe 1", "Atributos binários", "Atributos ordinais"],
                "significado": [
                    target_labels[0], target_labels[1],
                    "0/1 são categorias conforme a pergunta da UCI; Sex usa 0=feminino e 1=masculino",
                    "Saúde geral, idade, escolaridade e renda são faixas ordenadas",
                ],
            })
            display(coding_summary.style.hide(axis="index"))

            variable_dictionary = metadata.get("variables")
            if isinstance(variable_dictionary, pd.DataFrame):
                available = [
                    column for column in ["name", "role", "type", "description", "units"]
                    if column in variable_dictionary
                ]
                dictionary = variable_dictionary[available].copy()
                translated_names = {**feature_labels, "Diabetes_binary": TARGET_NAME}
                if "name" in dictionary:
                    dictionary.insert(
                        1, "nome_no_notebook",
                        dictionary["name"].map(translated_names).fillna(dictionary["name"]),
                    )
                display(dictionary.rename(columns={
                    "name": "nome_original", "role": "papel", "type": "tipo",
                    "description": "descrição_UCI", "units": "unidade",
                }))

            class_distribution = pd.DataFrame({
                "n": y.value_counts().sort_index(),
                "percentual": 100 * y.value_counts(normalize=True).sort_index(),
            })
            class_distribution.index = class_distribution.index.map(target_labels)
            display(class_distribution.round(1).rename_axis("classe do desfecho"))
            """
        ),
        markdown(
            "## Pergunta orientadora\n\n> Qual modelo apresenta melhor equilíbrio entre ordenação, erros e custo computacional na validação?"
        ),
        markdown("## Experimento: comparação\n\n> Todos os modelos viram exatamente os mesmos cinco folds?"),
        code(
            """
            models = get_default_classifiers(random_state=RANDOM_STATE)
            leaderboard = compare_classifiers(
                X_train, y_train, models=models, cv=5,
                scoring=["roc_auc", "f1", "recall", "precision"],
            )
            display(leaderboard.round(3))
            assert (leaderboard["status"] == "ok").all(), leaderboard[["model", "status"]]
            """
        ),
        code(
            """
            metric_columns = ["roc_auc", "f1", "recall", "precision", "balanced_accuracy"]
            leaderboard.set_index("model")[metric_columns].plot.bar(figsize=(11, 4), ylim=(0, 1), title="Leaderboard — média em cinco folds")
            plt.ylabel("Métrica"); plt.xticks(rotation=20, ha="right"); plt.show()
            leaderboard.set_index("model")["fit_time"].sort_values().plot.barh(title="Tempo médio de ajuste por fold")
            plt.xlabel("Segundos"); plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nO primeiro lugar depende da métrica. ROC-AUC mede ordenação; recall e precisão mostram trocas diferentes. Tempo também é parte do custo. Diferenças pequenas frente ao desvio-padrão pedem cautela."
        ),
        markdown("## Busca de hiperparâmetros\n\n> É possível ajustar sem consultar o teste?"),
        code(
            """
            best_name = leaderboard.iloc[0]["model"]
            best_model, search = tune_classifier(
                model_name=best_name, X=X_train, y=y_train,
                cv=5, n_iter=5 if FAST_MODE else 20,
                scoring="roc_auc", random_state=RANDOM_STATE,
            )
            print("Modelo:", best_name)
            print("Melhores parâmetros:", search.best_params_)
            display(tuning_results_frame(search).round(3))
            """
        ),
        markdown("## Avaliação final\n\n> O ajuste melhorou em dados realmente reservados?"),
        code(
            """
            default_model = get_default_classifiers(RANDOM_STATE)[best_name]
            default_model.fit(X_train, y_train)
            default_prob = default_model.predict_proba(X_test)[:, 1]
            tuned_prob = best_model.predict_proba(X_test)[:, 1]
            comparison = pd.DataFrame({
                "padrão": classification_report_health(y_test, default_prob >= 0.5, default_prob),
                "ajustado": classification_report_health(y_test, tuned_prob >= 0.5, tuned_prob),
            })
            display(comparison.loc[["roc_auc", "pr_auc", "f1", "sensibilidade", "especificidade"]].round(3))
            """
        ),
        code(
            """
            tuned_pred = (tuned_prob >= 0.5).astype(int)
            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            ConfusionMatrixDisplay.from_predictions(
                y_test, tuned_pred, cmap="Blues", ax=axes[0],
                display_labels=[target_labels[0], target_labels[1]],
            )
            axes[0].set_title("Matriz de confusão — ajustado")
            RocCurveDisplay.from_predictions(y_test, default_prob, name="Padrão", ax=axes[1])
            RocCurveDisplay.from_predictions(y_test, tuned_prob, name="Ajustado", ax=axes[1])
            axes[1].plot([0, 1], [0, 1], "--", color="grey")
            axes[1].set_title("ROC no teste final"); plt.tight_layout(); plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nO teste foi usado uma única vez, depois da escolha e do ajuste. Uma melhora de validação pode não se repetir no teste. O resultado compara algoritmos neste experimento, não estabelece utilidade clínica."
        ),
    ]
    cells += footer(
        [
            "A busca cobre espaços pequenos para caber no Colab; não é exaustiva.",
            "Múltiplas comparações aumentam o risco de escolher variações fortuitas.",
            "Desempenho agregado pode esconder diferenças por subgrupo e calibração inadequada.",
        ],
        "Mude a métrica de ordenação do leaderboard para `recall`. Registre se o vencedor muda e compare precisão, tempo e variabilidade — sem tocar no teste durante a escolha.",
        [
            "Comparações justas reutilizam os mesmos folds.",
            "Acurácia sozinha é frágil em classes desbalanceadas.",
            "Hiperparâmetros pertencem à validação; teste pertence somente ao final.",
        ],
        [
            "[UCI — CDC Diabetes Health Indicators](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)",
            "[scikit-learn — model selection](https://scikit-learn.org/stable/model_selection.html)",
            "[scikit-learn — RandomizedSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html)",
        ],
        ("numpy", "pandas", "scikit-learn", "matplotlib", "ucimlrepo"),
    )
    return cells


def notebook_05() -> list[dict]:
    filename = "05_imagens_gradcam.ipynb"
    cells = header(
        "05",
        "Classificação de imagens médicas e Grad-CAM com CNN pequena",
        filename,
        "cerca de 90 minutos",
        [
            "usar as divisões oficiais do PneumoniaMNIST",
            "treinar uma CNN pequena com validação e early stopping",
            "avaliar erros e métricas binárias",
            "gerar Grad-CAM e discutir seus limites",
        ],
        "Classificação binária, matrizes e noções iniciais de redes convolucionais.",
        f"[PneumoniaMNIST/MedMNIST+ — descrição e rótulos]({MEDMNIST_INFO_URL}), "
        "radiografias pediátricas reduzidas para 64 × 64; 0=normal e 1=pneumonia.",
        "MedMNIST é CC BY 4.0; a fonte original do subconjunto é de Kermany et al. O conjunto não se destina a uso clínico.",
    )
    cells += [
        execution_guide(
            filename,
            "imaging",
            "O encontro 05 funciona em CPU, mas o treinamento é mais rápido com GPU. A disponibilidade e a configuração do TensorFlow dependem do sistema operacional e do hardware local.",
        ),
        markdown("## Preparação do ambiente\n\n> Há GPU disponível? A execução continua em CPU com um aviso."),
        environment(["medmnist", "tensorflow"]),
        code(
            """
            import matplotlib.pyplot as plt
            import medmnist
            import numpy as np
            import pandas as pd
            import seaborn as sns
            import tensorflow as tf
            from pathlib import Path
            from medmnist import PneumoniaMNIST
            from sklearn.metrics import ConfusionMatrixDisplay

            from src.data_loading import ensure_medmnist_download
            from src.evaluation import classification_report_health, report_frame
            from src.gradcam import show_gradcam

            FAST_MODE = True
            DATASET_KEY = "pneumoniamnist"
            target_labels = {0: "0 Normal", 1: "1 Pneumonia"}
            dataset_info = medmnist.INFO[DATASET_KEY]
            seed_everything(RANDOM_STATE)  # TensorFlow já foi importado nesta célula.
            print("GPU:", tf.config.list_physical_devices("GPU") or "não encontrada — usando CPU")
            """
        ),
        markdown(
            "## Pergunta orientadora\n\n> Uma CNN pequena aprende sinais úteis neste benchmark reduzido, e onde a rede concentra influência em acertos e erros?"
        ),
        markdown("## Obtenção dos dados\n\n> As divisões oficiais foram preservadas?"),
        code(
            """
            medmnist_root = Path("/content/medmnist" if IN_COLAB else "data/cache/medmnist")
            ensure_medmnist_download(DATASET_KEY, 64, medmnist_root)
            train_data = PneumoniaMNIST(split="train", download=False, size=64, root=str(medmnist_root))
            val_data = PneumoniaMNIST(split="val", download=False, size=64, root=str(medmnist_root))
            test_data = PneumoniaMNIST(split="test", download=False, size=64, root=str(medmnist_root))

            def arrays(dataset):
                images = np.asarray(dataset.imgs)
                if images.ndim == 3:
                    images = images[..., None]
                return images.astype("float32") / 255.0, np.asarray(dataset.labels).ravel().astype(int)

            X_train, y_train = arrays(train_data)
            X_val, y_val = arrays(val_data)
            X_test, y_test = arrays(test_data)
            """
        ),
        markdown(
            """
            ### Dicionário do PneumoniaMNIST

            Cada exemplo é uma radiografia pediátrica em tons de cinza, redimensionada para 64 × 64. O rótulo `0` significa **normal** e o rótulo `1` significa **pneumonia**. Esses rótulos pertencem ao benchmark e não constituem diagnóstico produzido pelo notebook.
            """
        ),
        code(
            """
            official_labels = {int(code): label for code, label in dataset_info["label"].items()}
            assert official_labels == {0: "normal", 1: "pneumonia"}
            dataset_dictionary = pd.DataFrame({
                "campo": ["descrição", "tarefa", "canais", "rótulo 0", "rótulo 1", "licença"],
                "significado": [
                    dataset_info["description"], dataset_info["task"], dataset_info["n_channels"],
                    official_labels[0], official_labels[1], dataset_info["license"],
                ],
            })
            display(dataset_dictionary.style.hide(axis="index"))
            display(pd.Series(dataset_info["n_samples"], name="n").to_frame().rename_axis("divisão oficial"))
            """
        ),
        markdown("## Inspeção\n\n> Qual é o formato e o equilíbrio das classes?"),
        code(
            """
            for split, X_part, y_part in [("treino", X_train, y_train), ("validação", X_val, y_val), ("teste", X_test, y_test)]:
                counts = pd.Series(y_part).value_counts().sort_index()
                counts.index = counts.index.map(target_labels)
                print(split, X_part.shape, counts.to_dict())
            fig, axes = plt.subplots(2, 5, figsize=(10, 4))
            for axis, index in zip(axes.ravel(), np.linspace(0, len(X_train) - 1, 10, dtype=int)):
                axis.imshow(X_train[index].squeeze(), cmap="gray")
                axis.set_title(target_labels[int(y_train[index])])
                axis.axis("off")
            plt.suptitle("Exemplos do treino — imagens reduzidas e pré-processadas"); plt.tight_layout(); plt.show()
            """
        ),
        markdown("## Preparação e modelo\n\n> Uma arquitetura pequena é suficiente para o objetivo didático?"),
        code(
            """
            if FAST_MODE:
                rng = np.random.default_rng(RANDOM_STATE)
                keep = rng.choice(len(X_train), min(3_000, len(X_train)), replace=False)
                X_fit, y_fit = X_train[keep], y_train[keep]
            else:
                X_fit, y_fit = X_train, y_train

            model = tf.keras.Sequential([
                tf.keras.layers.Input(X_train.shape[1:]),
                tf.keras.layers.Conv2D(16, 3, activation="relu", padding="same"),
                tf.keras.layers.MaxPooling2D(),
                tf.keras.layers.Conv2D(32, 3, activation="relu", padding="same", name="last_conv"),
                tf.keras.layers.GlobalAveragePooling2D(),
                tf.keras.layers.Dense(1, activation="sigmoid"),
            ])
            model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy", tf.keras.metrics.AUC(name="auc")])
            """
        ),
        markdown("## Experimento\n\n> O desempenho de validação deixa de melhorar antes do limite de épocas?"),
        code(
            """
            early_stop = tf.keras.callbacks.EarlyStopping(
                monitor="val_auc", mode="max", patience=2, restore_best_weights=True
            )
            history = model.fit(
                X_fit, y_fit, validation_data=(X_val, y_val),
                epochs=5 if FAST_MODE else 10, batch_size=64,
                callbacks=[early_stop], verbose=2,
            )
            """
        ),
        code(
            """
            curves = pd.DataFrame(history.history)
            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            curves[["loss", "val_loss"]].plot(ax=axes[0], title="Loss por época")
            curves[["auc", "val_auc"]].plot(ax=axes[1], title="AUC por época")
            for axis in axes: axis.set_xlabel("Época")
            plt.tight_layout(); plt.show()
            """
        ),
        markdown("## Avaliação\n\n> Que erros aparecem no teste oficial?"),
        code(
            """
            probabilities = model.predict(X_test, batch_size=128, verbose=0).ravel()
            predictions = (probabilities >= 0.5).astype(int)
            report = classification_report_health(y_test, predictions, probabilities)
            display(report_frame(report).round(3))
            ConfusionMatrixDisplay.from_predictions(
                y_test, predictions, cmap="Blues",
                display_labels=[target_labels[0], target_labels[1]],
            )
            plt.title("Matriz de confusão — teste oficial"); plt.show()
            """
        ),
        markdown("## Grad-CAM\n\n> Onde houve influência para a saída, em acertos e erros?"),
        code(
            """
            categories = {
                "falso positivo": np.where((y_test == 0) & (predictions == 1))[0],
                "falso negativo": np.where((y_test == 1) & (predictions == 0))[0],
                "verdadeiro positivo": np.where((y_test == 1) & (predictions == 1))[0],
                "verdadeiro negativo": np.where((y_test == 0) & (predictions == 0))[0],
            }
            selected = [(name, int(indices[0])) for name, indices in categories.items() if len(indices)]
            if not any(name.startswith("falso") for name, _ in selected):
                print("O modelo não errou neste teste; exibiremos casos limítrofes sem inventar um erro.")
            used = {index for _, index in selected}
            for index in np.argsort(np.abs(probabilities - 0.5)):
                if int(index) not in used and len(selected) < 4:
                    selected.append(("caso limítrofe", int(index)))
            selected = selected[:4]
            print(selected)
            """
        ),
        code(
            """
            for name, index in selected:
                probability = probabilities[index]
                predicted_label = target_labels[int(predictions[index])]
                real_label = target_labels[int(y_test[index])]
                print(
                    f"{name}: real={real_label}; predito={predicted_label}; "
                    f"P(pneumonia)={probability:.3f}"
                )
                show_gradcam(model, X_test[index], "last_conv", class_index=int(predictions[index]))
                plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nGrad-CAM aponta regiões que influenciaram a saída da rede, não uma lesão confirmada nem uma justificativa clínica. Mapas difusos, bordas e artefatos podem revelar atalhos. Acertos não validam o mapa; erros são especialmente informativos."
        ),
    ]
    cells += footer(
        [
            "A população é pediátrica e a resolução 64 × 64 remove detalhes da imagem original.",
            "Equipamento, pré-processamento e atalhos visuais podem mudar o desempenho fora do benchmark.",
            "Grad-CAM não localiza doença com garantia e não constitui validação clínica.",
        ],
        "Escolha dois exemplos com probabilidades próximas de 0,5. Compare os mapas e escreva por que incerteza do modelo e mapa visual respondem a perguntas diferentes.",
        [
            "Divisões oficiais evitam contaminação entre treino, validação e teste.",
            "Matriz de confusão torna falsos positivos e negativos visíveis.",
            "Grad-CAM investiga a rede, mas não explica a biologia nem valida uso clínico.",
        ],
        [
            "[MedMNIST v2, Scientific Data (2023)](https://www.nature.com/articles/s41597-022-01721-8)",
            "[MedMNIST no GitHub](https://github.com/MedMNIST/MedMNIST)",
            "Kermany et al. Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning. Cell, 2018.",
            "Selvaraju et al. Grad-CAM. ICCV, 2017.",
        ],
        ("numpy", "pandas", "matplotlib", "scikit-learn", "tensorflow", "medmnist"),
    )
    return cells


def notebook_06() -> list[dict]:
    filename = "06_analise_sobrevivencia.ipynb"
    cells = header(
        "06",
        "Tempo até o evento: Kaplan–Meier e regressão de Cox",
        filename,
        "75–90 minutos",
        [
            "distinguir tempo, evento e censura",
            "estimar Kaplan–Meier e comparar grupos com log-rank",
            "interpretar hazard ratios de um modelo de Cox",
            "verificar proporcionalidade e comparar estratificação",
        ],
        "Estatística básica e interpretação de intervalos de confiança.",
        f"[NCCTG Lung Cancer — descrição das variáveis]({RDATASETS_LUNG_URL}), "
        "do pacote R survival, acessada pelo Rdatasets. A documentação explica códigos "
        "como status 1=censurado/2=óbito e sexo 1=masculino/2=feminino.",
        "Use os termos do pacote survival/Rdatasets e cite a documentação original.",
    )
    cells += [
        execution_guide(filename, "survival"),
        markdown("## Preparação do ambiente\n\n> Como registrar a estratégia de dados ausentes e o código de evento?"),
        environment(["lifelines"]),
        code(
            """
            from io import StringIO

            import matplotlib.pyplot as plt
            import pandas as pd
            import requests
            from lifelines import CoxPHFitter, KaplanMeierFitter
            from lifelines.plotting import add_at_risk_counts
            from lifelines.statistics import logrank_test

            from src.survival_utils import hazard_ratio_table, prepare_lung_data

            # No Rdatasets atual, o arquivo canônico usa o alias histórico `cancer`.
            # `survival/lung.csv` hoje aponta para outra tabela e é rejeitado pela validação.
            URL = "https://vincentarelbundock.github.io/Rdatasets/csv/survival/cancer.csv"
            """
        ),
        markdown(
            """
            ### Dicionário da base e recodificação

            A documentação original usa `status=1` para censura e `status=2` para óbito. Para as bibliotecas Python, o notebook cria `event=0` para censura e `event=1` para óbito observado. Sexo mantém o código original `1=masculino` e `2=feminino`.
            """
        ),
        code(
            """
            variable_labels = {
                "inst": "Instituição", "time": "Tempo de sobrevivência (dias)",
                "status": "Status original", "age": "Idade (anos)", "sex": "Sexo",
                "ph.ecog": "ECOG pelo médico", "ph.karno": "Karnofsky pelo médico",
                "pat.karno": "Karnofsky pelo paciente", "meal.cal": "Calorias nas refeições",
                "wt.loss": "Perda de peso em 6 meses (lb)",
            }
            lung_dictionary = pd.DataFrame({
                "nome_original": list(variable_labels),
                "nome_no_notebook": list(variable_labels.values()),
                "codificação/unidade": [
                    "código da instituição", "dias", "1=censurado; 2=óbito", "anos",
                    "1=masculino; 2=feminino",
                    "0=assintomático; 1=sintomático e ambulante; 2=no leito <50%; 3=no leito >50%; 4=restrito ao leito",
                    "0=pior; 100=melhor", "0=pior; 100=melhor", "calorias", "libras",
                ],
            })
            display(lung_dictionary.style.hide(axis="index"))
            display(pd.DataFrame({
                "campo": ["status original", "event usado no modelo"],
                "censura": [1, 0], "óbito observado": [2, 1],
            }).style.hide(axis="index"))
            """
        ),
        markdown(
            "## Pergunta orientadora\n\n> Como o tempo observado e a censura alteram a comparação de sobrevivência entre grupos?"
        ),
        markdown("## Obtenção e inspeção\n\n> O evento foi recodificado conforme a fonte: 1=censurado e 2=óbito?"),
        code(
            """
            response = requests.get(URL, timeout=30)
            response.raise_for_status()
            raw = pd.read_csv(StringIO(response.text))
            print("Dimensão original:", raw.shape)
            display(raw.head().rename(columns=variable_labels))
            display(raw.isna().sum().rename(index=variable_labels).rename("ausências").to_frame().T)
            """
        ),
        code(
            """
            lung, preparation = prepare_lung_data(raw, missing="drop")
            display(pd.Series(preparation, name="valor").to_frame())
            print("Evento=1 significa óbito observado; evento=0 significa censura.")
            assert set(lung["event"]) <= {0, 1}
            """
        ),
        markdown("## Kaplan–Meier global\n\n> Qual é a sobrevivência estimada e sua mediana?"),
        code(
            """
            km_global = KaplanMeierFitter(label="Amostra completa")
            km_global.fit(lung["time"], event_observed=lung["event"])
            ax = km_global.plot_survival_function(ci_show=True)
            add_at_risk_counts(km_global, ax=ax)
            ax.set(title=f"Kaplan–Meier global (n={len(lung)})", xlabel="Tempo (dias)", ylabel="Sobrevivência estimada")
            plt.tight_layout(); plt.show()
            print("Mediana de sobrevivência:", km_global.median_survival_time_, "dias")
            """
        ),
        markdown(
            "### Como interpretar\n\nA curva estima a probabilidade de permanecer sem o evento ao longo do tempo, incorporando censura sob pressupostos. A mediana é o tempo em que a estimativa cruza 0,5; não é a expectativa individual."
        ),
        markdown("## Estratificação visual e log-rank\n\n> As curvas por sexo diferem nesta amostra?"),
        code(
            """
            fig, ax = plt.subplots(figsize=(8, 5))
            fitted = []
            for label, group in lung.groupby("sex_label"):
                km = KaplanMeierFitter(label=label).fit(group["time"], group["event"])
                km.plot_survival_function(ax=ax)
                fitted.append(km)
            ax.set(title="Kaplan–Meier por sexo", xlabel="Tempo (dias)", ylabel="Sobrevivência estimada")
            add_at_risk_counts(*fitted, ax=ax)
            plt.tight_layout(); plt.show()
            """
        ),
        code(
            """
            male = lung[lung["sex"] == 1]
            female = lung[lung["sex"] == 2]
            logrank = logrank_test(
                male["time"], female["time"],
                event_observed_A=male["event"], event_observed_B=female["event"],
            )
            print(f"Log-rank: estatística={logrank.test_statistic:.3f}; p={logrank.p_value:.4f}")
            """
        ),
        markdown("## Cox sem estratificação\n\n> Quais associações permanecem ao considerar idade, sexo e desempenho ECOG?"),
        code(
            """
            cox_data = lung[["time", "event", "age", "sex_female", "ph.ecog"]]
            cph = CoxPHFitter()
            cph.fit(cox_data, duration_col="time", event_col="event")
            cox_labels = {
                "age": "Idade (por ano)",
                "sex_female": "Feminino vs. masculino",
                "ph.ecog": "ECOG (por nível)",
            }
            display(hazard_ratio_table(cph.summary).rename(index=cox_labels).round(3))
            ax = cph.plot(hazard_ratios=True)
            ax.set_yticklabels([cox_labels.get(tick.get_text(), tick.get_text()) for tick in ax.get_yticklabels()])
            plt.axvline(1, color="grey", linestyle="--")
            plt.title("Hazard ratios — Cox sem estratificação"); plt.show()
            print("Concordance index:", round(cph.concordance_index_, 3))
            """
        ),
        code(
            """
            # A função imprime violações e recomendações; não altera o modelo silenciosamente.
            cph.check_assumptions(cox_data, p_value_threshold=0.05, show_plots=False)
            """
        ),
        markdown(
            "### Como interpretar\n\nHazard é uma taxa instantânea condicionada a ainda estar sob risco. HR>1 indica hazard estimado maior por unidade/grupo, não uma diferença de probabilidade absoluta. p-valor não garante relevância clínica nem causalidade."
        ),
        markdown("## Cox estratificado\n\n> O que muda ao permitir uma função de base diferente para cada sexo?"),
        code(
            """
            stratified_data = lung[["time", "event", "age", "ph.ecog", "sex"]]
            cph_stratified = CoxPHFitter()
            cph_stratified.fit(
                stratified_data, duration_col="time", event_col="event", strata=["sex"]
            )
            display(hazard_ratio_table(cph_stratified.summary).rename(index=cox_labels).round(3))
            comparison = pd.DataFrame({
                "sem estrato": [cph.concordance_index_, cph.log_likelihood_],
                "sexo como estrato": [cph_stratified.concordance_index_, cph_stratified.log_likelihood_],
            }, index=["concordance index", "log-likelihood"])
            display(comparison.round(3))
            """
        ),
        markdown(
            "### Como interpretar\n\nO modelo estratificado não produz um único coeficiente para sexo: cada estrato pode ter hazard basal próprio, enquanto idade e ECOG mantêm coeficientes compartilhados. Compare ajuste e pressupostos, não apenas um número."
        ),
    ]
    cells += footer(
        [
            "Amostra pequena, observacional e sujeita a confundimento e seleção.",
            "Censura e o pressuposto de riscos proporcionais precisam ser considerados.",
            "Hazard ratio não é risco absoluto, diferença de sobrevivência nem efeito causal.",
        ],
        "Escolha outra variável documentada, justifique o tratamento de ausências e compare KM/log-rank. Escreva por que significância estatística não basta para relevância clínica.",
        [
            "Kaplan–Meier incorpora observações censuradas.",
            "Cox estima razões de hazards sob pressupostos verificáveis.",
            "Estratificar troca um coeficiente comum por hazards basais específicos.",
        ],
        [
            "[Rdatasets — lung](https://vincentarelbundock.github.io/Rdatasets/doc/survival/lung.html)",
            "[R survival — lung](https://stat.ethz.ch/R-manual/R-devel/library/survival/help/lung.html)",
            "[lifelines documentation](https://lifelines.readthedocs.io/)",
        ],
        ("numpy", "pandas", "matplotlib", "lifelines", "requests"),
    )
    return cells


def notebook_07() -> list[dict]:
    filename = "07_aprendizado_reforco.ipynb"
    cells = header(
        "07",
        "Aprendizado por reforço para planejamento de estoque em vigilância epidemiológica",
        filename,
        "75–90 minutos",
        [
            "distinguir estado, ação, recompensa e episódio",
            "treinar Q-learning tabular em nove estados",
            "comparar a política com três baselines em teste temporal",
            "discutir escolhas normativas da recompensa",
        ],
        "Python, arrays e noções de séries temporais.",
        f"Série semanal real da [API InfoDengue — descrição e acesso]({INFODENGUE_API_URL}); "
        "ações, estoques e recompensas são sintéticos.",
        "Consulte os termos do InfoDengue. A simulação não representa tratamento nem decisão clínica.",
    )
    cells += [
        execution_guide(filename, "reinforcement"),
        markdown("## Preparação do ambiente\n\n> Como obter a série real sem substituir falhas por números artificiais?"),
        environment([]),
        code(
            """
            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd
            import seaborn as sns

            from src.dengue_api import fetch_infodengue, missing_week_intervals
            from src.reinforcement_env import DengueInventoryEnv, evaluate_policy, train_q_learning

            FAST_MODE = True
            GEOCODE = 3303302  # Niterói
            GEOCODE_LABEL = "Niterói (RJ)"
            USE_RIO_FALLBACK = False  # mude para True para autorizar 3304557 explicitamente
            """
        ),
        markdown(
            "## Pergunta orientadora\n\n> Uma política aprendida em anos iniciais reduz custos da simulação nos anos finais, comparada a regras simples?"
        ),
        markdown("## Obtenção dos dados\n\n> A resposta foi validada, ordenada e datada? Há semanas ausentes?"),
        code(
            """
            dengue = fetch_infodengue(
                geocode=GEOCODE, disease="dengue", start_year=2016, end_year=2025,
                fallback_geocode=3304557 if USE_RIO_FALLBACK else None,
            )
            target = "casos_est" if "casos_est" in dengue else "casos"
            target_label = (
                "Casos estimados por nowcasting" if target == "casos_est" else "Casos notificados"
            )
            print("Fonte/cache e download:", dengue.attrs)
            print("Município:", GEOCODE_LABEL, "| código IBGE:", GEOCODE)
            print("Alvo:", f"{target} — {target_label}", "| intervalo:", dengue.data_iniSE.min(), "a", dengue.data_iniSE.max())
            display(missing_week_intervals(dengue).head(10))
            """
        ),
        markdown(
            """
            ### Dicionário dos dados e da simulação

            `casos_est` é uma estimativa semanal por nowcasting e pode ser revisada retrospectivamente; `casos` contém notificações semanais. A data representa o primeiro dia da semana epidemiológica. A demanda vem do InfoDengue, enquanto estados, ações, estoque, custos e recompensas são construções sintéticas deste exercício.
            """
        ),
        code(
            """
            infodengue_descriptions = {
                "data_iniSE": "Primeiro dia da semana epidemiológica (domingo)",
                "SE": "Código da semana epidemiológica",
                "casos_est": "Casos semanais estimados por nowcasting; sujeitos a revisão",
                "casos_est_min": "Limite inferior do intervalo de credibilidade de 95%",
                "casos_est_max": "Limite superior do intervalo de credibilidade de 95%",
                "casos": "Casos notificados na semana; sujeitos a revisão",
                "p_rt1": "Probabilidade estimada de Rt > 1",
                "p_inc100k": "Incidência estimada por 100 mil habitantes",
                "nivel": "Alerta: 1=verde; 2=amarelo; 3=laranja; 4=vermelho",
            }
            available_dictionary = pd.DataFrame([
                {"campo": field, "significado": description}
                for field, description in infodengue_descriptions.items() if field in dengue.columns
            ])
            display(available_dictionary.style.hide(axis="index"))
            """
        ),
        markdown(
            "### Como interpretar\n\nSemanas ausentes são exibidas e não recebem zero. Valores do InfoDengue podem ser revisados. Se a API falhar, a execução para com mensagem acionável; nenhum dado sintético substitui a série."
        ),
        markdown("## Preparação temporal\n\n> Os limites de estado e estoque são calculados somente no treino?"),
        code(
            """
            series = dengue.set_index("data_iniSE")[target].pipe(pd.to_numeric, errors="coerce")
            series.name = target_label
            missing_values = int(series.isna().sum())
            series = series.dropna().sort_index()
            split_date = series.index.max() - pd.DateOffset(years=2)
            train_series = series[series.index < split_date]
            test_series = series[series.index >= split_date]
            print(f"Valores ausentes removidos: {missing_values}")
            print("Treino:", train_series.index.min(), "a", train_series.index.max(), len(train_series))
            print("Teste:", test_series.index.min(), "a", test_series.index.max(), len(test_series))
            """
        ),
        code(
            """
            stock_levels = np.quantile(train_series, [0.25, 0.50, 0.75])
            train_env = DengueInventoryEnv(
                train_series.to_numpy(), stock_levels=stock_levels,
                shortage_cost=5.0, excess_cost=1.0, operational_cost=0.05,
            )
            state_labels = [
                f"{demand}/{trend}"
                for demand in ["demanda baixa", "demanda média", "demanda alta"]
                for trend in ["caindo", "estável", "subindo"]
            ]
            action_labels = ["estoque baixo", "estoque médio", "estoque alto"]
            print("Estoques simulados (q25, q50, q75 do treino):", stock_levels.round(1))
            print("Limites dos estados de demanda:", train_env.demand_thresholds.round(1))
            display(pd.DataFrame({
                "estado_id": range(9), "significado": state_labels,
            }).style.hide(axis="index"))
            display(pd.DataFrame({
                "ação_id": range(3), "ação": action_labels,
                "estoque_simulado": stock_levels.round(1),
            }).style.hide(axis="index"))
            """
        ),
        markdown(
            "## Ambiente simulado\n\nCada estado combina demanda recente baixa/média/alta e tendência caindo/estável/subindo. As ações são estoques baixo/médio/alto. A recompensa é o negativo de custo de falta + excesso + operação; falta custa mais por uma escolha explícita de configuração."
        ),
        markdown("## Experimento: Q-learning\n\n> A recompensa por episódio se estabiliza enquanto epsilon diminui?"),
        code(
            """
            q_table, history = train_q_learning(
                train_env, episodes=500 if FAST_MODE else 1_500,
                alpha=0.1, gamma=0.95,
                epsilon_start=1.0, epsilon_end=0.05,
                random_state=RANDOM_STATE,
            )
            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            history.set_index("episódio")["recompensa"].rolling(30, min_periods=1).mean().plot(ax=axes[0], title="Recompensa média móvel")
            history.plot(x="episódio", y="epsilon", ax=axes[1], legend=False, title="Exploração (epsilon)")
            plt.tight_layout(); plt.show()
            """
        ),
        code(
            """
            q_frame = pd.DataFrame(q_table, index=state_labels, columns=action_labels)
            sns.heatmap(q_frame, cmap="viridis", annot=True, fmt=".0f")
            plt.title("Q-table final (maior valor = ação preferida)"); plt.show()
            policy = np.argmax(q_table, axis=1)
            display(pd.DataFrame({"estado": state_labels, "ação": np.array(action_labels)[policy]}))
            """
        ),
        markdown("## Avaliação temporal\n\n> A política supera estoque médio, aleatório e regra do último nível?"),
        code(
            """
            test_env = DengueInventoryEnv(
                test_series.to_numpy(), stock_levels=stock_levels,
                shortage_cost=train_env.shortage_cost, excess_cost=train_env.excess_cost,
                operational_cost=train_env.operational_cost,
                demand_thresholds=train_env.demand_thresholds,
                trend_tolerance=train_env.trend_tolerance,
            )
            rng = np.random.default_rng(RANDOM_STATE)
            policies = {
                "Q-learning": policy,
                "sempre médio": np.ones(9, dtype=int),
                "aleatória": lambda state, env: int(rng.integers(3)),
                "regra último nível": lambda state, env: state // 3,
            }
            comparison = pd.DataFrame({name: evaluate_policy(test_env, rule) for name, rule in policies.items()}).T
            metric_labels = {
                "recompensa": "Recompensa acumulada",
                "falta": "Unidades em falta",
                "excesso": "Unidades em excesso",
                "semanas_com_falta": "Semanas com falta",
            }
            display(comparison.rename(columns=metric_labels).round(1))
            """
        ),
        code(
            """
            comparison[["falta", "excesso"]].plot.bar(figsize=(9, 4), title="Custos físicos simulados no teste")
            plt.ylabel("Unidades acumuladas"); plt.xticks(rotation=15); plt.show()
            comparison["recompensa"].plot.bar(title="Recompensa acumulada no teste (maior é melhor na simulação)")
            plt.ylabel("Recompensa"); plt.xticks(rotation=15); plt.show()
            """
        ),
        markdown(
            "### Como interpretar\n\nMaior recompensa significa somente melhor resultado **sob a função escolhida**. Não significa melhor decisão pública. Os quantis, estados e custos vieram do treino; o teste temporal não atualiza a política. Os dados históricos não mostram o efeito causal das ações simuladas."
        ),
    ]
    cells += footer(
        [
            "Estado, ações e recompensa simplificam logística, validade, capacidade, orçamento e incerteza.",
            "Dar peso maior à falta é uma escolha normativa, não uma propriedade descoberta nos dados.",
            "A demanda é real, mas nenhuma ação foi aplicada; não há evidência causal de impacto.",
        ],
        "Dobre o custo de excesso ou de falta, treine novamente e compare a política. Explique por que otimizar a nova recompensa não resolve sozinho uma decisão pública.",
        [
            "Q-learning aprende valores de estado-ação por tentativa na simulação.",
            "Limites e política devem ser aprendidos antes do teste temporal.",
            "A função de recompensa incorpora valores e precisa ser debatida.",
        ],
        [
            "[InfoDengue — tutorial da API](https://info.dengue.mat.br/tutorial_api_python/locale-en)",
            "Sutton & Barto. Reinforcement Learning: An Introduction, 2ª ed.",
        ],
        ("numpy", "pandas", "matplotlib", "seaborn", "requests"),
    )
    return cells


def notebook_08() -> list[dict]:
    filename = "08_series_temporais.ipynb"
    cells = header(
        "08",
        "Prevendo casos semanais de dengue com atributos de defasagem",
        filename,
        "75–90 minutos",
        [
            "visualizar tendência, sazonalidade e autocorrelação",
            "criar lags e janelas usando apenas o passado",
            "usar baseline, TimeSeriesSplit e teste no último ano",
            "avaliar erros e limites epidemiológicos",
        ],
        "Regressão supervisionada e noções de séries temporais.",
        f"Série semanal real da [API InfoDengue — descrição e acesso]({INFODENGUE_API_URL}), "
        "Niterói, 2016–2025.",
        "Consulte os termos do InfoDengue; notificações e estimativas podem ser revistas.",
    )
    cells += [
        execution_guide(filename, "time-series"),
        markdown("## Preparação do ambiente\n\n> Como preservar a ordem temporal desde o download?"),
        environment(["statsmodels"]),
        code(
            """
            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd
            import seaborn as sns
            from sklearn.ensemble import HistGradientBoostingRegressor
            from sklearn.inspection import permutation_importance
            from sklearn.model_selection import TimeSeriesSplit, cross_val_score
            from statsmodels.graphics.tsaplots import plot_acf

            from src.dengue_api import fetch_infodengue, missing_week_intervals
            from src.time_series import make_lag_features, regression_report, temporal_train_test_split

            FAST_MODE = True
            GEOCODE = 3303302
            GEOCODE_LABEL = "Niterói (RJ)"
            """
        ),
        markdown(
            "## Pergunta orientadora\n\n> Lags e sazonalidade melhoram a previsão de uma semana em relação a repetir o valor anterior?"
        ),
        markdown("## Obtenção e inspeção\n\n> O período termina em um ano completo e as lacunas estão explícitas?"),
        code(
            """
            dengue = fetch_infodengue(
                geocode=GEOCODE, disease="dengue", start_year=2016, end_year=2025
            )
            target = "casos_est" if "casos_est" in dengue else "casos"
            target_label = (
                "Casos estimados por nowcasting" if target == "casos_est" else "Casos notificados"
            )
            print("Download/fonte:", dengue.attrs)
            print("Município:", GEOCODE_LABEL, "| código IBGE:", GEOCODE)
            print("Alvo escolhido:", f"{target} — {target_label}")
            gaps = missing_week_intervals(dengue)
            display(gaps.head(10))
            """
        ),
        markdown(
            """
            ### Dicionário da série

            `data_iniSE` é o domingo que inicia a semana epidemiológica. Quando disponível, `casos_est` é usado porque aplica nowcasting para estimar casos ainda sujeitos a atraso de notificação; caso contrário, o notebook usa `casos`, que representa notificações semanais. Ambos podem sofrer revisões retrospectivas.
            """
        ),
        code(
            """
            infodengue_descriptions = {
                "data_iniSE": "Primeiro dia da semana epidemiológica (domingo)",
                "SE": "Código da semana epidemiológica",
                "casos_est": "Casos semanais estimados por nowcasting; sujeitos a revisão",
                "casos_est_min": "Limite inferior do intervalo de credibilidade de 95%",
                "casos_est_max": "Limite superior do intervalo de credibilidade de 95%",
                "casos": "Casos notificados na semana; sujeitos a revisão",
                "p_rt1": "Probabilidade estimada de Rt > 1",
                "p_inc100k": "Incidência estimada por 100 mil habitantes",
                "nivel": "Alerta: 1=verde; 2=amarelo; 3=laranja; 4=vermelho",
            }
            available_dictionary = pd.DataFrame([
                {"campo": field, "significado": description}
                for field, description in infodengue_descriptions.items() if field in dengue.columns
            ])
            display(available_dictionary.style.hide(axis="index"))
            """
        ),
        code(
            """
            observed = dengue.set_index("data_iniSE")[target].pipe(pd.to_numeric, errors="coerce").sort_index()
            observed.name = target_label
            full_index = pd.date_range(observed.index.min(), observed.index.max(), freq="7D")
            series = observed.reindex(full_index)
            missing_before = int(series.isna().sum())
            series = series.ffill()  # causal: nunca consulta a semana seguinte
            leading_missing = int(series.isna().sum())
            series = series.dropna()
            print(f"Semanas/valores preenchidos com a última observação passada: {missing_before - leading_missing}")
            print(f"Ausências iniciais sem passado, removidas: {leading_missing}")
            """
        ),
        markdown(
            "### Como interpretar\n\nO preenchimento foi explícito, usou somente a última observação passada e nunca inseriu zero. É uma conveniência pedagógica que cria platôs; uma análise operacional deveria estudar a causa de cada lacuna e propagar a incerteza."
        ),
        markdown("## Análise temporal\n\n> Há tendência, sazonalidade e memória semanal?"),
        code(
            """
            fig, ax = plt.subplots(figsize=(12, 4))
            series.plot(ax=ax, alpha=0.55, label=target_label)
            series.rolling(4).mean().plot(ax=ax, label="média móvel 4 semanas")
            ax.set(title=f"Dengue semanal — Niterói (n={len(series)})", xlabel="Semana", ylabel="Casos")
            ax.legend(); plt.show()

            seasonal = series.groupby(series.index.isocalendar().week.astype(int)).mean()
            seasonal.plot(title="Média por semana epidemiológica", figsize=(10, 3))
            plt.xlabel("Semana"); plt.ylabel("Casos médios"); plt.show()
            """
        ),
        code(
            """
            plot_acf(series, lags=52, zero=False)
            plt.title("Autocorrelação até 52 semanas")
            plt.xlabel("Defasagem (semanas)"); plt.show()
            """
        ),
        markdown("## Atributos sem futuro\n\n> Todas as janelas foram deslocadas antes de calcular a média e o desvio?"),
        code(
            """
            feature_data = make_lag_features(
                series, lags=[1, 2, 3, 4, 8, 12, 52],
                rolling_windows=[4, 8, 12], dropna=True,
            )
            temporal_feature_labels = {"target": target_label}
            for column in feature_data.columns:
                if column.startswith("lag_"):
                    weeks = column.removeprefix("lag_")
                    temporal_feature_labels[column] = f"Valor de {weeks} semana(s) atrás"
                elif column.startswith("média_móvel_"):
                    weeks = column.removeprefix("média_móvel_")
                    temporal_feature_labels[column] = f"Média das {weeks} semanas anteriores"
                elif column.startswith("desvio_móvel_"):
                    weeks = column.removeprefix("desvio_móvel_")
                    temporal_feature_labels[column] = f"Desvio-padrão das {weeks} semanas anteriores"
                elif column == "semana_seno":
                    temporal_feature_labels[column] = "Sazonalidade anual — seno"
                elif column == "semana_cosseno":
                    temporal_feature_labels[column] = "Sazonalidade anual — cosseno"
                elif column == "tendência":
                    temporal_feature_labels[column] = "Índice temporal crescente"
            display(pd.DataFrame({
                "atributo": list(temporal_feature_labels),
                "significado": list(temporal_feature_labels.values()),
            }).style.hide(axis="index"))
            display(feature_data.head())
            assert (feature_data["lag_1"] == series.shift(1).loc[feature_data.index]).all()
            print("Primeira linha utilizável:", feature_data.index.min(), "| atributos:", feature_data.shape[1] - 1)
            """
        ),
        markdown("## Divisão e validação\n\n> O último ano permanece intacto e os folds avançam no tempo?"),
        code(
            """
            train, test = temporal_train_test_split(feature_data, test_size=52)
            X_train, y_train = train.drop(columns="target"), train["target"]
            X_test, y_test = test.drop(columns="target"), test["target"]
            splitter = TimeSeriesSplit(n_splits=5)
            model = HistGradientBoostingRegressor(
                learning_rate=0.05, max_iter=150 if FAST_MODE else 300,
                l2_regularization=1.0, random_state=RANDOM_STATE,
            )
            cv_mae = -cross_val_score(model, X_train, y_train, cv=splitter, scoring="neg_mean_absolute_error")
            print("MAE temporal por fold:", cv_mae.round(1), "| média:", cv_mae.mean().round(1))
            print("Teste final:", test.index.min(), "a", test.index.max())
            """
        ),
        markdown("## Avaliação final\n\n> O modelo supera a previsão ingênua de repetir a última semana?"),
        code(
            """
            model.fit(X_train, y_train)
            model_prediction = np.maximum(model.predict(X_test), 0)
            baseline_prediction = X_test["lag_1"].to_numpy()
            reports = pd.DataFrame({
                "Baseline: repetir última semana": regression_report(y_test, baseline_prediction),
                "Modelo": regression_report(y_test, model_prediction),
            })
            display(reports.round(2))
            """
        ),
        code(
            """
            comparison = pd.DataFrame({
                "Observado": y_test,
                "Baseline: última semana": baseline_prediction,
                "Modelo": model_prediction,
            }, index=y_test.index)
            comparison.plot(figsize=(12, 4), title="Real versus previsto — último ano completo")
            plt.ylabel("Casos"); plt.xlabel("Semana"); plt.show()
            residuals = y_test - model_prediction
            fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
            residuals.plot(ax=axes[0], title="Resíduos no tempo")
            sns.histplot(residuals, kde=True, ax=axes[1]); axes[1].set_title("Distribuição dos resíduos")
            plt.tight_layout(); plt.show()
            """
        ),
        code(
            """
            importance = permutation_importance(
                model, X_test, y_test, scoring="neg_mean_absolute_error",
                n_repeats=10, random_state=RANDOM_STATE,
            )
            importance_series = pd.Series(
                importance.importances_mean, index=X_test.columns
            ).rename(index=temporal_feature_labels)
            importance_series.nlargest(12).sort_values().plot.barh(
                title="Importância por permutação no teste"
            )
            plt.xlabel("Aumento de desempenho ao manter o atributo"); plt.show()
            """
        ),
        markdown("## Previsão de um passo\n\n> Como construir atributos para a próxima semana usando somente a história disponível?"),
        code(
            """
            next_date = series.index[-1] + pd.Timedelta(days=7)
            extended = pd.concat([series, pd.Series([np.nan], index=[next_date])])
            future_features = make_lag_features(
                extended, lags=[1, 2, 3, 4, 8, 12, 52],
                rolling_windows=[4, 8, 12], dropna=False,
            ).loc[[next_date]].drop(columns="target")
            next_prediction = max(float(model.predict(future_features)[0]), 0)
            print(f"Previsão didática para {next_date.date()}: {next_prediction:.1f} — {target_label}")
            """
        ),
        markdown(
            "### Como interpretar\n\nPrever não é explicar. Compare sempre com o baseline: um modelo complexo que não reduz erros não trouxe ganho. A previsão pontual omite incerteza e não deve orientar ação de saúde pública."
        ),
    ]
    cells += footer(
        [
            "Notificações atrasam, são revistas e dependem do sistema de vigilância.",
            "Preenchimento causal, choques externos e mudanças estruturais podem distorcer padrões históricos.",
            "Sazonalidade e desempenho passado podem mudar; não há garantia para o futuro.",
            "A importância por permutação descreve o modelo e não identifica causas epidemiológicas.",
        ],
        "Remova o lag 52, repita a validação temporal e compare com o baseline. Discuta o que a diferença sugere sobre sazonalidade e o que ela não prova.",
        [
            "Lags e janelas precisam ser deslocados para não enxergar o alvo atual.",
            "Validação temporal e baseline são requisitos mínimos de uma comparação honesta.",
            "Boa previsão passada não é explicação causal nem autorização para agir.",
        ],
        [
            "[InfoDengue — tutorial da API](https://info.dengue.mat.br/tutorial_api_python/locale-en)",
            "[scikit-learn — TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)",
            "[statsmodels — time series analysis](https://www.statsmodels.org/stable/tsa.html)",
        ],
        ("numpy", "pandas", "matplotlib", "seaborn", "scikit-learn", "statsmodels", "requests"),
    )
    return cells


NOTEBOOK_BUILDERS = {
    "01_estatistica_descritiva.ipynb": notebook_01,
    "02_aprendizado_supervisionado.ipynb": notebook_02,
    "03_aprendizado_nao_supervisionado.ipynb": notebook_03,
    "04_comparacao_modelos_hiperparametros.ipynb": notebook_04,
    "05_imagens_gradcam.ipynb": notebook_05,
    "06_analise_sobrevivencia.ipynb": notebook_06,
    "07_aprendizado_reforco.ipynb": notebook_07,
    "08_series_temporais.ipynb": notebook_08,
}


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, builder in NOTEBOOK_BUILDERS.items():
        cells = builder()
        for index, cell in enumerate(cells, 1):
            cell["id"] = f"cell-{index:03d}"
        notebook = {
            "cells": cells,
            "metadata": {
                "colab": {"name": filename, "provenance": []},
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python", "version": "3.11"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        path = OUT / filename
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"criado: {path.relative_to(ROOT)} ({len(cells)} células)")


if __name__ == "__main__":
    build()
