from email.policy import default
from sqlite3 import DatabaseError
from xml.sax import default_parser_list
from matplotlib import pyplot as plt
import pandas as pd
from typing import List, Tuple
from matplotlib.gridspec import GridSpec
import numpy as np
from .analysis_method import *

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

def plot_cavityS21_fitting(freq:np.ndarray, raw:np.ndarray, fit:np.ndarray, dependency:np.array, title=None, output_fd=None):
    
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

    for rawdata, fitcurve, dep, c in zip(raw,fit,dependency, color):
        plot_style["marker_color"] = c
        plot_style["legend_label"] = None

        # plot amplitude subplot
        plot_rawdata = pd.DataFrame()
        plot_rawdata["x"] = freq
        plot_rawdata["y"] = np.abs(rawdata)
        plot_style["marker_style"] = "o"
        
        ax_amp = plot_basic2D( plot_rawdata, plot_style, ax_amp )

        plot_fitcurve = pd.DataFrame()
        plot_fitcurve["x"] = freq
        plot_fitcurve["y"] = np.abs(fitcurve)
        plot_style["marker_style"] = "-"
        ax_amp = plot_basic2D( plot_fitcurve, plot_style, ax_amp )


        # plot phase subplot
        plot_rawdata = pd.DataFrame()
        plot_rawdata["x"] = freq
        plot_rawdata["y"] = np.unwrap(np.angle(rawdata))
        plot_style["marker_style"] = "o"
        ax_pha = plot_basic2D( plot_rawdata, plot_style, ax_pha )

        plot_fitcurve = pd.DataFrame()
        plot_fitcurve["x"] = freq
        plot_fitcurve["y"] = np.unwrap(np.angle(fitcurve))
        plot_style["marker_style"] = "-"
        ax_pha = plot_basic2D( plot_fitcurve, plot_style, ax_pha )

        # plot IQ subplot
        plot_rawdata = pd.DataFrame()
        plot_rawdata["x"] = rawdata.real
        plot_rawdata["y"] = rawdata.imag
        plot_style["marker_style"] = "o"
        ax_iq = plot_basic2D( plot_rawdata, plot_style, ax_iq )

        plot_fitcurve = pd.DataFrame()
        plot_fitcurve["x"] = fitcurve.real
        plot_fitcurve["y"] = fitcurve.imag
        plot_style["marker_style"] = "-"
        plot_style["legend_label"] =f"{dep}"
        ax_iq = plot_basic2D( plot_fitcurve, plot_style, ax_iq )
    ax_amp.legend()
    ax_pha.legend()
    ax_iq.legend()
    if output_fd != None :
        full_path = f"{output_fd}/{title}_fitcurve.png"
        print(f"Saving plot at {full_path}")
        plt.savefig(f"{full_path}")
        plt.close()
    else:
        plt.show()



def plot_powerdeploss_fitting( powerloss, tanloss_result, title=None, output_fd=None ):

    fig = plt.figure(facecolor='white')
    axObj = fig.add_subplot()
    axObj.set_title(title)
    axObj.set_xlabel("n")
    axObj.set_ylabel("loss")

    n = powerloss["photons"].to_numpy()
    loss = powerloss["loss"].to_numpy()
    loss_err = powerloss["loss_err"].to_numpy()

    
    # Raw data 
    # Prepare plot data format
    powdep_loss = pd.DataFrame()
    powdep_loss["x"] = n
    powdep_loss["y"] = loss
    powdep_loss["yerr"] = loss_err
    # Prepare plot style format
    plot_style = default_plot_style
    plot_style["marker_style"] = "o"
    plot_basic2D( powdep_loss, plot_style, axObj)
    # Fitting curve
    # Prepare plot data format
    powdep_loss_fit = pd.DataFrame()
    fit_n = 10**(np.linspace(-2,6,100))
    powdep_loss_fit["x"] = fit_n
    powdep_loss_fit["y"] = tan_loss(fit_n, tanloss_result["A_TLS"].values, tanloss_result["const"].values, tanloss_result["nc"].values)
    # Prepare plot style format
    plot_style = default_plot_style
    plot_style["marker_style"] = "-"
    plot_basic2D( powdep_loss_fit, plot_style, axObj )

    axObj.set_xlabel("Photon Number")
    axObj.set_ylabel("Loss")
    axObj.set_xscale("log")
    axObj.set_yscale("log")
    if output_fd != None :
        plt.savefig(f"{output_fd}/{title}_fitcurve.png")
        plt.close()
    else:
        plt.show()




# Basic ploting
def plot_basic2D( data:pd.DataFrame, plot_style:dict=default_plot_style, axObj=None, output=None):
    """


    output : str output path and name

    """
    mk_style = plot_style["marker_style"]
    mk_size = plot_style["marker_size"]
    mk_color = plot_style["marker_color"]
    leg_label = plot_style["legend_label"]

    if axObj ==None :
        fig = plt.figure(figsize=(16,9),facecolor='white')
        axObj = fig.add_subplot()
        # axObj.set_title(plot_style["title"])
        axObj.set_xlabel(plot_style["xlabel"])
        axObj.set_ylabel(plot_style["ylabel"])
        axObj.set_xscale(plot_style["xscale"])
        axObj.set_yscale(plot_style["yscale"])
        

    x = data["x"].to_numpy()
    y = data["y"].to_numpy()
    if "yerr" in data:
        yerr = data["yerr"].to_numpy()
    else:
        yerr = None
    axObj.errorbar( x, y, yerr=yerr, fmt=mk_style, ms=mk_size, c=mk_color, label=leg_label )
    if axObj == None:
        plt.show()
    if output != None:
        plt.savefig(f"{output}.png")
        plt.close()


    return axObj

# Older style
def plot_multiCav_powerQ(dfs:List[pd.DataFrame], sample_name, assignment:pd.DataFrame, output=None ):
    
    plt.figure(facecolor='white', figsize=(8,5)) #figsize=(16,9),
    for df in dfs:
        print(f"ploting {df.Name}")
        if df.Name in assignment['measurement_label'].to_numpy():
            asi = assignment.loc[assignment['measurement_label'] == df.Name]
            a_marker_style = asi["marker_style"].values[0]
            a_color = asi["color"].values[0]
            a_clw = asi["center_linewidth"].values[0]
            x_axis = df["photons"].to_numpy()
            Qi = df["Qi_dia_corr"].to_numpy()
            Qi_err = df["Qi_dia_corr_err"].to_numpy()
            plt.errorbar(x_axis, Qi, yerr=Qi_err, ms = 5, fmt=a_marker_style, c=a_color, label=f"{df.Name}-{a_clw}um")
    plt.xlabel("Photon Number n",fontsize=16)
    #plt.xticks(fontsize=13)
    plt.ylabel("Qi",fontsize=16)
    #plt.yticks(fontsize=13)
    plt.legend()
    plt.title( f"{sample_name}",fontsize=16)
    plt.yscale('log')
    plt.xscale('log')
    #plt.show()
    if output != None :
        plt.savefig(f"{output}/{sample_name}_allQi.png")
    plt.close()

def plot_df(df:pd.DataFrame, xycols, axObj=None, log_scale=(False,False), title=None, output=None):
    """
    xycols : a array of 4 value tuple: ( xcol, ycol, yerrcol, label )
        xcol, ycol, yerrcol are names of column
        label is shown text in legend

    title : a 3 value tuple: ( Graph, x axis, y axis )

    log_scale : a list of 2 value tuple: ( xcol, ycol )
        xcol, ycol are bool, True for log scale

    output : str output path and name

    """
    if axObj == None:
        fig = plt.figure(figsize=(16,9),facecolor='white')
        axObj = fig.add_subplot()
    if type(xycols) != list:
        xycols = [xycols]
    for xcol, ycol, yerrcol, label in xycols:
        x = df[xcol].to_numpy()
        y = df[ycol].to_numpy()
        if yerrcol != None:
            yerr = df[yerrcol].to_numpy()
            axObj.errorbar( x, y, yerr=yerr, fmt="o", label=label )
        else:
            axObj.plot( x, y, "o", label=label )
    # plt.title( f"{df.Name}",fontsize=16)

    if title != None:
        axObj.set_title(title[0],fontsize=16)
        axObj.set_xlabel(title[1],fontsize=16)
        axObj.set_ylabel(title[2],fontsize=16)

    #plt.yticks(fontsize=13)
    axObj.legend()
    if log_scale[0] : axObj.set_xscale('log')
    if log_scale[1] : axObj.set_yscale('log')
    #plt.show()
    if output != None:
        plt.savefig(f"{output}.png")
        plt.close()
    return axObj