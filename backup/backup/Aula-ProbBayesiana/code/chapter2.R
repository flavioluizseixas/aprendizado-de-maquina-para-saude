
library(bnlearn)
data(marks)
str(marks)
ug = empty.graph(names(marks))
arcs(ug) = matrix(
  c("MECH", "VECT", "MECH", "ALG", "VECT", "MECH",
    "VECT", "ALG", "ALG", "MECH", "ALG",   "VECT",
    "ALG", "ANL", "ALG", "STAT", "ANL",    "ALG",
    "ANL", "STAT", "STAT", "ALG", "STAT",  "ANL"),
  ncol = 2, byrow = TRUE,
  dimnames = list(c(), c("from", "to")))
ug

#-----------------------------------------------------------------------------#

dag = empty.graph(names(marks))
arcs(dag) = matrix(
  c("VECT", "MECH", "ALG", "MECH", "ALG", "VECT",
    "ANL", "ALG", "STAT", "ALG", "STAT", "ANL"),
  ncol = 2, byrow = TRUE,
  dimnames = list(c(), c("from", "to")))
dag
mat = matrix(c(0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
      1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0), nrow = 5,
      dimnames = list(nodes(dag), nodes(dag)))
mat
dag2 = empty.graph(nodes(dag))
amat(dag2) = mat
all.equal(dag, dag2)
dag3 = empty.graph(nodes(dag))
dag3 = set.arc(dag3, "VECT", "MECH")
dag3 = set.arc(dag3, "ALG", "MECH")
dag3 = set.arc(dag3, "ALG", "VECT")
dag3 = set.arc(dag3, "ANL", "ALG")
dag3 = set.arc(dag3, "STAT", "ALG")
dag3 = set.arc(dag3, "STAT", "ANL")
all.equal(dag, dag3)
all.equal(ug, moral(dag))

#-----------------------------------------------------------------------------#

node.ordering(dag)
nbr(dag, "ANL")
mb(dag, "ANL")
"ANL" %in% mb(dag, "ALG")
"ALG" %in% mb(dag, "ANL")

chld = children(dag, "VECT")
par = parents(dag, "VECT")
o.par = sapply(chld, parents, x = dag)
unique(c(chld, par, o.par[o.par != "VECT"]))
mb(dag, "VECT")

#-----------------------------------------------------------------------------#

score(dag, data = marks, type = "loglik-g")
dag.eq = reverse.arc(dag, "STAT", "ANL")
score(dag.eq, data = marks, type = "loglik-g")
vstructs(dag)
vstructs(dag.eq)
vstructs(dag, moral = TRUE)
vstructs(dag.eq, moral = TRUE)
all.equal(cpdag(dag), cpdag(dag.eq))
all.equal(moral(dag), moral(dag.eq))
dag2 = drop.arc(dag, from = "STAT", to = "ANL")
dag3 = drop.arc(dag, from = "ALG", to = "VECT")
vstructs(dag2)
vstructs(dag3)
all.equal(cpdag(dag2), cpdag(dag3))
all.equal(moral(dag2), moral(dag3))
all.equal(moral(dag2), moral(dag))
all.equal(moral(dag3), moral(dag))

#-----------------------------------------------------------------------------#

library(deal)
deal.net = network(marks)
deal.net
m = paste("[MECH][VECT|MECH][ALG|MECH:VECT]",
          "[ANL|ALG][STAT|ALG:ANL]", sep = "")
deal.net = as.network(m, deal.net)
deal.net

library(catnet)
cat.net = cnCatnetFromEdges(names(marks),
            list(MECH = NULL, VECT = "MECH",
                 ALG = c("MECH", "VECT"), ANL = "ALG",
                 STAT = c("ALG", "ANL")))
cat.net

chld = cnEdges(cat.net)$VECT
par = cnParents(cat.net)$VECT
o.par = sapply(chld, function(node) { cnEdges(cat.net)[[node]] })
unique(unlist(c(chld, par, o.par[o.par != "VECT"])))

em = empty.graph(names(marks))
arcs(em) = cnMatEdges(cat.net)
em = model2network(deal::modelstring(deal.net))

#-----------------------------------------------------------------------------#

hl2 = list(arcs = vstructs(dag2, arcs = TRUE), lwd = 4, col = "black")
hl3 = list(arcs = vstructs(dag3, arcs = TRUE), lwd = 4, col = "black")

graphviz.plot(dag2, highlight = hl2, layout = "fdp", main = "dag2")
graphviz.plot(dag3, highlight = hl3, layout = "fdp", main = "dag3")
graphviz.plot(cpdag(dag2), highlight = hl2, layout = "fdp", main = "cpdag(dag2)")
graphviz.plot(cpdag(dag3), highlight = hl3, layout = "fdp", main = "cpdag(dag3)")

#-----------------------------------------------------------------------------#

options(width = 52)
bn.gs = gs(marks)
bn.gs
all.equal(bn.gs, iamb(marks))
all.equal(bn.gs, inter.iamb(marks))
all.equal(bn.gs, iamb(marks, test = "mc-cor"))
library(pcalg)
suff.stat = list(C = cor(marks), n = nrow(marks))
pc.fit = pc(suff.stat, indepTest = gaussCItest, p = ncol(marks), alpha = 0.05)
pc.fit
gs.graph = as.graphAM(bn.gs)
compareGraphs(pc.fit@graph, gs.graph)
bn.hc = hc(marks)
bn.hc
score(bn.gs, data = marks, type = "bic-g")
score(bn.hc, data = marks, type = "bic-g")
net = network(marks)
prior = jointprior(net, N = 5)
net = learn(net, marks, prior)$nw
best = autosearch(net, marks, prior)
mstring = deal::modelstring(best$nw)
mstring
bn.deal = model2network(mstring)
bnlearn::score(bn.deal, marks, type = "bge", iss = 5)
bn.hc = hc(marks)
bnlearn::score(bn.hc, marks, type = "bge", iss = 5)
heuristic = heuristic(best$nw, marks, prior,
              restart = 2, trylist = best$trylist)

#-----------------------------------------------------------------------------#

fitted = bn.fit(bn.gs, data = marks)
fitted$ALG
fitted$ALG = list(coef = c("(Intercept)" = 25, "ANL" = 0.5, "STAT" = 0.25), sd = 6.5)
fitted$ALG

MECH.par = list(coef = c("(Intercept)" = -10, "VECT" = 0.5, "ALG" = 0.6), sd = 13)
VECT.par = list(coef = c("(Intercept)" = 10, "ALG" = 1), sd = 10)
ALG.par = list(coef = c("(Intercept)" = 25, "ANL" = 0.5, "STAT" = 0.25), sd = 6.5)
ANL.par = list(coef = c("(Intercept)" = 25, "STAT" = 0.5), sd = 12)
STAT.par = list(coef = c("(Intercept)" = 43), sd = 17)
dist = list(MECH = MECH.par, VECT = VECT.par,
            ALG = ALG.par, ANL = ANL.par, STAT = STAT.par)
fitted2 = custom.fit(bn.gs, dist = dist)

#-----------------------------------------------------------------------------#

dmarks = discretize(marks, breaks = 2, method = "interval")
bn.dgs = gs(dmarks)
bn.dhc = hc(dmarks)
all.equal(cpdag(bn.dgs), cpdag(bn.dhc))
fitted = bn.fit(bn.dhc, data = dmarks)
fitted$ALG

netlist = cnSearchSA(dmarks)
best = cnFindBIC(netlist, nrow(dmarks))
cnMatEdges(best)

#-----------------------------------------------------------------------------#

latent = factor(c(rep("A", 44), "B", rep("A", 7), rep("B", 36)))
bn.A = hc(marks[latent == "A", ])
bn.B = hc(marks[latent == "B", ])
modelstring(bn.A)
modelstring(bn.B)
bn.LAT = hc(cbind(dmarks, LAT = latent))
bn.LAT

#-----------------------------------------------------------------------------#

library(bnlearn)
sachs = read.table("sachs.data.txt", header = TRUE)
dsachs = discretize(sachs, method = "hartemink", breaks = 3, ibreaks = 60, idisc = "quantile")
boot = boot.strength(data = dsachs, R = 500, algorithm = "hc",
         algorithm.args = list(score = "bde", iss = 10))
boot[(boot$strength > 0.85) & (boot$direction >= 0.5), ]
avg.boot = averaged.network(boot, threshold = 0.85)

nodes = names(dsachs)
start = random.graph(nodes = nodes,
method = "ic-dag", num = 500)
netlist = lapply(start, function(net) {
  hc(dsachs, score = "bde", iss = 10, start = net)
})
rnd = custom.strength(netlist, nodes = nodes)
rnd[(rnd$strength > 0.85) & (rnd$direction >= 0.5), ]
avg.start = averaged.network(rnd, threshold = 0.85)
all.equal(cpdag(avg.boot), cpdag(avg.start))
score(cextend(cpdag(avg.start)), dsachs, type = "bde", iss = 10)

library(catnet)
netlist = vector(500, mode = "list")
ndata = nrow(dsachs)
netlist = lapply(netlist, function(net) {
  boot = dsachs[sample(ndata, replace = TRUE), ]
  nets = cnSearchOrder(boot)
  best = cnFindBIC(nets, ndata)
  cnMatEdges(best)
})
sa = custom.strength(netlist, nodes = nodes)
sa[(sa$strength > 0.85) & (sa$direction >= 0.5), ]
avg.catnet = averaged.network(sa, threshold = 0.85)

all.equal(averaged.network(boot, threshold = 0.50),
averaged.network(boot, threshold = 0.70))
averaged.network(boot)
all.equal(avg.boot, averaged.network(boot))

isachs = read.table("sachs.interventional.txt", header = TRUE, colClasses = "factor")
wh = matrix(c(rep("INT", 11), names(isachs)[1:11]), ncol = 2)
bn.wh = tabu(isachs, whitelist = wh, score = "bde", iss = 10, tabu = 50)
tiers = list("INT", names(isachs)[1:11])
bl = tiers2blacklist(nodes = tiers)
bn.tiers = tabu(isachs, blacklist = bl, score = "bde", iss = 10, tabu = 50)
INT = sapply(1:11, function(x) { which(isachs$INT == x) })
nodes = names(isachs)[1:11]
names(INT) = nodes

start = random.graph(nodes = nodes, method = "melancon", num = 500,
          burn.in = 10ˆ5, every = 100)
netlist = lapply(start, function(net) {
  tabu(isachs[, 1:11], score = "mbde", exp = INT,
  iss = 10, start = net, tabu = 50)
})
arcs = custom.strength(netlist, nodes = nodes)
bn.mbde = averaged.network(arcs, threshold = 0.85)

