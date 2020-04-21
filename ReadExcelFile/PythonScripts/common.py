"""
Common functions and a colormap for the line charts (see 'chart.py').
"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from sqlalchemy import create_engine
import pandas as pd

import numpy as np
import scipy
from scipy import stats
from scipy.stats import mstats

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import io, sys, base64
import matplotlib.pyplot as plt

def print_figure(fig):
	"""
	Converts a figure (as created e.g. with matplotlib or seaborn) to a png image and this 
	png subsequently to a base64-string, then prints the resulting string to the console.
	"""
	
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	print(base64.b64encode(buf.getbuffer()))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Custom colormap that is used with line charts
COLOR_MAP = [
	'blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan',
	'darkblue', 'darkorange', 'darkgreen', 'darkred', 'rebeccapurple', 'darkslategray', 
	'mediumvioletred', 'dimgray', 'seagreen', 'darkcyan', 'deepskyblue', 'yellow', 
	'lightgreen', 'lightcoral', 'plum', 'lightslategrey', 'lightpink', 'lightgray', 
	'lime', 'cadetblue'
	]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Creating Random Walks

def create_random_walks(rho_market,rho_cluster,K,N,T):
    random_walks = np.zeros((N,T+1))
    
    market_factor = np.random.normal(0,1,T)
    
    cluster_factors = np.zeros((K,T))
    for k in range(0,K):
        cluster_factors[k,] = np.random.normal(0,1,T)
    
    idiosync_factors = np.zeros((N,T))
    for n in range(0,N):
        if n%2:
            idiosync_factors[n,] = np.random.normal(0,1,T)
        else:
            idiosync_factors[n,] = np.random.laplace(0,1/np.sqrt(2),T)
    
    increments = np.zeros((N,T))
    cluster_class = 0
    size_class = np.floor(N/K)
    
    for n in range(0,N):
        
        market_compo = np.sqrt(rho_market)*market_factor
        indus_compo = np.sqrt(rho_cluster)*cluster_factors[cluster_class,]
        idiosync_compo = np.sqrt(1-rho_market-rho_cluster)*idiosync_factors[n,]
        increments[n,] = market_compo + indus_compo + idiosync_compo
        
        if n%2:
            random_walks[n,T] = 2*cluster_class
        else:
            random_walks[n,T] = 2*cluster_class+1
            
        if(((n+1)%size_class == 0) and (cluster_class < K-1)):
            cluster_class += 1
            
    for n in range(0,N):
        random_walks[n,0] = 100
        for t in range(1,T):
            random_walks[n,t] = random_walks[n,t-1] + increments[n,t]
    
    return random_walks

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
