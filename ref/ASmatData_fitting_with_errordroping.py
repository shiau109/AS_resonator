from tools.circuit import notch_port
# Need install resonator_tool package first 
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
from os import listdir,makedirs
from os.path import isfile, join,exists
from shutil import rmtree
import matplotlib.gridspec as gridspec
from scipy import stats
from scipy.optimize import curve_fit as cf
def get_myDelay( fdata, zdata ):
    edge_range = int(len(fdata)*0.1)
    end_point = int(len(fdata)*0.05)
    phase2 = np.unwrap(np.angle(zdata))
    start_gradient, intercept, r_value, p_value, std_err = stats.linregress(fdata[0:edge_range],phase2[0:edge_range])
    start_delay = start_gradient*(-1.)/(np.pi*2.)
    end_gradient, intercept, r_value, p_value, std_err = stats.linregress(fdata[-edge_range:],phase2[-edge_range:])
    end_delay = end_gradient*(-1.)/(np.pi*2.)

    d_phase = np.mean(phase2[-edge_range:]) - np.mean(phase2[0:edge_range])
    
    se_delay = d_phase/(fdata[-end_point]-fdata[end_point])*(-1.)/(np.pi*2.)
    return (start_delay+end_delay+2*se_delay)/4


# fitiing tangent loss with vortex(c) and TLS term(a/(...))
def tan_loss(x,a,c,nc):
    return (c+a/(1+(x/nc)**2)**0.5)

def plot(df,Cav_name,save_mode=""):
    
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

fdName = "measuerment/withecco" # Type folder name (which the mat file live in, and which is in the same dir with this py file)
# fdName = "measuerment/withoutecco"
sample_name = "ITRI-Nb"

result_folder = f"{fdName}/Results"
# result_folder_sample = result_folder+"/"+sample_name
# fig_dir_sample = result_folder+"/Figure/"+sample_name
# para_dir_sample = result_folder+"/fit_paras/"+sample_name
result_folder_sample = result_folder+"/"
fig_dir_sample = result_folder+"/Figure/"
para_dir_sample = result_folder+"/fit_paras/"
droperror_sample = result_folder+"/droperror/"

goingon = 1

if not exists(result_folder):
    makedirs(result_folder)
    print("Results Directory created!")
else:
    print("Results Directory Exist Keep going!")
if not exists(droperror_sample):
    makedirs(droperror_sample)
    print("droperror_sample Directory create!")
else:
    print("droperror_sample Directory Exist Keep Going!")

if not exists(result_folder_sample):
    makedirs(result_folder_sample)
    print("Results Directory for this sample created!")
    goingon = 1
else:
    print("Results for this sample Exist!")
#     cover = input("This sample has a record, overwrite it or not (y/n): ")
#     if cover.lower() == "y" or cover.lower() == "yes":
#         rmtree(result_folder_sample)
# #         rmtree(fig_dir_sample)
# #         rmtree(para_dir_sample)
#         makedirs(result_folder_sample)
#         print("Results Directory for this sample renew!")
#         goingon = 1
#     else:
#         print("Results for this sample Exist!")

# create the sample folder in results directory
if goingon == 1:
    
    onlyfiles=[]
    for f in listdir(fdName):
        if len(f.split(".")) == 2 and f.split(".")[1] == "mat" and isfile(join(fdName, f)):
            onlyfiles.append(f)
    #onlyfiles = [f for f in listdir(fdName) if isfile(join(fdName, f))]
    print(onlyfiles)
    dependencyName = "Power" # Name of column in fit result


    for fn in onlyfiles:
        # Get data from file
        
        mat = scipy.io.loadmat(f"{fdName}/{fn}") 
        amp = mat["ZZA"].transpose()
        pha = mat["ZZP"].transpose()
        iqData = mat["ZZI"].transpose()+1j*mat["ZZQ"].transpose()
        xAxis = mat["x"][0] # Dependency
        yAxis = mat["y"][0]*1e9 # Freq
        xtitle = mat["xtitle"][0]
        ytitle = mat["ytitle"][0]

        # Fit part
        rlist = []
        fdata = {}
        fdata["frequency"] = yAxis
        for xi in range(xAxis.shape[-1]):
            freq_fit = yAxis
            iq_fit = iqData[xi]
            myResonator = notch_port()
            myResonator.add_data(freq_fit,iq_fit)
            
            fr = {}
            power = xAxis[xi]
            mydelay = get_myDelay(freq_fit,iq_fit)
            try:
                
                #delay, params =myResonator.get_delay(freq_fit,iq_fit)
                
                myResonator.autofit(electric_delay=mydelay)
                #myResonator.autofit()
                fr = myResonator.fitresults
                fr["delay"] = mydelay
                fr["photons_num"] = myResonator.get_photons_in_resonator(power-95)

                ## If you want to plot the raw data and fitting curve, use following code.  
                '''
                gs = gridspec.GridSpec(2, 2)
                ax_amp = plt.subplot(gs[0,0])
                ax_amp.plot(freq_fit,np.abs(iq_fit),label="raw")
                ax_amp.plot(freq_fit,np.abs(myResonator.z_data_sim),label="fit")

                ax_pha = plt.subplot(gs[1,0])
                ax_pha.plot(freq_fit,np.angle(iq_fit),label="raw")
                ax_pha.plot(freq_fit,np.angle(myResonator.z_data_sim),label="fit")

                ax_iq = plt.subplot(gs[0:,1])
                ax_iq.plot(iq_fit.real,iq_fit.imag,label="raw")
                ax_iq.plot(myResonator.z_data_sim.real,myResonator.z_data_sim.imag,label="fit")

                plt.show()
                '''
            except:
                print(fn, xi, "Fit failed")
                fr["delay"] = 0
            fr[dependencyName]=power
            
            rlist.append(fr)
        plt.show()
        dfResults = pd.DataFrame(rlist)

        # Change columns order
        newColOrder = list(dfResults.columns)
        newColOrder.remove(dependencyName)
        newColOrder.insert(0,dependencyName)
        dfResults = dfResults[newColOrder]
        #dictResult = dfResults.to_dict(orient="list")
        outfn = fn.replace(".mat","")
        
        
        dfResults.to_csv(result_folder_sample+"/"+f"{outfn}_fitResult.csv", index=False)
        
        condi_1 = (dfResults["Qi_dia_corr_err"] / dfResults["Qi_dia_corr"] > 0.1)|(dfResults["Qi_dia_corr_err"] > 1e7)
        condi_2 = (dfResults["absQc_err"] / dfResults["Qc_dia_corr"] > 0.1)
        condi_3 = (dfResults["Ql_err"] / dfResults["Ql"] > 0.1)
        indexNames = dfResults[(condi_1 | condi_2 | condi_3)].index
        dfResults.drop(indexNames , inplace=True)
        dfResults.to_csv(droperror_sample+"/"+f"{outfn}_fitResult.csv", index=False)
    file_dir = listdir(result_folder_sample)

    if not exists(fig_dir_sample):
        makedirs(fig_dir_sample)
        print("Figure Directory for this sample created!")
    else:
        print("Figure Directory for this sample Exist Keep Going!")

    

    # fig generate main program
    sum_dict = {}
    for filename in file_dir:
        if filename[-4:] == '.csv':
            print(filename)
            file_path = result_folder_sample+"/"+filename 
            df = pd.read_csv(file_path)
            
            
            cav_loc = filename.split("_")[0]
            plot_items = plot(df,cav_loc,"save")
            sum_dict[cav_loc] = plot_items

    plot_Qi_sum(sum_dict)   #save the all cavities Qi comparison figure
    print("Finish! \nSave Qi comparison figure completely!")

    # generate fitting parameters with .csv file
    
    if not exists(para_dir_sample):
        makedirs(para_dir_sample)
        print("para Directory create!")
    else:
        print("para Directory Exist Keep Going!")

        
    paras = {}
    for cav in sum_dict.keys():
        popt, pcov = cf(tan_loss,sum_dict[cav]["x"] ,1/sum_dict[cav]["y"],sigma=sum_dict[cav]["err"]**2)

        plt.figure(figsize=(16,9))
        plt.plot(sum_dict[cav]["x"],tan_loss(sum_dict[cav]["x"],*popt),"r",label="fit")
        plt.scatter(sum_dict[cav]["x"] ,1/sum_dict[cav]["y"],label="Ki")
        plt.legend()
        plt.title(cav)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel("Photon Number n",fontsize=15)
        plt.xticks(fontsize=13)
        plt.ylabel("Ki (1/Qi)",fontsize=15)
        plt.yticks(fontsize=14)
        
        plt.savefig(para_dir_sample+"/"+cav+".png")
        plt.close()

        paras[cav]={"fr (GHz)":float(int(cav[1:])/10000),"TLS":popt[0],"Const.":popt[1],"Nc":popt[2]}
        
    para_df = pd.DataFrame.from_dict(paras).T
    para_df.to_csv(para_dir_sample+"/"+"fitting_paras.csv")
    print("Fitting Complete!")