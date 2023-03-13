import numpy as np
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *



oneshot_ge = scipy.io.loadmat( f"7275_GE_oneshot_JPAoff.mat" ) 
g = oneshot_ge["ZZI"][0]+1j*oneshot_ge["ZZQ"][0]
e = oneshot_ge["ZZI"][1]+1j*oneshot_ge["ZZQ"][1]


g_plot = DataFrame()
g_plot["x"] = g.real
g_plot["y"] = g.imag

e_plot = DataFrame()
e_plot["x"] = e.real
e_plot["y"] = e.imag

plot_style = {
    "marker_style":"o",
    "marker_size":1,
}
fig = plt.figure(facecolor='white')
plt.subplots_adjust(left=0.15,
                        bottom=0.15, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.25, 
                        hspace=0.25)
gs = GridSpec(1,2)

pa_off = fig.add_subplot(gs[0,0])
pa_off.set_title(file_name)
plot_style.update( {"legend_label":"off G"})
plot_basic(plot_data[0],plot_style=plot_style,axObj=pa_off)
plot_style.update( {"legend_label":"off E"})
plot_basic(plot_data[1],plot_style=plot_style,axObj=pa_off)
plt.legend()

pa_on = fig.add_subplot(gs[0,1])
plot_style.update( {"legend_label":"on G"})
plot_basic(plot_data[2],plot_style=plot_style,axObj=pa_on)
plot_style.update( {"legend_label":"on E"})
plot_basic(plot_data[3],plot_style=plot_style,axObj=pa_on)
plt.legend()
# plt.show()