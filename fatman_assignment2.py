import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy
import math


def create_graph():
    g=nx.Graph()
    g.add_nodes_from(range(0,100))
    assign_bmi(g)
    add_foci_nodes(g,['yoga class','karate club','gym','movie club','eat_out'])
    add_foci_edges(g)
    return g


def visualize(g):
    nsize=[i['size'] for i in g._node.values()]
    nsize=list(numpy.array(nsize)*10)
    lab=get_labels(g)
    color=get_color(g)
    nx.draw(g,labels=lab,node_size=nsize,node_color=color)
    plt.show()

def get_color(g):
    c=[]
    for i in g.nodes():
        if g._node[i]['type']=='foci':
            c.append('red')
        else:
            if g._node[i]['label']==40:
                c.append('black')
            elif g._node[i]['label']==15:
                c.append('white')
            else:
                c.append('yellow')
    return c

def get_labels(g):
    d={}
    for i  in g.nodes():
        d[i]=g._node[i]['label']
    return d

def assign_bmi(g):
    for i in g.nodes():
        r=random.randint(15,40)
        g._node[i]['label']=r
        g._node[i]['type']='person'
        g._node[i]['size']=r

def get_foci_nodes(g):
    f=[]
    for i in g.nodes():
        if(g._node[i]['type']=='foci'):
            f.append(i)
    return f

def get_person_nodes(g):
    p=[]
    for i in g.nodes():
        if(g._node[i]['type']=='person'):
            p.append(i)
    return p

def add_foci_nodes(g,foci_list):
    l=len(g.nodes())
    for i in range(len(foci_list)):
        g.add_node(i+l)
        g._node[i+l]['label']=foci_list[i]
        g._node[i+l]['type']='foci'
        g._node[i+l]['size']=100



def add_foci_edges(g):
    foci_nodes=get_foci_nodes(g)
    person_nodes=get_person_nodes(g)
    for i in person_nodes:
        r=random.choice(foci_nodes)
        g.add_edge(i,r)

def homophily(g):
    initial=len(g.edges())
    pnodes=get_person_nodes(g)
    for u in pnodes:
        for v in pnodes:
            if u!=v:
                diff=abs(g._node[u]['label']-g._node[v]['label'])
                p=float(1)/float(diff+1000)
                r=random.uniform(0,1)
                if r<p:
                    g.add_edge(u,v)
    final=len(g.edges())
    return initial,final

def common_neighbours(g,u,v):
    nu=set(g.neighbors(u))
    nv=set(g.neighbors(v))
    return len(nu & nv)

def closure(g):
    initial=len(g.edges())
    array1=[]
    p=0.01 #probability that two nodes become friend due to common foci or friend
    for u in g.nodes():
        for v in g.nodes():
            if u!=v and (g._node[u]['type']=='person' or g._node[v]['type']=='person') and g.has_edge(u,v)==0:
                k=common_neighbours(g,u,v)
                prob=float(1)-math.pow(1-p,k)
                temp=[]
                temp.append(u)
                temp.append(v)
                temp.append(prob)
                array1.append(temp)
    for i in array1:
        u=i[0]
        v=i[1]
        p=i[2]
        r=random.uniform(0,1)
        if r<p:
            g.add_edge(u,v)
    final=len(g.edges())
    return initial,final
def Number_of_bmi40_nodes(g):
    final=0
    for  i in g.nodes():
        if g._node[i]['label']==40:
            final=final+1
    return final

def change_bmi(g):
    initial=Number_of_bmi40_nodes(g)
    fnodes=get_foci_nodes(g)
    for i in fnodes:
        if g._node[i]['label']=='eat_out':
            for nd in g.neighbors(i):
                if g._node[nd]['label']!=40:
                    g._node[nd]['label']=int(g._node[nd]['label'])+1
    final=Number_of_bmi40_nodes(g)
    return initial,final


g=create_graph()
# visualize(g)
print('number of Edges before homophily :',homophily(g)[0])
print('number of Edges after homophily :',homophily(g)[1])
print('number of Edges before implementing closure :',closure(g)[0])
print('number of Edges after implementing closure :',closure(g)[1])
print('number of nodes with BMI 40 before :',change_bmi(g)[0])
print('number of nodes with BMI 40 after :',change_bmi(g)[1])
# visualize(g)
