import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')

from resonator_as.ultility.file_structure import *
from resonator_as.ultility.io_translator import *

from resonator_as.analysis.analysis_method import *
from resonator_as.analysis.plot_method import *

# 1. Sample path setting
sample_name = "ITRI_343Chip2"
project_folder = r"D:\Data\resonator"   # empty string "" for relative path 
attenuation = 105

VNA_minpower = -60
# 1.1 File structure setting
sample_root = f"{project_folder}/{sample_name}"
raw_data_fd = f"{sample_root}/raw"
result_folder = f"{project_folder}/{sample_name}/results"
power_dep_folder = f"{result_folder}/power"
tanloss_folder = f"{result_folder}/tan_loss"
check_configure(f"{sample_root}", ["power"])

# 1.2 Find cavity data (mat file) in the folder "raw_data_fd"
mat_files = check_file_extension( raw_data_fd, "mat")
subgroup_struc = check_subgroup(mat_files)

# 2. Fit each cavity file(mat file)
tanloss_results = []
for cav_label, flist in subgroup_struc.items():
    powerQ_results_free = []
    powerQ_results_refined = []
    # 2.1 Merge same cavity data
    powerQ_raws = []
    raw_dfs = []
    merged_zdata = None
    seleted_power = []
    for fn in flist:
        input_power, freq, zdata = mat_to_numpy(f"{raw_data_fd}/{fn}.mat")
        print(input_power)
        zdata = zdata.transpose()
        if type(merged_zdata) == type(None):
            merged_zdata = zdata
        else:
            merged_zdata = np.vstack((merged_zdata, zdata))
        freq *=1e9
        
        for p in input_power.tolist():
            if p > VNA_minpower:
                seleted_power.append(p)
            else:
                seleted_power.append(VNA_minpower)

    print(f"{cav_label} fitting...")
    power_mk = np.array(seleted_power)-attenuation
    print(f"First try")
    df_fitParas_free, zdatas_norm_free, fitCurves_norm_free = fit_resonator_batch(freq, merged_zdata, power=power_mk)
    powerQ_results_free.append( df_fitParas_free )
    
    plot_cavityS21_fitting( freq, zdatas_norm_free, fitCurves_norm_free, input_power, title=f"{cav_label}_free", output_fd=power_dep_folder )
    df_powerQ_results_free = pd.concat(powerQ_results_free)
    df_powerQ_results_free.Name = cav_label
    ## Save result
    save_power_dep(df_powerQ_results_free, f"{power_dep_folder}/{cav_label}_free.csv")
    # Plotting
    plot_power_dependent_Q(df_powerQ_results_free, cav_label=f"{cav_label}_free", output_fd=power_dep_folder)

    delay_refined, amp_refined, Qc_refined, alpha_refined = get_fixed_paras( df_fitParas_free )
    print(f"delay:{delay_refined},\namp_norm{amp_refined},\nQc{Qc_refined},\nalpha{alpha_refined}")

    print(f"Second try")
    df_fitParas_refined, zdatas_norm_refined, fitCurves_norm_refined = fit_resonator_batch(freq, merged_zdata, power=power_mk, delay=delay_refined, Qc=Qc_refined, amp_norm=None, alpha=None)
    powerQ_results_refined.append( df_fitParas_refined )

    plot_cavityS21_fitting( freq, zdatas_norm_refined, fitCurves_norm_refined, input_power, title=f"{cav_label}_refined", output_fd=power_dep_folder )

    df_powerQ_results_refined = pd.concat(powerQ_results_refined)
    df_powerQ_results_refined.Name = cav_label

    ## Save result
    save_power_dep(df_powerQ_results_refined, f"{power_dep_folder}/{cav_label}_refined.csv")

    # Plotting
    plot_power_dependent_Q(df_powerQ_results_refined, cav_label=f"{cav_label}_refined", output_fd=power_dep_folder)


## After assignment each cavity, get foward analysis
assignment = pd.read_json(f"{raw_data_fd}/assignment.json")

collected_q_list = []
sample_result = []

# for fn in check_file_extension( power_dep_folder, "csv"):
## Collect assigned cavity
for cav_label in assignment["measurement_label"].values:
    file_name_free = f"{power_dep_folder}/{cav_label}_free.csv"
    cavity_result = pd.read_csv( file_name_free )
    if len(cavity_result.index)>0:
        cavity_result.Name = cav_label
        sample_result.append(cavity_result)
    else:
        print(f"No data in {cav_label}")
plot_multiCav_powerQ(sample_result, f"{sample_name}_free", assignment, output=power_dep_folder)


sample_result = []
for cav_label in assignment["measurement_label"].values:
    file_name_free = f"{power_dep_folder}/{cav_label}_refined.csv"
    cavity_result = pd.read_csv( file_name_free )
    if len(cavity_result.index)>0:
        cavity_result.Name = cav_label
        sample_result.append(cavity_result)
    
    else:
        print(f"No data in {cav_label}")

plot_multiCav_powerQ(sample_result, f"{sample_name}_refined", assignment, output=power_dep_folder)

# collected_q_result = pd.concat(collected_q_list)

# sample_statistic = pd.merge(collected_q_result, assignment, on="measurement_label")

# sample_statistic["fr"] = sample_statistic["fr"]/1e9
# # print(sample_statistic)

# # Plot tan loss model result
# xy_cols = [
#     ("center_linewidth","loss_diff",None),
#     ("center_linewidth","A_TLS","A_TLS_err"),
#     ("center_linewidth","const","const_err"),
#     ("center_linewidth","nc","nc_err")
#     ]
# xy_labels = [
#     ("Center Linewidth (um)","Loss difference"),
#     ("Center Linewidth (um)","TLS Loss"),
#     ("Center Linewidth (um)","Const Loss"),
#     ("Center Linewidth (um)","nc")
#     ]
# file_names = ["lw_Q","A_TLS","const","nc"]
# plot_list = assemble_plot_df( sample_statistic, xy_cols )
# for i, p in enumerate(plot_list):
#     fig = plt.figure(facecolor='white')
#     axObj = fig.add_subplot()
#     axObj.set_title(sample_name)
#     axObj.set_xlabel(xy_labels[i][0])
#     axObj.set_ylabel(xy_labels[i][1])

#     plot_basic(p, axObj=axObj)
#     plt.savefig(f"{result_folder}/clw/{file_names[i]}")
#     plt.close()
# plot_df(sample_statistic, ("fr","Qi_dia_corr","Qi_dia_corr_err",None), log_scale=(False,True), title=("","Photons","Internal Q"), output=f"{power_dep_folder}/fr_Q" )
# plot_df(sample_statistic, ("center_linewidth","Qi_dia_corr","Qi_dia_corr_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","Internal Q"), output=f"{result_folder}/clw/lw_Q")
# plot_df(sample_statistic, ("center_linewidth","A_TLS","A_TLS_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","TLS Loss"), output=f"{result_folder}/clw/A_TLS")
# plot_df(sample_statistic, ("center_linewidth","const","const_err",None), log_scale=(True,True), title=("","Center Linewidth (um))","Const Loss"), output=f"{result_folder}/clw/const" )
# plot_df(sample_statistic, ("center_linewidth","nc","nc_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","nc"), output=f"{result_folder}/clw/nc" )
