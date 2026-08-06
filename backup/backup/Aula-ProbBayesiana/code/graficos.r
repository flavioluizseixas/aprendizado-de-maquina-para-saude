# binomial
x <- 0:20
plot(x, dbinom(x, size=20, prob=.3),type='h')

# Hipergeometrica
m <- 10; n <- 7;
x <- 0:9
plot(x, dhyper(x, m, n, k),type='h')

# Poisson
m <- 1.8
x <- 0:9
plot(x, dpois(x,m),type='h')

# Binomial invertida
a <- 5
x <- 0:40
plot(x, dnbinom(x,a,prob=0.3),type='h')

