######################################################################
## Set the connection information corresponding to you dashDB instance
## You will find the connection informatation 
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

#Run select queries
colName <- "SepalLength"
df <- idaQuery('SELECT "',colName, '" FROM IRIS')
print(df)
numRows <- idaScalarQuery("SELECT COUNT(*) FROM IRIS")
print(numRows)

#For bigger tables, this approach is not feasible and it is better to use
#In-Database methods, see simple_pushdown.R

#Close the connection
idaClose(con)
