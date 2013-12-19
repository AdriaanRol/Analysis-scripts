import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## Import data
data = pd.read_excel('DummyData.xlsx','Blad1')
B_fields = data[u'B (gauss)'].values
uB_fields = data[u'uB (gauss)'].values
z = data[u'z(mm)'].values

magnetclass = data['Magnet Class'][0]
diameter = data['dimensions(mm)'][0]
height = data['dimensions(mm)'][1]

Br =  data['Brem'][0]

#http://www.supermagnete.de/eng/data_table.php

R = diameter /2
D = height
B_Calc = Br/2 *((D+z)/(np.sqrt(R**2+(D+z)**2))-z/(np.sqrt(R**2 +z**2)))

plt.plot(z,B_Calc)
plt.errorbar(z,B_fields,uB_fields)
plt.show()
