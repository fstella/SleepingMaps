import params
from connections import Synaptic_Matrix
from maps import Generate_Maps
from activity import Experiment
from analysis import Measures



import numpy as np
import matplotlib.pyplot as plt



para=params
para.get_par()

Mea=Measures(para.par)

for n_maps in range(para.par.Maps_list.size):
    
    for c_str in range(para.par.Wspa_str_list.size):
    
        for rr in range(para.par.Nrep):
    
            MU=Generate_Maps(para.par.Maps_list[n_maps],para.par)

            AA=Synaptic_Matrix(para.par)
            AA.Add_Spatial_Connections(para.par,MU,para.par.Wspa_str_list[c_str])
            AA.Compute_Wake_Similarity(para.par,MU)

            

            EE=Experiment(para.par)

            EE.run(para.par,AA)

            n_ch=int(np.floor(para.par.steps/para.par.steps_chunk))
        
            for cc in range(n_ch):
                # I reinitialize the network every steps_chunk steps, so I compute quantites for each period 
                f_bin=0+cc*para.par.steps_chunk
                l_bin=f_bin+para.par.steps_chunk
                
                for tt in range(para.par.twin_size_list.size):
                
                    Mea.ActivityVar(para.par,para.par.twin_size_list[tt],EE.ActStore[:,f_bin:l_bin])
                    Mea.CoFiring(para.par,para.par.twin_size_list[tt],EE.ActStore[:,f_bin:l_bin],AA.C,MU)
        
                    Mea.All_ActVar[n_maps,c_str,tt] += Mea.ActVar/n_ch/para.par.Nrep
                    Mea.All_CoF[n_maps,c_str,tt] += Mea.CoF_max/n_ch/para.par.Nrep
        
plt.figure(1)

for ss in range(6):
    plt.subplot(2,3,ss+1)
    for pp in range(4):
        plt.plot(Mea.All_CoF[pp,ss,:],color=(1-pp/4, 0, pp/4))

plt.show()



plt.figure(2)

for ss in range(6):
    plt.subplot(2,3,ss+1)
    for pp in range(4):
        plt.plot(Mea.All_ActVar[pp,ss,:],color=(1-pp/4, 0, pp/4))

plt.show()        
