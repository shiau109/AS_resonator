import scipy.io
import pandas as pd
import numpy as np

def combine_data( subgroup:dict, raw_data_fd, power_limit=(-60,15) ):
    """
    Merge data of the same resonator
    """
    for cav_label, flist in subgroup.items():

        merged_zdata = None
        checked_power = []
        for fn in flist:
            input_power, freq, zdata = mat_to_numpy(f"{raw_data_fd}/{fn}.mat")
            zdata = zdata.transpose()
            if type(merged_zdata) == type(None):
                merged_zdata = zdata
            else:
                merged_zdata = np.vstack((merged_zdata, zdata))
            freq *=1e9
            
            min_power = power_limit[0]
            max_power = power_limit[1]
            input_power[input_power<min_power] = min_power
            input_power[input_power>max_power] = max_power
            checked_power.append(input_power)


def mat_to_numpy( file_name ):

    mat = scipy.io.loadmat( file_name )   
    # amp = mat["ZZA"].transpose()
    # pha = mat["ZZP"].transpose()
    try:
        s21 = mat["ZZI"]+1j*mat["ZZQ"]
    except:
        s21 = mat["ZZA"]*np.exp(1j*mat["ZZP"])
    
    x = mat["x"]
    if x.shape[0] == 1:
        x = x[0] 
    else:
        x = x.transpose()[0]
    
    y = mat["y"]
    if y.shape[0] == 1:
        y = y[0] 
    else:
        y = y.transpose()[0]
    xtitle = mat["xtitle"][0]
    ytitle = mat["ytitle"][0]
    return x, y, s21

def mat_to_df( file_name, commonX=False ):

    frequency, dependency, s21 = mat_to_numpy( file_name )

    if commonX:
        df = pd.DataFrame()
        df["frequency"] = frequency
        for single_S21 in s21:
            df[f"{dependency}"] = single_S21
        return df
    else:
        dfs = []
        for single_S21 in s21:
            df = pd.DataFrame()
            df["x"] = frequency
            df["y"] = single_S21
        return dfs