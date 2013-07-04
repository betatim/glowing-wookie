#-- GAUDI jobOptions generated on Thu Apr 25 11:51:46 2013
#-- Contains event types : 
#--   27173002 - 197 files - 2549496 events - 1008.53 GBytes


#--  Extra information about the data processing phases:


#--  Processing Pass Step-16758 

#--  StepId : 16758 
#--  StepName : Sim05 with Nu=2.0 (w/o spillover) - MD - MC11a 
#--  ApplicationName : Gauss 
#--  ApplicationVersion : v41r1 
#--  OptionFiles : $APPCONFIGOPTS/Gauss/Beam3500GeV-md100-MC11-nu2.py;$DECFILESROOT/options/@{eventType}.py;$LBPYTHIAROOT/options/Pythia.py;$APPCONFIGOPTS/Gauss/G4PL_LHEP_EmNoCuts.py 
#--  DDDB : MC11-20111102 
#--  CONDDB : sim-20111111-vc-md100 
#--  ExtraPackages : AppConfig.v3r122;DecFiles.v25r2;SQLDDDB.v6r20 
#--  Visible : Y 


#--  Processing Pass Step-16379 

#--  StepId : 16379 
#--  StepName : Trigger - TCK 0x40760037 Flagged - MD - MC11a 
#--  ApplicationName : Moore 
#--  ApplicationVersion : v12r8g1 
#--  OptionFiles : $APPCONFIGOPTS/Moore/MooreSimProduction.py;$APPCONFIGOPTS/Conditions/TCK-0x40760037.py;$APPCONFIGOPTS/Moore/DataType-2011.py 
#--  DDDB : MC11-20111102 
#--  CONDDB : sim-20111111-vc-md100 
#--  ExtraPackages : AppConfig.v3r120;SQLDDDB.v6r20 
#--  Visible : Y 


#--  Processing Pass Step-15578 

#--  StepId : 15578 
#--  StepName : Stripping17NoPrescalingFlagged for MC11 MagDown 
#--  ApplicationName : DaVinci 
#--  ApplicationVersion : v29r1p1 
#--  OptionFiles : $APPCONFIGOPTS/DaVinci/DV-Stripping17-Stripping-MC-NoPrescaling.py 
#--  DDDB : MC11-20111102 
#--  CONDDB : sim-20111111-vc-md100 
#--  ExtraPackages : AppConfig.v3r116;SQLDDDB.v6r20 
#--  Visible : Y 


#--  Processing Pass Step-16578 

#--  StepId : 16578 
#--  StepName : Reco12a for MC11 - MagDown 
#--  ApplicationName : Brunel 
#--  ApplicationVersion : v41r1p1 
#--  OptionFiles : $APPCONFIGOPTS/Brunel/DataType-2011.py;$APPCONFIGOPTS/Brunel/MC-WithTruth.py;$APPCONFIGOPTS/Brunel/MC11a_dedxCorrection.py;$APPCONFIGOPTS/Brunel/TrigMuonRawEventFix.py 
#--  DDDB : MC11-20111102 
#--  CONDDB : sim-20111111-vc-md100 
#--  ExtraPackages : AppConfig.v3r122;SQLDDDB.v6r20 
#--  Visible : Y 


#--  Processing Pass Step-15798 

#--  StepId : 15798 
#--  StepName : Digi11 w/o spillover - MD - MC11a 
#--  ApplicationName : Boole 
#--  ApplicationVersion : v23r1 
#--  OptionFiles : $APPCONFIGOPTS/Boole/Default.py;$APPCONFIGOPTS/L0/L0TCK-0x0037.py 
#--  DDDB : MC11-20111102 
#--  CONDDB : sim-20111111-vc-md100 
#--  ExtraPackages : AppConfig.v3r118;SQLDDDB.v6r20 
#--  Visible : N 


#--  Processing Pass Step-16498 

#--  StepId : 16498 
#--  StepName : Sim05 with Nu=2.0 (w/o spillover) - MD - MC11a 
#--  ApplicationName : Gauss 
#--  ApplicationVersion : v41r1 
#--  OptionFiles : $APPCONFIGOPTS/Gauss/Beam3500GeV-md100-MC11-nu2.py;$DECFILESROOT/options/@{eventType}.py;$LBPYTHIAROOT/options/Pythia.py;$APPCONFIGOPTS/Gauss/G4PL_LHEP_EmNoCuts.py 
#--  DDDB : MC11-20111102 
#--  CONDDB : sim-20111111-vc-md100 
#--  ExtraPackages : AppConfig.v3r122;DecFiles.v25r1;SQLDDDB.v6r20 
#--  Visible : Y 

from Gaudi.Configuration import * 
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles(['LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000001_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000002_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000003_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000004_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000005_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000006_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000007_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000008_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000009_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000010_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000011_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000012_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000013_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000014_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000015_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000016_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000017_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000018_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000019_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000020_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000021_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000022_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000024_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000026_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000027_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000028_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000029_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000030_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000031_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000032_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000033_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000034_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000035_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000036_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000037_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000038_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000039_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000040_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000041_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000042_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014047/0000/00014047_00000043_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000001_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000002_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000003_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000004_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000005_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000006_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000007_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000008_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000009_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000010_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000011_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000012_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000013_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000014_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000015_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000016_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000017_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000018_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000019_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000020_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000021_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000022_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000023_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000024_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000025_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000026_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000027_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000028_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000029_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000030_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000031_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000032_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000033_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000034_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000035_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000036_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000037_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000038_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000039_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000040_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000041_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000042_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000043_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000045_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000046_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000047_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000048_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000049_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000050_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000051_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000052_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000053_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000054_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000055_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000056_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000057_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000058_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000059_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000060_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000061_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000062_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000063_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000064_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000065_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000066_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000067_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000068_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000069_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000070_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000071_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000072_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000073_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000074_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000075_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000076_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000077_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000078_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000079_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000080_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000081_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000082_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000083_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000084_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000085_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000086_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000087_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000088_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000089_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000090_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000091_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000092_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000093_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000094_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000095_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000096_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000097_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000098_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000099_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000100_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000101_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000102_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000103_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000104_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000105_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000106_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000107_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000108_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000109_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000110_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000111_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000112_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000113_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000114_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000115_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000116_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000117_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000118_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000119_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000120_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000121_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000122_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000123_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000124_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000125_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000126_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000127_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000128_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000129_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000130_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000131_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000132_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000133_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000134_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000135_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000136_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000137_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000138_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000139_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000140_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000141_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000142_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000143_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000144_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000145_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000146_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000147_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000148_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000149_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000150_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000151_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000152_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000153_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000154_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000155_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000156_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00014932/0000/00014932_00000157_1.allstreams.dst'
], clear=True)
