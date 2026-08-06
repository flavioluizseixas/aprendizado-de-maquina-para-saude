library(bnlearn)
library(gRain)

dag = read.bif('cancer.bif', debug = FALSE)
graphviz.chart(dag)

dag.junction = compile(as.grain(dag))
querygrain(dag.junction, nodes = c("Cancer"))
gin.find <- setFinding(dag.junction, nodes = c("Pollution", "Xray"), states = c("high", "positive"))
querygrain(gin.find, nodes = c("Cancer"))
