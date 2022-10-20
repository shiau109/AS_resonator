from matplotlib import pyplot as plt
import pandas as pd
from typing import List, Tuple



def plot_powerQ(df:pd.DataFrame, output_path, save_mode=True):
    
    # condi_1 = (df["Qi_dia_corr_err"] / df["Qi_dia_corr"] < 0.1)
    # condi_2 = (df["absQc_err"] / df["Qc_dia_corr"] < 0.1)
    # condi_3 = (df["Ql_err"] / df["Ql"] < 0.1)
    x_axis = df[["photons"]].values.flatten()
    Qi = df[["Internal Q"]].values.flatten()
    Qc = df[["Coupling Q"]].values.flatten()
    Ql = df[["Loaded Q"]].values.flatten()
    Qi_err = df[["Qi_dia_corr_err"]].values.flatten()
    Qc_err = df[["absQc_err"]].values.flatten()
    Ql_err = df[["Ql_err"]].values.flatten()

    # x_axis = df[(condi_1 | condi_2 | condi_3)]["photons"]
    # Qi = df[(condi_1 | condi_2 | condi_3)]["Qi_dia_corr"]
    # Qc = df[(condi_1 | condi_2 | condi_3)]["Qc_dia_corr"]
    # Ql = df[(condi_1 | condi_2 | condi_3)]["Ql"]
    
    # Qi_err = df[(condi_1 | condi_2 | condi_3)]["Qi_dia_corr_err"]
    # Qc_err = df[(condi_1 | condi_2 | condi_3)]["absQc_err"]
    # Ql_err = df[(condi_1 | condi_2 | condi_3)]["Ql_err"]

    plt.figure(figsize=(16,9),facecolor='white')
    plt.errorbar(x_axis,Qi,yerr=Qi_err, fmt="o",label="Qi")
    plt.errorbar(x_axis,Qc,yerr=Qc_err, fmt="o",label="Qc")
    plt.errorbar(x_axis,Ql,yerr=Ql_err, fmt="o",label="Ql")
    plt.xlabel("Photon Number n",fontsize=16)
    #plt.xticks(fontsize=13)
    plt.ylabel("Quality factor",fontsize=16)
    #plt.yticks(fontsize=13)
    plt.legend()
    #plt.title( f"{df.Name}",fontsize=16)
    plt.yscale('log')
    plt.xscale('log')
    #plt.show()
    if save_mode:
        plt.savefig(f"{output_path}/{df.Name}.png")
    plt.close()
    return {"x":x_axis,"y":Qi,"err":Qi_err}

def plot_multiCav_powerQ(dfs:List[pd.DataFrame], sample_name, output_path, assignment:pd.DataFrame, save_mode=True ):
    
    print(assignment['measurement label'])
    plt.figure(figsize=(16,9),facecolor='white')
    for df in dfs:
        print(f"ploting {df.Name}")
        if df.Name in assignment['measurement label'].values:
            asi = assignment.loc[assignment['measurement label'] == df.Name]
            print(asi["color"].values[0])
            a_color = asi["color"].values[0]
            x_axis = df[["photons"]].values.flatten()
            Qi = df[["Internal Q"]].values.flatten()
            Qi_err = df[["Qi_dia_corr_err"]].values.flatten()
            plt.errorbar(x_axis,Qi,yerr=Qi_err, fmt="o", c= a_color,label=df.Name)
    plt.xlabel("Photon Number n",fontsize=16)
    #plt.xticks(fontsize=13)
    plt.ylabel("Qi",fontsize=16)
    #plt.yticks(fontsize=13)
    plt.legend()
    plt.title( f"{sample_name}",fontsize=16)
    plt.yscale('log')
    plt.xscale('log')
    #plt.show()
    if save_mode :
        plt.savefig(f"{output_path}/{sample_name}_allQi.png")
    plt.close()

def plot_Qi_sum( df, xcol, ycol, yerrcol, sample_name, output_name ):


    if type(xcol) is tuple:
        xcol_name = xcol[0]
        xcol_unit = xcol[1]
        xcol_rescale = xcol[2]
        xcol_log = xcol[3]
    else:
        xcol_name = xcol
        xcol_unit = f""
        xcol_rescale = 1
        xcol_log = False

    if type(ycol) is tuple:
        ycol_name = ycol[0]
        ycol_unit = ycol[1]
        ycol_rescale = ycol[2]
        ycol_log = ycol[3]

    else:
        ycol_name = ycol
        ycol_unit = f""
        ycol_rescale = 1
        ycol_log = False


    x = df[[xcol_name]].values.flatten()/xcol_rescale
    y = df[[ycol_name]].values.flatten()/ycol_rescale
    yerr = df[[yerrcol]].values.flatten()/ycol_rescale
    #figsize=(16,12)
    plt.figure(facecolor='white')
    plt.errorbar(x,y,yerr=yerr,ms = 5, fmt="o")
    plt.xlabel(f"{xcol_name}{xcol_unit}")#,fontsize=30)
    #plt.xticks(fontsize=27)
    plt.ylabel(f"{ycol_name}{ycol_unit}")#,fontsize=30)
    #plt.yticks(fontsize=27)
    #plt.legend( loc="lower right")#,fontsize=25)
    plt.title( f"{sample_name}" )#,fontsize=30)
    if xcol_log : plt.xscale('log')
    if ycol_log : plt.yscale('log')

    #plt.show()
    plt.savefig(f"{output_name}.png")
    plt.close()

