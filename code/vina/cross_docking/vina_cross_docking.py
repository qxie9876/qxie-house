'''
Created on Dec 20, 2019

@author: xieqin
@mail: 987671584@qq.com
'''
# 需要将所有的蛋白及小分子叠合后进行cross-docking(pymol)
# self_cross_docking
# 为了验证蛋白的稳定性，用以选择对接的蛋白
# 生成了蛋白小分子RMSD矩阵，可根据横行判断蛋白的稳定性
# 横：蛋白口袋的容忍
# 纵：小分子对蛋白的容忍
# 通过autodock以配体为中心，生成gpf文件以生成center中心
# 需要在ligand中存配体小分子，在protein文件夹中存受体蛋白
# 请将蛋白和所要对接的小分子的名称一一对应，例如:1a30.mol2, 1a30.mol2

import re
import os
import subprocess
import getopt
import sys

def usage():
    "Print helpful, accurate usage statement to stdout."
    print("Usage: cross_docking.py -r <dir> -l <dir> -s 'num,num,num' -e num -n num -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/")

    print("	Optional parameters:")
    print("     [-r]         receptor         dir *.mol2")
    print("     [-l]         ligand           dir *.mol2")
    print("     [-s]         size             'x, y, z'")
    print("     [-e]         exhaustiveness    num")
    print("     [-n]         maxinum number of binding modes to generate")
    print("     [-p]         AutodockTools' path")
    print("     [-h]         print command usage")

def getArgs():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:l:s:e:n:p:h", ["help"])
    except getopt.GetoptError as err:
	# print help information and exit:
        print (str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
		
    for o, a in opts:

        if o in ("-r", "--receptor_dir"):
            pro_path = a		
        elif o in ("-l", "--ligand_dir"):
            lig_path = a	
        elif o in ("-s", "--size"):
            size = a		
        elif o in ("-e", "--exhaustiveness"):
            exhaustiveness = a	
        elif o in ("-n", "--num_modes"):
            num_modes = a
        elif o in ("-p", "--path_pre"):
            path_pre = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "Unrecognized option"
			
    return (pro_path, lig_path, size, exhaustiveness, num_modes, path_pre)    

if __name__ == '__main__':
    (pro_path, lig_path, size, exhaustiveness, num_modes, path_pre)=getArgs()

size = size.split(",")

# 生成所需文件夹
pro_pdbqt_path = 'pro_pdbqt'
lig_pdbqt_path = 'lig_pdbqt'
gpf_path = 'gpf'
vina_txt_path = 'vina_txt'
vina_pdbqt_path = 'vina_pdbqt'

dirs = [pro_pdbqt_path, lig_pdbqt_path, gpf_path,
        vina_txt_path, vina_pdbqt_path]

for i in dirs:
    if not os.path.exists(i):
        os.mkdir(i)

def runcmd(command):
    ret = subprocess.run(command)
    if ret.returncode == 0:
        print('success: ',ret)
    else:
        print('error: ',ret)

def pro_prepared(pro,proname):
    command = (['pythonsh',
                f"{path_pre}prepare_receptor4.py",
                '-r',f'{pro_path}/{pro}',
                '-o',f'{pro_pdbqt_path}/{proname}.pdbqt',
                '-A','hydrogens',
                '-U','nphs'])
    runcmd(command)
def lig_prepared(lig,ligname):
    command = (['pythonsh',
                f"{path_pre}prepare_ligand4.py",
                '-l',f'{lig_path}/{lig}',
                '-o',f'{lig_pdbqt_path}/{ligname}.pdbqt',
                '-A','hydrogens'])
    runcmd(command)

def generate_gpf(lig, ligname, pro, proname):
    command =  (["pythonsh",
                f"{path_pre}prepare_gpf4.py",
                "-l",f"{lig_pdbqt_path}/{lig}",
                "-r",f"{pro_pdbqt_path}/{pro}",
                "-o",f"{gpf_path}/{proname}@{ligname}.gpf",
                "-y","-n","-p","npts=27,27,27"])
    runcmd(command)

def generate_center(gpf):
    with open(f"{gpf_path}/{gpf}",'r') as fh:
        allLines = fh.readlines()
        for line in allLines:
            if re.search("gridcenter",line):
                center = line.split()
                center_x = center[1]
                center_y = center[2]
                center_z = center[3]
    return center_x, center_y, center_z

def vina_dock(proname,ligname,center_x,center_y,center_z):
    command = (["vina",
                "--receptor", f"{pro_pdbqt_path}/{proname}.pdbqt",
                "--ligand", f"{lig_pdbqt_path}/{ligname}.pdbqt",
                "--center_x", center_x,
                "--center_y", center_y,
                "--center_z", center_z,
                "--size_x", size[0],
                "--size_y", size[1],
                "--size_z", size[2],
                "--exhaustiveness",exhaustiveness,
                "--num_modes", num_modes,
                "--out", f"{vina_pdbqt_path}/{proname}_{ligname}.pdbqt",
                "--log", f"{vina_txt_path}/{proname}_{ligname}.txt"])
    runcmd(command)    

index_pro = 1
for pro in os.listdir(pro_path):
    print(f'----------NO.{index_pro}--------\n')
    proname = pro.split('.')[0]
    pro_prepared(pro,proname)    
    index_pro += 1

index_lig = 1
for lig in os.listdir(lig_path):
    print(f'\n-------- NO.{index_lig} -------\n')
    ligname = lig.split('.')[0]
    lig_prepared(lig,ligname)   
    index_lig += 1

index_dpf = 1
for pro in os.listdir(pro_pdbqt_path):
    for lig in os.listdir(lig_pdbqt_path):
        print(f'\n------ NO.{index_dpf} ------\n')
        proname = pro.split('.')[0]
        ligname = lig.split('.')[0]
        generate_gpf(lig,ligname,pro,proname)
        index_dpf += 1  
print('\n---------- GENERATE gpf OVER-----------')
                
# vina对接
index_vina = 1
for gpf in os.listdir(gpf_path):
    print(f'\n------ NO.{index_vina} vina  --------\n')
    x = re.compile('.*(?=@)')
    y = re.compile('(?<=@).*(?=\.)')
    proname = re.findall(x,gpf)
    ligname = re.findall(y,gpf)
    center_x, center_y, center_z = generate_center(gpf)
    vina_dock(proname[0],ligname[0],center_x,center_y,center_z)
    index_vina += 1
print('\n--------- Vina OVER -----------')
