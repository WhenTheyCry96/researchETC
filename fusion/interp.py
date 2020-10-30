import csv
import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, griddata

# Geometric Values
c  = np.linspace(0.55, 0.85, 7)
r1 = np.linspace(0.9, 1.3, 9)
r2 = np.linspace(5.5, 8.5, 9)

Bm_c = [24.317,
23.891,
23.506,
23.142,
22.858,
22.358,
22.073,
]

Bm_r1 = [26.453,
2.53E+01,
2.43E+01,
2.34E+01,
2.25E+01,
2.18E+01,
2.11E+01,
2.02E+01,
1.97E+01,   
]

intop_Bm_c  = interp1d(c, Bm_c, kind='cubic')
intop_Bm_r1 = interp1d(r1, Bm_r1, kind='cubic')

cnew  = np.linspace(0.55, 0.85)
r1new = np.linspace(0.9, 1.3)

def B_intop(c_in, r1_in):
    Bmc  = intop_Bm_c(c_in) 
    Bmr1 = intop_Bm_r1(r1_in)
    return 0.5*(Bmc+Bmr1)

C, R1  = np.meshgrid(cnew,r1new)

B_show = B_intop(C, R1)

# save data into csv
with open('Bm_c_r1.csv', mode='w') as csvfile:
    csvf = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvf.writerow(['R1 [m]', 'C [m]', 'Bm [T]'])
    for ri in r1new:
        for ci in cnew:
            csvf.writerow([ri, ci, B_intop(ci, ri)])
    
# matplotlib
fig, ax = plt.subplots()
cs = ax.contourf(C, R1, B_show,locator=ticker.LinearLocator())
#ax.set_title('B max')
#ax.grid()
cbar = fig.colorbar(cs)
plt.tight_layout()
plt.show()