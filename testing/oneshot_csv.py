
import numpy as np
from matplotlib import pyplot as plt

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
from general.file_structure import *
from general.analysis_method import *
from general.plot_method import *
from general.format_trans import *


folder_name = r"C:\Users\shiau\OneDrive\Desktop\oneshot_test\ZI_SHFQC_DATA\ave_test"

mat_files = check_file_extension( folder_name, "csv")

# 2. Fit each cavity file(mat file)
tanloss_results = []
for file_name in mat_files:
    # file_name = r"iq_cloud_19_5_TWPA(p_dressed_22_92dBm_1us)_PURE"
    print(f"Open {folder_name}/{file_name}.csv")
    oneshot_data = pd.read_csv(f"{folder_name}/{file_name}.csv")

    print(oneshot_data.columns)
    plot_data = assemble_plot_df(oneshot_data,[('I_g_off','Q_g_off'),('I_e_off','Q_e_off'),('I_g_on','Q_g_on'),('I_e_on','Q_e_on')])
    plot_style = {
        "marker_style":"o",
        "marker_size":1,
    }
    fig = plt.figure(facecolor='white')
    plt.subplots_adjust(left=0.15,
                            bottom=0.15, 
                            right=0.9, 
                            top=0.9, 
                            wspace=0.25, 
                            hspace=0.25)
    gs = GridSpec(1,2)

    pa_off = fig.add_subplot(gs[0,0])
    pa_off.set_title(file_name)
    plot_style.update( {"legend_label":"off G"})
    plot_basic(plot_data[0],plot_style=plot_style,axObj=pa_off)
    plot_style.update( {"legend_label":"off E"})
    plot_basic(plot_data[1],plot_style=plot_style,axObj=pa_off)
    plt.legend()

    pa_on = fig.add_subplot(gs[0,1])
    plot_style.update( {"legend_label":"on G"})
    plot_basic(plot_data[2],plot_style=plot_style,axObj=pa_on)
    plot_style.update( {"legend_label":"on E"})
    plot_basic(plot_data[3],plot_style=plot_style,axObj=pa_on)
    plt.legend()
    # plt.show()

    ave_shot = pd.DataFrame()
    for col_name in oneshot_data.columns.to_list():
        print(col_name)
        
        raw_arr = oneshot_data[col_name].to_numpy()
        ave_shot[col_name] = np.mean(raw_arr.reshape(-1, 10), axis=1)
    # np.mean(arr.reshape(-1, 3), axis=1)
    plot_data = assemble_plot_df(ave_shot,[('I_g_off','Q_g_off'),('I_e_off','Q_e_off'),('I_g_on','Q_g_on'),('I_e_on','Q_e_on')])
    plot_style = {
        "marker_style":"o",
        "marker_size":1,
    }
    # fig = plt.figure(facecolor='white')
    # plt.subplots_adjust(left=0.15,
    #                         bottom=0.15, 
    #                         right=0.9, 
    #                         top=0.9, 
    #                         wspace=0.25, 
    #                         hspace=0.25)
    # gs = GridSpec(1,2)

    # pa_off = fig.add_subplot(gs[0,0])
    # pa_off.set_title(file_name)
    plot_style.update( {"legend_label":"ave off G"})
    plot_basic(plot_data[0],plot_style=plot_style,axObj=pa_off)
    plot_style.update( {"legend_label":"ave off E"})
    plot_basic(plot_data[1],plot_style=plot_style,axObj=pa_off)
    plt.legend()

    # pa_on = fig.add_subplot(gs[0,1])
    plot_style.update( {"legend_label":"ave on G"})
    plot_basic(plot_data[2],plot_style=plot_style,axObj=pa_on)
    plot_style.update( {"legend_label":"ave on E"})
    plot_basic(plot_data[3],plot_style=plot_style,axObj=pa_on)
    plt.legend()
    plt.show()
# x, y, iqdata_g = mat_to_numpy("testing/JPA67_fp1110_25.mat")



