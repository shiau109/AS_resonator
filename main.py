from file_structure import *
from fitting_method import *
from plot_method import *
sample_name = "88v1"

check_configure(sample_name, ["power", "tan_loss"])
raw_data_path = f"{sample_name}/raw"
for fn in check_file_extension( raw_data_path, "mat"):
    print(fn)
    results = mat_file_analysis(f"{raw_data_path}/{fn}", "power", f"{sample_name}/results/power")
    plot_powerQ(results, sample_name, fn, f"{sample_name}/results/power", "save")
    
for fn in check_file_extension( f"{sample_name}/results/power", "csv"):
    print(fn)