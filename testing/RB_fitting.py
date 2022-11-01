import scipy.io
import pandas as pd
from scipy.optimize import curve_fit 
import numpy as np
from os import listdir,makedirs
from os.path import isfile, join,exists
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *


def gate_fidelity_decay(x, A, p, B):
    return A*p**x +B

def fit_gate_fidelity( seq_lens, signal ):
    
    fidelity_ave = np.mean(signal, axis=0) 
    upper_bound = [1e2,1,1e2]
    lower_bound = [-1e2,0,-1e2]
    try:
        popt, pcov = curve_fit(gate_fidelity_decay, seq_lens, fidelity_ave, bounds=(lower_bound,upper_bound))
        p_sigma = np.sqrt(np.diag(pcov))
    except:
        popt = [0,0,0]
        p_sigma = [0,0,0]
    results_dict = {
        "A": [popt[0]],
        "p": [popt[1]],
        "B": [popt[2]],
        "A_err": [p_sigma[0]],
        "p_err": [p_sigma[1]],
        "B_err": [p_sigma[2]],
    }
    results = pd.DataFrame(results_dict)

    return results

check_file_extension("testing/","mat")
x, y, iqdata = mat_to_numpy("testing/2DRB_2.mat")
print(x, y)
signal = np.angle(iqdata)

fit_result = fit_gate_fidelity( x, signal )
print(fit_result)
e_clf = (1-fit_result["p"].to_numpy()[0])/2
e_xyg = e_clf/1.875
print("average error per Clifford",e_clf)
print("average error per XY gate",e_xyg)

total_x = np.array([])
total_y = np.array([])
for i in range(y.shape[0]):
    total_x = np.append(total_x, x)
    total_y = np.append(total_y, signal[i])
plot_data_raw = {
    "x":total_x,
    "y":total_y
}
plot_df_raw = pd.DataFrame(plot_data_raw)

plot_data_raw_ave = {
    "x":x,
    "y":np.mean(signal, axis=0) 
}
plot_df_raw_ave = pd.DataFrame(plot_data_raw_ave)


plot_data_fit = {
    "x":x,
    "y":gate_fidelity_decay(x,fit_result["A"].to_numpy()[0],fit_result["p"].to_numpy()[0],fit_result["B"].to_numpy()[0])
}
plot_df_fit = pd.DataFrame(plot_data_fit)

fig = plt.figure(facecolor='white')
axObj = fig.add_subplot()
axObj.set_title("Randomized Banchmarking")
axObj.set_xlabel("Number of Gate")
axObj.set_ylabel("Phase")

default_plot_style = {
    "marker_style":"o",
    "marker_size":1,
    "marker_color":None,
    "legend_label":None,
    "xlabel":None,
    "ylabel":None,
    "xscale":"linear",
    "yscale":"linear"
}
raw_style = default_plot_style
raw_style["marker_size"] = 1
raw_style["legend_label"] = "raw"
plot_basic2D(plot_df_raw, axObj=axObj, plot_style = raw_style)

ave_style = default_plot_style
ave_style["marker_size"] = 5
ave_style["legend_label"] = "ave"
plot_basic2D(plot_df_raw_ave, axObj=axObj, plot_style = ave_style)

fit_style = default_plot_style
fit_style["marker_style"] = "-"
fit_style["legend_label"] = "fit"
plot_basic2D(plot_df_fit, axObj=axObj, plot_style = fit_style)

axObj.legend()

axObj.text(0.5, 0.9, f"Random times {y.shape[0]}", fontsize=10, transform=axObj.transAxes)
axObj.text(0.5, 0.85, f"{r'$r_{Clifford}$='}{e_clf:e}", fontsize=10, transform=axObj.transAxes)
axObj.text(0.5, 0.8, f"{r'$r_{gate}$='}{e_xyg:e}", fontsize=10, transform=axObj.transAxes)

plt.show()