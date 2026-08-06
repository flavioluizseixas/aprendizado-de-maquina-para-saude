#***************************************************************#
# www.metodosexatos.com                                         #
# Prof.Ms. André Santos | andre@metodosexatos.com.br            #
# Curso Análise Bayesiana: Monte Carlo com Cadeias de Markov    #
# Cadeias de Markov                                             #
# Data: 10/12/2019                                              #
#***************************************************************#

# Exemplo - Manejo de Aves (MCCM)

# Pacotes requeridos
#install.packages("expm")
#install.packages("markovchain")
#install.packages("diagram")
#install.packages("pracma")
library("expm")
library("markovchain")
library("diagram")
library("pracma")

# Matriz de transição
nomes <- c("Ilha 1","Ilha 2","Ilha 3", "Ilha 4")
byrow <- TRUE
M <- matrix(data = c(0.5, 0.3, 0.2, 0.0,
                     0.2, 0.4, 0.3, 0.1,
                     0.1, 0.1, 0.6, 0.2,
                     0.1, 0.2, 0.3, 0.4), byrow = byrow, nrow = 4,
            dimnames = list(nomes, nomes))
M

# Cálculo matricial para o instante t+1:
pt <- rep(1/4, 4)
pt <- matrix(t(pt)%*%M)
pt

# Estados Iniciais
ilha1 <- 1/4
ilha2 <- 1/4
ilha3 <- 1/4
ilha4 <- 1/4
estadosIniciais <- c(ilha1, ilha2, ilha3, ilha4)
estadosIniciais

# Cadeia de Markov
cadeiaMarkov <-new("markovchain", states = nomes, byrow = byrow, transitionMatrix = M, name = "Modelo:")
cadeiaMarkov

defaultMc <- new("markovchain")
defaultMc

mcList <- new("markovchainList", markovchains = list(cadeiaMarkov, defaultMc), name = "Lista da Cadeia de Markov")
mcList

# Produto Matricial (Pt+1)
estadosIniciais * (cadeiaMarkov^1)
estadosIniciais * (cadeiaMarkov^2)
estadosIniciais * (cadeiaMarkov^3)
estadosIniciais * (cadeiaMarkov^4)

n <- 20
for(i in 1:n){
    matriz <- matrix(data = round(c(estadosIniciais* (cadeiaMarkov^i)),3),
                   byrow = byrow, nrow = 1, ncol = length(estadosIniciais))
  print(matriz[1,])
}
