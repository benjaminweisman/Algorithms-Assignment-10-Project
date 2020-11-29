import pandas as pd
import networkx as nx
import matplotlib.pyplot as mp
from datetime import datetime
import numpy as np
from array import array
from scipy.stats.mstats import gmean


df = pd.read_csv ('Code Cap.csv')

print(df)

G=nx.from_pandas_edgelist(df, source='SOURCE', target='TARGET', edge_attr='CAPACITY', create_using=nx.MultiDiGraph())


nx.draw_networkx(G)
mp.show()
nx.edges(G)
len(list(nx.edges(G)))


for u in G:
    for v in G:
        if nx.has_path(G,u,v):
            print(G.get_edge_data(u,v))
            
            
G.get_edge_data('EWR', 'SFO')




# M=nx.DiGraph()
# M.add_edge(1,2,weight=2)
# nx.edges(M)
# # nx.floyd_warshall(G,1,2)
# M.get_edge_data(1,2)


