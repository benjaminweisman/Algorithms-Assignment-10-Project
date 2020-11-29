import pandas as pd
import networkx as nx
import matplotlib.pyplot as mp
from datetime import datetime
import numpy as np
from array import array
from scipy.stats.mstats import gmean


df = pd.read_csv ('Code Cap.csv')

print(df)

G=nx.from_pandas_edgelist(df, source='SOURCE', target='TARGET', edge_attr='CAPACITY', create_using=nx.DiGraph())


nx.draw_networkx(G)
mp.show()
