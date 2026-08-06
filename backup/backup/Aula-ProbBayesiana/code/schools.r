setwd("~/Dev/tex/ml4healthcare/4-Aula-ProbBayesiana/code")
library(rjags)
schools <- read.table ("schools.dat", header=TRUE)
J <- nrow(schools)
y <- schools$estimate
sigma.y <- schools$sd
data <- list ("J", "y", "sigma.y")
inits <- function() {list (theta=rnorm(J,0,100), mu.theta=rnorm(1,0,100), sigma.theta=runif(1,0,100))}
parameters <- c("theta", "mu.theta", "sigma.theta")
schools.sim <- bugs (data, inits, parameters, "schools.bug", n.chains=3, n.iter=1000)
