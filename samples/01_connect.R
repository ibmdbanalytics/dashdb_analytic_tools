library(ibmdbR)

con <- idaConnect('BLUDB','','')
idaInit(con)

#Show tables and views in the user schema
idaShowTables()

#Close the connection
idaClose(con)
