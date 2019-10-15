"""
Script to generate Activity 

"""

import numpy as np


class Experiment:

	def __init__(self, par):
		self.Act=np.zeros(par.N_e)
		aa=np.random.permutation(par.N_e)
		self.Act[aa[:par.N_act]] = 1
		self.ActStore=np.empty((par.N_e,par.steps))

	def run(self,par,W):
		for t in range(par.steps):
			
			if np.mod(t,par.steps_chunk)==0:
				self.Act=np.zeros(par.N_e)
				aa=np.random.permutation(par.N_e)
				self.Act[aa[:par.N_act]] = 1
				self.ActStore[:,t]=self.Act

			else:	

				#Spread activity
				Act_New= W*self.Act + np.random.standard_normal(self.Act.shape)*(par.sigma**0.5)
				Act_New[Act_New<0]=0
				
				#Apply thresholding
				ActS = np.argsort(Act_New)[::-1]
				
				Act_temp=np.zeros(par.N_e)
				Act_temp[ActS[:par.N_act]]=Act_New[ActS[:par.N_act]];

				Act_temp /= np.sum(Act_temp)/par.Act_Norm # TO DO: Normalization should depend on the number of active units

				self.Act=Act_temp
				self.ActStore[:,t]=self.Act


