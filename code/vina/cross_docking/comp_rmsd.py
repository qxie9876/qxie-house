import re
import os
import subprocess
import getopt
import sys
# import seaborn as sns
# from matplotlib import pyplot as plt
# import pandas as pd

def usage():
    "Print helpful, accurate usage statement to stdout."
    print("Usage: comp_rmsd.py -f <dir> -s <dir> -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/")
    print("     [-f]      first_pdbqt_path        <first_pdbqt>")
    print("     [-s]      second_pdbqt_path       <second_pdbqt>")
    print("     [-p]      AutodockTools' path")

def getArgs():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:s:p:h", ["help"])
    except getopt.GetoptError as err:
        print (str(err)) 
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-f", "--first_pdbqt"):
            first_path = a   
        elif o in ("-s", "--second_pdbqt"):
            second_path = a   
        elif o in ("-p", "--path_pre"):
            path_pre = a   
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "Unrecognized option"			
    return first_path, second_path, path_pre

if __name__ == '__main__':
    (first_path, second_path, path_pre)=getArgs()

# pdbqt format compute rmsd
def runcmd(command):
    ret = subprocess.run(command)
    if ret.returncode == 0:
        print('success: ',ret)
    else:
        print('error: ',ret)

rmsd_path = 'rmsd.txt'
pictures_path = 'results_matrix'

subprocess.call(f'mkdir {pictures_path}',shell=True)

f_confs = []
s_confs = []
df_names = []
for first in os.listdir(first_path):
    for second in os.listdir(second_path):
        #print(first)
        #print(second)
        x = re.compile('(?<=_)[0-9].*?(?=\.)')
        y = re.findall(x,first)
        #print(y)
        if len(y) != 0:

            if re.search(y[0], second):
                f_confs.append(first)
                print(f_confs)
                s_confs.append(second)
                a = first.split('.')
                df_names.append(a[0])
            else:
                continue
        else:
            pass
#print(len(f_confs))
dicts = dict(zip(f_confs,s_confs))

index_rmsd = 1
for f_conf,s_conf in dicts.items():
    print(f'\n---------NO.{index_rmsd}---------\n')
    command = (['pythonsh',
                f"{path_pre}compute_rms_between_conformations.py",
                "-f",f"{first_path}/{f_conf}",
                "-s",f"{second_path}/{s_conf}",
                "-o","rmsd.txt"])
    runcmd(command)
    index_rmsd += 1

# def sear_name(string):
#     x1 = re.compile('(?<=/).*?(?=_[0-9])')
#     x2 = re.compile('(?<=_)[0-9].*?(?=\.)')
#     f_name = re.findall(x1, string)
#     s_name = re.findall(x2, string)
#     return f_name[0], s_name[0]
# names = []
# rmsds = []
# with open(rmsd_path,'r') as fh:
#     allLines = fh.readlines()[1:]
# for line in allLines:
#     a = line.split() 
#     f_name, s_name = sear_name(a[0])
#     name_ls = [f_name,s_name]
#     name = '@'.join(name_ls)
#     rmsd = a[-1]
#     names.append(name)
#     rmsds.append(rmsd)

# pro_ls = []
# lig_ls = []
# for name in names:
#     x = re.compile('.*(?=@)')
#     y = re.compile('(?<=@).*')
#     pro = re.findall(x,name)
#     lig = re.findall(y,name)
#     pro_ls.append(pro[0])
#     lig_ls.append(lig[0])
# dicts_rmsd = dict(zip(names,rmsds))
# df_non = pd.DataFrame(columns=set(lig_ls), index=set(pro_ls))

# for name, rmsd in dicts_rmsd.items():
#     print(name)
#     x = re.compile('.*(?=@)')
#     y = re.compile('(?<=@).*')
#     pro = re.findall(x,name)
#     lig = re.findall(y,name)
#     df_non.loc[pro[0],lig[0]] = float(rmsd)

# #print(df_non)
# df_non.to_csv('result.csv')
# df = pd.read_csv('result.csv',index_col=0)

# #print(df)
# ax = sns.heatmap(df,
#                  annot=True,
#                  vmin=0,vmax=7,
#                  cmap=plt.cm.Blues,
#                  fmt='.4f',
#                  cbar=True,
#                  square=True)
# plt.xlabel('Ligand')
# plt.ylabel('Protein')
# plt.title('Cross Docking Rmsd Matrix')
# plt.savefig(f'results_pictures.jpg')
