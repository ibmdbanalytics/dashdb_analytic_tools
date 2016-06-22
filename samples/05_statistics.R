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
