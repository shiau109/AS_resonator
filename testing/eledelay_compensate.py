import numpy as np
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *

delay = 78# 78
const_phi = 0.1
close_current = 0.055
ref_current = -0.18
x, y, iqdata = mat_to_numpy("testing/6696_FD_JPA68_noP.mat")
probe_freq = y
bias_current = x*1000

ref_idx = np.searchsorted(bias_current, ref_current)

signal = 20*np.log10(abs(iqdata.transpose()*np.exp(-1j*y*delay)))
# signal = np.angle(iqdata.transpose()*np.exp(1j *((probe_freq-probe_freq[0])*delay*2*np.pi+const_phi) ) )
mx,my=np.meshgrid(probe_freq,bias_current)
close_idx = np.searchsorted(bias_current, close_current)
print(signal[0][10]-signal[0][0], probe_freq[10]-probe_freq[0])
print(ref_idx, close_idx)
norm_signal = np.angle(iqdata.transpose()/iqdata.transpose()[ref_idx])
diff_norm_signal = np.diff(norm_signal, axis=0)
print(diff_norm_signal.shape)

plt.figure(0)
plt.plot(probe_freq,signal[close_idx])
plt.figure(1)
plt.pcolormesh(mx,my,signal)
plt.xlabel("Frequency (GHz)")
plt.ylabel("Bias Current (mA)")
plt.colorbar()

plt.figure(2)
plt.pcolormesh(mx,my,norm_signal, vmin=-np.pi, vmax=np.pi)
plt.xlabel("Frequency (GHz)")
plt.ylabel("Bias Current (mA)")
plt.colorbar()

plt.figure(3)
mx,my=np.meshgrid(probe_freq,bias_current[1:])
plt.pcolormesh(mx,my,diff_norm_signal)
plt.xlabel("Frequency (GHz)")
plt.ylabel("Bias Current (mA)")
# plt.pcolormesh(mx,my,signal, vmin=-30, vmax=0)
plt.colorbar()

plt.show()