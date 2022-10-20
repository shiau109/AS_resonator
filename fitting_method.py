from resonator_tools.circuit import notch_port
from electronic_delay import *
import scipy.io
import pandas as pd

def mat_file_analysis( file_name, dependency_name:str, output_path ):

    mat = scipy.io.loadmat( file_name ) 
    
    amp = mat["ZZA"].transpose()
    pha = mat["ZZP"].transpose()
    iqData = mat["ZZI"].transpose()+1j*mat["ZZQ"].transpose()
    dependency = mat["x"][0] # Dependency
    frequency = mat["y"][0]*1e9 # Freq (GHz)
    xtitle = mat["xtitle"][0]
    ytitle = mat["ytitle"][0]

    # Fit part
    rlist = []
    fdata = {}
    fdata["frequency"] = frequency
    for xi in range(dependency.shape[-1]):
        freq_fit = frequency
        iq_fit = iqData[xi]
        myResonator = notch_port()
        myResonator.add_data(freq_fit,iq_fit)
        
        fr = {}
        dep_value = dependency[xi]
        mydelay = get_myDelay(freq_fit,iq_fit)
        try:
            
            #delay, params =myResonator.get_delay(freq_fit,iq_fit)
            
            myResonator.autofit(electric_delay=mydelay)
            #myResonator.autofit()
            fit_results = myResonator.fitresults
            fit_results["delay"] = mydelay
            fit_results["photons_num"] = myResonator.get_photons_in_resonator(dep_value-95)

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
            print(f"{file_name} {xi}th {dependency_name} {dep_value} Fit failed")
            fr["delay"] = 0
        fit_results[dependency_name]=dep_value
        
        rlist.append(fit_results)
    #plt.show()
    all_results = pd.DataFrame(rlist)

    # Change columns order
    newColOrder = list(all_results.columns)
    newColOrder.remove(dependency_name)
    newColOrder.insert(0,dependency_name)
    all_results = all_results[newColOrder]
    #dictResult = dfResults.to_dict(orient="list")
    #outfn = fn.replace(".mat","")
    outfn = file_name.replace(".mat","").split("/")[-1]
        
        
    all_results.to_csv(f"{output_path}/{outfn}_fitresult.csv", index=False)
    
    condi_1 = (all_results["Qi_dia_corr_err"] / all_results["Qi_dia_corr"] < 0.1)|(all_results["Qi_dia_corr_err"] < 1e8)|(all_results["Qi_dia_corr"] > 0)
    condi_2 = (all_results["absQc_err"] / all_results["Qc_dia_corr"] < 0.1)|(all_results["Qc_dia_corr"] > 0)
    condi_3 = (all_results["Ql_err"] / all_results["Ql"] < 0.1)|(all_results["Ql"] > 0)
    indexNames = all_results[(condi_1 | condi_2 | condi_3)].index
    #all_results.drop(indexNames , inplace=True)
    #dfResults.to_csv(droperror_sample+"/"+f"{outfn}_fitResult.csv", index=False)

    return all_results