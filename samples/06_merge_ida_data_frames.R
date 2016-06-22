#Upload the table if it does not exist yet
if(!idaExistTable("IRIS"))
  as.ida.data.frame(iris,"IRIS")

#Create an ida.data.frame pointer to table IRIS
idf <- ida.data.frame("IRIS")

#Try for instance a self-join 
idfMerge <- idaMerge(idf[idf$Species=='setosa',c("Species","SepalLength")], idf[idf$Species=='versicolor',c("Species","SepalLength")],by="SepalLength")
head(idfMerge)

#Close the connection
idaClose(con)
