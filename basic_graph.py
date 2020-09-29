
import networkx as nx
import numpy
import matplotlib.pyplot as plt
import random

def createnetwork(cities,costs,no_of_edges):
    g=nx.Graph()
    for i in cities:
        g.add_node(i)
    nodes=[i for i in g.nodes()]   
    while(g.number_of_edges()<=no_of_edges):
        n1=random.choice(nodes)
        n2=random.choice(nodes)
        if n1!=n2 and g.has_edge(n1,n2)==0:
            w=random.choice(costs)
            g.add_edge(n1,n2,weight=w)
    return g

def shortest_paths(g):
    for i in g.nodes():
        for j in g.nodes():
            try:
                print(i,j,'--',nx.dijkstra_path_length(g,i,j))
            except:
                print(i,j,'--','unreachable')
            

cities=[i[:-1] for i in open('cities.txt','r').readlines()]
costs=[i for i in range(100,2001,100)]
g=createnetwork(cities,costs,25)
shortest_paths(g)
# pos=nx.circular_layout(g)    
# nx.draw(g,pos,with_labels=1 )
# plt.show()