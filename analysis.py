"""
Script to analyze Activity 

"""

import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

import skimage

class Measures:

	def __init__(self, par):
		self.All_CoF=np.zeros((par.Maps_list.size,par.Wspa_str_list.size,par.twin_size_list.size))
		self.All_ActVar=np.zeros((par.Maps_list.size,par.Wspa_str_list.size,par.twin_size_list.size))
		self.All_BumpForm=np.zeros((par.Maps_list.size,par.Wspa_str_list.size))

		Act=np.zeros(par.N_m)
		Act[0:par.N_act]=1

		Bump_Score=0
		for ii in range(par.N_m):
			for jj in range(par.N_m):
				if(ii!=jj):
					tor_dist=min(abs(ii-jj),par.N_m-abs(ii-jj))	
					Bump_Score+=Act[ii]*Act[jj]*np.exp(-tor_dist**2/(2*par.Conn_spread**2))
		self.Bump_Ref=Bump_Score		

	def ActivityVar(self,par,t_win, ActStore):
		#n_chunk=np.floor()
		A_Red=skimage.measure.block_reduce(ActStore, (1,t_win), np.sum)
		DD=1-pdist(A_Red.T,metric='correlation')

		#DD=sp.spatial.distance.squareform(DD)

		self.ActVar=np.mean(DD)

	def CoFiring(self,par, t_win, ActStore, Wake_Simil, MU):
		A_Red=skimage.measure.block_reduce(ActStore+np.random.random(ActStore.shape)*0.0001, (1,t_win), np.sum) # Just added some noise to avoid NaN
		DD_S=1-pdist(A_Red,metric='correlation')
		DD_S=squareform(DD_S)

		CoF_map=np.zeros(Wake_Simil.shape[2])

		for mm in range(Wake_Simil.shape[2]):
			DD_W=Wake_Simil[:,:,mm]
			DD_W_Cells=DD_W[np.ix_(MU[mm,:],MU[mm,:])]
			

			DD_S_Cells=DD_S[np.ix_(MU[mm,:],MU[mm,:])]
			
			co=np.corrcoef(squareform(DD_W_Cells),squareform(DD_S_Cells))
			CoF_map[mm]=co[0,1]

		self.CoF_max=np.max(CoF_map)
		self.CoF_mea=np.mean(CoF_map)	

	def BumpFormation(self,par, ActStore, MU):	
		A_Red=ActStore
		#np.zeros((MU.shape[0],A_Red.shape[1]))
		nn_t=0
		self.Bump_Score=0
		for tt in range(5,A_Red.shape[1],20):
			nn_t+=1
			Act=A_Red[:,tt]
			Act[Act>0]=1
			Bump_Comp=0
			for mm in range(MU.shape[0]):
				Bump_S=0
				Act_map=Act[MU[mm,:]]
				AC=np.where(Act_map)[0]
				for ii in AC:
					for jj in AC:
						if(ii!=jj):
							tor_dist=min(abs(ii-jj),par.N_m-abs(ii-jj))	
							Bump_S+=np.exp(-tor_dist**2/(2*par.Conn_spread**2))
				Bump_Comp=np.max((Bump_Comp,Bump_S))				
			self.Bump_Score+=Bump_Comp	
		
		self.Bump_Score/=nn_t					





