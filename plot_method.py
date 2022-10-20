from matplotlib import pyplot as plt
import pandas as pd




def plot(df:pd.DataFrame,Cav_name,save_mode=""):
    
    condi_1 = (df["Qi_dia_corr_err"] / df["Qi_dia_corr"] < 0.1)
    condi_2 = (df["absQc_err"] / df["Qc_dia_corr"] < 0.1)
    condi_3 = (df["Ql_err"] / df["Ql"] < 0.1)
    
    x_axis = df[(condi_1 | condi_2 | condi_3)]["photons_num"]
    Qi = df[(condi_1 | condi_2 | condi_3)]["Qi_dia_corr"]
    Qc = df[(condi_1 | condi_2 | condi_3)]["Qc_dia_corr"]
    Ql = df[(condi_1 | condi_2 | condi_3)]["Ql"]
    
    Qi_err = df[(condi_1 | condi_2 | condi_3)]["Qi_dia_corr_err"]
    Qc_err = df[(condi_1 | condi_2 | condi_3)]["absQc_err"]
    Ql_err = df[(condi_1 | condi_2 | condi_3)]["Ql_err"]
    
    plt.figure(figsize=(16,9),facecolor='white')
    plt.errorbar(x_axis,Qi,yerr=Qi_err, fmt="o",label="Qi")
    plt.errorbar(x_axis,Qc,yerr=Qc_err, fmt="o",label="Qc")
    plt.errorbar(x_axis,Ql,yerr=Ql_err, fmt="o",label="Ql")
    plt.xlabel("Photon Number n",fontsize=16)
    plt.xticks(fontsize=13)
    plt.ylabel("Q",fontsize=16)
    plt.yticks(fontsize=13)
    plt.legend()
    plt.title(sample_name+"-"+Cav_name,fontsize=16)
    plt.yscale('log')
    plt.xscale('log')
    if save_mode == "save":
        plt.savefig(fig_dir_sample+"/"+Cav_name+".png")
    plt.close()
    return {"x":x_axis,"y":Qi,"err":Qi_err}

def plot_Qi_sum(plot_dict):
    plt.figure(figsize=(32,18),facecolor='white')
    for cav in plot_dict.keys():
        plt.errorbar(plot_dict[cav]["x"],plot_dict[cav]["y"],yerr=plot_dict[cav]["err"],ms = 15, fmt="o",label=cav)
    plt.xlabel("Photon Number n",fontsize=30)
    plt.xticks(fontsize=27)
    plt.ylabel("Qi",fontsize=30)
    plt.yticks(fontsize=27)
    plt.legend(loc="lower right",fontsize=25)
    plt.title(sample_name+"-Qi",fontsize=30)
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig(fig_dir_sample+"/"+sample_name+".png")
    plt.close()
