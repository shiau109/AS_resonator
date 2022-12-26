import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')

from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *

# 1. Sample path setting
sample_name = "TSRI_Ta_CPW_1"
project_folder = r"Z:\data\resonator" # empty string "" for relative path 
attenuation = 111

# 1.1 File structure setting
check_configure(sample_name, ["power", "tan_loss", "clw"])
raw_data_fd = f"{project_folder}/{sample_name}/raw"
result_folder = f"{project_folder}/{sample_name}/results"
power_dep_folder = f"{result_folder}/power"
tanloss_folder = f"{result_folder}/tan_loss"

# 1.2 Find cavity data (mat file) in the folder "raw_data_fd"
mat_files = check_file_extension( raw_data_fd, "mat")
subgroup_struc = check_subgroup(mat_files)

# 2. Fit each cavity file(mat file)
tanloss_results = []
for cav_label, flist in subgroup_struc.items():
    powerQ_results = []
    
    # 2.1 Merge same cavity data
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
    powerQ_result.Name = cav_label

    # plot_fitdata(raw_dfs)


    ## Save result
    save_power_dep(powerQ_result, f"{power_dep_folder}/{cav_label}.csv")

    # 2.2 Plotting
    # 2.2 plot setting
    plot_power_dependent_Q(powerQ_result, cav_label=cav_label, output_fd=power_dep_folder)

    # Fit loss model
    powerQ_result = pd.read_csv( f"{power_dep_folder}/{cav_label}.csv" )
    if len(powerQ_result.index) > 0:
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
        tanloss_result["measurement_label"] = cav_label
        tanloss_results.append(tanloss_result)
        plot_powerdeploss_fitting(pdloss, tanloss_result, title=cav_label, output_fd=f"{tanloss_folder}" )


sample_tanloss = pd.concat(tanloss_results)
save_tanloss( sample_tanloss, f"{tanloss_folder}/tan_loss.csv")
# plot_df( sample_tanloss, f"{sample_name}/results/tan_loss")


## After assignment each cavity, get foward analysis
assignment = pd.read_json(f"{raw_data_fd}/assignment.json")

collected_q_list = []
sample_result = []

# for fn in check_file_extension( power_dep_folder, "csv"):
## Collect assigned cavity
for cav_label in assignment["measurement_label"].values:
    file_name = f"{power_dep_folder}/{cav_label}.csv"
    cavity_result = pd.read_csv( file_name )
    if len(cavity_result.index)>0:
        cavity_result.Name = cav_label
        sample_result.append(cavity_result)
    
        ## Find low power Q
        collected_q = pd.DataFrame()
        lpq = find_row(file_name, "photons", 0.1)
        collected_q["photons_hp"] = lpq["photons"]
        loss_lp = 1/lpq["Qi_dia_corr"].to_numpy()
        loss_lp_err = loss_lp*lpq["Qi_dia_corr_err"].to_numpy()*loss_lp
        collected_q["loss_lp"] = loss_lp
        collected_q["loss_lp_err"] = loss_lp_err

        hpq = find_row(file_name, "photons", 1e5)
        collected_q["photons_hp"] = hpq["photons"]
        loss_hp = 1/hpq["Qi_dia_corr"].to_numpy()
        loss_hp_err = loss_hp*hpq["Qi_dia_corr_err"].to_numpy()*loss_hp
        collected_q["loss_hp"] = loss_hp
        collected_q["loss_hp_err"] = loss_hp_err

        collected_q["loss_diff"] = loss_lp-loss_hp
        collected_q["fr"] = hpq["fr"]

        collected_q["measurement_label"] = cav_label
        collected_q_list.append( collected_q )
    else:
        print(f"No data in {cav_label}")


plot_multiCav_powerQ(sample_result, sample_name, assignment, output=power_dep_folder)
collected_q_result = pd.concat(collected_q_list)

sample_statistic = pd.merge(collected_q_result, assignment, on="measurement_label")

sample_statistic = pd.merge(sample_statistic, sample_tanloss, on="measurement_label")
sample_statistic["fr"] = sample_statistic["fr"]/1e9
# print(sample_statistic)

# Plot tan loss model result
xy_cols = [
    ("center_linewidth","loss_diff",None),
    ("center_linewidth","A_TLS","A_TLS_err"),
    ("center_linewidth","const","const_err"),
    ("center_linewidth","nc","nc_err")
    ]
xy_labels = [
    ("Center Linewidth (um)","Loss difference"),
    ("Center Linewidth (um)","TLS Loss"),
    ("Center Linewidth (um)","Const Loss"),
    ("Center Linewidth (um)","nc")
    ]
file_names = ["lw_Q","A_TLS","const","nc"]
plot_list = assemble_plot_df( sample_statistic, xy_cols )
for i, p in enumerate(plot_list):
    fig = plt.figure(facecolor='white')
    axObj = fig.add_subplot()
    axObj.set_title(sample_name)
    axObj.set_xlabel(xy_labels[i][0])
    axObj.set_ylabel(xy_labels[i][1])

    plot_basic(p, axObj=axObj)
    plt.savefig(f"{result_folder}/clw/{file_names[i]}")
    plt.close()
# plot_df(sample_statistic, ("fr","Qi_dia_corr","Qi_dia_corr_err",None), log_scale=(False,True), title=("","Photons","Internal Q"), output=f"{power_dep_folder}/fr_Q" )
# plot_df(sample_statistic, ("center_linewidth","Qi_dia_corr","Qi_dia_corr_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","Internal Q"), output=f"{result_folder}/clw/lw_Q")
# plot_df(sample_statistic, ("center_linewidth","A_TLS","A_TLS_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","TLS Loss"), output=f"{result_folder}/clw/A_TLS")
# plot_df(sample_statistic, ("center_linewidth","const","const_err",None), log_scale=(True,True), title=("","Center Linewidth (um))","Const Loss"), output=f"{result_folder}/clw/const" )
# plot_df(sample_statistic, ("center_linewidth","nc","nc_err",None), log_scale=(True,True), title=("","Center Linewidth (um)","nc"), output=f"{result_folder}/clw/nc" )
