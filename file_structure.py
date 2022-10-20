from os import listdir,makedirs
from shutil import rmtree
from os.path import isfile, join,exists


def check_configure( sample_name ):

    result_folder = f"{fdName}/Results"
    result_folder_sample = result_folder+"/"+sample_name
    fig_dir_sample = result_folder+"/Figure/"+sample_name
    para_dir_sample = result_folder+"/fit_paras/"+sample_name

    goingon = 0

    if not exists(result_folder):
        makedirs(result_folder)
        print("Results Directory created!")
    else:
        print("Results Directory Exist Keep going!")


    if not exists(result_folder_sample):
        makedirs(result_folder_sample)
        print("Results Directory for this sample created!")
        goingon += 1
    else:
        cover = input("This sample has a record, overwrite it or not (y/n): ")
        if cover.lower() == "y" or cover.lower() == "yes":
            rmtree(result_folder_sample)
            rmtree(fig_dir_sample)
            rmtree(para_dir_sample)
            makedirs(result_folder_sample)
            print("Results Directory for this sample renew!")
            goingon += 1
        else:
            print("Results for this sample Exist!")

def check_file_extension( fd_name:str, file_ext:str ):
    """
    return a list of file name with specific file extension
    arg:
        fd_name : searched folder
        file_ext :  Filename Extension
    """
    filename_list = []
    for f in listdir(fd_name):
        if len(f.split(".")) == 2 and f.split(".")[1] == file_ext and isfile(join(fd_name, f)):
            filename_list.append(f)
    return filename_list