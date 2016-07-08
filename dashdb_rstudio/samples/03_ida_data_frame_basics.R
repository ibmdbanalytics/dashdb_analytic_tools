library(ibmdbR)

######################################################################
## Set the connection information corresponding to you dashDB instance
## You will find the connection information 
## under Connect -> Connection Information in the dashDB web ui
######################################################################
host.name <- ""
user.name <-""
pwd <- ""
######################################################################

if((nchar(host.name)==0)||(nchar(user.name)==0)||(nchar(pwd)==0))
  stop("Please specify the host.name, user.name and pwd by setting the variables above.")

con <- idaConnect(paste("DASHDB",";Database=BLUDB;Hostname=",host.name,";Port=50000;PROTOCOL=TCPIP;UID=", user.name,";PWD=",pwd,sep=""),"","")
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
