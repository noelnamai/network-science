setwd(".")
library("networkD3")

nodes = read.csv("Rnodes.csv")
links = read.csv("Rlinks.csv"); head(links, 10)

network = forceNetwork(Links=links, Nodes=nodes, Nodesize="degree", 
                       Source="source", Target="target", Value="value", 
                       NodeID="name", Group="industry", opacity=10, fontSize=10, 
                       fontFamily="serif", charge=-500, zoom=TRUE, 
                       radiusCalculation=JS("Math.sqrt(d.nodesize)*2.5")); network

saveNetwork(network, file="network.html", selfcontained=TRUE)



df = read.csv("http://www.barabasilab.com/pubs/CCNR-ALB_Publications/200705-14_PNAS-HumanDisease/Suppl/supplementary_tableS1.txt", sep="\t", skip=1, names=FALSE)
names(df) = tolower(names(df))
head(df)
