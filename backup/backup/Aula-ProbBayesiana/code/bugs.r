sink("ru486_mcmc.bugs")
cat("model {
    teta ~ dunif(0,1)
    x ~ dbin(teta,n)
    }")
sink()
