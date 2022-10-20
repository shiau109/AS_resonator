from os import listdir,makedirs
from shutil import rmtree
from os.path import isfile, join,exists


def check_configure( sample_fdname, subfd_names ):
    rawdata_folder = f"{sample_fdname}/raw"
    result_folder = f"{sample_fdname}/results"



    if not exists(result_folder):
        makedirs(result_folder)
        print("Create results Directory!")
    else:
        print("Results Directory Exist, Keep going!")

    for subfd in subfd_names:
        subfd = f"{result_folder}/{subfd}"
        if not exists(subfd):
            makedirs(subfd)
            print(f"Create subfolder {subfd} in result!")
        else:
            cover = input("This sample has a record, overwrite it or not (y/n): ")
            if cover.lower() == "y" or cover.lower() == "yes":
                rmtree(subfd)
                makedirs(subfd)
                print(f"Subfolder {subfd}  this sample renew!")
            else:
                print(f"Results for this sample Exist!")

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