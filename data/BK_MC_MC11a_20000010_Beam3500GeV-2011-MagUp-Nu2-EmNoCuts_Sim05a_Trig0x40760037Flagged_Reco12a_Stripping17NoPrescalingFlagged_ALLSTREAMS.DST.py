#-- GAUDI jobOptions generated on Sun Sep  8 12:21:08 2013
#-- Contains event types : 
#--   20000010 - 330 files - 4580479 events - 1714.34 GBytes


#--  Extra information about the data processing phases:

from Gaudi.Configuration import * 
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles(['LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000001_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000002_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000003_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000004_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000005_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000006_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000007_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000008_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000009_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000010_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000011_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000012_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000013_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000014_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000015_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000016_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000017_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000018_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000019_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000020_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000021_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000022_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000023_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000024_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000025_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000026_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000027_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000028_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000029_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000030_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000031_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000032_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000033_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000034_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000035_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000036_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000037_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000038_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000039_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000040_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000041_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000042_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000043_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000044_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000045_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000046_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000047_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000048_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000049_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000050_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000051_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000052_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000053_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000054_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000055_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000056_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000057_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000058_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000059_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000060_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000061_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000062_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000063_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000064_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000065_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000066_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000067_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000068_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000069_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000070_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000071_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000072_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000073_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000074_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000075_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000076_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000077_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000078_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000079_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000080_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000081_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000082_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000083_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000084_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000085_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000086_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000087_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000088_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000089_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000090_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000091_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000092_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000093_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000094_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000095_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000096_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000097_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000098_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000099_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000100_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000101_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000102_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000103_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000104_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000105_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000106_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000107_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000108_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000109_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000110_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000111_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000112_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000113_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000114_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000115_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000116_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000117_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000118_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000119_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000120_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000121_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000122_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000123_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000124_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000125_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000126_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000127_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000128_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000129_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000130_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000131_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000132_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000133_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000134_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000135_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000136_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000137_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000138_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000139_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000140_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000141_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000142_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000143_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000144_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000145_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000146_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000147_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000148_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000149_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000150_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000151_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000152_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000153_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000154_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000155_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000156_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000157_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000158_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000159_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000160_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000161_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000162_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000163_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000164_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000165_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000166_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000167_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000168_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000169_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000170_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000171_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000172_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000173_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000174_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000175_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000176_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000177_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000178_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000179_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000180_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000181_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000182_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000183_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000184_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000185_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000186_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000187_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000188_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000189_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000190_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000191_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000192_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000193_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000194_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000195_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000196_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000197_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000198_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000199_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000200_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000201_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000202_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000203_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000204_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000205_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000206_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000207_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000208_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000209_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000210_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000211_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000212_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000213_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000214_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000215_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000216_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000217_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000218_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000219_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000220_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000221_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000222_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000223_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000224_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000225_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000226_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000227_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000228_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000229_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000230_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000231_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000232_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000233_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000234_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000235_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000236_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000237_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000238_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000239_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000240_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000241_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000242_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000243_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000244_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000245_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000246_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000247_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000248_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000249_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000250_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000251_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000252_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000253_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000254_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000255_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000256_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000257_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000258_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000259_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000260_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000261_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000262_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000263_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000264_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000265_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000266_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000267_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000268_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000269_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000270_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000271_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000272_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000273_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000274_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000275_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000276_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000277_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000278_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000279_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000280_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000281_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000282_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000283_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000284_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000285_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000286_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000287_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000288_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000289_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000290_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000291_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000292_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000293_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000294_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000295_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000296_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000297_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000298_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000299_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000300_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000301_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000302_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000303_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000304_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000305_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000306_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000307_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000308_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000309_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000310_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000311_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000312_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000313_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000314_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000315_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000316_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000317_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000318_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000319_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000320_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000321_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000322_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000323_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000324_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000326_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000327_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000328_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000329_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000330_1.allstreams.dst',
'LFN:/lhcb/MC/MC11a/ALLSTREAMS.DST/00017285/0000/00017285_00000331_1.allstreams.dst'
], clear=True)
