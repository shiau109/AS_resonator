import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')

from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *

sample_name = "TSRI_Ta_CPW_1"
project_folder = r"Z:\data\cavity" # empty string "" for relative path 
attenuation = 111
# check_configure(sample_name, ["power", "tan_loss", "clw"])
raw_data_fd = f"{project_folder}/{sample_name}/raw"
result_folder = f"{project_folder}/{sample_name}/results"
power_dep_folder = f"{result_folder}/power"
tanloss_folder = f"{result_folder}/tan_loss"

# Fit each cavity file (mat file) in a sample
mat_files = check_file_extension( raw_data_fd, "mat")
file_struc = check_subgroup(mat_files)

tanloss_results = []
for cl, flist in file_struc.items():
    powerQ_results = []
    
    # Merge same cavity data
    powerQ_raws = []
    raw_dfs = []

    for fn in flist:
        input_power, freq, s21 = mat_to_numpy(f"{raw_data_fd}/{fn}.mat")
        s21 = s21.transpose()
        freq *=1e9
        power_mk = input_power-attenuation
        part_result, fitCurves = cavityQ_fit_dependency(freq, s21, power=power_mk)
        powerQ_results.append( part_result )
        part_raw_dfs = mat_to_df( f"{raw_data_fd}/{fn}.mat" )
        raw_dfs.extend(part_raw_dfs)
        # plot_cavityS21_fitting( freq, s21, fitCurves, input_power, title=fn )
        plot_cavityS21_fitting( freq, s21, fitCurves, input_power, title=fn, output_fd=power_dep_folder )
    powerQ_result = pd.concat(powerQ_results)
    powerQ_result.Name = cl


    # plot_fitdata(raw_dfs)


    # Save result
    save_power_dep(powerQ_result, f"{power_dep_folder}/{cl}.csv")
    plot_info = [("photons","Qi_dia_corr","Qi_dia_corr_err","Internal Q"),
        ("photons","Qc_dia_corr","absQc_err","Coupling Q"),
        ("photons","Ql","Ql_err","Loaded Q")]
    # Save plot result
    plot_df(powerQ_result, plot_info, log_scale=(True,True), title=(cl,"Photons","Quality factor"), output=f"{power_dep_folder}/{cl}" )

    # Fit loss model
    powerQ_result = pd.read_csv( f"{power_dep_folder}/{cl}.csv" )
    pdloss = pd.DataFrame()
    n = powerQ_result["photons"].to_numpy()
    qi = powerQ_result["Qi_dia_corr"].to_numpy()
    qi_err = powerQ_result["Qi_dia_corr_err"].to_numpy()
    loss = 1/qi
    loss_err = loss*qi_err/qi
    pdloss["photons"] = n
    pdloss["loss"] = loss
    pdloss["loss_err"] = loss_err

    tanloss_result = fit_tanloss( n, loss, loss_err )
    tanloss_result["measurement_label"] = cl
    tanloss_results.append(tanloss_result)
    plot_powerdeploss_fitting(pdloss, tanloss_result, title=cl, output_fd=f"{tanloss_folder}" )


sample_tanloss = pd.concat(tanloss_results)
save_tanloss( sample_tanloss, f"{tanloss_folder}/tan_loss.csv")
# plot_df( sample_tanloss, f"{sample_name}/results/tan_loss")


## After assignment each cavity, get foward analysis
assignment = pd.read_json(f"{raw_data_fd}/assignment.json")

para_list = []
sample_result = []

# for fn in check_file_extension( power_dep_folder, "csv"):
## Collect assigned cavity
for cl in assignment["measurement_label"].values:
    file_name = f"{power_dep_folder}/{cl}.csv"
    cavity_result = pd.read_csv( file_name )
    cavity_result.Name = cl
    sample_result.append(cavity_result)

    
    ## Find low power Q
    paras = find_paras(file_name, "photons", 0.1)
    paras["measurement_label"] = cl

    para_list.append( paras )


plot_multiCav_powerQ(sample_result, sample_name, assignment, output=power_dep_folder)
lpq_result = pd.concat(para_list)

sample_statistic = pd.merge(lpq_result, assignment, on="measurement_label")
sample_statistic = pd.merge(sample_statistic, sample_tanloss, on="measurement_label")
sample_statistic["fr"] = sample_statistic["fr"]/1e9
# print(sample_statistic)
plot_df(sample_statistic, ("fr","Qi_dia_corr","Qi_dia_corr_err",None), log_scale=(False,True), title=("","Photons","Internal Q"), output=f"{power_dep_folder}/fr_Q" )
plot_df(sample_statistic, ("center_linewidth","Qi_dia_corr","Qi_dia_corr_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","Internal Q"), output=f"{result_folder}/clw/lw_Q")
plot_df(sample_statistic, ("center_linewidth","A_TLS","A_TLS_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","TLS Loss"), output=f"{result_folder}/clw/A_TLS")
plot_df(sample_statistic, ("center_linewidth","const","const_err",None), log_scale=(True,True), title=("","Center Linewidth (um))","Const Loss"), output=f"{result_folder}/clw/const" )
plot_df(sample_statistic, ("center_linewidth","nc","nc_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","nc"), output=f"{result_folder}/clw/nc" )
