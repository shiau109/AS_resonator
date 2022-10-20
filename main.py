from tracemalloc import Statistic
from file_structure import *
from analysis_method import *
from plot_method import *
sample_name = "88v1"

#check_configure(sample_name, ["power", "tan_loss"])
raw_data_fd = f"{sample_name}/raw"

# Fit each cavity file (mat file) in a sample
mat_files = check_file_extension( raw_data_fd, "mat")
file_struc = check_subgroup(mat_files)
for cl, flist in file_struc.items():
    result_list = []
    for fn in flist:
        print(fn)
        result_list.append( mat_file_analysis(f"{raw_data_fd}/{fn}.mat", "power") )
    cavity_result = pd.concat(result_list)
    cavity_result.Name = cl
    save_power_dep(cavity_result, f"{sample_name}/results/power/{cl}.csv")
    plot_powerQ(cavity_result, f"{sample_name}/results/power")


power_dep_folder = f"{sample_name}/results/power"
## After assignment each cavity, get foward analysis
assignment = pd.read_json(f"{raw_data_fd}/assignment.json")

para_list = []
sample_result = []

# for fn in check_file_extension( power_dep_folder, "csv"):
## Collect assigned cavity
for cl in assignment["measurement label"].values:
    file_name = f"{power_dep_folder}/{cl}.csv"
    cavity_result = pd.read_csv( file_name )
    cavity_result.Name = cl
    sample_result.append(cavity_result)

    ## Find low power Q
    paras = find_paras(file_name, "photons", 0.1)
    paras["measurement label"] = cl

    para_list.append( paras )


plot_multiCav_powerQ(sample_result, sample_name, f"{sample_name}/results/power", assignment, save_mode=True)
lpq_result = pd.concat(para_list)

sample_statistic = pd.merge(lpq_result, assignment, on="measurement label")
# print(sample_statistic)
plot_df(sample_statistic, ("Resonant Frequency","(GHz)",1e9), ("Internal Q","",1), "Qi_dia_corr_err", f"{sample_name}/results/fr_Q", log_scale=(False,True) )
plot_df(sample_statistic, ("center linewidth","(um)",1), ("Internal Q","",1), "Qi_dia_corr_err", f"{sample_name}/results/lw_Q", log_scale=(True,True) )
