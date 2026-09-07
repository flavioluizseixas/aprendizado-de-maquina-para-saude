"""Gera a Tarefa 2 usando o documento da Tarefa 1 como modelo visual.

Execute com Python 3, sem dependências adicionais:
    python scripts/create_task2_docx.py
"""

from datetime import datetime, timezone
from pathlib import Path
from xml.dom import minidom
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "tarefas" / "Tarefa_1_Estatistica_Descritiva.docx"
OUTPUT = ROOT / "tarefas" / "Tarefa_2_Aprendizado_Supervisionado.docx"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

OBJECTIVES = [
    "separar treinamento e teste e ajustar o pré-processamento sem vazamento;",
    "avaliar regressão logística e Random Forest no mesmo teste reservado;",
    "interpretar sensibilidade, especificidade, ROC-AUC, PR-AUC e o efeito do limiar;",
    "estimar e interpretar odds ratios ajustadas e intervalos de confiança de 95%;",
    "investigar os modelos com importância por permutação e SHAP;",
    "distinguir previsão, associação condicional, explicabilidade e causalidade.",
]

RULES = [
    "Use Python em Jupyter ou Google Colab, com numpy, pandas, matplotlib, seaborn, "
    "scikit-learn, statsmodels, shap e ucimlrepo. Siga a preparação do notebook 02.",
    "Use FAST_MODE = True: amostra estratificada de 30.000 registros e random_state = 42. "
    "Mantenha os atributos e os rótulos em português adotados no notebook.",
    "Separe 80% para treinamento e 20% para teste, com stratify = y e random_state = 42. "
    "Ajuste imputação, padronização e classificadores preditivos somente no treinamento.",
    "Diabetes_binary: 0 = sem diabetes; 1 = pré-diabetes/diabetes. Consulte o dicionário "
    "da UCI para os códigos binários e ordinais; o alvo não distingue pré-diabetes de diabetes.",
    "Use limiar inicial de 0,5 e os parâmetros especificados nos itens. As métricas de "
    "desempenho devem usar somente o teste reservado, com a mesma divisão para os dois modelos.",
]

# Cada item contém título, orientação e resultados solicitados, sem gabarito numérico.
TASKS = [
    (
        "Dados, rótulos e divisão treino/teste",
        "Carregue a base UCI 891 com load_cdc_diabetes e prepare os conjuntos de entrada e alvo.",
        [
            "Registre fonte, alvo, tamanho da amostra e semente. Apresente o dicionário de variáveis "
            "e a distribuição do alvo em contagens e percentuais.",
            "Separe X e y, excluindo Diabetes_binary dos atributos. Mostre as dimensões de "
            "X_train e X_test e verifique a proporção das classes em cada partição.",
            "Explique a finalidade da estratificação e por que o teste não participa do ajuste "
            "do pré-processamento ou dos classificadores.",
        ],
    ),
    (
        "Inspeção de correlações",
        "Investigue associações monotônicas entre os atributos e o indicador-alvo.",
        [
            "Calcule a correlação de Spearman na amostra, como na referência. Liste os 12 atributos "
            "com maior correlação absoluta com o alvo, preservando o sinal dos coeficientes.",
            "Construa um heatmap desses atributos e do alvo. Comente códigos ordinais, redundância "
            "e limites da interpretação; correlação não demonstra causalidade.",
            "Esta exploração é descritiva: mantenha todos os atributos nos modelos. Não use esse "
            "ranking, que inclui o teste, para selecionar variáveis ou ajustar configurações.",
        ],
    ),
    (
        "Pipeline preditivo de regressão logística",
        "Construa e ajuste um pipeline que aprenda todas as transformações apenas no treinamento.",
        [
            "Use SimpleImputer(strategy = 'median'), StandardScaler e LogisticRegression com "
            "max_iter = 1_000, class_weight = 'balanced' e random_state = 42, nessa ordem.",
            "Preserve a codificação dos atributos usada no pipeline da referência. Obtenha as "
            "probabilidades da classe 1 no teste e classifique como positivo quando p ≥ 0,5.",
            "Explique o papel da imputação, da padronização e dos pesos de classe. Diferencie "
            "probabilidade estimada de decisão produzida por um limiar.",
        ],
    ),
    (
        "Avaliação da regressão logística no teste",
        "Descreva o desempenho do classificador no conjunto que não participou do ajuste.",
        [
            "Apresente VP, VN, FP e FN, acurácia, acurácia balanceada, sensibilidade, "
            "especificidade, precisão, F1, ROC-AUC e PR-AUC. Na função do projeto, pr_auc "
            "é calculada como average precision (AP).",
            "Produza a matriz de confusão e as curvas ROC e precisão-recall. Inclua as linhas "
            "de referência: diagonal na ROC e proporção da classe positiva no teste na curva PR.",
            "Interprete falsos positivos e falsos negativos em relação ao alvo. Explique por que "
            "acurácia e ROC-AUC, isoladamente, não descrevem todos os erros.",
        ],
    ),
    (
        "Modelo inferencial e odds ratios ajustadas",
        "Ajuste um segundo modelo logístico para estimar associações condicionais, separado do pipeline preditivo.",
        [
            "Use toda a amostra analítica de casos completos e informe participantes e eventos. "
            "Ajuste um GLM binomial com intercepto, sem penalização nem pesos de classe, "
            "com cov_type = 'HC3'. Inclua simultaneamente os atributos do quadro da referência.",
            "Mantenha as binárias em 0/1 e BMI, MentHlth e PhysHlth nas unidades originais. "
            "Codifique GenHlth, Age, Education e Income com dummies, omitindo o nível 1 "
            "como referência. Explicite o contraste de cada OR.",
            "Apresente coeficientes, OR = exp(coeficiente), IC95% robustos e valores-p, "
            "excluindo o intercepto da tabela. Construa o gráfico das 15 associações com maior "
            "valor absoluto do coeficiente, com eixo logarítmico e linha em OR = 1.",
            "Interprete uma exposição escolhida: contraste, direção, magnitude e IC95%. "
            "Diferencie odds de probabilidade e risco e discuta o caso em que o intervalo inclui 1.",
            "Explique por que os coeficientes do pipeline regularizado, padronizado e ponderado "
            "não são as OR deste modelo, e por que o uso da amostra completa aqui não constitui "
            "uma avaliação de generalização preditiva.",
        ],
    ),
    (
        "SHAP da regressão logística inferencial",
        "Explique as saídas do mesmo GLM usado para estimar as OR, utilizando seus coeficientes e intercepto.",
        [
            "Use shap.LinearExplainer com máscara Independent, até 500 registros de fundo "
            "(semente 42) e até 300 registros para explicação (semente 43). Preserve as dummies "
            "e configure max_samples para manter toda a amostra de fundo.",
            "Produza os gráficos de barras de importância média absoluta e beeswarm, "
            "com até 12 atributos. Interprete posição, cor e dispersão no beeswarm.",
            "Explique o significado de contribuições positivas e negativas na escala de log-odds. "
            "Compare a OR da exposição escolhida com sua distribuição SHAP; se necessário, "
            "amplie a exibição para incluir esse atributo.",
            "Diferencie o contraste global da OR das contribuições às previsões. Considere "
            "as categorias de referência e o efeito de atributos correlacionados na interpretação.",
        ],
    ),
    (
        "Random Forest: avaliação e comparação",
        "Treine um segundo classificador e avalie-o na mesma partição de teste usada pela regressão logística.",
        [
            "Ajuste um imputador de mediana no treinamento e transforme treino e teste. Use "
            "RandomForestClassifier com n_estimators = 150, class_weight = 'balanced_subsample', "
            "n_jobs = -1 e random_state = 42, sem padronização.",
            "Com limiar 0,5, apresente as métricas, a matriz de confusão e as curvas solicitadas "
            "no item 4. Reúna as métricas dos dois classificadores em uma tabela comparativa.",
            "Compare capacidade de ordenação e tipos de erro. Fundamente a leitura em mais "
            "de uma métrica e não apresente desempenho calculado no treinamento.",
        ],
    ),
    (
        "Importância por permutação no teste",
        "Investigue a dependência do desempenho da Random Forest em relação a cada atributo.",
        [
            "Use o modelo ajustado no treinamento e o teste já imputado. Execute permutation_importance "
            "com scoring = 'roc_auc', n_repeats = 3, random_state = 42 e n_jobs = -1.",
            "Mostre os 12 atributos com maior queda média de ROC-AUC em um gráfico de barras "
            "horizontais. Explique o que a queda mede e por que atributos correlacionados podem "
            "ter sua importância subestimada.",
            "Não use essa análise do teste para selecionar atributos ou reajustar hiperparâmetros; "
            "ela descreve o modelo já avaliado.",
        ],
    ),
    (
        "SHAP da Random Forest final",
        "Após concluir a avaliação, reajuste o imputador e uma nova Random Forest na amostra completa.",
        [
            "Mantenha os parâmetros do item 7. Use até 300 registros para explicação (semente 42) "
            "e até 100 registros de fundo (semente 43), com shap.Explainer.",
            "Selecione a saída da classe 1 quando houver uma dimensão por classe. Produza barras "
            "e beeswarm para até 12 atributos, além do gráfico de dependência do atributo com "
            "maior média do valor absoluto de SHAP.",
            "Identifique a escala da saída explicada antes de interpretar as contribuições. "
            "Diferencie este modelo final daquele usado nas métricas e na permutação: "
            "não calcule novas métricas de desempenho na amostra completa.",
        ],
    ),
    (
        "Experimento com limiares de decisão",
        "Retome as probabilidades de teste do pipeline preditivo de regressão logística, sem novo ajuste.",
        [
            "Aplique os limiares 0,3; 0,5; 0,7. Apresente, para cada um, sensibilidade, "
            "especificidade, FP e FN em uma tabela.",
            "Explique como os erros mudam ao variar o limiar e por que ROC-AUC e AP "
            "permanecem iguais quando as probabilidades são as mesmas.",
            "Trate a comparação como exercício didático, sem escolher um limiar de uso a partir "
            "do teste. Explique por que essa escolha exigiria validação separada e definição "
            "prévia dos custos dos erros.",
        ],
    ),
    (
        "Síntese, limitações e reprodutibilidade",
        "Conclua com três aprendizados e uma discussão breve dos limites dos resultados.",
        [
            "Aborde autorrelato, desbalanceamento, limiar e mudança de população. Explique "
            "por que desempenho, OR, permutação e SHAP não demonstram causalidade nem validam uso clínico.",
            "No GLM, discuta a linearidade na log-odds das variáveis contínuas e a ausência de "
            "interações. Os IC95% HC3 não incorporam pesos, estratos ou conglomerados do "
            "BRFSS; não devem ser apresentados como estimativas populacionais nacionais.",
            "Registre as versões de Python e das bibliotecas utilizadas e cite a fonte dos dados.",
        ],
    ),
]


def text_content(node):
    return "".join(
        child.data for text in node.getElementsByTagName("w:t")
        for child in text.childNodes if child.nodeType == child.TEXT_NODE
    )


def replace_text(paragraph, text, run_index=0):
    """Substitui o texto e preserva as propriedades do parágrafo e do run escolhido."""
    doc = paragraph.ownerDocument
    runs = paragraph.getElementsByTagName("w:r")
    run = runs[run_index].cloneNode(True) if runs else doc.createElementNS(W_NS, "w:r")
    for child in list(run.childNodes):
        if child.nodeName != "w:rPr":
            run.removeChild(child)
    for child in list(paragraph.childNodes):
        if child.nodeName != "w:pPr":
            paragraph.removeChild(child)
    for i, line in enumerate(text.split("\n")):
        if i:
            run.appendChild(doc.createElementNS(W_NS, "w:br"))
        t = doc.createElementNS(W_NS, "w:t")
        t.setAttribute("xml:space", "preserve")
        t.appendChild(doc.createTextNode(line))
        run.appendChild(t)
    paragraph.appendChild(run)
    return paragraph


def paragraph_property(paragraph, name, **attributes):
    doc = paragraph.ownerDocument
    props = next((c for c in paragraph.childNodes if c.nodeName == "w:pPr"), None)
    if props is None:
        props = doc.createElementNS(W_NS, "w:pPr")
        paragraph.insertBefore(props, paragraph.firstChild)
    element = doc.createElementNS(W_NS, f"w:{name}")
    for key, value in attributes.items():
        element.setAttribute(f"w:{key}", str(value))
    # Respeita a ordem das propriedades no esquema WordprocessingML.
    order = {"w:pStyle": 0, "w:keepNext": 1, "w:keepLines": 2, "w:pageBreakBefore": 3}
    before = next((c for c in props.childNodes
                   if order.get(c.nodeName, 4) > order[element.nodeName]), None)
    props.insertBefore(element, before)


def build_parts():
    with ZipFile(TEMPLATE) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    doc = minidom.parseString(parts["word/document.xml"])
    body = doc.getElementsByTagName("w:body")[0]
    elements = [n for n in body.childNodes if n.nodeType == n.ELEMENT_NODE]

    def template(prefix):
        return next(n for n in elements if text_content(n).startswith(prefix)).cloneNode(True)

    band = template("TAREFA 1")
    title = template("Conhecendo indicadores")
    subtitle = template("Estatística descritiva,")
    question = template("Pergunta orientadora")
    context = template("CONTEXTO")
    heading = template("O que você deverá demonstrar")
    bullet = template("obter e inspecionar")
    source = template("Fonte oficial")
    important = template("IMPORTANTE")
    item_heading = template("1Obtenção dos dados")
    intro = template("Carregue o conjunto UCI")
    instructions = template("Construa um notebook executável")
    section = doc.getElementsByTagName("w:sectPr")[0].cloneNode(True)
    for child in list(body.childNodes):
        body.removeChild(child)

    def append_paragraph(base, text, page_break=False, keep_next=False):
        p = replace_text(base.cloneNode(True), text)
        paragraph_property(p, "keepLines")
        if keep_next:
            paragraph_property(p, "keepNext")
        if page_break:
            paragraph_property(p, "pageBreakBefore")
        body.appendChild(p)
        return p

    band.getElementsByTagName("w:t")[0].firstChild.data = "TAREFA 2"
    body.appendChild(band)
    append_paragraph(intro, "")
    append_paragraph(title, "Predição e explicabilidade\nem saúde")
    append_paragraph(subtitle, "Aprendizado supervisionado, desempenho e interpretação")
    replace_text(question, "Um modelo consegue ordenar pessoas com e sem o indicador-alvo, "
                 "e quais erros aparecem quando escolhemos um limiar?", run_index=2)
    # Mantém a identificação laranja da pergunta e o corpo em itálico azul.
    label = template("Pergunta orientadora").getElementsByTagName("w:r")[0].cloneNode(True)
    label.getElementsByTagName("w:t")[0].firstChild.data = "Pergunta orientadora  "
    question.insertBefore(label, question.getElementsByTagName("w:r")[0])
    body.appendChild(question)
    replace_text(context.getElementsByTagName("w:p")[1],
                 "Você analisará o conjunto CDC Diabetes Health Indicators (UCI 891), derivado do "
                 "BRFSS, com indicadores de saúde e comportamentos autorrelatados. Seu objetivo é "
                 "construir classificadores, avaliar seus erros e interpretar associações e contribuições "
                 "às previsões. O exercício tem finalidade educacional e não produz um diagnóstico.")
    body.appendChild(context)
    append_paragraph(heading, "O que você deverá demonstrar")
    for objective in OBJECTIVES:
        append_paragraph(bullet, objective)
    append_paragraph(heading, "Base, ambiente e regras de comparabilidade")
    body.appendChild(source)
    for rule in RULES:
        append_paragraph(bullet, rule)
    replace_text(important.getElementsByTagName("w:p")[1],
                 "A referência é o notebook 02_aprendizado_supervisionado.ipynb. "
                 "Desenvolva também a atividade de comparação de limiares proposta ao final dele.")
    body.appendChild(important)

    append_paragraph(heading, "Enunciado", page_break=True)
    append_paragraph(instructions, "Construa um notebook executável do início ao fim. Organize cada item "
                     "com uma célula Markdown que explique a pergunta, seguida do código, da saída e de "
                     "uma interpretação breve em linguagem própria.")
    for number, (name, instruction, bullets) in enumerate(TASKS, 1):
        if number in (5, 8):
            append_paragraph(heading, "Enunciado · continuação", page_break=True)
        elif number > 1:
            spacer = append_paragraph(intro, "", keep_next=True)
            spacing = spacer.getElementsByTagName("w:spacing")[0]
            spacing.setAttribute("w:after", "0")
            spacing.setAttribute("w:line", "80")
            spacing.setAttribute("w:lineRule", "exact")
        table = item_heading.cloneNode(True)
        ps = table.getElementsByTagName("w:p")
        replace_text(ps[0], str(number))
        replace_text(ps[1], name)
        for p in ps:
            paragraph_property(p, "keepNext")
        row_props = table.getElementsByTagName("w:trPr")[0]
        row_props.insertBefore(doc.createElementNS(W_NS, "w:cantSplit"), row_props.firstChild)
        body.appendChild(table)
        append_paragraph(intro, instruction, keep_next=True)
        for instruction_bullet in bullets:
            append_paragraph(bullet, instruction_bullet)

    append_paragraph(heading, "Formato de entrega")
    append_paragraph(intro, "Entregue nome_sobrenome_tarefa2.ipynb executado, com tabelas e figuras "
                     "visíveis, interpretações autorais, fonte dos dados e versões do ambiente. "
                     "O arquivo deve executar de cima para baixo sem depender de estado oculto.")
    body.appendChild(section)

    # Remove identificadores repetidos e marcas de revisão/paginação herdadas do modelo.
    for node in doc.getElementsByTagName("*"):
        for attr in list(node.attributes.keys()):
            if attr in ("w14:paraId", "w14:textId") or attr.startswith("w:rsid"):
                node.removeAttribute(attr)
    for tag in ("w:proofErr", "w:lastRenderedPageBreak", "w:bookmarkStart", "w:bookmarkEnd"):
        for node in list(doc.getElementsByTagName(tag)):
            node.parentNode.removeChild(node)
    parts["word/document.xml"] = doc.toxml(encoding="UTF-8")

    footer = minidom.parseString(parts["word/footer1.xml"])
    replace_text(footer.getElementsByTagName("w:tc")[0].getElementsByTagName("w:p")[0],
                 "Tarefa 2  •  Aprendizado supervisionado")
    parts["word/footer1.xml"] = footer.toxml(encoding="UTF-8")

    core = minidom.parseString(parts["docProps/core.xml"])
    values = {
        "dc:title": "Tarefa 2 — Aprendizado supervisionado",
        "dc:subject": "Aprendizado de Máquina para Saúde",
        "dc:description": "Enunciado alinhado ao notebook 02_aprendizado_supervisionado.ipynb.",
        "cp:keywords": "saúde, classificação, regressão logística, Random Forest, odds ratio, SHAP",
        "dcterms:modified": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }
    for tag, value in values.items():
        nodes = core.getElementsByTagName(tag)
        if nodes:
            node = nodes[0]
            for child in list(node.childNodes):
                node.removeChild(child)
            node.appendChild(core.createTextNode(value))
    parts["docProps/core.xml"] = core.toxml(encoding="UTF-8")
    app = minidom.parseString(parts["docProps/app.xml"])
    for tag in ("Pages", "Words", "Characters", "CharactersWithSpaces", "Lines", "Paragraphs", "TotalTime"):
        for node in list(app.getElementsByTagName(tag)):
            node.parentNode.removeChild(node)
    parts["docProps/app.xml"] = app.toxml(encoding="UTF-8")
    return parts


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in build_parts().items():
            archive.writestr(name, content)
    print(OUTPUT)


if __name__ == "__main__":
    main()
