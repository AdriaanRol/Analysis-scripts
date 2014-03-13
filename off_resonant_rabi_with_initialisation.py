import numpy as np
import pylab as plt

t_list = np.linspace(0.0,300.0,1000) #Time in ns

#Omega_R = 2*np.pi/(2*120.0)
Omega_R = 2*np.pi/(100.0)
Delta = 2*np.pi * 2.16e6*1e-9

print Omega_R
print Delta

Omega_prnt = Omega_R/(2*np.pi)*1e3
Delta_prnt = Delta/(2*np.pi)*1e3
prefactor = Omega_R**2/(Delta**2 +Omega_R**2)
print 'prefactor = %.2f' %prefactor


P0 = 1-Omega_R**2/(Omega_R**2) *np.sin(t_list/2*np.sqrt(Omega_R**2))**2
P1 = 1-Omega_R**2/(Delta**2 +Omega_R**2) *np.sin(t_list/2*np.sqrt(Delta**2+Omega_R**2))**2

#Scenario population inversion

init_F = .78

a1 = init_F/3.0
a2 = 2*init_F/3.0 #part in the two side dips
a3 = (1-init_F)/3.0
a4 = 2*(1-init_F)/3.0
Sum_osc = ((a1*P0+a2*P1) - (a3*P0+a4*P1) ) +(1-a1-a2+a3+a4)#Division is because of normalisation at 1

plt.plot(t_list,Sum_osc)
plt.xlabel('time ns')
plt.ylabel('F(|0>)')
plt.ylim(0,1)
plt.title(r'Simulated Electron Rabi: $\omega_R$ =%.1f  MHz, $\Delta$ = %.1f MHz, $F_{init}$ = %.2f' %(Omega_prnt, Delta_prnt, init_F))
plt.grid(True)

plt.show()
