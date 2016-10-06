setwd(".")
library("networkD3")

nodes = read.csv("Rnodes.csv")
links = read.csv("Rlinks.csv"); head(links, 10)

nodes$group = sample(c(1,2,3), nrow(nodes), replace=TRUE)

network = forceNetwork(Links=links, Nodes=nodes, Source="source", Target="target", Value="value", NodeID="name", Group="group", opacity=10, fontSize=10, fontFamily="serif"); network

source = c(2,2,2,2,2,5,6,7,7,7,7,8,8,9,9,10,12,13,14,14,16,17,19,19,19,21,21,24)
target = c(24,25,19,21,7,20,9,24,25,19,21,25,12,16,26,21,25,22,27,15,26,22,24,25,21,24,25,25)

nodes = data.frame(name=c(0:27))
links = data.frame(source, target)

network = forceNetwork(Links=links, Nodes=nodes, Source="source", Target="target", Value="value", NodeID="name", Group="group", opacity=10, fontSize=10, fontFamily="serif"); network
