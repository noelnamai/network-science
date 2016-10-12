setwd(".")
library("networkD3")

nodes = read.csv("Rnodes.csv")
links = read.csv("Rlinks.csv"); head(links, 10)

nodes$group = sample(c(1,2,3), nrow(nodes), replace=TRUE)

network = forceNetwork(Links=links, Nodes=nodes, Source="source", Target="target", Value="value", NodeID="name", Group="group", opacity=10, fontSize=10, fontFamily="serif"); network

