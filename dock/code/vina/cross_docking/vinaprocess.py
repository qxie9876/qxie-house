import re
import os
import getopt
import sys

def usage():
    "Print helpful, accurate usage statement to stdout."
    print("Usage: vinaprocess.py -d <dir>")
    print("     [-d]      vina_pdbqt_path        <vina_pdbqt>")

def getArgs():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h", ["help"])
    except getopt.GetoptError as err:
        print (str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-d", "--dir"):
            vina_pdbqt_path = a   
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            assert False, "Unrecognized option"			
    return vina_pdbqt_path

if __name__ == '__main__':
    vina_pdbqt_path=getArgs()


vina_first_conf_path = 'vina_first_conf'
if not os.path.exists(vina_first_conf_path):
    os.mkdir(vina_first_conf_path)
# vina post-process
print("\n---------------- vina post-process --------------\n")
modelRe=re.compile("^MODEL 1$")
endModelRe=re.compile("^ENDMDL")
scoModelRe=re.compile("REMARK VINA RESULT:")

indexs = []
scores = []
modelFlag = False
for lig_vina in os.listdir(vina_pdbqt_path):
    ligVinaName = lig_vina.split('.')[0]
    fh_pdbqt = open(f'{vina_first_conf_path}/{lig_vina}','w')
    with open(f'{vina_pdbqt_path}/{lig_vina}','r') as fh:
        allLines = fh.readlines()
        indexs.append(ligVinaName)
        for line in allLines:
            # first conformation score
            if re.search(modelRe,line):
                modelFlag=True
            if re.search(scoModelRe,line):
                a = line.split()
                scores.append(a[3])
            if modelFlag:
                fh_pdbqt.write(line)
            if re.search(endModelRe,line):
                modelFlag=False

dicts = dict(zip(indexs,scores))
dicts2 = sorted(dicts.items(), key=lambda x: float(x[1]))
fh_score = open(f'first_score.txt','w')
for i in dicts2:
    fh_score.write(f'{i[0]}       {i[1]}\n')

print("\n--------- OVER ---------")
print('\n----- Store first conformation in vina_first_conf folder -------')
print('\n----- first confomation score store in first_score.txt file -------')
