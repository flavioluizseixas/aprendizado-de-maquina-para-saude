
# Tarefa 2

## Modelagem da relação entre o índice de massa corporal (IMC) e a pressão arterial sistólica (PAS)

A base de dados National Health and Nutrition Examination Survey (NHANES) contém uma vasta gama de informações sobre a saúde e nutrição de indivíduos nos Estados Unidos. Neste exercício, vamos utilizar os dados da pesquisa de 2015-2016 para estudar a relação entre o Índice de Massa Corporal (IMC) e a Pressão Arterial Sistólica (PAS) em adultos com idade entre 20 e 60 anos.

**Objetivo:** criar um modelo de regressão linear para prever a Pressão Arterial Sistólica (PAS) a partir do Índice de Massa Corporal (IMC) e avaliar o desempenho deste modelo. Além disso, você deve interpretar os resultados obtidos, com foco na relação entre essas duas variáveis.

## Base de Dados:

Vamos utilizar as seguintes tabelas do NHANES 2015-2016:

- **Demographic Variables:** Contém informações demográficas como idade e sexo.
  - **Atributo de interesse:** RIDAGEYR (Idade em anos)
  - [Link para a tabela](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.htm)

- **Body Measures:** Contém informações sobre medidas corporais, incluindo o Índice de Massa Corporal (IMC).
  - **Atributo de interesse:** BMXBMI (Índice de Massa Corporal)
  - [Link para a tabela](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BMX_I.htm)

- **Blood Pressure:** Contém dados sobre medições de pressão arterial.
  - **Atributo de interesse:** BPXSY1 (Pressão Arterial Sistólica - 1ª Medição)
  - [Link para a tabela](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BPX_I.htm)

- **Laboratory Data - Glucose:** Contém dados sobre medições de glicose em jejum.
  - **Atributo de interesse:** LBXGLU (Glicose)
  - [Link para a tabela](https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/GLU_I.htm)


Os dados estão disponíveis em formato XPT no seguinte link:
- [Base NHANES 2015-2016](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=examination)


## Atividades:

1. Carregamento de dados:
  - Baixe e carregue as tabelas necessárias para a análise.

2. Merge dos dados:
  - Realize o merge das três tabelas utilizando o atributo SEQN (número de identificação único de cada participante) como chave.

3. Filtragem dos dados:
  - Selecione os participantes com idade entre 20 e 60 anos (RIDAGEYR).
  - Filtre as colunas de interesse: RIDAGEYR (Idade), BMXBMI (IMC) e BPXSY1 (PAS).

4. Análise exploratória:
  - Visualize a relação entre o Índice de Massa Corporal (IMC), a Pressão Arterial Sistólica (PAS) utilizando gráficos apropriados (por exemplo, scatter plot).

5. Estimativa do modelo:
  - Crie um modelo de regressão linear simples para prever a Pressão Arterial Sistólica (PAS) a partir do Índice de Massa Corporal (IMC).

6. Avaliação do modelo:
  - Avalie a qualidade do modelo usando métricas como o $R^2$, o erro médio absoluto (MAE) ou o erro quadrático médio (MSE).

7. Interprete os coeficientes do modelo.

## Perguntas:

1. Podemos afirmar, com base no modelo, que existe uma relação estatisticamente significativa entre o Índice de Massa Corporal (IMC) e a Pressão Arterial Sistólica (PAS)? Explique.

2. Refaça o exercício para IMC e o nível de glicose no sangue (LBGLU), e IMC e a circunferência da cintura (BMXWAIST). Quais dessas medidas estão correlacionadas?

3. Utilizando o modelo de regressão, qual seria o valor estimado da circunferência da cintura para um indivíduo com IMC igual a 25?

- **Opcional:** verificar possíveis correlações para IMC e o nível de triglicérides (LBXTR) e colesterol total (LBXTC).