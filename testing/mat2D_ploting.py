
import numpy as np
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *

file_name = r"C:\Users\shiau\Downloads\7394_6000M_134uA.mat"
x, y, iqdata_1 = mat_to_numpy( file_name )
iqdata_1 = scipy.io.loadmat( file_name )
xyrotate = False
# x = x*1000.
signal = iqdata_1["ZZA"]
mx,my=np.meshgrid(x,y)
vmax = 5
vmin = -10
plt.figure(figsize=(16, 10))

plt.rc('font', size=20)          # controls default text sizes

plt.xlabel("Pumping Frequency (GHz)")
plt.ylabel("Pumping Power (dBm)")

if xyrotate == True:
    plt.pcolormesh(my,mx,signal, vmin=vmin, vmax=vmax)
else:
    plt.pcolormesh(mx,my,signal, vmin=vmin, vmax=vmax)
plt.colorbar()
plt.MaxNLocator(3)

plt.subplots_adjust(left=0.25,
                    bottom=0.18, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.25, 
                    hspace=0.25)
plt.show()