# Create a pointer to the private R object storage table of the current user.
myPrivateObjects <- ida.list(type='private')

# Use the pointer created in the previous example to store a series of numbers in an object with 
# the name 'series100' in the private R object storage table of the current user.
myPrivateObjects['series100'] <- 1:100

# Retrieve the object with the name 'series100' from the 
# private R object storage table of the current user.
x <- myPrivateObjects['series100']


# Delete the object with name 'series100' from the 
# private R object storage table of the current user.

myPrivateObjects['series100'] <- NULL

# List all objects in the private R object storage table of the current user.
names(myPrivateObjects)

# Return the number of objects in the private R object storage table of the current user.
length(myPrivateObjects)

# Create a pointer to the public R object storage table of the current user.
# Note: This is only supported on systems configured to allow object sharing
# See the documentation of ida.list for more details
#myPublicObjects <- ida.list(type="public")

#Close the connection
idaClose(con)

