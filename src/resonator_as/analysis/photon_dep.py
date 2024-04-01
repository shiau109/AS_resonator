

from resonator_as.ultility.io_translator import mat_to_numpy, to_dataset
import numpy as np

from resonator_as.analysis.analysis_method import *
from resonator_as.analysis.plot_method import *
# from typing import List
from xarray import Dataset
class PhotonDepResonator():

    def __init__( self, name:str ):
        self.name = name
        self._all_data = []
    
    @property
    def all_data( self )->List[Dataset]:
        return self._all_data
    
    def import_mat( self, file_name, attenuation ):

        power, freq, s21 = mat_to_numpy( file_name )
        # print(power, freq,s21.shape)
        dataset = to_dataset(s21.transpose(), freq, power)
        
        dataset.attrs["file_name"] = file_name
        dataset.attrs["attenuation"] = attenuation

        self.all_data.append(dataset)

    def do_analysis( self, output_fd ):

        print(f"{self.name} start analysis")
        
        alldata_results = []
        alldata_plot = []
        alldata_power = []
        for dataset in self.all_data:
            file_name = dataset.attrs["file_name"]
            attenuation = float(dataset.attrs["attenuation"])
            print(f"{file_name} with {attenuation} dB attenuation")
            power = dataset.coords["power"].values
            freq = dataset.coords["frequency"].values 
            idata = dataset.sel(mixer='I').data_vars["zdata"].values
            qdata = dataset.sel(mixer='Q').data_vars["zdata"].values
            zdata = idata +1j*qdata
            power_mk = power-attenuation
            df_fitParas, zdatas_norm, fitCurves_norm = fit_resonator_batch(freq, zdata, power=power_mk)
            alldata_results.append(df_fitParas)
            alldata_power.extend(power_mk.tolist())
            for plot_data in zip(zdatas_norm,fitCurves_norm):
                alldata_plot.append((freq,plot_data[0],plot_data[1]))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(alldata_power)))
        plot_resonatorFitting( alldata_power, alldata_plot, colors, output_fd=output_fd)
        df_powerQ_results = pd.concat(alldata_results)
        df_powerQ_results.Name = self.name
        return df_powerQ_results
    