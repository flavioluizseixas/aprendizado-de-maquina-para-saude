"""Gera figuras, DOCX e PDF da apostila.

Dependências editoriais: matplotlib, numpy, python-docx, Pandoc e Typst.
Aceita Typst no PATH ou a distribuição incluída no Quarto para Windows.
"""

from pathlib import Path
import math
import subprocess
import shutil
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "apostilas"
STEM = "apostila_regressao_logistica"
FIG = OUT / "figuras" / "regressao_logistica"
REVIEW = OUT / "revisao"
BLUE = "#005373"
TEAL = "#007F83"
GREY = "#D9E2E8"


def save_figure(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def figures():
    FIG.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(8.5, 4.1))
    for i in range(100):
        ax.scatter(i % 20, 4 - i // 20, s=105, color=TEAL if i < 20 else GREY)
    ax.text(-.4, 6.0, "20 eventos em um total de 100", color=BLUE, fontsize=16, weight="bold")
    ax.text(0, -2.45, "PROBABILIDADE\n20 / 100 = 20%", fontsize=13, color=BLUE, linespacing=1.6)
    ax.text(10.5, -2.45, "ODDS\n20 / 80 = 0,25", fontsize=13, color=BLUE, linespacing=1.6)
    ax.set(xlim=(-1, 20), ylim=(-3.1, 6.7))
    ax.axis("off")
    save_figure(fig, "probabilidade_odds")

    fig, ax = plt.subplots(figsize=(8.5, 3.7))
    eta = np.linspace(-5, 5, 400)
    ax.plot(eta, 1 / (1 + np.exp(-eta)), color=BLUE, linewidth=2.8)
    points = [(math.log(.25), .2, "odds = 0,25\np = 20%"),
              (0, .5, "odds = 1\np = 50%"),
              (math.log(4), .8, "odds = 4\np = 80%")]
    for x, y, label in points:
        ax.scatter(x, y, color=TEAL, s=45, zorder=4)
        ax.annotate(label, (x, y), xytext=(-70, 18) if x < 0 else (12, -3),
                    textcoords="offset points", fontsize=10, color=BLUE)
    ax.set(xlabel="Log-odds do perfil (η)", ylabel="Probabilidade do evento", ylim=(0, 1), xlim=(-5, 5))
    ax.set_yticks(np.arange(0, 1.01, .2), ["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=.18)
    fig.tight_layout()
    save_figure(fig, "curva_logistica")

    fig, ax = plt.subplots(figsize=(8.5, 3.4))
    labels = ["Idade (+1 ano)", "Internação prévia\n(sim versus não)", "Acompanhamento\n(sim versus não)"]
    bs = np.array([.04, math.log(2), math.log(.7)])
    ses = np.array([.025, .25, .22])
    ors, low, high = np.exp(bs), np.exp(bs-1.96*ses), np.exp(bs+1.96*ses)
    y = np.array([2, 1, 0])
    ax.errorbar(ors, y, xerr=[ors-low, high-ors], fmt="o", color=BLUE,
                ecolor=TEAL, capsize=5, markersize=7, linewidth=2)
    ax.axvline(1, color="#64748B", linestyle="--", linewidth=1.2)
    ax.set_yticks(y, labels)
    ax.set_xscale("log")
    ax.set_xticks([.25, .5, 1, 2, 4], ["0,25", "0,50", "1,00", "2,00", "4,00"])
    ax.minorticks_off()
    ax.set(xlim=(.25, 4), ylim=(-.55, 2.55), xlabel="Odds ratio e IC95% — valores hipotéticos")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=15)
    ax.grid(axis="x", alpha=.12)
    fig.tight_layout()
    save_figure(fig, "or_intervalos")


def template():
    REVIEW.mkdir(parents=True, exist_ok=True)
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Cm(2.5)
    s.header_distance = s.footer_distance = Cm(1.2)
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = "Aptos", Pt(11.5)
    normal.paragraph_format.line_spacing = 1.12
    normal.paragraph_format.space_after = Pt(7)
    normal.paragraph_format.widow_control = True
    for name, size in [("Title", 28), ("Subtitle", 15), ("Heading 1", 20), ("Heading 2", 15), ("Heading 3", 12)]:
        st = doc.styles[name]
        st.font.name, st.font.size = "Aptos", Pt(size)
        st.font.color.rgb = RGBColor.from_string("005373")
        st.font.bold = False
        st.paragraph_format.space_before = Pt(15 if name.startswith("Heading") else 5)
        st.paragraph_format.space_after = Pt(8)
        st.paragraph_format.keep_with_next = True
    footer = s.footer.paragraphs[0]
    footer.alignment = 1
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    footer._p.append(fld)
    path = REVIEW / "modelo_apostila.docx"
    doc.save(path)
    return path


def format_docx(path):
    doc = Document(path)
    # A populated, clickable contents list also works in readers that do not
    # update Word TOC fields. Page numbering is provided by the PDF outline.
    entries = []
    anchor = None
    for element in doc._element.body:
        if element.tag == qn("w:bookmarkStart"):
            anchor = element.get(qn("w:name"))
        if element.tag == qn("w:p") and element.xpath('./w:pPr/w:pStyle[@w:val="Heading1"]'):
            title = "".join(element.xpath('.//w:t/text()'))
            entries.append((title, anchor))
    for content in doc._element.xpath('.//w:sdtContent'):
        for element in list(content)[1:]:
            content.remove(element)
        for title, anchor in entries:
            p = OxmlElement("w:p")
            pr = OxmlElement("w:pPr")
            spacing = OxmlElement("w:spacing")
            spacing.set(qn("w:after"), "80")
            pr.append(spacing)
            p.append(pr)
            link = OxmlElement("w:hyperlink")
            link.set(qn("w:anchor"), anchor)
            run = OxmlElement("w:r")
            rpr = OxmlElement("w:rPr")
            size = OxmlElement("w:sz")
            size.set(qn("w:val"), "21")
            rpr.append(size)
            run.append(rpr)
            text = OxmlElement("w:t")
            text.text = title
            run.append(text)
            link.append(run)
            p.append(link)
            content.append(p)
    starts = ("Apresentação", "11. Oficina", "12. Gabarito", "13. Folha", "Fontes citadas", "Apêndice")
    for p in doc.paragraphs:
        if p.style.name == "Heading 1" and p.text.startswith(starts):
            p.paragraph_format.page_break_before = True
        if p.style.name in ["Caption", "Image Caption"]:
            p.paragraph_format.space_after = Pt(9)
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor.from_string("475569")
        if p._p.xpath(".//w:drawing"):
            p.paragraph_format.keep_with_next = True
        # Prevent an equation from remaining alone on the next page.
        if p._p.xpath(".//m:oMathPara"):
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
    for table in doc.tables:
        table.autofit = False
        count = len(table.columns)
        if count == 6:
            widths = [5.0, 1.55, 1.35, 1.3, 3.0, 1.6]
        elif count == 5:
            widths = [1.3, 3.1, 3.2, 3.4, 2.8]
        elif count == 4:
            widths = [4.0, 4.0, 4.0, 4.0]
        elif count == 3:
            widths = [4.4, 4.3, 7.3]
        else:
            widths = [5.0, 11.0]
        scale = 16 / sum(widths)
        for col, width in zip(table.columns, widths):
            col.width = Cm(width * scale)
        for ri, row in enumerate(table.rows):
            props = row._tr.get_or_add_trPr()
            props.append(OxmlElement("w:cantSplit"))
            if ri == 0:
                props.append(OxmlElement("w:tblHeader"))
            for ci, cell in enumerate(row.cells):
                cell.width = Cm(widths[ci] * scale)
                shade = OxmlElement("w:shd")
                shade.set(qn("w:fill"), "EAF2F6" if ri == 0 else ("F7F9FA" if ri % 2 == 0 else "FFFFFF"))
                cell._tc.get_or_add_tcPr().append(shade)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(4)
                    p.paragraph_format.line_spacing = 1.04
                    p.paragraph_format.keep_with_next = ri == 0
                    for run in p.runs:
                        run.font.size = Pt(10 if count < 6 else 9.5)
                        if ri == 0:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor.from_string("005373")
    doc.save(path)


def main():
    figures()
    ref = template()
    target = OUT / f"{STEM}.docx"
    subprocess.run(["pandoc", str(OUT / f"{STEM}.md"), "--from=markdown", "--to=docx",
                    "--standalone", "--toc", "--toc-depth=1", f"--reference-doc={ref}",
                    f"--resource-path={OUT}", "--output", str(target)], check=True, cwd=ROOT)
    format_docx(target)
    build_pdf()
    print(target)
    print("Palavras (Markdown):", len((OUT / f"{STEM}.md").read_text(encoding="utf-8").split()))


def build_pdf():
    typst = shutil.which("typst")
    if not typst:
        bundled = Path.home() / "AppData/Local/Programs/Quarto/bin/tools/x86_64/typst.exe"
        if bundled.is_file():
            typst = str(bundled)
    if not typst:
        raise RuntimeError("Typst não encontrado no PATH nem na instalação local do Quarto.")
    source = REVIEW / f"{STEM}.typ"
    subprocess.run(["pandoc", str(OUT / f"{STEM}.md"), "--from=markdown", "--to=typst", "--wrap=none",
                    "--standalone", f"--template={ROOT / 'scripts/apostila_regressao_logistica.typst'}",
                    f"--resource-path={OUT}", "--output", str(source)], check=True, cwd=ROOT)
    data = source.read_text(encoding="utf-8").replace('image("figuras/', 'image("../figuras/')
    data = re.sub(r"(?m)^\+ (<fonte-\d+>) ", r"+ #box[]\1 ", data)
    # Pandoc emits the decimal comma as math punctuation; use a compact literal.
    data = re.sub(r'(\d+) \\, (\d+)', r'"\1,\2"', data)
    data = data.replace('columns: (13.64%, 18.18%, 18.18%, 18.18%, 13.64%, 18.18%),',
                        'columns: (34%, 11%, 10%, 10%, 20%, 15%),')
    # Keep short introductions with their equations or example lists.
    data = re.sub(r'(?m)^([^\n=][^\n]*:)\n\n(\$ [^\n]+ \$)\n',
                  r'#block(breakable: false)[\n\1\n\n\2\n]\n', data)
    data = re.sub(r'(?m)^(#strong\[Exemplo hipotético:\][^\n]*:)\n\n((?:- [^\n]+\n)+)',
                  r'#block(breakable: false)[\n\1\n\n\2]\n', data)
    for title in ["11. Oficina", "12. Gabarito", "13. Folha", "Fontes citadas", "Apêndice"]:
        data = data.replace(f"\n= {title}", f"\n#pagebreak(weak: true)\n\n= {title}")
    source.write_text(data, encoding="utf-8")
    subprocess.run([typst, "compile", "--root", str(ROOT), str(source), str(OUT / f"{STEM}.pdf")],
                   check=True, cwd=ROOT)



if __name__ == "__main__":
    main()
