'''
Created on Dec 13, 2019

@author: xieqin
@mail: 987671584@qq.com
'''
# more than 100 thousands moleculars docking
import re
import os
import getopt
import sys
import subprocess

def usage():
    "Print helpful, accurate usage statement to stdout."
    print("Usage: vina_small_batch.py -l <file.mol2> -r <file.mol2> -c 'num,num,num' -s 'num,num,num' -e num -n num -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/")

    print("	Optional parameters:")
    print("     [-l]         ligands          *.mol2 file")
    print("     [-r]         protein          *.mol2 file")
    print("     [-c]         center           'x, y, z'")
    print("     [-s]         size             'x, y, z'")
    print("     [-e]         exhaustiveness   num")
    print("     [-n]         maxinum number of binding modes to generate")
    print("     [-p]         AutodockTools' path")
    print("     [-h]         print command usage")

def getArgs():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:r:c:s:e:n:p:h", ["help"])
    except getopt.GetoptError as err:
	# print help information and exit:
        print (str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
		
    for o, a in opts:
        if o in ("-l", "--ligands"):
            ligFile = a   
        elif o in ("-r", "--receptor"):
            proFile = a 	
        elif o in ("-c", "--center"):
            center = a
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
			
    return (ligFile, proFile, center, size, exhaustiveness, num_modes, path_pre)    

if __name__ == '__main__':
    (ligFile, proFile, center, size, exhaustiveness, num_modes, path_pre)=getArgs()

def runcmd(command):
    ret = subprocess.run(command)
    if ret.returncode == 0:
        print('success: ',ret)
    else:
        print('error: ',ret)

def pro_prepared(pro,proname):
    command = (['pythonsh',
                f"{path_pre}prepare_receptor4.py",
                '-r',f'{pro}',
                '-o',f'{proname}.pdbqt',
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

def vina_dock(ligname):
    command = (["vina",
                "--receptor", f"{proname}.pdbqt",
                "--ligand", f"{lig_pdbqt_path}/{ligname}.pdbqt",
                "--center_x", center[0],
                "--center_y", center[1],
                "--center_z", center[2],
                "--size_x", size[0],
                "--size_y", size[1],
                "--size_z", size[2],
                "--exhaustiveness",exhaustiveness,
                "--num_modes", num_modes,
                "--out", f"{vina_pdbqt_path}/{ligname}.pdbqt",
                "--log", f"{vina_txt_path}/{ligname}.txt"])
    runcmd(command)        

center = center.split(",")
size = size.split(",")

lig_path = 'ligand'
lig_pdbqt_path = 'lig_pdbqt'
vina_txt_path = 'vina_txt'
vina_pdbqt_path = 'vina_pdbqt'

dirs = [lig_path, lig_pdbqt_path, 
        vina_txt_path, vina_pdbqt_path]
for i in dirs:
    if not os.path.exists(i):
        os.mkdir(i)

# split moleculers to N folders
index = 0
with open(ligFile,'r') as fh:
    ligname = ligFile.split('.')[0]
    allLines = fh.readlines()
    writeindex = 0
    for line in allLines:
        if re.search('@<TRIPOS>MOLECULE',line):
            index += 1
            fh2 = open(f'{lig_path}/{ligname}_{index}.mol2','w')
            if writeindex == 0 or 2:
                writeindex = 1
            else:
                writeindex = 0 or 2

        if writeindex == 1:
            fh2.write(line)
    fh2.close()  
print("\n-------- Split Mols OVER --------\n")

# Convert protein file format to pdbqt
print(f'\n--------- deal with {proFile} --------\n')
proname = proFile.split('.')[0]
pro_prepared(proFile,proname)

index = 1
file_index = 1
for lig in os.listdir(lig_path):
    print(f'\n---------vina start ----------')
    print(f'\n-------------NO.{index}-----------\n')
    ligname = lig.split('.')[0]
    lig_prepared(lig,ligname)    
    vina_dock(ligname)
    index += 1
