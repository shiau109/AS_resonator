from matplotlib.gridspec import GridSpec
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
print(sys.path)

from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *


freq, dependency, iqdata = mat_to_numpy("testing/6827_pulseCavityE01.mat")

raw = iqdata

fig = plt.figure(facecolor='white',figsize=(20,9))

gs = GridSpec(2, 2)
ax_amp = plt.subplot(gs[0,0])
ax_amp.set_xlabel("Frequency")
ax_amp.set_ylabel("|S21|")
ax_pha = plt.subplot(gs[1,0])
ax_pha.set_xlabel("Frequency")
ax_pha.set_ylabel("S21.angle")
ax_iq = plt.subplot(gs[0:,1])
ax_iq.set_xlabel("S21.real")
ax_iq.set_ylabel("S21.imag")

plot_style = default_plot_style

color = plt.cm.rainbow(np.linspace(0, 1, dependency.shape[-1]))

for rawdata, dep, c in zip(raw,dependency, color):
    if dep > 500:
        plot_style["marker_color"] = c
        plot_style["legend_label"] = None
        plot_style["marker_size"] = 0.5
        # plot amplitude subplot
        plot_rawdata = pd.DataFrame()
        plot_rawdata["x"] = freq
        plot_rawdata["y"] = np.abs(rawdata)
        plot_style["marker_style"] = "o"
        ax_amp = plot_basic( plot_rawdata, plot_style, ax_amp )


        # plot phase subplot
        plot_rawdata = pd.DataFrame()
        plot_rawdata["x"] = freq
        # plot_rawdata["y"] = np.unwrap(np.angle(rawdata))
        plot_rawdata["y"] = np.angle(rawdata)
        plot_style["marker_style"] = "o"
        ax_pha = plot_basic( plot_rawdata, plot_style, ax_pha )

        # plot IQ subplot
        plot_rawdata = pd.DataFrame()
        plot_rawdata["x"] = rawdata.real
        plot_rawdata["y"] = rawdata.imag
        plot_style["marker_style"] = "o"
        ax_iq = plot_basic( plot_rawdata, plot_style, ax_iq )

ax_amp.legend()
ax_pha.legend()
ax_iq.legend()
plt.show()