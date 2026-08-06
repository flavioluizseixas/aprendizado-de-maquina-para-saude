# Carregar pacotes necessários
library(survival)
library(ggplot2)
library(survminer)
library(dplyr)

# Carregar o conjunto de dados cancer
data(cancer, package="survival")

# Limpeza dos dados: remover observações com dados ausentes
cancer <- cancer %>%
  na.omit()

# Visualizar os dados
head(cancer)

#inst: Institution code
#time: Survival time in days
#status: censoring status 1=censored, 2=dead
#age: Age in years
#sex: Male=1 Female=2
#ph.ecog: ECOG performance score as rated by the physician. 0=asymptomatic, 1= symptomatic but completely ambulatorph.karno: Karnofsky performance score (bad=0-good=100) rated by physician
#pat.karno: Karnofsky performance score as rated by patient
#meal.cal: Calories consumed at meals
#wt.loss: Weight loss in last six months (pounds)

# Análise descritiva
summary(cancer)

# Ajustar o modelo de Weibull
weibull_model <- survreg(Surv(time, status) ~ age + sex + meal.cal, data = cancer, dist = "weibull")

# Resumo do modelo de Weibull
summary(weibull_model)

# Ajustar o modelo de Cox
cox_model <- coxph(Surv(time, status) ~ age + sex + meal.cal, data = cancer)

# Resumo do modelo de Cox
summary(cox_model)

# Comparar os dois modelos
# (AIC para ambos os modelos)
weibull_aic <- AIC(weibull_model)
cox_aic <- AIC(cox_model)

cat("AIC do modelo Weibull:", weibull_aic, "\n")
cat("AIC do modelo Cox:", cox_aic, "\n")

# Análise de sobrevivência - Kaplan-Meier
km_fit <- survfit(Surv(time, status) ~ sex, data = cancer)

# Visualização das curvas de sobrevivência de Kaplan-Meier
ggsurvplot(km_fit, data = cancer,
           title = "Curvas de Sobrevivência de Kaplan-Meier por Sexo",
           xlab = "Tempo (dias)",
           ylab = "Probabilidade de Sobrevivência",
           risk.table = TRUE,
           pval = TRUE,
           legend.labs = c("Masculino", "Feminino"))

# Visualização dos efeitos dos preditores no modelo de Cox
ggforest(cox_model, data = cancer)

# Visualização dos efeitos dos preditores no modelo Weibull
# Obter os valores preditos do modelo Weibull
predicted_survival <- predict(weibull_model, type = "response")

# Adicionar os valores preditos ao conjunto de dados
cancer$predicted_survival <- predicted_survival

# Modificar a variável 'sex' para ser um fator com labels descritivos
cancer$sex <- factor(cancer$sex, levels = c(1, 2), labels = c("Masculino", "Feminino"))

# Criar um gráfico de dispersão para visualizar os efeitos do modelo Weibull
ggplot(cancer, aes(x = age, y = predicted_survival, color = as.factor(sex))) +
  geom_point() +
  labs(title = "Efeitos do Modelo Weibull",
       x = "Idade",
       y = "Sobrevivência Predita",
       color = "Sexo") +
  theme_minimal()
