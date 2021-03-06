#-- GAUDI jobOptions generated on Thu Jul 18 16:27:02 2013
#-- Contains event types : 
#--   27163003 - 204 files - 3519490 events - 738.37 GBytes


#--  Extra information about the data processing phases:


#--  Processing Pass Step-124620 

#--  StepId : 124620 
#--  StepName : Digi13 with G4 dE/dx 
#--  ApplicationName : Boole 
#--  ApplicationVersion : v26r3 
#--  OptionFiles : $APPCONFIGOPTS/Boole/Default.py;$APPCONFIGOPTS/Boole/DataType-2012.py;$APPCONFIGOPTS/Boole/Boole-SiG4EnergyDeposit.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py 
#--  DDDB : fromPreviousStep 
#--  CONDDB : fromPreviousStep 
#--  ExtraPackages : AppConfig.v3r164 
#--  Visible : Y 


#--  Processing Pass Step-124632 

#--  StepId : 124632 
#--  StepName : TCK-0x409f0045 Flagged for Sim08 2012 
#--  ApplicationName : Moore 
#--  ApplicationVersion : v14r8p1 
#--  OptionFiles : $APPCONFIGOPTS/Moore/MooreSimProductionWithL0Emulation.py;$APPCONFIGOPTS/Conditions/TCK-0x409f0045.py;$APPCONFIGOPTS/Moore/DataType-2012.py;$APPCONFIGOPTS/L0/L0TCK-0x0045.py 
#--  DDDB : fromPreviousStep 
#--  CONDDB : fromPreviousStep 
#--  ExtraPackages : AppConfig.v3r164 
#--  Visible : Y 


#--  Processing Pass Step-124630 

#--  StepId : 124630 
#--  StepName : Stripping20-NoPrescalingFlagged for Sim08 
#--  ApplicationName : DaVinci 
#--  ApplicationVersion : v32r2p1 
#--  OptionFiles : $APPCONFIGOPTS/DaVinci/DV-Stripping20-Stripping-MC-NoPrescaling.py;$APPCONFIGOPTS/DaVinci/DataType-2012.py;$APPCONFIGOPTS/DaVinci/InputType-DST.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py 
#--  DDDB : fromPreviousStep 
#--  CONDDB : fromPreviousStep 
#--  ExtraPackages : AppConfig.v3r164 
#--  Visible : Y 


#--  Processing Pass Step-124834 

#--  StepId : 124834 
#--  StepName : Reco14a for MC 
#--  ApplicationName : Brunel 
#--  ApplicationVersion : v43r2p7 
#--  OptionFiles : $APPCONFIGOPTS/Brunel/DataType-2012.py;$APPCONFIGOPTS/Brunel/MC-WithTruth.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py 
#--  DDDB : fromPreviousStep 
#--  CONDDB : fromPreviousStep 
#--  ExtraPackages : AppConfig.v3r164 
#--  Visible : Y 


#--  Processing Pass Step-125080 

#--  StepId : 125080 
#--  StepName : Sim08a - 2012 - MU - Pythia8 
#--  ApplicationName : Gauss 
#--  ApplicationVersion : v45r3 
#--  OptionFiles : $APPCONFIGOPTS/Gauss/Sim08-Beam4000GeV-mu100-2012-nu2.5.py;$DECFILESROOT/options/@{eventType}.py;$LBPYTHIA8ROOT/options/Pythia8.py;$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py 
#--  DDDB : Sim08-20130503-1 
#--  CONDDB : Sim08-20130503-1-vc-mu100 
#--  ExtraPackages : AppConfig.v3r171;DecFiles.v27r6 
#--  Visible : Y 


#--  Processing Pass Step-125337 

#--  StepId : 125337 
#--  StepName : Sim08a - 2012 - MU - Pythia8 
#--  ApplicationName : Gauss 
#--  ApplicationVersion : v45r3 
#--  OptionFiles : $APPCONFIGOPTS/Gauss/Sim08-Beam4000GeV-mu100-2012-nu2.5.py;$DECFILESROOT/options/@{eventType}.py;$LBPYTHIA8ROOT/options/Pythia8.py;$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py 
#--  DDDB : Sim08-20130503-1 
#--  CONDDB : Sim08-20130503-1-vc-mu100 
#--  ExtraPackages : AppConfig.v3r171;DecFiles.v27r8 
#--  Visible : Y 

from Gaudi.Configuration import * 
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles(['LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000001_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000002_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000003_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000004_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000005_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000006_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000007_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000008_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000009_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000011_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000013_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000014_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000015_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000016_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000017_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000018_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000019_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000020_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000021_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000022_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000023_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000024_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000025_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000026_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000027_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000028_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000029_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000030_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000031_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000032_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000033_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000034_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000035_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000036_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000037_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000038_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000039_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000040_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000041_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000042_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000043_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000044_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000045_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000046_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000047_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000048_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000049_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000050_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000051_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000052_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000053_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000054_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000055_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000056_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000057_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000058_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000059_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000060_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000061_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000062_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000063_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000064_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000065_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000066_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000067_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000068_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000069_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000070_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000071_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000072_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000073_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000074_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000075_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000076_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000077_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000078_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000079_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000080_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000081_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000082_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000083_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000084_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000085_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000086_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000087_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000088_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000089_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000090_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000091_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000092_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000093_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000094_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000095_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000096_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000097_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000098_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000099_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000100_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000101_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000102_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000103_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000104_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000105_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000106_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000107_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000108_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000109_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000110_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000111_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000112_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000113_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000114_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000115_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000116_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000117_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000118_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000119_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000120_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000121_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000122_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000123_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000124_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000125_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000126_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000127_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000128_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000129_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000130_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000131_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000132_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000133_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000134_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000135_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000136_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000137_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000138_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000139_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000140_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000141_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000142_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000143_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000144_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000145_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025298/0000/00025298_00000146_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000001_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000002_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000003_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000004_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000005_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000006_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000007_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000008_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000009_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000010_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000011_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000012_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000013_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000014_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000015_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000016_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000017_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000018_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000019_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000020_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000021_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000022_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000023_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000024_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000025_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000026_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000027_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000028_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000029_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000030_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000031_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000032_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000033_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000034_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000035_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000036_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000037_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000038_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000039_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000040_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000041_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000042_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000043_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000044_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000045_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000046_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000047_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000048_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000049_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000050_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000051_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000052_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000053_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000054_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000055_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000056_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000057_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000058_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000059_1.allstreams.dst',
'LFN:/lhcb/MC/2012/ALLSTREAMS.DST/00025923/0000/00025923_00000060_1.allstreams.dst'
], clear=True)
