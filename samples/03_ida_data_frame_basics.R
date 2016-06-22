library(ibmdbR)

con <- idaConnect('BLUDB','','')
idaInit(con)

#Upload the table if it does not exist yet
if(!idaExistTable("IRIS"))
  as.ida.data.frame(iris,"IRIS")

#Create an ida.data.frame pointer to table IRIS
idf <- ida.data.frame("IRIS")

#Several functions can be applied to the ida.data.frame and are 
#pushed-down for execution in SQL (see also statistics-pushdown.R)
#Try for instance the following
dim(idf)
names(idf)
head(idf)

#You can select rows and/or columns from an ida.data.frame using an R like syntax
idf2 <- idf[idf$SepalLength>6,c("Species","SepalWidth")]

dim(idf2)
head(idf2)

#You can also construct new columns on an ida.data.frame
idf$X <- idf$SepalLength + idf$SepalWidth

head(idf)
     
#Many other functions are available for ida.data.frame, such as statistics, sampling
#or analytics algorithms, e.g. k-means

#Close the connection
idaClose(con)
