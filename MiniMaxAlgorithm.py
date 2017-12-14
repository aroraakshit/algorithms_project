
# coding: utf-8

# In[10]:

#import packages
import networkx as nx
import random as rnd
from MinMaxClass import MinMaxNode, MinMaxTree
import math


# In[2]:

def makeTree(G,H,turn,node):
    if turn==0: #player: attacker
        infectedList=[]
        nodeAttribute=nx.get_node_attributes(G,"infected") #a dictionary of node attributes returned: {1:0, 2:0, 3:0, 4:0, 5:0}
        for e in nodeAttribute.keys():
            if nodeAttribute[e]==-1:
                infectedList.append(e)
        for i in infectedList:
            for e in nx.all_neighbors(G,i):
                if nodeAttribute[e]==0:
                    K=G.copy()
                    nx.set_node_attributes(K,{e:{"infected":-1}})
                    x=node.addChild(e)
                    makeTree(K,H,1,x)
    elif turn==1: #player: defender
        possibleList=[]
        nodeAttribute=nx.get_node_attributes(G,"infected")
        for e in nodeAttribute.keys():
            if nodeAttribute[e]==0:
                possibleList.append(e)
        for i in possibleList:
            K=G.copy()
            nx.set_node_attributes(K,{i:{"infected":1}})
            x=node.addChild(i)
            makeTree(K,H,0,x)


# In[3]:

#applying minimax algorithm (attacker is maximizing, defendor is minimizing)
def minimax(node,turn,depth):
    global temp
    temp=temp+1
    #when leaf node is reached, return the rank of the node
    if node.isLeaf() == True:
        node.set_rank(depth)
        return depth
    
    if turn==0:
        #attacker's turn
        max_rank = 0
        for c in node.get_children():
            label1 = c.get_label()
            tempA = minimax(c,1,depth+1)
            if(tempA > max_rank):
                max_node = c
                max_label = label1
                max_rank = tempA
        node.set_rank(max_rank)
        return (max_rank)
    elif turn==1:
        min_rank = 1000000000000
        for c in node.get_children():
            label1 = c.get_label()
            tempD = minimax(c,0,depth+1)
            if(tempD < min_rank):
                max_node = c
                max_label = label1
                min_rank = tempD
            node.set_rank(min_rank)
        return (min_rank)


# In[4]:

#applying minimax algorithm (attacker is maximizing, defendor is minimizing)
def minimaxwithab(node,turn,depth,alpha,beta):
    #when leaf node is reached, return the rank of the node
    global temp1
    temp1=temp1+1
    if node.isLeaf() == True:
        node.set_rank(depth)
        return depth
    
    if turn==0:
        #attacker's turn
        max_rank = 0
        for c in node.get_children():
            label1 = c.get_label()
            tempA = minimaxwithab(c,1,depth+1,alpha, beta)
            if(tempA > max_rank):
                max_node = c
                max_label = label1
                max_rank = tempA
            if(max_rank > alpha):
                alpha = max_rank
            if(beta <= alpha):
                break
        node.set_rank(max_rank)
        return (max_rank)
    elif turn==1:
        #defender's turn
        min_rank = 100000
        for c in node.get_children():
            label1 = c.get_label()
            tempD = minimaxwithab(c,0,depth+1, alpha, beta)
            if(tempD < min_rank):
                max_node = c
                max_label = label1
                min_rank = tempD
            if(min_rank < beta):
                beta = min_rank
            if(beta <= alpha):
                break
        node.set_rank(min_rank)
        return (min_rank)
    


# In[5]:

def getPrunedGraph(G,i):
    K=nx.Graph()
    queue=[i]
    K.add_node(i, depth=0)
    nx.set_node_attributes(K,{i:{"visited":1, "infected":-1}})
    curr_count=0
    curr_depth=0
    for i in queue:
        if nx.get_node_attributes(K,"depth")[i]>curr_depth:
            if curr_count<=nx.get_node_attributes(K,"depth")[i]:
                break
            else:
                curr_count=0
                curr_depth=nx.get_node_attributes(K,"depth")[i]
        child=nx.all_neighbors(G,i)
        for c in child:
            if not K.has_node(c):
                K.add_node(c,depth=nx.get_node_attributes(K,"depth")[i]+1,infected=nx.get_node_attributes(G,"infected")[c])
                queue.append(c)
                curr_count=curr_count+1
            K.add_edge(i,c)
    return K


# In[15]:

#make root of minimax
for ratio in range(200,400,1):
    ratio=ratio/200
    for num in range(10,500):
        
        graph_properties=[num,math.floor(num*ratio)]
        result=graph_properties
        for i in range(0,100):
            G=nx.gnm_random_graph(graph_properties[0],graph_properties[1], directed=True)
            for n in G.nodes():
                G.node[n]['infected']=0

            i=rnd.randint(0,len(G.nodes())-1)
            G.node[i]['infected'] = -1
            G1=getPrunedGraph(G,i)
            k=nx.get_node_attributes(G,"infected")
            k1=nx.get_node_attributes(G1,"infected")
            for i in k.keys():
                if k[i]==-1:
                    label=i
                    break
            temp=0
            temp1=0
            H = MinMaxTree(label)
            K= MinMaxTree(label)
            makeTree(G,H,1,H.root)
            makeTree(G,K,1,K.root)
            unpruned_minimax=minimax(H.root,1,1)
            unpruned_minimax_explored=temp
            unpruned_minimaxwithab=minimaxwithab(K.root,1,1,-1000000000,1000000)
            unpruned_minimaxwithab_explored=temp1
            temp=0
            temp1=0
            H1 = MinMaxTree(label)
            K1 =  MinMaxTree(label)
            makeTree(G1,H1,1,H1.root)
            makeTree(G1,K1,1,K1.root)
            pruned_minimax=minimax(H1.root,1,1)
            pruned_minimax_explored=temp
            pruned_minimaxwithab=minimaxwithab(K1.root,1,1,-1000000000,1000000)
            pruned_minimaxwithab_explored=temp1
            
            result.append(unpruned_minimax)
            result.append(unpruned_minimax_explored)
            result.append(unpruned_minimaxwithab)
            result.append(unpruned_minimaxwithab_explored)
            result.append(pruned_minimax)
            result.append(pruned_minimax_explored)
            result.append(pruned_minimaxwithab)
            result.append(pruned_minimaxwithab_explored)
            with open("result.csv","a") as r:
                r.write(str(result))
                r.write("\n")
            break
        break
    break
                
                


# In[ ]:



