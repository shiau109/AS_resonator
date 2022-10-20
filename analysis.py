from resonator_tools.circuit import notch_port
from electronic_delay import *
import scipy.io
import pandas as pd

def mat_file_analysis( file_name, dependency_name:str ):

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
            #fr["delay"] = mydelay
            #fr["photons_num"] = myResonator.get_photons_in_resonator(power-95)

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
        
        rlist.append(fr)
    #plt.show()
    all_results = pd.DataFrame(rlist)

    # Change columns order
    newColOrder = list(all_results.columns)
    newColOrder.remove(dependency_name)
    newColOrder.insert(0,dependency_name)
    dfResults = dfResults[newColOrder]
    #dictResult = dfResults.to_dict(orient="list")
    #outfn = fn.replace(".mat","")
    return 