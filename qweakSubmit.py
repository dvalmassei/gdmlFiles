import sys
import os
import subprocess
import time

sourceDir = "/w/halla-scshelf2102/moller12gev/dvalmass/QWeak/QwGeant4"
config = "Qweak_QtorAll_Oct0_04122023_001_"
generator = "beam"

runrange= range(int(sys.argv[1]),int(sys.argv[2]))

outDir="/lustre19/expphy/volatile/halla/moller12gev/dvalmass/QweakSim/"+config
jobs=outDir+"/jobs"

if not os.path.exists(outDir):
  os.system("mkdir "+outDir)
if not os.path.exists(jobs):
  os.system("mkdir "+jobs)

runjobs = sourceDir + "/batchMacros/jobs"

if not os.path.exists(runjobs):
  os.system("mkdir "+runjobs)

qtor = (150,300,450,600,750,900)

for i in runrange:
  jsubf=open(runjobs + "/test_" + str(qtor[i%6]) + "_" + config + str(i//6)+".mac","w")
  jsubf.write("/control/execute myQweakConfiguration.mac\n")
  jsubf.write("/control/execute macros/dvalmass_qtor.mac\n")
  jsubf.write("/TrackingAction/TrackingFlag 3\n")
  jsubf.write("/EventGen/SelectOctant 0\n")
  jsubf.write("/EventGen/SetBeamEnergy 887 MeV\n")
  jsubf.write("/MagneticField/SetActualCurrent "+ str(qtor[i%6]) +"\n")
  jsubf.write("/Analysis/RootFileName "+outDir + "/test_" + str(qtor[i%6]) + "_" + str(i//6) + ".root\n")
  jsubf.write("/run/verbose 0\n")
  jsubf.write("/tracking/verbose 0\n")
  jsubf.write("/run/beamOn 10000\n")

for i in runrange:
  #outfile=outDir+"/test_"+generator+"_"+str(i)+".root"
  jsubf=open(jobs + "/test_" + str(qtor[i%6]) + "_" + config + str(i//6)+ ".sh", "w")
  jsubf.write("#!/bin/bash\n")
  jsubf.write("#SBATCH --account=halla\n")
  jsubf.write("#SBATCH --partition=production\n")
  jsubf.write("#SBATCH --job-name=TEST\n")
  jsubf.write("#SBATCH --time=12:00:00\n")
  jsubf.write("#SBATCH --nodes=1\n")
  jsubf.write("#SBATCH --ntasks=1\n")
  jsubf.write("#SBATCH --cpus-per-task=1\n")
  jsubf.write("#SBATCH --mem=2G\n")
  jsubf.write("tcsh -c \"source /apps/root/6.18.00/setroot_CUE\"\n")
  jsubf.write("cd "+sourceDir+"\n")
  jsubf.write("echo \"Current working directory is `pwd`\"\n")
  jsubf.write("build/QweakSimG4 " + runjobs + "/test_" + str(qtor[i%6]) + "_" + config + str(i//6)+ ".mac" +"\n")
  print("sbatch "+jobs + "/test_" + str(qtor[i%6]) + "_" + config + str(i//6) + ".sh")
