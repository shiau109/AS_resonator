
from resonator_as.ultility.file_structure import *
from resonator_as.ultility.io_translator import *
# from analysis.analysis_method import *
from resonator_as.analysis.plot_method import *
import os
import json
# 1. Sample path setting
sample_name = "ITRI_343Chip1"
project_folder = r"D:\Data\resonator"   # empty string "" for relative path 

# 1.1 File structure setting
sample_root = f"{project_folder}/{sample_name}"
raw_data_fd = f"{sample_root}/raw"
result_folder = f"{project_folder}/{sample_name}/results"

fit_folder = f"{result_folder}/power_dep_fit"

check_configure(f"{sample_root}", ["power_dep_fit"])


# subgroup_struc = check_subgroup(mat_files)

# each cavity file(mat file)
from resonator_as.analysis.photon_dep import PhotonDepResonator 
all_resonator_result = []
folder_list = [d for d in os.listdir(raw_data_fd) if os.path.isdir(os.path.join(raw_data_fd, d))]

for cav_label in folder_list:
    create_subfolder(fit_folder,cav_label)
    result_folder = f"{fit_folder}/{cav_label}"

    resonator_data_folder = f"{raw_data_fd}/{cav_label}"
    resonator = PhotonDepResonator(cav_label)
    # Find cavity data (mat file) in the folder
    mat_files = check_file_extension( resonator_data_folder, "mat")
    df_config = pd.read_json(f'{resonator_data_folder}/config.json')
    for index, row in df_config.iterrows():
        attenuation = row["attenuation"]
        file_name = row["file_name"]
        print(f"{file_name} with {attenuation} dB attenuation")
        resonator.import_mat(f"{resonator_data_folder}/{file_name}",attenuation)
    result = resonator.refined_analysis( result_folder )
    all_resonator_result.append( result )
    
    df_results = pd.concat(all_resonator_result)
    df_results.Name = cav_label

    # Plotting
    df_powerQ_free = pd.read_csv( f"{fit_folder}/{cav_label}/free_result.csv" )
    plot_singleRes_powerQ_free(df_powerQ_free, cav_label=f"{cav_label}", output_fd=result_folder)
    plot_singleRes_powerloss_free(df_powerQ_free, cav_label=f"{cav_label}", output_fd=result_folder)

    df_powerQ_refined = pd.read_csv( f"{fit_folder}/{cav_label}/refined_result.csv" )
    plot_singleRes_powerQ_refined(df_powerQ_refined, cav_label=f"{cav_label}", output_fd=result_folder)
    plot_singleRes_powerloss_refined(df_powerQ_refined, cav_label=f"{cav_label}", output_fd=result_folder)


## After assignment each cavity, get foward analysis
assignment = pd.read_json(f"{raw_data_fd}/assignment.json")
plot_multiRes_powerQ_free( fit_folder, assignment, fit_folder)
plot_multiRes_powerQ_refined( fit_folder, assignment, fit_folder)

