import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy
import math
def addnodes(g,n):
    l=len(g.nodes())
    for i in range(n):
        g.add_node(i+l)


def add_random_edges(g,n):
    nodes=[i for i in g.nodes()]
    c=g.number_of_edges()
    num=g.number_of_nodes()
    while(g.number_of_edges()-c<n):
        if(g.number_of_edges()==num*(num-1)/2):
            print('cant add this many edges')
            break
        n1=random.choice(nodes)
        n2=random.choice(nodes)
        if(n1!=n2 and g.has_edge(n1,n2)==0):
            g.add_edge(n1,n2)
def assign_bmi(g,attr):
    nodes=g.nodes()
    for i in nodes:
        attr[i]={}
        rn=random.randint(15,40)
        attr[i]['label']=rn
        attr[i]['type']='person'
        attr[i]['size']=rn
    return attr

def get_labels(attr):
    d={}
    for i in range(len(attr)):
        d[i]=attr[i]['label']
    return d


def visualize(g,attr):
    nsize=[i['size'] for i in attr.values()]
    nsize=list(numpy.array(nsize)*10)
    lab=get_labels(attr)
    color=get_color(g,attr)
    nx.draw(g,labels=lab,node_size=nsize,node_color=color)
    plt.show()

def add_foci_nodes(g,attr,foci_list):
    l=len(g.nodes())
    for i in range(len(foci_list)):
        g.add_node(i+l)
        attr[i+l]={}
        attr[i+l]['label']=foci_list[i]
        attr[i+l]['type']='foci'
        attr[i+l]['size']=100

def get_foci_nodes(g,attr):
    f=[]
    for i in g.nodes():
        if(attr[i]['type']=='foci'):
            f.append(i)
    return f

def get_person_nodes(g,attr):
    p=[]
    for i in g.nodes():
        if(attr[i]['type']=='person'):
            p.append(i)
    return p

def get_color(g,attr):
    c=[]
    for i in g.nodes():
        if(attr[i]['type']=='foci'):
            c.append('red')
        else:
            c.append('yellow')
    return c

def add_foci_edges(g,attr):
    foci_nodes=get_foci_nodes(g,attr)
    person_nodes=get_person_nodes(g,attr)
    for i in person_nodes:
        r=random.choice(foci_nodes)
        g.add_edge(i,r)

def homophily(g,attr):
    pnodes=get_person_nodes(g,attr)
    for u in pnodes:
        for v in pnodes:
            if u!=v:
                diff=abs(attr[u]['label']-attr[v]['label'])
                p=float(1)/float(diff+1000)
                r=random.uniform(0,1)
                if r<p:
                    g.add_edge(u,v)
def common_neighbours(g,u,v):
    nu=set(g.neighbors(u))
    nv=set(g.neighbors(v))
    return len(nu & nv)

def closure(g,attr):
    array1=[]
    p=0.01 #probability that two nodes become friend due to common foci or friend
    for u in g.nodes():
        for v in g.nodes():
            if u!=v and (attr[u]['type']=='person' or attr[v]['type']=='person') and g.has_edge(u,v)==0:
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

def change_bmi(g,attr):
    fnodes=get_foci_nodes(g,attr)
    for i in fnodes:
        if(attr[i]['label']=='eatout'):
            for nd in g.neighbors(i):
                if attr[nd]['label']!=40:
                    attr[nd]['label']=attr[nd]['label']+1
    for i in fnodes:
        if(attr[i]['label']=='gym'):
            for nd in g.neighbors(i):
                if attr[nd]['label']!=15:
                    attr[nd]['label']=attr[nd]['label']-1

g=nx.Graph()
attr={}
addnodes(g,100)
assign_bmi(g,attr)
add_foci_nodes(g,attr,['yoga class','karate club','gym','movie club','eatout'])
add_foci_edges(g,attr)
visualize(g,attr)
for i in range(10):
    homophily(g,attr)
    closure(g,attr)
    change_bmi(g,attr)
    visualize(g,attr)