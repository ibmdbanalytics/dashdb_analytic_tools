##############################################
#   IN-DATABASE LINEAR REGRESSION FUNCTION   #
##############################################

# This sample evaluates a large amount of data that relates the number of users of a system to the
# amount of memory used and creates a plot of the line that best fits these data points. Such a
# plot can be used to predict memory usage when the number of users is known. The relatively low
# standard-error value returned by the linear regression function indicates that the relationship
# between memory usage and number of users is indeed strongly linear.  

# Before processing data, most native R functions require that the data first be extracted from a
# database to working memory. Such a function is called an in-application function. A different type
# of function, called an in-database function, operates directly on data in a database, without the
# data first having to be extracted. Consequently, you can use an in-database function to analyze
# large amounts of data that would be impractical or impossible to extract. 

# An in-database function can exploit performance-enhancing features of the underlying database
# management system, such as BLU columnar technology. It also avoids security issues associated with
# extracting data, and ensures that the data being analyzed is as current as possible.

# This sample employs the in-database linear regression function (idaLm), which performs better than
# the corresponding in-application function (lm) for large data sets. To explore the differences
# between in-database and in-application functions, run both this sample and the sample that uses
# the corresponding in-application function, and compare the elapsed times.

# Subsequent comments in this sample script describe the steps carried out by its R statements.

# Load the required packages.
library(ggplot2)
library(scales)
library(ibmdbR)

######################################################################
## Set the connection information corresponding to you dashDB instance
## You will find the connection informatation 
## under Connect -> Connection Information in the dashDB web ui
######################################################################
host.name <- ""
#host.name <- "awh-yp-small02.services.dal.bluemix.net"

user.name <-"dash104803"
pwd <- "IV4mZs1r9Vg5"
######################################################################

if((nchar(host.name)==0)||(nchar(user.name)==0)||(nchar(pwd)==0))
  stop("Please specify the host.name, user.name and pwd by setting the variables above.")

con <- idaConnect(paste("DASHDB",";Database=BLUDB;Hostname=",host.name,";Port=50000;PROTOCOL=TCPIP;UID=", user.name,";PWD=",pwd,sep=""),"","")
idaInit(con)

# A IDA data frame is similar to a regular R data frame, but instead of holding data directly it 
# instead holds a reference to a table or view in the database, or to a selection of rows and 
# columns within a particular table or view.

# Create a IDA data frame that refers to the table SHOWCASE_SYSUSAGE, which contains resource 
# measurements from different systems:
#   SID      System ID 
#   DATE     Measurement timestamp 
#   USERS    Number of active users on the system 
#   MEMUSED  Memory usage 
#   ALERT    Whether an alert was triggered 
sysusage<-ida.data.frame('SAMPLES.SHOWCASE_SYSUSAGE')

# Create a ida data frame that refers to the table SHOWCASE_SYSTEMS, which contains additional 
# information about the systems.
systems<-ida.data.frame('SAMPLES.SHOWCASE_SYSTEMS')

# Create a ida data frame that refers to the table SHOWCASE_SYSTYPES, which contains information 
# about the system types.
systypes<-ida.data.frame('SAMPLES.SHOWCASE_SYSTYPES')

# Display the first few rows of each of these tables.
writeLines("Excerpt from SHOWCASE_SYSUSAGE:")
head(sysusage)
writeLines("")
writeLines("Excerpt from SHOWCASE_SYSTEMS:")
head(systems)
writeLines("")
writeLines("Excerpt from SHOWCASE_SYSTYPES:")
head(systypes)
writeLines("")

# Projection and selections are possible on a ida data frame.
# Select the variables USERS and MEMUSED for all rows for which
# memory usage is larger than 50000 MB.
sysusage2 <- sysusage[sysusage$MEMUSED>50000,c("MEMUSED","USERS")]
writeLines("Number of seconds during which memory usage exceeded 50000 MB:")
dim(sysusage2)
writeLines("")

# The idaMerge function is similar to the merge function, but is used to join ida data frames 
# rather than data frames.
# Join the three tables on their TYPEID and SID columns.
mergedSys<-idaMerge(systems, systypes, by='TYPEID')
mergedUsage<-idaMerge(sysusage, mergedSys, by='SID')


# Alternatively, this could be written this in one line, like this:
#mergedUsage<-idaMerge(sysusage, idaMerge(systems, systypes, by='TYPEID'), by='SID')

writeLines("Dimensions of merged table mergedSys:")
dim(mergedSys)
writeLines("")
writeLines("Dimensions of merged table mergedUsage:")
dim(mergedUsage)
writeLines("")

# Build a linear prediction model that correlates memory usage with the number of active users.
lm1 <- idaLm(MEMUSED~USERS, mergedUsage)

# The output of the idaLm function is formatted differently from that of the lm function.
writeLines("Information about the linear prediction model:")
lm1
writeLines("")

# Calculate the maximum number of users.
maxUsers <- max(mergedUsage[,'USERS'])[1,1];
writeLines("Maximum number of users:")
maxUsers
writeLines("")

# Obtain a random sample of 1000 data points for visualization
dfSample <- idaSample(mergedUsage[,c("MEMUSED", "USERS")], 1000)

# Plot a histogram that shows relative frequency of various amounts of memory used.
ggplot(dfSample) + geom_histogram(aes(x=MEMUSED, y=..count../sum(..count..)), binwidth=1000, colour="black", fill="white") + scale_y_continuous(labels=percent_format()) + labs(title="Memory Used") + labs(x="Memory Used",y="Frequency")

# Plot a histogram that shows relative frequency of various numbers of users.
ggplot(dfSample) + geom_histogram(aes(x=USERS, y=..count../sum(..count..)), binwidth=7, colour="black", fill="white") + scale_y_continuous(labels=percent_format()) + labs(title="Active Users") + labs(x="Number of Users",y="Frequency")

# Create a scatter plot of number of users vs. memory usage, and overlay that plot with the line that
# represents the calculated linear relationship. In a model generated by the idaLm function, the first
# coefficient is the slope of the line in MB/user and the second coefficient is the Y intercept.
ggplot(dfSample, aes(x=USERS, y=MEMUSED)) + geom_point(shape=1) + labs(title="Memory used") + labs(x="Number of Users",y="Memory Used (MB)") + stat_function(fun=function(x){x*lm1$coefficients[1]+lm1$coefficients[2]}, aes(colour="blue")) + scale_colour_manual("Legend", values=c("blue"), labels=c("idaLM"))

#Clean up
idaDropView(mergedSys@table)
idaDropView(mergedUsage@table)

idaClose(con)

