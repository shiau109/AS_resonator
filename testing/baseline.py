
import numpy as np
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *


x, y, iqdata_e = mat_to_numpy("testing/excited_cavity.mat")
x, y, iqdata_g = mat_to_numpy("testing/ground_cavity.mat")
signal = abs(iqdata_e-iqdata_g)
mx,my=np.meshgrid(x,y)

plt.pcolormesh(mx,my,signal)
plt.show()