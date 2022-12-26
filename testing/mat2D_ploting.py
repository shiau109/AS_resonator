
import numpy as np
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *


x, y, iqdata_1 = mat_to_numpy("testing/2Q_swap/5576_Q2SWAP.mat")
# x, y, iqdata_g = mat_to_numpy("testing/JPA67_fp1110_25.mat")
xyrotate = False

signal = np.angle(iqdata_1)
mx,my=np.meshgrid(x,y)

plt.figure(figsize=(16, 10))

plt.rc('font', size=20)          # controls default text sizes

plt.ylabel("Z1 Voltage (V)")
plt.xlabel("Swap time (ns)")

if xyrotate == True:
    plt.pcolormesh(my,mx,signal)
else:
    plt.pcolormesh(mx,my,signal)
# plt.colorbar()
plt.MaxNLocator(3)

plt.subplots_adjust(left=0.25,
                    bottom=0.18, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.25, 
                    hspace=0.25)
plt.show()