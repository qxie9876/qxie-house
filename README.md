# autodock
预先配置vina, autodock, rdock, smina和mgltools中pythonsh的环境
Linux操作系统，python3环境

1. autodock
 autodock_single.py 单分子单蛋白对接

 运行脚本 autodock_single.py -l <file> -r <file> -s 'npts=num,num,num' -c '-y'\
 -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/

2. smina
 smina.py 可用于单蛋白与多分子对接，蛋白格式pdbqt, 小分子存于一个文件中(mol2,pdb,sd)

 运行脚本 smina.py -l <file> -r <file.pdbqt> -c 'num,num,num' -s 'num,num,num' -e num -n num

3. rdock（rigid dock）
 rdock.py 可用于单蛋白与多分子对接，蛋白格式mol2, 小分子存于一个文件中(sd)
 运行脚本 vina_screening.py -l <file.sd> -r <file.mol2> -n 50

4. vina

(1) vina_single.py 单分子单蛋白对接

 运行脚本 vina_single.py -l <file> -r <file> -c 'num,num,num' -s 'num,num,num' -e num -n num\ 
  -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/

(2) vina_small_batch.py 单蛋白多分子对接,蛋白为mol2格式，小分子存于一个mol2文件中

 运行脚本 vina_small_batch.py -l <file.mol2> -r <file.mol2> -c 'num,num,num' -s 'num,num,num'\
  -e num -n num -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/

(3) vina_cross_docking.py 需要蛋白和小分子两个文件夹

 运行脚本 cross_docking.py -r <dir> -l <dir> -s 'num,num,num' -e num -n num\
 -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24

(4) vinaprocess.py 对脚本2和脚本3 vina对接的结果进行处理，生成打分第一的构象及打分的txt文档

 运行脚本 cross_docking.py -r <dir> -l <dir> -s 'num,num,num' -e num -n num\
 -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24

(5) comp_rmsd.py 计算cross_docking的对接结果中打分第一的构象与对接前小分子rmsd值

 运行脚本 comp_rmsd.py -f <dir> -s <dir>\
 -p /home/qxie/softwares/mgltools_1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24

(6) crossDockProcess.py 将cross_docking的结果生成矩阵热图(此脚本需要seaborn包)
 运行脚本 crossDockProcess.py -r rmsd.txt
