# Revisão da proposta de apostila

Data: 14/09/2026.

Material: **Da probabilidade à interpretação — Regressão logística, coeficientes, odds e odds ratio**.

A proposta foi elaborada para uma turma iniciante da área da saúde, com percurso principal sem programação e ponte opcional para o notebook mínimo do encontro 02. Segue a organização das apostilas de Informática em Saúde Aplicada à Enfermagem: apresentação, objetivos, caso condutor, explicações graduais, pausas, oficina, síntese, glossário e referências. A apresentação usa página A4, margens de 2,5 cm e títulos azuis.

## Entregas

- PDF com 18 páginas, sumário clicável e marcadores de navegação.
- Word editável, com sumário de links internos e equações editáveis.
- Markdown como fonte do conteúdo.
- Três figuras originais e oito atividades com gabarito comentado.

## Fontes verificadas

Os dois arquivos consultados estão em `C:/Users/flavio/Dev/aula-aprendizado-de-maquina-para-saude/pdfs/`:

- `Applied Logistic Regression, 2nd ed_ -- D_W_ Hosmer and S_ Lemeshow -- 2009 -- 5970db5652aee2ffce7b6e8ac0de28e6 -- Anna’s Archive.pdf`: 397 páginas; arquivo digitalizado, consultado visualmente nos trechos citados. A ficha editorial registra a 2ª edição de 2000. Nos trechos referenciados, a página do PDF corresponde à página impressa acrescida de 21.
- `Logistic Regression_ Binary and Multinomial -- G_ David Garson -- 2014 -- Statistical Associates Publishing -- isbn13 9781626380240 -- f1460addc189d89271147b0ead82dd56 -- Anna’s Archive.pdf`: 224 páginas, com texto extraível; a paginação impressa coincide com o contador nos trechos citados.

As páginas específicas constam em “Fontes citadas” na apostila. A integração com o projeto foi conferida no notebook `02_aprendizado_supervisionado_versão_minima.ipynb`, sem executá-lo nem apresentar resultados empíricos novos. Os casos, os coeficientes e os erros-padrão são explicitamente hipotéticos.

## Conferências realizadas

- Recálculo da OR bruta, do risco relativo, das conversões entre probabilidade e odds e dos exemplos de mudança de unidade.
- Recálculo das três OR, dos IC95% e dos valores-p de Wald da tabela didática.
- Conferência das probabilidades do modelo hipotético e das respostas dos exercícios.
- Verificação dos dez destinos das citações e dos links internos do Word.
- Correspondência estrutural entre Markdown e Word: 79 expressões matemáticas, 16 tabelas e 3 figuras.
- Revisão visual das páginas do PDF por miniaturas e das páginas com fórmulas e tabelas ampliadas; conferência automatizada de margens, páginas, imagens e destinos dos links.

O PDF foi renderizado com Typst. O Word foi verificado estruturalmente; sua paginação pode variar conforme a versão do editor e as fontes disponíveis. O documento editável usa Aptos, como a referência; o PDF usa Calibri.

## Regeneração

Na raiz do projeto, execute `python scripts/gerar_apostila_regressao_logistica.py`. O gerador utiliza Pandoc, Typst, matplotlib, numpy e python-docx; as dependências editoriais não foram acrescentadas às dependências dos notebooks. O template do PDF está em `scripts/apostila_regressao_logistica.typst`.

A pasta temporária `revisao/`, ignorada pelo Git, é recriada pelo gerador. Os PDFs originais e as apostilas usadas como referência não foram alterados.
