
import numpy as np
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *

x_tar, y_tar, iqdata_tar = mat_to_numpy("testing/zl_cross/5998_C2-Z2_with_AB.mat")
x_other, y_other, iqdata_other = mat_to_numpy("testing/zl_cross/5997_C1-Z2_with_AB.mat")
# x_tar, y_tar, iqdata_tar = mat_to_numpy("testing/zl_cross/5644_C2-Z2_without_AB.mat")
# x_other, y_other, iqdata_other = mat_to_numpy("testing/zl_cross/5639_C1-Z2_without_AB.mat")

xyrotate = False


signal_tar = np.abs(iqdata_tar)
signal_other = np.abs(iqdata_other)

mx_tar,my_tar=np.meshgrid(x_tar,y_tar)
mx_other,my_other=np.meshgrid(x_other,y_other)


fig = plt.figure(figsize=(8, 8))
plt.rc('font', size=20)          # controls default text sizes
fig.tight_layout()
plt.subplots_adjust(left=0.25,
                    bottom=0.18, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.25, 
                    hspace=0.25)
gs = GridSpec(2, 1)
ax_tar = plt.subplot(gs[0,0])
# ax_amp.set_xlabel("Frequency (GHz)")
# ax_tar.set_ylabel("Probing Frequency (GHz)")
# ax_amp.xaxis.set_major_locator(plt.MaxNLocator(2))
ax_tar.locator_params(tight=True)
zaxmin = y_tar.min()
zaxmax = y_tar.max()
zaxmid = (zaxmin+zaxmax)/2
zaxdf = zaxmax-zaxmin
t = [ zaxmid-zaxdf/2.5, zaxmid, zaxmid+zaxdf/2.5]
ax_tar.set_xticks([])
# ax_tar.set_yticks(['{:,.5f}'.format(x) for x in t])

ax_other = plt.subplot(gs[1,0])
ax_other.set_xlabel("Z2 Voltage (V)")

ax_other.locator_params(tight=True)
zaxmin = y_other.min()
zaxmax = y_other.max()
zaxmid = (zaxmin+zaxmax)/2
zaxdf = zaxmax-zaxmin
t = [ zaxmid-zaxdf/2.5, zaxmid, zaxmid+zaxdf/2.5]
# ax_other.set_yticks(t)




if xyrotate == True:
    ax_tar.pcolormesh(my_tar,mx_tar,signal_tar)
    ax_other.pcolormesh(my_other,mx_other,signal_other)
else:
    ax_tar.pcolormesh(mx_tar,my_tar,signal_tar)
    ax_other.pcolormesh(mx_other,my_other,signal_other)
# plt.colorbar()
ax_tar.set_ylim(6.6903, 6.6915)
#ax_other.set_ylim(-0.2, 0.2)
ax_tar.set_xlim(-0.4, 0.4)
ax_other.set_xlim(-0.4, 0.4)
ax_tar.yaxis.set_major_locator(plt.MaxNLocator(3))
ax_other.yaxis.set_major_locator(plt.MaxNLocator(3))
ax_tar.xaxis.set_major_locator(plt.MaxNLocator(5))
ax_other.xaxis.set_major_locator(plt.MaxNLocator(5))

fig.text(0.05, 0.3, f"Probing Frequency (GHz)", rotation=90, fontsize=20)


plt.show()