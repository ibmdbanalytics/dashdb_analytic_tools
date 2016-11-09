library(SparkR, lib.loc = c(file.path(Sys.getenv("SPARK_HOME"), "R", "lib")))

cf = list(
     spark.master="spark://<host>:25000",
     spark.authenticate="true",
     spark.authenticate.secret="<secret>",
     spark.driver.memory="1g",spark.executor.memory="533m",
     spark.executor.cores="16",spark.cores.max="16",
     spark.ui.port="25052",spark.fileserver.port="25053",spark.broadcast.port="25054",spark.replClassServer.port="25055",spark.executor.port="25058",
     spark.port.maxRetries="1"
     )
sparkR.session(sparkConfig = cf)


df <- as.DataFrame(faithful)
head(summarize(groupBy(df, df$waiting), count = n(df$waiting)))
