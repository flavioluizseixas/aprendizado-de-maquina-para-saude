"""Valida JSON, metadados, células obrigatórias e sintaxe dos notebooks."""

from __future__ import annotations

import ast
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "notebooks").glob("*.ipynb"))
NOTICE_FRAGMENT = "finalidade exclusivamente educacional"


def validate_notebook(path: Path) -> list[str]:
    errors: list[str] = []
    notebook = nbformat.read(path, as_version=4)
    text = "\n".join(cell.source for cell in notebook.cells)
    header = notebook.cells[0].source if notebook.cells else ""
    if NOTICE_FRAGMENT not in text:
        errors.append("aviso educacional ausente")
    if "colab.research.google.com/github/" not in text:
        errors.append("botão Colab ausente")
    if any(line.startswith("    ") for line in header.splitlines() if line.strip()):
        errors.append("cabeçalho Markdown contém bloco de código por indentação")
    source_section = header.partition("## Fonte e licença")[2]
    if not source_section or "](" not in source_section:
        errors.append("fonte descritiva sem link no cabeçalho")
    if "Três aprendizados principais" not in text:
        errors.append("síntese final ausente")
    if "Versões" not in text:
        errors.append("registro de versões ausente")
    if path.name[:2] in {f"{number:02d}" for number in range(2, 9)}:
        if "## Onde executar" not in text or "### Computador local" not in text:
            errors.append("instruções de execução Colab/local ausentes")
        if "Dicionário" not in text:
            errors.append("dicionário de dados ou rótulos ausente")
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type == "code":
            try:
                ast.parse(cell.source)
            except SyntaxError as exc:
                errors.append(f"célula {index} com sintaxe inválida: {exc}")
            if cell.get("outputs"):
                errors.append(f"célula {index} contém saída versionada")
    return errors


def main() -> None:
    if len(NOTEBOOKS) != 8:
        raise SystemExit(f"Esperados 8 notebooks; encontrados {len(NOTEBOOKS)}.")
    failures = {path.name: validate_notebook(path) for path in NOTEBOOKS}
    failures = {name: errors for name, errors in failures.items() if errors}
    if failures:
        details = "\n".join(f"- {name}: {', '.join(errors)}" for name, errors in failures.items())
        raise SystemExit(f"Falhas nos notebooks:\n{details}")
    print(f"OK: {len(NOTEBOOKS)} notebooks válidos, sem saídas versionadas.")


if __name__ == "__main__":
    main()
