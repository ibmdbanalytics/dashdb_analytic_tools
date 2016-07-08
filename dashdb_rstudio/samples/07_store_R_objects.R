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

# Create a pointer to the private R object storage table of the current user.
myPrivateObjects <- ida.list(type='private')

# Use the pointer created in the previous example to store a series of numbers in an object with 
# the name 'series100' in the private R object storage table of the current user.
myPrivateObjects['series100'] <- 1:100

# Retrieve the object with the name 'series100' from the 
# private R object storage table of the current user.
x <- myPrivateObjects['series100']

# Print object
x

# List all objects in the private R object storage table of the current user.
names(myPrivateObjects)

# Return the number of objects in the private R object storage table of the current user.
length(myPrivateObjects)

# Delete the object with name 'series100' from the 
# private R object storage table of the current user.
myPrivateObjects['series100'] <- NULL

# Return the number of objects in the private R object storage table of the current user.
length(myPrivateObjects)

# Create a pointer to the public R object storage table of the current user.
# Note: This is only supported on systems configured to allow object sharing
# See the documentation of ida.list for more details
#myPublicObjects <- ida.list(type="public")

#Close the connection
idaClose(con)