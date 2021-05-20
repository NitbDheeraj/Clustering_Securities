# -*- coding: utf-8 -*-
"""
Created on Thu May 20 18:41:23 2021

@author: dheer
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture
from astroML.plotting.tools import draw_ellipse

class Plot():
    
    def PlotKmeans(encoded_values,y_kmeans, n ):
        plt.figure()
        plt.scatter(encoded_values[:, 0], encoded_values[:, 1], c=y_kmeans, s=5, cmap='Dark2')
        #plt.text(encoded_values[:, 0], encoded_values[:, 1], labels, fontsize=8)
        plt.xlabel(r'$x$', fontsize=16)
        plt.ylabel(r'$y$', fontsize=16)
        plt.title(r'$k$-means, $N_{clusters} = %i$'%n, fontsize=16)
        plt.show()
        
    def plot_gmm(firstvar, secondvar, labels, name):
        X = np.vstack([firstvar, secondvar]).T # GaussianMixture requires a 2D array as input
        
        K = np.arange(1, 6)
        models = [None for i in K]
        
        models = [GaussianMixture(K[i], random_state=1, covariance_type='full', \
                  n_init=10).fit(X) for i in range(len(K))]
        
        AIC = [m.aic(X) for m in models]
        BIC = [m.bic(X) for m in models]
        logL = [m.score(X) for m in models]
        for i in range(len(K)):
            print('K = %d  AIC = %.1f  BIC = %.1f  logL = %.3f'%(K[i], AIC[i], BIC[i], logL[i]))
        
        gmm_best = models[np.argmin(AIC)] # choose the best model with smallest AIC
        
        print('mu =', gmm_best.means_.flatten())
        print('sig =', np.sqrt(gmm_best.covariances_.flatten()))
        print('pk =', gmm_best.weights_.flatten())
        
        plt.figure()
        
        plt.scatter(firstvar, secondvar, s=2)
        plt.xlabel(r'$x$', fontsize=20)
        plt.ylabel(r'$y$', fontsize=20)
        plt.title('Gaussian Mixture Model, %s'%(name), fontsize=14)
        plt.tight_layout()
        
        for mu, C, w in zip(gmm_best.means_, gmm_best.covariances_, gmm_best.weights_):
            draw_ellipse(mu, C, scales=[2], fc='none', ec='k')
            
        if name == 'bigtech':
            for i in range(len(firstvar)):
                plt.text(firstvar[i], secondvar[i], labels[i], color="red", fontsize=4)
    
        plt.show()