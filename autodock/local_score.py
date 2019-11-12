import re
import os
import subprocess

filenames = os.listdir()

filenames = os.listdir(path)
def runcmd(command):
    ret = subprocess.run(command)
    if ret.returncode == 0:
        print("success: ",ret)
    else:
        print("error: ",ret)

protein = []
ligand = []
for i in filenames:
    x = re.search('protein.pdbqt',i)
    y = re.search('ligand.pdbqt',i)
    if x:
        protein.append(i)
    elif y:
        ligand.append(i)
    else:
        continue

index = 1
for i in protein:
    for j in ligand:
        if re.search(i[:4],j):
            print(f"--------------NO.{index}-------------------")
            print("---------------生成打分文件-----------------")
            command = (["pythonsh",
            "/home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_gpf4.py",
            "-r",f"{i}","-l",f"{j}"])
            runcmd(command)
    index += 1