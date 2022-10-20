from tracemalloc import Statistic
from file_structure import *
from analysis_method import *
from plot_method import *
sample_name = "88v1"

#check_configure(sample_name, ["power", "tan_loss"])
raw_data_fd = f"{sample_name}/raw"
assignment = pd.read_json(f"{raw_data_fd}/assignment.json")

mat_files = check_file_extension( raw_data_fd, "mat")
file_struc = check_subgroup(mat_files)
sample_result = []
for cl, flist in file_struc.items():
    result_list = []
    for fn in flist:
        print(fn)
        result_list.append( mat_file_analysis(f"{raw_data_fd}/{fn}.mat", "power") )
    cavity_result = pd.concat(result_list)
    cavity_result.Name = cl
    save_power_dep(cavity_result, f"{sample_name}/results/power/{cl}.csv")
    plot_powerQ(cavity_result, f"{sample_name}/results/power")
    sample_result.append(cavity_result)

plot_multiCav_powerQ(sample_result, sample_name, f"{sample_name}/results/power", assignment, save_mode=True)

power_dep_folder = f"{sample_name}/results/power"
# Find low power Q
para_list = []
for fn in check_file_extension( power_dep_folder, "csv"):
    paras = find_paras(f"{power_dep_folder}/{fn}.csv", "photons", 1)
    paras["measurement label"] = fn

    para_list.append( paras )
lpq_result = pd.concat(para_list)

sample_statistic = pd.merge(lpq_result, assignment, on="measurement label")

plot_Qi_sum(sample_statistic, ("Resonant Frequency","(GHz)",1e9,False), ("Internal Q","",1,True), "Qi_dia_corr_err", sample_name, f"{sample_name}/results/fr_Q" )
plot_Qi_sum(sample_statistic, ("center linewidth","(um)",1,True), ("Internal Q","",1,True), "Qi_dia_corr_err", sample_name, f"{sample_name}/results/lw_Q" )
