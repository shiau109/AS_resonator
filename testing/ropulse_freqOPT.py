from matplotlib.gridspec import GridSpec
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
print(sys.path)

from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *


x, y, iqdata_g = mat_to_numpy("testing/6827_pulseCavityG01.mat")
x, y, iqdata_e = mat_to_numpy("testing/6827_pulseCavityE01.mat")

mx,my=np.meshgrid(x,y)
raw = iqdata_g-iqdata_e
dist = np.abs(raw)
start_idx = 200 
end_idx = 1700
# print(y[start_idx], y[end_idx], y[start_idx]-y[end_idx])
# plot_rawdata = pd.DataFrame()
# plot_rawdata["x"] = x
# plot_rawdata["y"] = np.mean(dist[start_idx:end_idx], axis=0)
# plot_style={}
# plot_style["marker_style"] = "o"
# ax_amp = plot_basic( plot_rawdata, plot_style )
plt.pcolormesh(mx,my,dist)

temp_amp = np.abs(iqdata_g).transpose()
plt.pcolormesh(mx,my,(temp_amp).transpose(), vmax=0.10, vmin=0.05 )

plt.colorbar()

plt.show()


temp_amp = np.abs(iqdata_e).transpose()
plt.pcolormesh(mx,my,(temp_amp).transpose(), vmax=0.10, vmin=0.05 )
plt.colorbar()

plt.show()



