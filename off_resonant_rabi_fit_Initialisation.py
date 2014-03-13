import numpy as np
import pylab as plt
import h5py

def Rabi_evolution(transition_driven='msp1'):
    #Initial nitrogen-state Population
    a1 = 1/3.0  #part in the central dip
    a2 = 2/3.0  #part in the two side dips

    #initial guess electron-state population
    eP1 = .83#Part of pupulation initialised in ms0
    eP2 = .16 #Part of pupulation initialised in ms-1
    eP3 = 1-eP1-eP2 #Part of pupulation initialised in ms+1
    print 'C ms0 = %.2f' % eP1
    print 'C ms-1= %.2f' % eP2
    print 'C ms+1 = %.2f' % eP3

    #Check if populations add up to 1
    if eP1+eP2+eP3 !=1:
        print "caution! sum of populations != 1"

    t_list = np.linspace(0.0,300.0,1000) #Time in ns

    #Rabi Frequency dependent on transition being driven
    if transition_driven == 'msm1':
        Omega_R = 2*np.pi/(110.0)
    elif transition_driven == 'msp1':
        Omega_R = 2*np.pi/(2*125.0)

    Delta = 2*np.pi * 2.16e6*1e-9

    # print Omega_R
    # print Delta

    Omega_prnt = Omega_R/(2*np.pi)*1e3
    Delta_prnt = Delta/(2*np.pi)*1e3
    prefactor = Omega_R**2/(Delta**2 +Omega_R**2)
    print 'prefactor = %.2f' %prefactor


    P0 = 1-Omega_R**2/(Omega_R**2) *np.sin(t_list/2*np.sqrt(Omega_R**2))**2
    PD = 1-Omega_R**2/(Delta**2 +Omega_R**2) *np.sin(t_list/2*np.sqrt(Delta**2+Omega_R**2))**2

    PT = a1*P0 +a2*PD

    if transition_driven =='msm1':
        P_ms0 = eP1*PT+eP2*(1-PT)
        P_msm1 = eP2*PT +eP1*(1-PT)
        P_msp1 = eP3+t_list*0
    elif transition_driven =='msp1':
        P_ms0 = eP1*PT+eP3*(1-PT)
        P_msm1 = eP2+t_list*0
        P_msp1 = eP3*PT +eP1*(1-PT)

    Normalised_Osc = P_ms0 +eP2 +eP3

    ###########################
    ##### Importing the data #######
    ###########################
    if transition_driven =='msm1':
        h5filepath='/Users/Adriaan/Documents/teamdiamond/data_for_analysis/20140312/172721_ElectronRabi_Hans_sil1_Rabi-1/172721_ElectronRabi_Hans_sil1_Rabi-1.hdf5'
    else:
        h5filepath='/Users/Adriaan/Documents/teamdiamond/data_for_analysis/20140312/172801_ElectronRabi_Hans_sil1_Rabi+1/172801_ElectronRabi_Hans_sil1_Rabi+1.hdf5'


    f = h5py.File(h5filepath,'r')
    name = f.keys()[0]
    g = f[name]
    adwingrpname = g.keys()[1]
    adwingrp = g[adwingrpname]

    reps = adwingrp['completed_reps'].value
    sweep_pts = adwingrp.attrs['sweep_pts'] #in ns
    RO_data = adwingrp['RO_data'].value
    normalized_RO_data = RO_data/(float(reps/len(sweep_pts)))


    ###########################
    #### plotting of the data #######
    ###########################
    fig, (ax0, ax1)  = plt.subplots(nrows=2)
    if transition_driven == 'msm1':
        ax0.set_title(r'Simulated Rabi driving $\mathrm{ms}_0 \leftrightarrow \mathrm{ms}_{-1}$ with: $\omega_R$ =%.1f  MHz, $\Delta$ = %.1f MHz' %(Omega_prnt, Delta_prnt))
    else:
        ax0.set_title(r'Simulated Rabi driving $\mathrm{ms}_0 \leftrightarrow \mathrm{ms}_{+1}$ with: $\omega_R$ =%.1f  MHz, $\Delta$ = %.1f MHz' %(Omega_prnt, Delta_prnt))

    ax0.plot(t_list,P_ms0, label ='ms0')
    ax0.plot(t_list,P_msm1,label='ms-1')
    ax0.plot(t_list,P_msp1,label='ms+1')
    ax0.set_xlabel('time ns')
    ax0.set_ylabel('population in msX state')
    ax0.set_ylim(-.01,1)
    ax0.grid(True)

    ax0.legend(['ms0','ms-1','ms+1'])

    ax1.plot(t_list,Normalised_Osc,label = 'simulated oscillation')
    ax1.plot(sweep_pts,normalized_RO_data, 'ro',label ='measured data')
    print sweep_pts
    print normalized_RO_data

    ax1.set_xlabel('time ns')
    ax1.set_ylabel('normalised population in ms0')
    ax1.legend(['simulated oscillation','measured data (no RO corr)'])
    ax1.set_ylim(0,1)
    ax1.grid(True)



Rabi_evolution(transition_driven='msm1')
Rabi_evolution(transition_driven='msp1')


plt.show()