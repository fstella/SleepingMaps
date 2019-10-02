"""Sleeping Maps parameters

This script contains the parameters for the Sleepin Maps Model.
"""

import os

import numpy as np

from bunch import *
par = Bunch()
aux = Bunch()

################################################################################
#                            main parameters                               #
################################################################################
def get_par():
    """ Get main parameters.

    For each simulation, change these parameters manually.
    """
    par.N_e = 200                                  # excitatory neurons
    par.N_m = int(np.floor(par.N_e*0.3))              # neurons per map
    par.N_act = int(np.floor(par.N_e*0.05))             # neurons active at any time 

    par.Conn_norm = 1                              # normalization of post_synaptic connection strengths 
    par.Conn_spread = np.floor(par.N_m*0.1)         # Amplitude of the spatial connections (I am assuming a constant env dimension 
                                            # so that the spread of connections is proportional to the number of cells coding for it  )

    par.Conn_sigma = 0.1                                 # Noise in connection strengths 
    
    par.sigma = 0.003                                # activity noise variance

    par.Wbetween_str = 0                           # strength of between maps connections
    par.Wwithin_str = 0                            # strength of within maps connections

    par.steps = 2000                             # Total simulation length
    par.steps_chunk = 500                        # Length of each simulation chunk 

    par.Maps_list=np.arange(1,11,3)                # range of stored maps
    par.Wspa_str_list=np.arange(0.5,1.6,0.2)           # range of spatial connections strength 
    par.twin_size_list=np.arange(1,50,5)           # range of time window size for analysis 

    par.Nrep = 3                                     # number of averaged simulations 

    



