import json
import urllib2
import pickle
import md5
from datetime import datetime

import TCKUtils.utils as TckUtils

#{
#"beamenergy": 3500.0,
#"LHCState": "PHYSICS",
#"prev_runid": 90574,
#"programVersion": "v12r5",
#"avLumi": "170.92674577155",
#"runid": 90613, "veloPosition":
#"Closed", "endtime": "2011-05-01T19:08:18",
#"betaStar": "3.5",
#"destination": "OFFLINE",
#"veloOpening": "-0.000701904296875",
#"state": "IN BKK",
#"program": "Moore",
#"avHltPhysRate": "1478.9629629702",
#"partitionid": 32767,
#"starttime": "2011-05-01T19:07:24",
#"magnetCurrent": "-5850",
#"runtype": "COLLISION11",
#"avL0PhysRate": "390202.18823799",
#"avMu": "1.1887201725309",
#"avPhysDeadTime": "1.3495270357191",
#"magnetState": "DOWN",
#"next_runid": 90614,
#"partitionname": "LHCb",
#"tck": "5963826"}

class Run:
  def __init__(self,run):
    self.startTime = datetime.strptime(run["starttime"],"%Y-%m-%dT%H:%M:%S")
    self.endTime = datetime.strptime(run["endtime"],"%Y-%m-%dT%H:%M:%S")
    self.year = self.startTime.year
    delta = (self.endTime-self.startTime)
    self.totalSeconds = delta.days * 86400 + delta.seconds
    self.lumi = float(self.totalSeconds) * float(run["avLumi"])
    #self.lumi = (float(self.totalSeconds)*(1.-1e-3*float(run["avPhysDeadTime"]))) * float(run["avLumi"])
    #self.lumi = float(self.totalSeconds) * (float(run["avLumi"])-float(run["avPhysDeadTime"]))
    self.beamEnergy = run["beamenergy"]
    self.id = run["runid"]
    self.nextRunId = run["next_runid"]
    self.mag = run["magnetState"].lower()
    self.tck = "0x{0:0>8x}".format(int(run["tck"]))

  #def __str__(self):
    #return "Run(%i)"%(self.runId)
  def __repr__(self):
    return "Run(%i)"%(self.id)
  def __str__(self):
    return "Run(%i)"%(self.id)


class RunCounter:
  def __init__(self):
    self.results = {}
    self.hlt = HltInterface()

  def add(self,run):
    try:
      self.results[run.year][run.tck][run.mag] += run.lumi
    except KeyError:
      try:
        self.results[run.year]
        try:
          self.results[run.year][run.tck]["up"] = 0.
          self.results[run.year][run.tck]["down"] = 0.
          self.results[run.year][run.tck][run.mag] += run.lumi
        except KeyError:
          self.results[run.year][run.tck] = {}
          self.results[run.year][run.tck]["up"] = 0.
          self.results[run.year][run.tck]["down"] = 0.
          self.results[run.year][run.tck][run.mag] += run.lumi
      except KeyError:
        self.results[run.year] = {}
        self.results[run.year][run.tck] = {}
        self.results[run.year][run.tck]["up"] = 0.
        self.results[run.year][run.tck]["down"] = 0.
        self.results[run.year][run.tck][run.mag] += run.lumi

  def __repr__(self):
    return "RunCounter()"
  def __str__(self):
    return "RunCounter(%s)"%(self.results)

  def summaryByYear(self):
    print ""
    for year,tckarr in self.results.iteritems():
      magsum = {}
      for tck,magarr in tckarr.iteritems():
        for mag,lumi in magarr.iteritems():
          try:
            magsum[mag] += lumi
          except KeyError:
            magsum[mag] = lumi
      print "{0:<10}  Down: {1:<12.8f} Up: {2:<12.8f} Total: {3:<12.8f}".format(year,magsum["down"]*1e-9,magsum["up"]*1e-9,(magsum["down"]+magsum["up"])*1e-9)

  def summaryByTck(self):
    print ""
    tcksum = {}
    for year,tckarr in self.results.iteritems():
      for tck,magarr in tckarr.iteritems():
        for mag,lumi in magarr.iteritems():
          try:
            tcksum[tck][mag] += lumi
          except KeyError:
            try:
              tcksum[tck]["up"] = 0.
              tcksum[tck]["down"] = 0.
              tcksum[tck][mag] += lumi
            except KeyError:
              tcksum[tck] = {}
              tcksum[tck]["up"] = 0.
              tcksum[tck]["down"] = 0.
              tcksum[tck][mag] += lumi
    for tck,mararr in tcksum.iteritems():
      print "{0:<10}  Down: {1:<12.8f} Up: {2:<12.8f} Total: {3:<12.8f}".format(tck,mararr["down"]*1e-9,mararr["up"]*1e-9,(mararr["down"]+mararr["up"])*1e-9)

  def allTcks(self):
    tcks = []
    for year,tckarr in self.results.iteritems():
      for tck,magarr in tckarr.iteritems():
        if tck not in tcks:
          tcks.append(tck)
    tcks.sort()
    return tcks

  def tckYear(self,targetTck):
    for year,tckarr in self.results.iteritems():
      for tck,magarr in tckarr.iteritems():
        if targetTck == tck:
          return year

  def allHlt2Lines(self):
    hltLines = []
    for tck in self.allTcks():
      for line in self.hlt.getHlt2Lines(tck):
        if line not in hltLines:
          hltLines.append(line)

    return hltLines

  def allHlt1Lines(self):
    hltLines = []
    for tck in self.allTcks():
      for line in self.hlt.getHlt1Lines(tck):
        if line not in hltLines:
          hltLines.append(line)

    return hltLines

  def summaryByHltLines(self,hltLines=None,hltLevel=2,year=None,magnet=None):
    print ""
    getAllHltLines = {
      1: self.allHlt1Lines,
      2: self.allHlt2Lines
      }
    activeHltLine = {
      1: self.hlt.hlt1lineActive,
      2: self.hlt.hlt2lineActive
      }
    if hltLines == None:
      hltLines = getAllHltLines[hltLevel]()
    lumi_sum = {}
    scale_avg = {}
    for line in hltLines:
      lumi_sum[line] = {True:0.,False:0.}
      scale_avg[line] = {}
      scale_avg[line]['prescale'] = 0.
      scale_avg[line]['postscale'] = 0.
      scale_avg[line]['lumi'] = 0.
      for yr,tckarr in self.results.iteritems():
        if year != None:
          if year != yr:
            continue
        for tck,magarr in tckarr.iteritems():
          pre = self.hlt.getHltScaler(tck,line,"Pre")
          post = self.hlt.getHltScaler(tck,line,"Post")
          active = activeHltLine[hltLevel](tck,line)
          for mag,lumi in magarr.iteritems():
            if magnet == None:
              lumi_sum[line][active] += lumi
              if active:
                scale_avg[line]['lumi'] += lumi
                scale_avg[line]['prescale'] += lumi*pre
                scale_avg[line]['postscale'] += lumi*post
            else:
              if magnet == mag:
                lumi_sum[line][active] += lumi
                if active:
                  scale_avg[line]['lumi'] += lumi
                  scale_avg[line]['prescale'] += lumi*pre
                  scale_avg[line]['postscale'] += lumi*post
      if scale_avg[line]['lumi'] != 0.:
        scale_avg[line]['prescale'] /= scale_avg[line]['lumi']
        scale_avg[line]['postscale'] /= scale_avg[line]['lumi']
      #print "'%sRunFrac':%f,"%(line,(lumi_sum[line][True]/(lumi_sum[line][True]+lumi_sum[line][False])))
      print "{0:<60}  Active: {1:<12.8f} Not active: {2:<12.8f}  PreScale: {3:<12.8f} PostScale: {4:<12.8f}".format(line,lumi_sum[line][True]*1e-9,lumi_sum[line][False]*1e-9,scale_avg[line]['prescale'],scale_avg[line]['postscale'])

  def lineSummary(self,hltLines,hltLevel=2,year=None,magnet=None):
    print ""
    activeHltLine = {
      1: self.hlt.hlt1lineActive,
      2: self.hlt.hlt2lineActive
      }
    lumi_sum = {}
    scale_avg = {}
    for line in hltLines:
      print line
      for yr,tckarr in self.results.iteritems():
        if year != None:
          if year != yr:
            continue
        for tck,magarr in tckarr.iteritems():
          pre = self.hlt.getHltScaler(tck,line,"Pre")
          post = self.hlt.getHltScaler(tck,line,"Post")
          active = activeHltLine[hltLevel](tck,line)
          for mag,lumi in magarr.iteritems():
            if magnet == None:
              if lumi != 0.:
                print "{0:<4}  TCK: {1:<10}  Active: {2:<5}  Magnet: {3:<4}  PreScale: {4:<6.4f}  PostScale: {5:<6.4f}  Lumi: {6:<10.8f}".format(yr,tck,"True" if active else "False",mag,pre,post,lumi*1e-9)
            else:
              if magnet == mag:
                if lumi != 0.:
                  print "{0:<4}  TCK: {1:<10}  Active: {2:<5}  Magnet: {3:<4}  PreScale: {4:<6.4f}  PostScale: {5:<6.4f}  Lumi: {6:<10.8f}".format(year,tck,"True" if active else "False",mag,pre,post,lumi*1e-9)


  def checkTriggerPropities(self,arr):
    tcks = self.allTcks()
    cuts = {}
    for line,leaf,prop in arr:
      name = leaf + "__" + prop
      print ""
      print name
      cuts[name] = []
      total = 0.
      for tck in tcks:
        active = self.hlt.hlt2lineActive(tck,line) if "Hlt2" in line else self.hlt.hlt1lineActive(tck,line)
        if not active:
          continue
        pre = self.hlt.getHltScaler(tck,line,"Pre")
        post = self.hlt.getHltScaler(tck,line,"Post")
        year = self.tckYear(tck)
        lumi = self.results[year][tck]["down"] + self.results[year][tck]["up"]
        total += lumi
        m = md5.new()
        cuts[name].append( self.hlt.getTriggerProperty(tck,leaf,prop) )
        m.update(cuts[name][-1])
        print "{0:<4}  TCK: {1:<10}  Active: {2:<5}  PreScale: {3:<6.4f}  PostScale: {4:<6.4f}  Lumi: {5:<10.8f}  Total: {6:<10.8f}  Cuts: {7}".format(year,tck,"True" if active else "False",pre,post,lumi*1e-9,total*1e-9,m.hexdigest()+" "+cuts[name][-1].replace(" ",""))



  def summaryByHlt1Lines(self,hltLines=None):
    self.summaryByHltLines(hltLevel=1)

  def summaryByHlt2Lines(self,hltLines=None):
    self.summaryByHltLines(hltLevel=2)

  def summary(self):
    self.summaryByYear()
    self.summaryByTck()
    self.summaryByHlt1Lines()
    self.summaryByHlt2Lines()


class HltInterface:
  def __init__(self):
    self.tckList = {}
    self.hlt1LineList = {}
    self.hlt2LineList = {}
    self.hltScales = {}
    self.configTrees = {}
    for name, tckClass in TckUtils.getConfigurations().iteritems():
      for tckInt in tckClass.info['TCK']:
        tck = "0x{0:0>8x}".format(tckInt)
        self.tckList[tck] = { "hlttype":tckClass.info["hlttype"],
                              "label":tckClass.info["label"],
                              "release":tckClass.info["release"],
                              "id":tckClass.info["id"] }

  def getHlt1Lines(self,tck):
    try:
      return self.hlt1LineList[tck]
    except KeyError:
      try:
        result = TckUtils.getHlt1Lines(int(tck,16))
      except TypeError:
        result = []
      self.hlt1LineList[tck] = [r.replace("Hlt::Line/","") for r in result]
      return self.hlt1LineList[tck]

  def getHlt2Lines(self,tck):
    try:
      return self.hlt2LineList[tck]
    except KeyError:
      try:
        result = TckUtils.getHlt2Lines(int(tck,16))
      except TypeError:
        result = []
      self.hlt2LineList[tck] = [r.replace("Hlt::Line/","") for r in result]
      return self.hlt2LineList[tck]

  def getHltScaler(self,tck,line,position="Pre"):
    if position not in ["Pre","Post"]:
      raise ValueError
    name = line+position+"Scaler"
    try:
      return self.hltScales[tck][name]
    except KeyError:
      #result = 1.
      try:
        self.hltScales[tck]
        return 1.0
      except KeyError:
        self.hltScales[tck] = {}
        try:
          result = TckUtils.getProperties(int(tck,16),".*/.*Scaler","AcceptFraction")
          for iline, h in result.iteritems():
            try:
              self.hltScales[tck][iline] = float(h["AcceptFraction"])
            except ValueError:
              self.hltScales[tck][iline] = 1.
        except TypeError:
          pass
        try:
          return self.hltScales[tck][name]
        except KeyError:
          #print self.hltScales
          #print tck,name
          return 1.0
          #raise ValueError

      return float(result)

  def hlt1lineActive(self,tck,line):
    return (line in self.getHlt1Lines(tck)) and (self.getHltScaler(tck,line) != 0.)

  def hlt2lineActive(self,tck,line):
    return (line in self.getHlt2Lines(tck)) and (self.getHltScaler(tck,line) != 0.)

  def getTree(self,tck):
    try:
      return self.configTrees[tck]
    except KeyError:
      #print tck, int(tck,16)
      self.configTrees[tck] = TckUtils.getConfigTree( int(tck,16) )
      return self.configTrees[tck]

  def getTriggerProperty(self,tck,leaf,prop):
    try:
      return self.getTree(tck).leafs()[leaf].properties()[prop]
    except KeyError:
      return "Trigger not run"
    except TypeError:
      return "No TCK?"

  def __repr__(self):
    return "HltInterface()"
  def __str__(self):
    return "HltInterface()"




def runIsValid(run):
  if not run["LHCState"] == "PHYSICS":
    print "LHCState not PHYSICS", run["LHCState"]
    return False
  if not run["veloPosition"] == "Closed":
    print "velo not Closed", run["veloPosition"]
    return False
  if not run["state"] == "IN BKK":
    print "state not IN BKK", run["state"]
    return False
  if not run["destination"] == "OFFLINE":
    print "destination not OFFLINE", run["destination"]
    return False
  if not run["partitionname"] == "LHCb":
    print "partitionname not LHCb", run["partitionname"]
    return False
  if not "COLLISION" in run["runtype"]:
    print "COLLISION not in runtype:", run["runtype"]
    return False

  #if not run["runtype"] == ("COLLISION"+run["starttime"][2:4]):
    #print "runtype not COLLISION:", run["runtype"]
    #return False

  magState = run["magnetState"].lower()
  if not (magState == "up" or magState == "down"):
    print "magnetState not up or down", run["magnetState"]
    return False

  if int(run["tck"]) < 0:
    print "tck is negative", run["tck"]
    return False

  return True


def getRun(run,cache):
  try:
    result = cache[run]
    #print "Found cached run %i" %(run)
  except KeyError:
    url = 'http://lbrundb.cern.ch/api/run/%i/'%(run)
    print "getting", url
    data = urllib2.urlopen(url)
    result = json.load(data)
    cache[run] = result
  return result

def getRuns(firstRun=90613,lastRun=134455):
  pickle_file = open("runbd.pkl", 'rb')
  cache = pickle.load(pickle_file)
  pickle_file.close()

  allRuns = []

  first = getRun(firstRun,cache)
  if runIsValid(first):
    allRuns.append(Run(first))

  nRuns = 1
  nextId = allRuns[-1].nextRunId
  while nextId <= lastRun:
    run = getRun(nextId,cache)
    nextId = run["next_runid"]
    if runIsValid(run):
      try:
        allRuns.append(Run(run))
      except ValueError:
        print "ERROR: unable to parse time string of run %i" % (run["runid"])
      except KeyError:
        print "ERROR: json from run DB missing propities:", run
      nRuns += 1

  pickle_file = open("runbd.pkl", 'wb')
  pickle.dump(cache,pickle_file)
  pickle_file.close()

  return allRuns

if __name__ == "__main__":

  print "Downloading or loading cache of runs, this may take a while"
  runs = getRuns()
  summer = RunCounter()

  #print runs
  for r in runs:
    summer.add(r)
    #print r.id, r.year, r.tck, r.lumi

  summer.summary()
  #summer.lineSummary(["Hlt2B2HHLTUnbiased","Hlt2Topo2BodyBBDT"])
  #summer.summaryByHlt2Lines(magnet="down",year=2012)
  #summer.summaryByHlt2Line(["Hlt2TopoMu2BodyBBDT","Hlt2SingleMuon","Hlt2CharmHadD02HHXDst_LeptonhhX","Hlt2CharmHadD02HH_D02PiPi","Hlt2CharmHadD02HH_D02KPi","Hlt2CharmHadD02HH_D02KK"])

  summer.checkTriggerPropities([
    ("Hlt1TrackMuon", "Hlt1TrackMuonL0DUFilter", "Code"),
    ("Hlt1TrackMuon", "GECLooseUnit", "Code"),
    ("Hlt1TrackMuon", "HltPV3D", "Code"),
    ("Hlt1TrackMuon", "Hlt1TrackMuonUnit", "Code"),

    ("Hlt1TrackAllL0","HltPV3D","Code"),
    ("Hlt1TrackAllL0","GECLooseUnit","Code"),
    ("Hlt1TrackAllL0","Hlt1TrackAllL0Unit","Code"),

    ("Hlt2Dst2PiD02KPi","Hlt2Dst2PiD02KPiPreScaler","AcceptFraction"),
    ("Hlt2Dst2PiD02KPi","Hlt2Dst2PiD02KPiHltFilter","Code"),
    ("Hlt2Dst2PiD02KPi","HltPV3D","Code"),
    ("Hlt2Dst2PiD02KPi","Hlt2Dst2PiD02KPiKPi","CombinationCut"),
    ("Hlt2Dst2PiD02KPi","Hlt2Dst2PiD02KPiKPi","MotherCut"),
    ("Hlt2Dst2PiD02KPi","Hlt2Dst2PiD02KPiKPi","DaughtersCuts"),

    ("Hlt2Dst2PiD02PiPi","Hlt2Dst2PiD02PiPiPreScaler","AcceptFraction"),
    ("Hlt2Dst2PiD02PiPi","Hlt2Dst2PiD02PiPiHltFilter","Code"),
    ("Hlt2Dst2PiD02PiPi","HltPV3D","Code"),
    ("Hlt2Dst2PiD02PiPi","HHlt2Dst2PiD02PiPiPiPi","CombinationCut"),
    ("Hlt2Dst2PiD02PiPi","HHlt2Dst2PiD02PiPiPiPi","MotherCut"),
    ("Hlt2Dst2PiD02PiPi","HHlt2Dst2PiD02PiPiPiPi","DaughtersCuts"),

    #("Hlt2CharmHadD02HH_D02PiPi", "Hlt2CharmHadD02HHPionsFilter", "Code"),
    #("Hlt2CharmHadD02HH_D02PiPi", "Hlt2CharmHadD02HH_D02PiPiCombine", "CombinationCut"),
    #("Hlt2CharmHadD02HH_D02PiPi", "Hlt2CharmHadD02HH_D02PiPiCombine", "MotherCut"),
    #("Hlt2CharmHadD02HH_D02PiPi", "Hlt2CharmHadD02HH_D02PiPiFilter", "Code"),
    ])

  summer.summary()
  summer.lineSummary(["Hlt2Dst2PiD02KPi", "Hlt2Dst2PiD02PiPi", "Hlt2Dst2PiD02EMu"])


