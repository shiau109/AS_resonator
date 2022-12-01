

from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *


flux, freq, s21 = mat_to_numpy(f"testing/pdc.mat")
s21 = s21.transpose()
freq *=1e9

part_result, fitCurves = cavityQ_fit_dependency(freq, s21)
part_result["flux"] = flux
# print(part_result["Qc_dia_corr"].to_numpy())
condi_1 = (part_result["Qi_dia_corr_err"] / part_result["Qi_dia_corr"] > 0.2) | (part_result["Qi_dia_corr"] < 0) #|(df["Qi_dia_corr_err"] < 1e8)
condi_2 = (part_result["absQc_err"] / part_result["absQc"] > 0.2) | (part_result["absQc"] < 0)
condi_3 = (part_result["Ql_err"] / part_result["Ql"] > 0.2) | (part_result["Ql"] < 0)
indexNames = part_result[(condi_1 | condi_2 | condi_3)].index 
part_result.drop(indexNames , inplace=True)

fig = plt.figure()
axObj = fig.add_subplot()
axObj.set_xlabel("flux")
axObj.set_ylabel("Q")
plot_style = {}
plot_style["legend_label"] = "Qc"
plotdf = pd.DataFrame()
plotdf["x"] = part_result["flux"].to_numpy()
plotdf["y"] = part_result["fr"].to_numpy()
plot_basic( plotdf, plot_style=plot_style, axObj=axObj )
# plotdf["x"] = part_result["flux"].to_numpy()
# plotdf["y"] = part_result["Qi_dia_corr"].to_numpy()
# plot_style["legend_label"] = "Qi"
plot_basic( plotdf, plot_style=plot_style, axObj=axObj )
plt.legend()
plt.show()