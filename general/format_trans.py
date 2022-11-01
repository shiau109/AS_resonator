import scipy.io
import pandas as pd

def mat_to_numpy( file_name ):

    mat = scipy.io.loadmat( file_name )   
    # amp = mat["ZZA"].transpose()
    # pha = mat["ZZP"].transpose()
    s21 = mat["ZZI"]+1j*mat["ZZQ"]
    x = mat["x"]
    if x.shape[0] == 1:
        x = x[0] # Dependency
    else:
        x = x.transpose()[0]
    
    y = mat["y"]
    if y.shape[0] == 1:
        y = y[0] # Freq (Hz)
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