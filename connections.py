"""Synapses matrices

This script contains the functions to generate the connectivity matrix
"""

import numpy as np



class Synaptic_Matrix:
    """
    Dense connection matrix class for I-E, E-I and E-U synapses.

    This class contains every synaptic plasticity related methods.
    """

    def __init__(self, par):
        """
        Creates a randomly initialized fully connected matrix

        Arguments:
        par -- Simulation parameters 
        
        """
        self.W = np.zeros((par.N_e,par.N_e))


    def Normalize(self, par,conn_str):
        # normalize matrix post_synaptic strengths 
        if self.W.size > 0:
            z = abs(self.W).sum(1)
            z[z==0]=1
            self.W /= z[:,None]
            self.W *= par.Conn_norm*conn_str 

    def Add_Spatial_Connections(self, par, MU, conn_str):
        # add spatially dependent connections
        for mm in range(MU.shape[0]):
            for ii in range(MU.shape[1]):
                C1=MU[mm,ii]
                for jj in range(ii):
                    C2=MU[mm,jj]

                    tor_dist=min(abs(ii-jj),par.N_m-abs(ii-jj))

                    self.W[C1,C2] += conn_str*np.exp(-tor_dist**2/(2*par.Conn_spread**2))
                    self.W[C2,C1] = self.W[C1,C2]



        self.W += np.random.random(self.W.shape)*par.Conn_sigma            
        np.fill_diagonal(self.W, 0)
        self.Normalize(par,conn_str)            

    def Compute_Wake_Similarity(self, par, MU):
        # Compute cell firing similarity based on their place field distances
        self.C=np.zeros((par.N_e,par.N_e,MU.shape[0]))
        for mm in range(MU.shape[0]):
            for ii in range(MU.shape[1]):
                C1=MU[mm,ii]
                for jj in range(ii):
                    C2=MU[mm,jj]

                    tor_dist=min(abs(ii-jj),par.N_m-abs(ii-jj))
                    
                    self.C[C1,C2,mm] = np.exp(-tor_dist**2/(2*par.Conn_spread**2))
                    self.C[C2,C1,mm] = self.C[C1,C2,mm]    

    def Add_Baseline_Connections(self, par, conn_str_bet, conn_str_wit):
        self.W += np.ones(self.W.shape)*conn_str_bet
        np.fill_diagonal(self.W, 0)

        for mm in range(MU.shape[0]):
            for ii in range(MU.shape[1]):
                C1=MU[mm,ii]
                for jj in range(ii-1):
                    C2=MU[mm,ii]
                    self.W[C1,C2] += conn_str_wit
                    self.W[C2,C1] = self.W[C1,C2]
            
        self.Normalize(par)   


    def __mul__(self, x):
        """
        Replace matrix-array multiplication for dot product, in order to make
        the code a big shorter and more readable.
        """

        return self.W.dot(x)



