'''
Created on Dec 13, 2019

@author: xieqin
@mail: 987671584@qq.com
'''
# single protein and single ligand docking

import re
import os
import getopt
import sys
import subprocess

def usage():
    "Print helpful, accurate usage statement to stdout."
    print("Usage: autodock_single.py -l <file> -r <file> -s 'npts=num,num,num' -c '-y' -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/")

    print("     [-l]      ligand          file")
    print("     [-r]      protein         file")
    print("     [-s]      size            'npts=60,60,66'")
    print("     [-c]      gridcenter      center grids on center of ligand: '-y' OR center grids on coordinate: 'gridcenter=2.5,6.5,-7.5'")
    print("     [-p]      path_pre        AutodockTools' path")


def getArgs():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:r:s:c:p:h", ["help"])
    except getopt.GetoptError as err:
        print (str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    receptor = ligands = None
    parameters = []

    for o, a in opts:
        if o in ("-l", "--ligands"):
            ligFile = a   
        elif o in ("-r", "--receptor"):
            proFile = a
        elif o in ("-s", "--size"):
            size = a  
        elif o in ("-c", "--center"):
            center = a
        elif o in ("-p", "--path"):
            path_pre = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "Unrecognized option"
			
    return (ligFile, proFile, size, center, path_pre)    

if __name__ == '__main__':
    (ligFile, proFile, size, center, path_pre)=getArgs()

def runcmd(command):
    ret = subprocess.run(command)
    if ret.returncode == 0:
        print("success: ",ret)
    else:
        print("error: ",ret)

res_path = 'result'
if not os.path.exists(res_path):
    os.mkdir(res_path)
proname = proFile.split('.')[0]
ligname = ligFile.split('.')[0]


# Convert protein file format to pdbqt
print(f'\n--------------- deal with {proFile} --------------\n')
command = (['pythonsh', f"{path_pre}prepare_receptor4.py",
            '-r',proFile,
            '-o',f'{proname}.pdbqt',
            '-A','hydrogens',
            '-U','nphs'])
runcmd(command)

# Convert ligand file format to pdbqt
print(f'\n--------------- deal with {ligFile} --------------\n')
command2 = (['pythonsh', f"{path_pre}prepare_ligand4.py",
            '-l',ligFile,
            '-o',f'{ligname}.pdbqt',
            '-A','hydrogens'])
runcmd(command2)

# generate gpf file
print("\n--------------- generate gpf -----------------\n")

if center == '-y':
    command3 = (["pythonsh",f'{path_pre}prepare_gpf4.py',
                 "-l", f'{ligname}.pdbqt', 
                 "-r", f'{proname}.pdbqt',            
                 "-y", "-n",
                 "-p", size,
                 "-o", f'{proname}_{ligname}.gpf'])
else:
    command3 = (["pythonsh",f'{path_pre}prepare_gpf4.py',
                 "-l", f'{ligname}.pdbqt', 
                 "-r", f'{proname}.pdbqt',
                 "-p", center,
                 "-p", size,
                 "-o", f'{proname}_{ligname}.gpf'])
runcmd(command3)

# generate dpf file
print("\n--------------- generate dpf -----------------\n")

command4 = (["pythonsh",f'{path_pre}prepare_dpf4.py',
            "-l", f'{ligname}.pdbqt', 
            "-r", f'{proname}.pdbqt',
            "-o", f'{proname}_{ligname}.dpf'])
runcmd(command4)

# autogrid
print("\n---------------autogrid-----------------\n")
command5 = (["autogrid4",
             "-p",f'{proname}_{ligname}.gpf',
             "-l",f'{proname}_{ligname}.glg'])
runcmd(command5)

# autodock
print("\n---------------autodock-----------------\n")
command6 = (["autodock4",
             "-p",f'{proname}_{ligname}.dpf',
             "-l",f'{res_path}/{proname}_{ligname}.dlg'])
runcmd(command6)

# result post-process
modelFlag = False 
modelFlag_sco = False
modelRe=re.compile("DOCKED: MODEL")
stmodelRe=re.compile("DOCKED: REMARK")
endModelRe=re.compile("DOCKED: ENDMDL")
scoModelRe=re.compile("DOCKED: USER    Estimated Free Energy of Binding")
    
def pdbqt_write(line):
    fh_pdbqt.write(f'{line[8:]}')

fh_txt = open(f"{res_path}/{proname}_{ligname}.txt",'w')
fh_pdbqt = open(f"{res_path}/{proname}_{ligname}.pdbqt",'w')
names = []
scores = [] 
with open(f'{res_path}/{proname}_{ligname}.dlg','r') as fh:
    allLines = fh.readlines()
for line in allLines:
    if re.search(modelRe,line):
        a = line.split()                    
        names.append(a[-1])
        pdbqt_write(line)

    if re.search(scoModelRe,line):
        a = line.split()
        scores.append(a[-3])
        pdbqt_write(line)

    if re.search(stmodelRe,line):
        modelFlag = True
    
    if modelFlag:
        pdbqt_write(line)

    if re.search(endModelRe,line):
        modelFlag=False
dicts = dict(zip(names,scores))
for name,score in dicts.items():
    fh_txt.write(f'{name}     {score}\n')

if not os.path.exists('map'):
    os.mkdir('map')
subprocess.call('mv *.map* map',shell=True)
print('\n------ Store map in map folder --------\n')
print('\n------ Store results in result folder ------')