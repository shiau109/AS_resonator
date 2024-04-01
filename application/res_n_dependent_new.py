
from resonator_as.ultility.file_structure import *
from resonator_as.ultility.io_translator import *
# from analysis.analysis_method import *
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

# Find cavity data (mat file) in the folder "raw_data_fd"
mat_files = check_file_extension( raw_data_fd, "mat")
subgroup_struc = check_subgroup(mat_files)

# each cavity file(mat file)
from resonator_as.analysis.photon_dep import PhotonDepResonator 
all_resonator_result = []
for cav_label, flist in subgroup_struc.items():
    create_subfolder(power_dep_folder,cav_label)
    resonator = PhotonDepResonator(cav_label)
    for fn in flist:
        resonator.import_mat(f"{raw_data_fd}/{fn}",105)
    result = resonator.do_analysis( f"{power_dep_folder}/{cav_label}" )
    all_resonator_result.append( result )
    
    df_results = pd.concat(all_resonator_result)
    df_results.Name = cav_label
    ## Save result
    # save_power_dep(df_results, f"{power_dep_folder}/{cav_label}.csv")
    # Plotting
    # plot_power_dependent_Q(df_results, cav_label=f"{cav_label}", output_fd=power_dep_folder)


## After assignment each cavity, get foward analysis
assignment = pd.read_json(f"{raw_data_fd}/assignment.json")

collected_q_list = []
sample_result = []

# for fn in check_file_extension( power_dep_folder, "csv"):
## Collect assigned cavity
# for cav_label in assignment["measurement_label"].values:
#     file_name_free = f"{power_dep_folder}/{cav_label}.csv"
#     cavity_result = pd.read_csv( file_name_free )
#     if len(cavity_result.index)>0:
#         cavity_result.Name = cav_label
#         sample_result.append(cavity_result)
#     else:
#         print(f"No data in {cav_label}")
# plot_multiCav_powerQ(sample_result, f"{sample_name}", assignment, output=power_dep_folder)
