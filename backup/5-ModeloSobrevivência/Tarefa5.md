# Análise de Sobrevivência em Pacientes com Cancer de Pulmao

O foco é modelar e interpretar fatores associados à sobrevivência de pacientes com câncer de pulmão, aplicando os modelos de Weibull e Cox e realizando uma análise de decomposição.

## Objetivo
Este projeto tem como objetivo analisar fatores associados à sobrevivência de pacientes com câncer de pulmão a partir do conjunto de dados cancer. Utilizando os modelos de Weibull e Cox, a análise busca identificar e interpretar os efeitos de variáveis preditoras (como idade, sexo e ingestão calórica) na sobrevivência dos pacientes, além de realizar uma decomposição para compreender a contribuição relativa de cada variável.

## Metodologia
1. Coleta e Preparação de Dados

- Carregar o conjunto de dados cancer usando data(cancer, package="survival"). Este conjunto de dados também está disponivel no endereço https://github.com/flavioluizseixas/aprendizado-de-maquina-na-saude/blob/main/5-ModeloSobreviv%C3%AAncia/data/cancer_data.csv
- Explorar e preparar os dados, removendo valores ausentes e fazendo uma análise descritiva das variáveis relevantes (tempo de sobrevivência, status de censura, idade, sexo, ingestão calórica diária, entre outros).
- As seguintes variáveis estão presentes no dataset
  - inst: Institution code
  - time: Survival time in days
  - status: censoring status 1=censored, 2=dead
  - age: Age in years
  - sex: Male=1 Female=2
  - ph.ecog: ECOG performance score as rated by the physician. 0=asymptomatic, 1= symptomatic but completely ambulatorph.karno: Karnofsky performance score (bad=0-good=100) rated by physician
  - pat.karno: Karnofsky performance score as rated by patient
  - meal.cal: Calories consumed at meals
  - wt.loss: Weight loss in last six months (pounds)

3. Análise de Kaplan-Meier

- Realizar uma análise de sobrevivência Kaplan-Meier para estimar as curvas de sobrevivência dos pacientes, categorizados por variáveis como sexo.
- Visualizar as curvas Kaplan-Meier e interpretar as diferenças na sobrevivência entre os grupos.
Modelagem de Sobrevivência

4. Análise de Decomposição

- Aplicar uma análise de decomposição para avaliar a contribuição relativa de cada variável preditora nos modelos de Weibull e Cox.
- Interpretar como cada preditor influencia o risco e o tempo de sobrevivência dos pacientes, utilizando gráficos de efeitos marginais e curvas de sobrevivênci

5. Visualização e Interpretação

- Visualizar os resultados das análises de sobrevivência e decomposição usando gráficos que representem as curvas de sobrevivência para diferentes grupos e os efeitos das variáveis preditoras.
- Comparar e interpretar os efeitos dos preditores nos modelos de Weibull e Cox, discutindo as implicações clínicas.