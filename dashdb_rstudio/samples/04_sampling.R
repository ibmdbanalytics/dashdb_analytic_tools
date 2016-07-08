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

#Take a random sample without replacement of size 10
df <- idaSample(idf,10)
print(df)

#Take a stratified sample 
df <- idaSample(idf,10,'Species')
print(df)

#Close the connection
idaClose(con)
