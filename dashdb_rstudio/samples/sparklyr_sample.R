library(sparklyr)

cf <- spark_config()
cf$spark.master <- "spark://<host>:25000"
cf$spark.authenticate <-"true"
cf$spark.authenticate.secret <-"<secret>"
cf$spark.driver.memory="1g"
cf$spark.executor.memory="533m"
cf$spark.executor.cores=16
cf$spark.cores.max=16
cf$spark.ui.port=25052
cf$spark.fileserver.port=25053
cf$spark.broadcast.port=25054
cf$spark.replClassServer.port=25055
cf$spark.executor.port=25058
cf$spark.port.maxRetries=1
sc <- spark_connect(config = cf)

library(dplyr)
mtcars_tbl <- copy_to(sc, mtcars)

fit <- mtcars_tbl %>%
    ml_linear_regression(response = "mpg", features = c("wt", "cyl"))
summary(fit)
