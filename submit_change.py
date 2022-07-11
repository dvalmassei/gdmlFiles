import sys
import os
import subprocess
import time

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

sourceDir = "/work/halla/moller12gev/dvalmass/qsim-gdml/build"
config = "LAM_2.2_c_30mm_d2_18mm_07062022_001"
generator = "beam"

runrange= range(int(sys.argv[1]),int(sys.argv[2]))

outDir="/lustre19/expphy/volatile/halla/moller12gev/dvalmass/sim_out/"+config
jobs=outDir+"/jobs"

if not os.path.exists(outDir):
  os.system("mkdir "+outDir)
if not os.path.exists(jobs):
  os.system("mkdir "+jobs)

runjobs = sourceDir + "/macros/jobs"

if not os.path.exists(runjobs):
  os.system("mkdir "+runjobs)

for i in runrange:
  jsubf=open(runjobs + "/test_"+str(i)+".mac","w")
  jsubf.write("#/qsim/fDetMode 2\n")
  jsubf.write("#/qsim/fQMode 1\n")
  jsubf.write("#/qsim/fStandMode 0\n")
  jsubf.write("/qsim/fSourceMode 1\n")
  jsubf.write("#/qsim/fQuartzPolish 0.975\n")
  jsubf.write("#/qsim/fDetAngle 0 deg\n")
  jsubf.write("#/qsim/fDetPosX 0 cm\n")
  jsubf.write("#/qsim/fDetPosY 0 cm\n")
  jsubf.write("/run/initialize\n")
  jsubf.write("/qsim/filename "+outDir+"/test_"+str(i)+".root\n")
  #jsubf.write("/qsim/seed 50\n")
  jsubf.write("/qsim/emin   1.313 GeV\n")
  jsubf.write("/qsim/emax   1.313 GeV\n")
  jsubf.write("/gun/particle e-\n")
  jsubf.write("/run/beamOn 10000\n")


for i in runrange:
  offset = 10*i
  #outfile=outDir+"/test_"+generator+"_"+str(i)+".root"
  jsubf=open(jobs+"/test_"+str(i)+".sh", "w")
  jsubf.write("#!/bin/bash\n")
  jsubf.write("#SBATCH --account=halla\n")
  jsubf.write("#SBATCH --partition=production\n")
  jsubf.write("#SBATCH --job-name=TEST\n")
  jsubf.write("#SBATCH --time=00:40:00\n")
  jsubf.write("#SBATCH --nodes=1\n")
  jsubf.write("#SBATCH --ntasks=1\n")
  jsubf.write("#SBATCH --cpus-per-task=1\n")
  jsubf.write("#SBATCH --mem=2G\n")
  jsubf.write("tcsh -c \"source /apps/root/6.18.00/setroot_CUE\"\n")
  jsubf.write("cd "+sourceDir+"\n")
  jsubf.write("echo \"Current working directory is `pwd`\"\n")
  replace_line("LAM_2.2.gdml", 20, "  <constant name=\"offset\" value=\"" +str(offset)+ "\" /> \n")
  jsubf.write("./qsim gdmlfiles/LAM_2.2.gdml "+runjobs+"/test_"+str(i)+".mac" +"\n")
  print("sbatch "+jobs+"/test_"+str(i)+".sh")
                                                                                  1,3           Top
