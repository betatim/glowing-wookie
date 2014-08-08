import os
import platform

#from wookie import make_dir

#base = "/tmp/%s/"%(os.getenv("USER"))

#_at_cern = "lxplus" in platform.node()
#if os.getenv("USER") == "thead" and not _at_cern:
  #path = "/tmp/thead/ntuples/"
#if os.getenv("USER") == "thead" and _at_cern:
  #path = "/afs/cern.ch/work/t/tbird/demu/ntuples/"

#plotspath = base + "demu-plots/"
## place to store output from one script/stage
## that is read in by another script, not too
## expensive to re-generate
#workingpath = base +"demu-working/"

#if os.getenv("USER") == "tbird":
path = "/afs/cern.ch/work/t/tbird/demu/ntuples/"
plotspath = "/afs/cern.ch/user/t/tbird/emu/glowing-wookie/scripts/fitters/"

## Slowly transition to using this
## for ntuples
#ntuplepath = path

#for p in (path, plotspath, workingpath):
  #make_dir(p)

#castorURL = "root://castorlhcb.cern.ch/" \
            #"/castor/cern.ch/user/t/tbird/demu/ntuples/{f}?svcClass=lhcbuser"
castorURL = "root://castorlhcb.cern.ch//castor/cern.ch/user/t/tbird/demu/ntuples/{f}"
localURL = path+"{f}"

def combine_cuts(cuts):
  ret = ""
  last_cut = len(cuts) - 1
  if isinstance(cuts, list):
    for cut_number,(cut) in enumerate(cuts):
      ret += "(%s)" % cut
      #if cut_number is not 0:
      if cut_number is not last_cut:
        ret += "&&"

  elif isinstance(cuts, tuple):
    for cut_number,(cut,positive) in enumerate(cuts):
      if positive:
        ret += "(%s)" % cut
      else:
        ret += "!(%s)" % cut

      #if cut_number is not 0:
      if cut_number is not last_cut:
        ret += "&&"
  elif isinstance(cuts, str):
    return cuts

  else:
    raise TypeError("cuts is not a list, tuple or string")

  return ret




class CutList:
  def __init__(self, arr=[]):
    self.cut_list = arr

  def get_list(self,array=None,from_cut=None,to_cut=None):
    ret = []
    if array == None:
      found_start = False
      if from_cut == None:
        found_start = True

      for k,v in self.cut_list:
        if not found_start:
          if from_cut == k:
            found_start = True
            ret.append(v)
          continue
        if to_cut == k:
          break
        ret.append(v)
    else:
      for i in array:
        for k,v in self.cut_list:
          if k == i:
            ret.append(v)
    return ret

  def get_name_list(self,array=None,from_cut=None,to_cut=None):
    ret = []
    if array == None:
      found_start = False
      if from_cut == None:
        found_start = True

      for k,v in self.cut_list:
        if not found_start:
          if from_cut == k:
            found_start = True
            ret.append(k)
          continue
        if to_cut == k:
          break
        ret.append(k)
    else:
      for i in array:
        for k,v in self.cut_list:
          if k == i:
            ret.append(k)
    return ret

  def get_cut(self,name):
    for k,v in self.cut_list:
      if k == name:
        return v
    raise KeyError("Requested cut doesn't exist in this list")



emu_cuts = CutList([
    ("mcmatch", "abs(x1_TRUEID)==11 && abs(x2_TRUEID)==13 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT"),
    ("ls", "x1_ID*x2_ID<0"),
    ("l0", "x2_L0MuonDecision_TOS == 1"),
    ("hlt1", "x2_Hlt1TrackMuonDecision_TOS == 1"),
    ("hlt2", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1"),
    #("hlt2_1740_1950", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1740 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1950 )"),
    #("hlt2_1790_1950", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1790 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1950 )"),
    #("hlt2_1790_1930", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1790 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1930 )"),
    ("hlt2_1815_1915", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1815 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1915 )"),
    ("dtf", "abs(Dst_DTF_CHI2)<100"),
    ("mass", "Dst_DTF_D0_MM > 1815 && Dst_DTF_D0_MM < 1915 && (Dst_DTF_Dst_MM-Dst_DTF_D0_MM)>139.4"),
    #("pid", "x1_ProbNNe>0.32 && x2_ProbNNmu>0.2 && pi_ProbNNpi>0.9"),
    ("ghost", "pi_ProbNNghost<0.05"),
    ("pid", "x1_PIDe>6 && x2_ProbNNmu>0.4"),
  ])

pipiasemu_cuts = CutList([
    ("mcmatch", "abs(x1_TRUEID)==211 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT"),
    ("ls", "x1_ID*x2_ID<0"),
    #("l0", "x2_L0MuonDecision_TOS == 1"),
    #("hlt1", "x2_Hlt1TrackMuonDecision_TOS == 1"),
    ("hlt2", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1"),
    #("hlt2_1740_1950", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1740 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1950 )"),
    #("hlt2_1790_1950", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1790 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1950 )"),
    #("hlt2_1790_1930", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1790 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1930 )"),
    ("hlt2_1815_1915", "D0_Hlt2CharmHadD02HH_D02PiPiDecision_TOS == 1 && (SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass > 1815 && SelReport_Hlt2CharmHadD02HH_D02PiPiDecision_Particle_measuredMass < 1915 )"),
    ("dtf", "abs(Dst_DTF_CHI2)<100"),
    ("mass", "Dst_DTF_D0_MM > 1815 && Dst_DTF_D0_MM < 1915 && (Dst_DTF_Dst_MM-Dst_DTF_D0_MM)>139.4"),
    #("pid", "x1_ProbNNe>0.32 && x2_ProbNNmu>0.2 && pi_ProbNNpi>0.9"),
    ("ghost", "pi_ProbNNghost<0.05"),
    #("pid", "x1_PIDe>4 && x2_ProbNNmu>0.4"),
  ])

pipi_cuts = CutList([
    ("mcmatch", "abs(x1_TRUEID)==211 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT"),
    ("ls", "x1_ID*x2_ID<0"),
    ("l0", "x1_L0HadronDecision_TOS == 1 || x2_L0HadronDecision_TOS == 1"),
    ("hlt1", "( x1_L0HadronDecision_TOS == 1 && x1_Hlt1TrackAllL0Decision_TOS == 1 ) || ( x2_L0HadronDecision_TOS == 1 && x2_Hlt1TrackAllL0Decision_TOS  == 1 )"),
    ("hlt2", "Dst_Hlt2Dst2PiD02PiPiDecision_TOS == 1"),
    ("dtf", "abs(Dst_DTF_CHI2)<100"),
    ("mass", "Dst_DTF_D0_MM > 1815 && Dst_DTF_D0_MM < 1915 && (Dst_DTF_Dst_MM-Dst_DTF_D0_MM)>139.4"),
    ("ghost", "pi_ProbNNghost<0.05"),
    ("pid", "x1_ProbNNpi>0.6 && x2_ProbNNpi>0.6"),
    #("pid", "x1_ProbNNpi > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNpi*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNk < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7"),
  ])

kpi_cuts = CutList([
    ("mcmatch", "abs(x1_TRUEID)==321 && abs(x2_TRUEID)==211 && abs(pi_TRUEID)==211 && abs(x1_MC_MOTHER_ID) == 421 && abs(x2_MC_MOTHER_ID) == 421 && abs(x1_MC_GD_MOTHER_ID) == 413 && abs(x2_MC_GD_MOTHER_ID) == 413 && abs(pi_MC_MOTHER_ID) == 413 && pi_MC_MOTHER_KEY==x1_MC_GD_MOTHER_KEY && x1_MC_GD_MOTHER_KEY==x2_MC_GD_MOTHER_KEY && Dst_BKGCAT < 60 && Dst_BKGCAT==D0_BKGCAT"),
    ("ls", "x1_ID*x2_ID<0"),
    ("l0", "x1_L0HadronDecision_TOS == 1 || x2_L0HadronDecision_TOS == 1"),
    ("hlt1", "( x1_L0HadronDecision_TOS == 1 && x1_Hlt1TrackAllL0Decision_TOS == 1 ) || ( x2_L0HadronDecision_TOS == 1 && x2_Hlt1TrackAllL0Decision_TOS  == 1 )"),
    ("hlt2", "Dst_Hlt2Dst2PiD02KPiDecision_TOS == 1"),
    ("dtf", "abs(Dst_DTF_CHI2)<100"),
    ("mass", "(Dst_DTF_Dst_MM-Dst_DTF_D0_MM)>139.4"),
    #("mass", "Dst_DTF_D0_MM > 1815 && Dst_DTF_D0_MM < 1915 && (Dst_DTF_Dst_MM-Dst_DTF_D0_MM)>139.4"),
    ("ghost", "pi_ProbNNghost<0.05"),
    ("pid", "x1_PIDK > 6 && x2_PIDK<0"),
    #("pid", "x1_ProbNNk > 0.6 && x2_ProbNNpi>0.6"),
    #("pid", "x1_ProbNNk > 0.6 && x2_ProbNNpi > 0.6 && x1_ProbNNk*x2_ProbNNpi > 0.7 && pi_ProbNNpi > 0.6 && x1_ProbNNpi < 0.7  && x2_ProbNNk < 0.7  && pi_ProbNNk < 0.7"),
  ])

cut_titles = {
  "mcmatch": "MC matched stripping",
  "ls": "Like-sign cut",
  "l0": "L0 trigger",
  "hlt1": "HLT1 trigger",
  "hlt2": "HLT2 trigger",
  "hlt2_1740_1950": "Trigger mass 1740-1950",
  "hlt2_1790_1950": "Trigger mass 1790-1950",
  "hlt2_1790_1930": "Trigger mass 1790-1930",
  "hlt2_1815_1915": "Trigger mass 1815-1915",
  "dtf": "DTF converged",
  "mass": "Mass 1815-1915",
  "ghost": "Slow \\pip{} ghosts",
  "loosepid": "Loose PID cuts",
  "pid": "Offline PID cuts",
  }




#cut_lists = {
  #"emu": [val for key, val in cuts["emu"].iteritems()],
  #"pidemu": [val for key, val in cuts["emu"].iteritems() if not key in ["pid"]],
  #"pipi": [val for key, val in cuts["pipi"].iteritems()],
  #"pidpipi": [val for key, val in cuts["pipi"].iteritems() if not key in ["pid"]],
  #"kpi": [val for key, val in cuts["kpi"].iteritems()],
  #"pidkpi": [val for key, val in cuts["kpi"].iteritems() if not key in ["pid"]],
#}









lumi = {
  "unblind" : 0.25,
  "2011" : 1.11,
  "2012" : 2.08,
  }


  #'pidemu2011blind': {
    #'infile' : datasets["emu2011blind"]["file"],
    #'outfile': directory+"emu/pid_emu_2011_blind.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list(["ls","l0","hlt1","dtf","ghost"])),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'pidemu2011unblind': {
    #'infile' : datasets["emu2011unblind"]["file"],
    #'outfile': directory+"emu/pid_emu_2011_unblind.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list(["ls","l0","hlt1","dtf","ghost"])),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},

  #'emu2011unblind': {
    #'infile' : datasets["emu2011unblind"]["file"],
    #'outfile': directory+"emu/fitter_emu_2011_unblind.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list(from_cut="ls")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},
  #'mvaemu2011blind': {
    #'infile' : datasets["emu2011blind"]["file"],
    #'outfile': directory+"emu/mva_emu_2011_blind.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list(["ls","l0","hlt1","dtf","pid","ghost"])),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'emu2011blind': {
    #'infile' : datasets["emu2011blind"]["file"],
    #'outfile': directory+"emu/fitter_emu_2011_blind.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list(["ls","l0","hlt1","dtf","pid","ghost"])),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},

  #'mvapipi2011': {
    #'infile' : datasets["pipi2011"]["file"],
    #'outfile': directory+"pipi/mva_pipi_2011.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls",to_cut="pid")+["abs(Dst_DTF_D0_M-1865)<15 && abs(Dst_DTF_Dst_M-Dst_DTF_D0_M-145.5)<0.5"]),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'mvapipi2012': {
    #'infile' : datasets["pipi2012"]["file"],
    #'outfile': directory+"pipi/mva_pipi_2012.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls",to_cut="pid")+["abs(Dst_DTF_D0_M-1865)<15 && abs(Dst_DTF_Dst_M-Dst_DTF_D0_M-145.5)<0.5"]),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},

  #'pidpipi2011': {
    #'infile' : datasets["pipi2011"]["file"],
    #'outfile': directory+"pipi/pid_pipi_2011.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls",to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'pidpipi2012': {
    #'infile' : datasets["pipi2012"]["file"],
    #'outfile': directory+"pipi/pid_pipi_2012.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls",to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},

  #'pipi2011': {
    #'infile' : datasets["pipi2011"]["file"],
    #'outfile': directory+"pipi/fitter_pipi_2011.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},
  #'pipi2012': {
    #'infile' : datasets["pipi2012"]["file"],
    #'outfile': directory+"pipi/fitter_pipi_2012.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},

  #'pidkpi2011': {
    #'infile' : datasets["kpi2011"]["file"],
    #'outfile': directory+"kpi/pid_kpi_2011.root",
    #'cuts'   : combine_cuts(kpi_cuts.get_list(from_cut="ls",to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'pidkpi2012': {
    #'infile' : datasets["kpi2012"]["file"],
    #'outfile': directory+"kpi/pid_kpi_2012.root",
    #'cuts'   : combine_cuts(kpi_cuts.get_list(from_cut="ls",to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},

  #'kpi2011': {
    #'infile' : datasets["kpi2011"]["file"],
    #'outfile': directory+"kpi/fitter_kpi_2011.root",
    #'cuts'   : combine_cuts(kpi_cuts.get_list(from_cut="ls")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},
  #'kpi2012': {
    #'infile' : datasets["kpi2012"]["file"],
    #'outfile': directory+"kpi/fitter_kpi_2012.root",
    #'cuts'   : combine_cuts(kpi_cuts.get_list(from_cut="ls")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},

  #'mcmvaemu2011': {
    #'infile' : datasets["mcemu2011"]["file"],
    #'outfile': directory+"mcemu/mva_emu_2011.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list()),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'mcmvaemu2012': {
    #'infile' : datasets["mcemu2012"]["file"],
    #'outfile': directory+"mcemu/mva_emu_2012.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list()),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},

  #'mcpidemu2011': {
    #'infile' : datasets["mcemu2011"]["file"],
    #'outfile': directory+"mcemu/pid_emu_2011.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list(to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'mcpidemu2012': {
    #'infile' : datasets["mcemu2012"]["file"],
    #'outfile': directory+"mcemu/pid_emu_2012.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list(to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},

  #'mcemu2011': {
    #'infile' : datasets["mcemu2011"]["file"],
    #'outfile': directory+"mcemu/fitter_emu_2011.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list()),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},
  #'mcemu2012': {
    #'infile' : datasets["mcemu2012"]["file"],
    #'outfile': directory+"mcemu/fitter_emu_2012.root",
    #'cuts'   : combine_cuts(emu_cuts.get_list()),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},

  #'mcpidpipi2011': {
    #'infile' : datasets["mcpipi2011"]["file"],
    #'outfile': directory+"mcpipi/pid_pipi_2011.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list(to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'mcpidpipi2012': {
    #'infile' : datasets["mcpipi2012"]["file"],
    #'outfile': directory+"mcpipi/pid_pipi_2012.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list(to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},

  #'mcpipi2011': {
    #'infile' : datasets["mcpipi2011"]["file"],
    #'outfile': directory+"mcpipi/fitter_pipi_2011.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list()),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},
  #'mcpipi2012': {
    #'infile' : datasets["mcpipi2012"]["file"],
    #'outfile': directory+"mcpipi/fitter_pipi_2012.root",
    #'cuts'   : combine_cuts(pipi_cuts.get_list()),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},

  #'mcpidkpi2011': {
    #'infile' : datasets["mckpi2011"]["file"],
    #'outfile': directory+"mckpi/pid_kpi_2011.root",
    #'cuts'   : combine_cuts(kpi_cuts.get_list(to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'mcpidkpi2012': {
    #'infile' : datasets["mckpi2012"]["file"],
    #'outfile': directory+"mckpi/pid_kpi_2012.root",
    #'cuts'   : combine_cuts(kpi_cuts.get_list(to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},

  #'mckpi2011': {
    #'infile' : datasets["mckpi2011"]["file"],
    #'outfile': directory+"mckpi/fitter_kpi_2011.root",
    #'cuts'   : combine_cuts(kpi_cuts.get_list()),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},
  #'mckpi2012': {
    #'infile' : datasets["mckpi2012"]["file"],
    #'outfile': directory+"mckpi/fitter_kpi_2012.root",
    #'cuts'   : combine_cuts(kpi_cuts.get_list()),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : True
  #},


  #'mcpidpipiasemu2012': {
    #'infile' : datasets["mcpipiasemu2012"]["file"],
    #'outfile': directory+"mcpipi/pid_emu_2012.root",
    #'cuts'   : combine_cuts(pipiasemu_cuts.get_list()),
      ##combine_cuts(pipi_cuts.get_list(to_cut="ls") + emu_cuts.get_list(from_cut="ls",to_cut="pid")),
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'mva'    : False
  #},
  #'mcpidpipiasemu2011': {
    #'infile' : datasets["mcpipiasemu2011"]["file"],
    #'inPath' : "Demu_NTuple/Demu_NTuple",
    #'cuts'   : combine_cuts(pipiasemu_cuts.get_list()),
    #'mva'    : False

    #'outfile': directory+"mcpipi/pid_emu_2011.root",
      ##combine_cuts(pipi_cuts.get_list(to_cut="ls") + emu_cuts.get_list(from_cut="ls",to_cut="pid")),
  #},



datasets = {}

  # e Mu Data

datasets["emu2011blind"] = {
    "lumi" : lumi["2011"]-lumi["unblind"],
    "file" : castorURL.format(f="emu/strip_emu_2011_blind.root"),
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["emu2011unblind"] = {
    "lumi" : lumi["unblind"],
    "file" : localURL.format(f="emu/strip_emu_2011_unblind.root"),
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["pidemu2011blind"] = {
    "lumi" : lumi["2011"]-lumi["unblind"],
    "file" : path+"emu/pid_emu_2011_blind.root",
    "tree" : "subTree",

    'infile' : datasets["emu2011blind"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(["ls","l0","hlt1","dtf","ghost"])),
    'mva'    : False,
  }
datasets["pidemu2011unblind"] = {
    "lumi" : lumi["unblind"],
    "file" : path+"emu/pid_emu_2011_unblind.root",
    "tree" : "subTree",

    'infile' : datasets["emu2011unblind"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(["ls","l0","hlt1","dtf","ghost"])),
    'mva'    : False,
  }
datasets["mvaemu2011blind"] = {
    "lumi" : lumi["2011"]-lumi["unblind"],
    "file" : path+"emu/mva_emu_2011_blind.root",
    "tree" : "subTree",

    'infile' : datasets["emu2011blind"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(["ls","l0","hlt1","dtf","pid","ghost"])),
    'mva'    : False,
  }
datasets["mvaemu2011unblind"] = {
    "lumi" : lumi["unblind"],
    "file" : path+"emu/mva_emu_2011_blind.root",
    "tree" : "subTree",

    'infile' : datasets["emu2011unblind"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(from_cut="ls")),
    'mva'    : False,
  }
datasets["fitteremu2011blind"] = {
    "lumi" : lumi["2011"]-lumi["unblind"],
    "file" : path+"emu/fitter_emu_2011_blind.root",
    "tree" : "subTree",

    'infile' : datasets["emu2011blind"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(["ls","l0","hlt1","dtf","pid","ghost"])),
    'mva'    : True,
  }
datasets["fitteremu2011unblind"] = {
    "lumi" : lumi["unblind"],
    "file" : path+"emu/fitter_emu_2011_unblind.root",
    "tree" : "subTree",

    'infile' : datasets["emu2011unblind"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(from_cut="ls")),
    'mva'    : True,
  }
datasets["fitterlooseemu2011unblind"] = {
    "lumi" : lumi["unblind"],
    "file" : path+"emu/fitter_loose_emu_2011_unblind.root",
    "tree" : "subTree",

    'infile' : datasets["emu2011unblind"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(from_cut="ls",to_cut="pid")+["x1_PIDe>2 && x2_ProbNNmu>0.2"]),
    'mva'    : True,
  }

  # e Mu MC

datasets["mcemu2011"] = {
    "events" : {"magup":  1010498, "magdown": 1029498},
    "file" : path+"mcemu/strip_emu_2011.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcemu2012"] = {
    "events" : {"magup":  2030990, "magdown": 2017492},
    "file" : path+"mcemu/strip_emu_2012.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcnopidemu2011"] = {
    "events" : {"magup":  1010498, "magdown": 1029498},
    "file" : path+"mcemu/strip_nopid_emu_2011.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcnopidemu2012"] = {
    "events" : {"magup":  2030990, "magdown": 2017492},
    "file" : path+"mcemu/strip_nopid_emu_2012.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcpidemu2011"] = {
    "events" : {"magup":  1010498, "magdown": 1029498},
    "file" : path+"mcemu/pid_emu_2011.root",
    "tree" : "subTree",

    'infile' : datasets["mcemu2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(to_cut="pid")),
    'mva'    : True,
  }
datasets["mcpidemu2012"] = {
    "events" : {"magup":  2030990, "magdown": 2017492},
    "file" : path+"mcemu/pid_emu_2012.root",
    "tree" : "subTree",

    'infile' : datasets["mcemu2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list(to_cut="pid")),
    'mva'    : True,
  }
datasets["mcmvaemu2011"] = {
    "events" : {"magup":  1010498, "magdown": 1029498},
    "file" : path+"mcemu/mva_emu_2011.root",
    "tree" : "subTree",

    'infile' : datasets["mcemu2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list()),
    'mva'    : False,
  }
datasets["mcmvaemu2012"] = {
    "events" : {"magup":  2030990, "magdown": 2017492},
    "file" : path+"mcemu/mva_emu_2012.root",
    "tree" : "subTree",

    'infile' : datasets["mcemu2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list()),
    'mva'    : False,
  }
datasets["mcfitteremu2011"] = {
    "events" : {"magup":  1010498, "magdown": 1029498},
    "file" : path+"mcemu/fitter_emu_2011.root",
    "tree" : "subTree",

    'infile' : datasets["mcemu2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list()),
    'mva'    : True,
  }
datasets["mcfitteremu2012"] = {
    "events" : {"magup":  2030990, "magdown": 2017492},
    "file" : path+"mcemu/fitter_emu_2012.root",
    "tree" : "subTree",

    'infile' : datasets["mcemu2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(emu_cuts.get_list()),
    'mva'    : True,
  }

  # Pi Pi Data

datasets["pipi2011"] = {
    "lumi" : lumi["2011"],
    "file" : castorURL.format(f="pipi/strip_pipi_2011.root"),
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["pipi2012"] = {
    "lumi" : lumi["2012"],
    "file" : castorURL.format(f="pipi/strip_pipi_2012.root"),
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["fitterpipi2011"] = {
    "lumi" : lumi["2011"],
    "file" : localURL.format(f="pipi/fitter_pipi_2011.root"),
    "tree" : "subTree",

    'infile' : datasets["pipi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls")),
    'mva'    : True,
  }
datasets["fitterpipi2012"] = {
    "lumi" : lumi["2012"],
    "file" : localURL.format(f="pipi/fitter_pipi_2012.root"),
    "tree" : "subTree",

    'infile' : datasets["pipi2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls")),
    'mva'    : True,
  }

datasets["pidpipi2012"] = {
    "lumi" : lumi["2012"],
    "file" : localURL.format(f="pipi/pid_pipi_2012.root"),
    "tree" : "subTree",

    'infile' : datasets["pipi2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls",to_cut="pid")),
    'mva'    : False,
  }
datasets["pidpipi2011"] = {
    "lumi" : lumi["2011"],
    "file" : localURL.format(f="pipi/pid_pipi_2011.root"),
    "tree" : "subTree",

    'infile' : datasets["pipi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls",to_cut="pid")),
    'mva'    : False,
  }

datasets["mvapipi2012"] = {
    "lumi" : lumi["2012"],
    "file" : localURL.format(f="pipi/mva_pipi_2012.root"),
    "tree" : "subTree",

    'infile' : datasets["pipi2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls",to_cut="pid")+["abs(Dst_DTF_D0_M-1865)<15 && abs(Dst_DTF_Dst_M-Dst_DTF_D0_M-145.5)<0.5"]),
    'mva'    : False,
  }
datasets["mvapipi2011"] = {
    "lumi" : lumi["2011"],
    "file" : localURL.format(f="pipi/mva_pipi_2011.root"),
    "tree" : "subTree",

    'infile' : datasets["pipi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list(from_cut="ls",to_cut="pid")+["abs(Dst_DTF_D0_M-1865)<15 && abs(Dst_DTF_Dst_M-Dst_DTF_D0_M-145.5)<0.5"]),
    'mva'    : False,
  }
#datasets["splotpipi2011"] = {
    #"lumi" : lumi["2011"],
    #"file" : localURL.format(f="pipi/splot_pipi_2011.root"),
    #"tree" : "subTree",
  #}
#datasets["splotpipi2012"] = {
    #"lumi" : lumi["2012"],
    #"file" : localURL.format(f="pipi/splot_pipi_2012.root"),
    #"tree" : "subTree",
  #}

  # Pi Pi MC

datasets["mcpipi2011"] = {
    "events" : {"magup": 502999, "magdown":516999 },
    "file" : path+"mcpipi/strip_pipi_2011.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcpipi2012"] = {
    "events" : {"magup": 1000998, "magdown":1022495},
    "file" : path+"mcpipi/strip_pipi_2012.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }

datasets["mcpidpipi2011"] = {
    "events" : datasets["mcpipi2011"]["events"],
    "file"   : path+"mcpipi/pid_pipi_2011.root",
    "tree"   : "subTree",

    'infile' : datasets["mcpipi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list(to_cut="pid")),
    'mva'    : False,
  }
datasets["mcpidpipi2012"] = {
    "events" : datasets["mcpipi2012"]["events"],
    "file"   : path+"mcpipi/pid_pipi_2012.root",
    "tree"   : "subTree",

    'infile' : datasets["mcpipi2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list(to_cut="pid")),
    'mva'    : False,
  }
datasets["mcfitterpipi2011"] = {
    "events" : datasets["mcpipi2011"]["events"],
    "file"   : path+"mcpipi/fitter_pipi_2011.root",
    "tree"   : "subTree",

    'infile' : datasets["mcpipi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list()),
    'mva'    : True,
  }
datasets["mcfitterpipi2012"] = {
    "events" : datasets["mcpipi2012"]["events"],
    "file"   : path+"mcpipi/fitter_pipi_2012.root",
    "tree"   : "subTree",

    'infile' : datasets["mcpipi2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(pipi_cuts.get_list()),
    'mva'    : True,
  }

  # K Pi Data

datasets["kpi2011"] = {
    "lumi" : lumi["2011"],
    "file" : castorURL.format(f="kpi/strip_kpi_2011.root"),
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["kpi2012"] = {
    "lumi" : lumi["2012"],
    "file" : castorURL.format(f="kpi/strip_kpi_2012.root"),
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["pidkpi2011"] = {
    "lumi" : lumi["2011"],
    "file"   : path+"kpi/pid_kpi_2011.root",
    "tree"   : "subTree",

    'infile' : datasets["kpi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(kpi_cuts.get_list(from_cut="ls",to_cut="pid")),
    'mva'    : False,
  }
datasets["pidkpi2012"] = {
    "lumi" : lumi["2012"],
    "file"   : path+"kpi/pid_kpi_2012.root",
    "tree"   : "subTree",

    'infile' : datasets["kpi2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(kpi_cuts.get_list(from_cut="ls",to_cut="pid")),
    'mva'    : False,
  }
datasets["fitterkpi2011"] = {
    "lumi" : lumi["2011"],
    "file" : localURL.format(f="kpi/fitter_kpi_2011.root"),
    "tree" : "subTree",

    'infile' : datasets["kpi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(kpi_cuts.get_list(from_cut="ls")),
    'mva'    : True,
  }
datasets["fitterkpi2012"] = {
    "lumi" : lumi["2012"],
    "file" : localURL.format(f="kpi/fitter_kpi_2012.root"),
    "tree" : "subTree",

    'infile' : datasets["kpi2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(kpi_cuts.get_list(from_cut="ls")),
    'mva'    : True,
  }
#datasets["splotkpi2011"] = {
    #"lumi" : lumi["2011"],
    #"file" : localURL.format(f="kpi/splot_kpi_2011.root"),
    #"tree" : "subTree",
  #}
#datasets["splotkpi2012"] = {
    #"lumi" : lumi["2012"],
    #"file" : localURL.format(f="kpi/splot_kpi_2012.root"),
    #"tree" : "subTree",
  #}

  # K Pi MC

datasets["mckpi2011"] = {
    "events" : {"magup": 1765500, "magdown":1763993 },
    "file"   : path+"mckpi/strip_kpi_2011.root",
    "tree"   : "Demu_NTuple/Demu_NTuple",
  }
datasets["mckpi2012"] = {
    "events" : {"magup": 3519490, "magdown":3513735},
    "file"   : path+"mckpi/strip_kpi_2012.root",
    "tree"   : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcpidkpi2011"] = {
    "events" : datasets["mckpi2011"]["events"],
    "file"   : path+"mckpi/pid_kpi_2011.root",
    "tree"   : "subTree",

    'infile' : datasets["mckpi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(kpi_cuts.get_list(to_cut="pid")),
    'mva'    : False,
  }
datasets["mcpidkpi2012"] = {
    "events" : datasets["mckpi2012"]["events"],
    "file"   : path+"mckpi/pid_kpi_2012.root",
    "tree"   : "subTree",

    'infile' : datasets["mckpi2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(kpi_cuts.get_list(to_cut="pid")),
    'mva'    : False,
  }
datasets["mcfitterkpi2011"] = {
    "events" : datasets["mckpi2011"]["events"],
    "file"   : path+"mckpi/fitter_kpi_2011.root",
    "tree"   : "subTree",

    'infile' : datasets["mckpi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(kpi_cuts.get_list()),
    'mva'    : True,
  }
datasets["mcfitterkpi2012"] = {
    "events" : datasets["mckpi2012"]["events"],
    "file"   : path+"mckpi/fitter_kpi_2012.root",
    "tree"   : "subTree",

    'infile' : datasets["mckpi2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts(kpi_cuts.get_list()),
    'mva'    : True,
  }

  # Pi Pi as e Mu MC

datasets["mcpipiasemu"] = {
    "events" : {"magup": 1000998+502999, "magdown":1022495+516999},
    "file" : path+"mcpipi/strip_emu.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcpipiasemu2011"] = {
    "events" : {"magup": 502999, "magdown":516999},
    "file" : path+"mcpipi/strip_emu_2011.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcpipiasemu2012"] = {
    "events" : {"magup": 1000998, "magdown":1022495},
    "file" : path+"mcpipi/strip_emu_2012.root",
    "tree" : "Demu_NTuple/Demu_NTuple",
  }
datasets["mcfitterpipiasemu2011"] = {
    "events" : datasets["mcpipiasemu2011"]["events"],
    "file"   : path+"mcpipi/fitter_emu_2011.root",
    "tree"   : "subTree",

    'infile' : datasets["mcpipiasemu2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts([pipi_cuts.get_cut("mcmatch")]+emu_cuts.get_list(from_cut="dtf", to_cut="pid")),
    'mva'    : True,
  }
datasets["mcfitterpipiasemu2012"] = {
    "events" : datasets["mcpipiasemu2012"]["events"],
    "file"   : path+"mcpipi/fitter_emu_2012.root",
    "tree"   : "subTree",

    'infile' : datasets["mcpipiasemu2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts([pipi_cuts.get_cut("mcmatch")]+emu_cuts.get_list(from_cut="dtf", to_cut="pid")),
    'mva'    : True,
  }
datasets["mcfitterloosepipiasemu2011"] = {
    "events" : datasets["mcpipiasemu2011"]["events"],
    "file"   : path+"mcpipi/fitter_loose_emu_2011.root",
    "tree"   : "subTree",

    'infile' : datasets["mcpipiasemu2011"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts([pipi_cuts.get_cut("mcmatch")]+emu_cuts.get_list(from_cut="dtf", to_cut="pid")),
    'mva'    : True,
  }
datasets["mcfitterloosepipiasemu2012"] = {
    "events" : datasets["mcpipiasemu2012"]["events"],
    "file"   : path+"mcpipi/fitter_loose_emu_2012.root",
    "tree"   : "subTree",

    'infile' : datasets["mcpipiasemu2012"]["file"],
    'intree' : "Demu_NTuple/Demu_NTuple",
    'cuts'   : combine_cuts([pipi_cuts.get_cut("mcmatch")]+emu_cuts.get_list(from_cut="dtf", to_cut="pid")),
    'mva'    : True,
  }

