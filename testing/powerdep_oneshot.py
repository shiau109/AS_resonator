
import numpy as np
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *


y, x, iqdata_e = mat_to_numpy("testing/OS06002600E.mat")
iqdata_e = iqdata_e.transpose()
y, x, iqdata_g = mat_to_numpy("testing/OS06002600G.mat")
iqdata_g = iqdata_g.transpose()



plot_style = default_plot_style
dependency = y
color = plt.cm.rainbow(np.linspace(0, 1, dependency.shape[-1]))

for g, e, dep, c in zip(iqdata_e, iqdata_g, dependency, color):
    
    fig = plt.figure(facecolor='white',figsize=(20,9))

    gs = GridSpec(2, 2)
    ax_gnd = plt.subplot(gs[0,0])
    ax_gnd.set_xlabel("I")
    ax_gnd.set_ylabel("Q")
    ax_gnd.set_title(f"GND {dep}")  

    ax_exc = plt.subplot(gs[1,0])
    ax_exc.set_xlabel("I")
    ax_exc.set_ylabel("Q")
    ax_exc.set_title(f"EXC {dep}")

    ax_mix = plt.subplot(gs[0:,1])
    ax_mix.set_xlabel("I")
    ax_mix.set_ylabel("Q")
    ax_mix.set_title(f"XYL {dep}")

    plot_style["marker_color"] = "r"
    plot_style["legend_label"] = None
    plot_style["marker_size"] = 0.5
    # plot amplitude subplot
    plot_data_g = pd.DataFrame()
    plot_data_g["x"] = g.real
    plot_data_g["y"] = g.imag
    plot_style["marker_style"] = "o"
    ax_gnd = plot_basic2D( plot_data_g, plot_style, ax_gnd )


    # plot phase subplot
    plot_style["marker_color"] = "b"
    plot_data_e = pd.DataFrame()
    plot_data_e["x"] = e.real
    plot_data_e["y"] = e.imag
    plot_style["marker_style"] = "o"
    ax_exc = plot_basic2D( plot_data_e, plot_style, ax_exc )

    plot_style["marker_color"] = "r"
    plot_data_g = pd.DataFrame()
    plot_data_g["x"] = g.real
    plot_data_g["y"] = g.imag
    plot_style["marker_style"] = "o"
    ax_mix = plot_basic2D( plot_data_g, plot_style, ax_mix )
    plot_style["marker_color"] = "b"
    plot_data_e = pd.DataFrame()
    plot_data_e["x"] = e.real
    plot_data_e["y"] = e.imag
    plot_style["marker_style"] = "o"
    ax_mix = plot_basic2D( plot_data_e, plot_style, ax_mix )


    plt.show()