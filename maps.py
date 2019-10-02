"""
Script to randomly assign cells to different 1-D maps 

"""

import numpy as np


def Generate_Maps(N_maps,par):
	Map_Units=np.empty((N_maps,par.N_m),dtype=np.int)
	for i in range(N_maps):
		AA=np.random.permutation(par.N_e)	
		Map_Units[i,:]=AA[0:par.N_m]

	#Map_Units=Map_Units.astype(int)
	return Map_Units