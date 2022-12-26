import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')

from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *

class RS_analyzer:


    def __init__(self) -> None:
        
        self.power_calibration = -66

    def import_mat( self, path_names ) -> None:
        data = []
        dependency = []
        freq = []
        for p_name in path_names:
            x, y, matdata = mat_to_numpy(p_name)
            data.append(matdata)
            freq.append(y)
            dependency.append(x)

        self.freq = freq
        self.rawdata = data
        self.dependency = dependency

    def fit_res_model( self ):
        for s21 in self.rawdata:
            power_mk = input_power-attenuation
            part_result, fitCurves = cavityQ_fit_dependency(freq, s21, power=power_mk)
            powerQ_results.append( part_result )
            part_raw_dfs = mat_to_df( f"{raw_data_fd}/{fn}.mat" )
            raw_dfs.extend(part_raw_dfs)
            # plot_cavityS21_fitting( freq, s21, fitCurves, input_power, title=fn )

    def cavityQ_fit_dependency( self, power ):

        freq = self.freq
        s21 = self.rawdata
        # Fit part
        fitParas = []
        fitCurves = []

        if s21.ndim == 1:
            s21 = np.array([s21])
        
        for xi in range(s21.shape[0]):
            freq_fit = freq
            iq_fit = s21[xi]
            myResonator = notch_port()        
            
            try:
                # print("auto fitting")
                #delay, params =myResonator.get_delay(freq_fit,iq_fit)
                # myResonator.autofit(electric_delay=mydelay)
                mydelay = get_myDelay( freq_fit, iq_fit ) 

                delay, amp_norm, alpha, fr, Ql, A2, frcal =\
                        myResonator.do_calibration(freq_fit,iq_fit, fixed_delay=mydelay)
                myResonator.z_data = myResonator.do_normalization(freq_fit,iq_fit,delay,amp_norm,alpha,A2,frcal)

                myResonator.fitresults = myResonator.circlefit(freq_fit,myResonator.z_data,fr,Ql)
                myResonator.z_data_sim = myResonator._S21_notch(
                    freq_fit,fr=myResonator.fitresults["fr"],
                    Ql=myResonator.fitresults["Ql"],
                    Qc=myResonator.fitresults["absQc"],
                    phi=myResonator.fitresults["phi0"],
                    a=amp_norm,alpha=alpha,delay=delay)
                fit_results = myResonator.fitresults
                fit_results["A"] = amp_norm
                fit_results["alpha"] = alpha
                fit_results["delay"] = delay

                fit_results["photons"] = myResonator.get_photons_in_resonator(power[xi])
                fitCurves.append(myResonator.z_data_sim)
                
            except:
                print(f"{xi} Fit failed")
            
            fitParas.append(fit_results)
        df_fitParas = pd.DataFrame(fitParas)

        
        # Refined fitting
        chi = df_fitParas["chi_square"].to_numpy()
        weights = 1/chi**2
        min_chi_idx = chi.argmin()
        # print(df_fitParas["alpha"].to_numpy())
        # print(np.unwrap( df_fitParas["alpha"].to_numpy(), period=np.pi))

        fixed_delay = np.average(df_fitParas["delay"].to_numpy(), weights=weights)
        fixed_amp = np.average(df_fitParas["A"].to_numpy(), weights=weights)
        # fixed_alpha = np.average(np.unwrap( df_fitParas["alpha"].to_numpy(), period=np.pi), weights=weights)
        
        # fixed_delay = df_fitParas["delay"].to_numpy()[min_chi_idx]  
        # fixed_amp = df_fitParas["A"].to_numpy()[min_chi_idx]  
        # fixed_alpha = df_fitParas["alpha"].to_numpy()[min_chi_idx] 
        
        fitParas = []
        fitCurves = []
        for xi in range(s21.shape[0]):
            freq_fit = freq
            iq_fit = s21[xi]
            myResonator = notch_port()        
            try:
                # print("2nd fitting")

                delay, amp_norm, alpha, fr, Ql, A2, frcal =\
                        myResonator.do_calibration(freq_fit,iq_fit,fixed_delay=fixed_delay)

                myResonator.z_data = myResonator.do_normalization(freq_fit,iq_fit,fixed_delay,fixed_amp,alpha,A2,frcal)
                myResonator.fitresults = myResonator.circlefit(freq_fit,myResonator.z_data,fr,Ql)
                myResonator.z_data_sim = myResonator._S21_notch(
                    freq_fit,fr=myResonator.fitresults["fr"],
                    Ql=myResonator.fitresults["Ql"],
                    Qc=myResonator.fitresults["absQc"],
                    phi=myResonator.fitresults["phi0"],
                    a=fixed_amp,alpha=alpha,delay=fixed_delay)

                fit_results = myResonator.fitresults
                fit_results["A"] = fixed_amp
                fit_results["alpha"] = alpha
                fit_results["delay"] = fixed_delay
                
                fitCurves.append(myResonator.z_data_sim)
                
            except:
                print(f"{xi} Fit failed")
            
            fitParas.append(fit_results)
        df_fitParas = pd.DataFrame(fitParas)
        
        return df_fitParas, fitCurves
    def plot_cavityS21_fitting( self, title=None, output_fd=None):
        
        freq = self.freq
        raw = self.rawdata
        fitted = self.fitdata
        dep = self.dependency

        fig = plt.figure(facecolor='white',figsize=(20,9))

        gs = GridSpec(2, 2)
        
        ax_amp = plt.subplot(gs[0,0])
        ax_amp.set_xlabel("Frequency (GHz)")
        ax_amp.set_ylabel("|S21|")
        ax_pha = plt.subplot(gs[1,0])
        ax_pha.set_xlabel("Frequency (GHz)")
        ax_pha.set_ylabel("S21.angle")
        ax_iq = plt.subplot(gs[0:,1])
        ax_iq.set_xlabel("S21.real")
        ax_iq.set_ylabel("S21.imag")
        ax_iq.set_title(title)
        plot_style = {}

        color = plt.cm.rainbow(np.linspace(0, 1, dep.shape[-1]))

        for rawdata, fitcurve, dep, c in zip( raw, fitted, dep, color):
            plot_style["marker_color"] = c
            plot_style["legend_label"] = None

            # plot amplitude subplot
            plot_rawdata = pd.DataFrame()
            plot_rawdata["x"] = freq
            plot_rawdata["y"] = np.abs(rawdata)
            plot_style["marker_style"] = "o"
            
            ax_amp = plot_basic( plot_rawdata, plot_style, ax_amp )

            plot_fitcurve = pd.DataFrame()
            plot_fitcurve["x"] = freq
            plot_fitcurve["y"] = np.abs(fitcurve)
            plot_style["marker_style"] = "-"
            ax_amp = plot_basic( plot_fitcurve, plot_style, ax_amp )


            # plot phase subplot
            plot_rawdata = pd.DataFrame()
            plot_rawdata["x"] = freq
            plot_rawdata["y"] = np.unwrap(np.angle(rawdata))
            plot_style["marker_style"] = "o"
            ax_pha = plot_basic( plot_rawdata, plot_style, ax_pha )

            plot_fitcurve = pd.DataFrame()
            plot_fitcurve["x"] = freq
            plot_fitcurve["y"] = np.unwrap(np.angle(fitcurve))
            plot_style["marker_style"] = "-"
            ax_pha = plot_basic( plot_fitcurve, plot_style, ax_pha )

            # plot IQ subplot
            plot_rawdata = pd.DataFrame()
            plot_rawdata["x"] = rawdata.real
            plot_rawdata["y"] = rawdata.imag
            plot_style["marker_style"] = "o"
            ax_iq = plot_basic( plot_rawdata, plot_style, ax_iq )

            plot_fitcurve = pd.DataFrame()
            plot_fitcurve["x"] = fitcurve.real
            plot_fitcurve["y"] = fitcurve.imag
            plot_style["marker_style"] = "-"
            plot_style["legend_label"] =f"{dep}"
            ax_iq = plot_basic( plot_fitcurve, plot_style, ax_iq )
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

    def get_myDelay( fdata, zdata, edge_ratio = 0.1 ):
        total_length = fdata.shape[-1]
        edge_range = int(len(fdata)*edge_ratio)

        phase2 = np.unwrap(np.angle(zdata))
        start_delay = section_delay( fdata, zdata, start=0, end=edge_range)
        end_delay = section_delay( fdata, zdata, start=total_length-edge_range, end=total_length)

        endpoint_1 = (np.mean(fdata[-edge_range:]), np.mean(phase2[-edge_range:]))
        endpoint_2 = (np.mean(fdata[0:edge_range]), np.mean(phase2[0:edge_range]))
        se_delay = two_point_delay( endpoint_1, endpoint_2 )

        return (start_delay+end_delay+2*se_delay)/4


    def section_delay( fdata, zdata, start=0, end=1 ):
        """
        Arg
        start : is the index of position point in total data point
        end : is the index of position point in total data point
        """

        phase2 = np.unwrap(np.angle(zdata))
        gradient, intercept, r_value, p_value, std_err = stats.linregress(fdata[start:end],phase2[start:end])
        delay = gradient*(-1.)/(np.pi*2.)

        return delay

    def two_point_delay( first, second ):
        
        if first[0] > second[0]:
            del_f = first[0]-second[0]
            del_phase = first[1]-second[1]
        elif first[0] < second[0]:
            del_f = second[0]-first[0]
            del_phase = second[1]-second[1] 
        gradient = del_phase/del_f
        delay = gradient*(-1.)/(np.pi*2.)
        return delay