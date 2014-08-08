

def varAtLimit(var,p):
  if var.Class().GetName() == "RooCategory":
    return False
  else:
    r = var.getMax() - var.getMin()
    if r == 0.:
      print var.GetName()
      sys.exit("Variable "+var.GetName()+" has no range!")
    v = var.getVal() - var.getMin()
    if v/r < p:
      return True
    elif v/r > 1.-p :
      return True
    else:
      return False


def varErrorAtLimit(var,p):
  if var.Class().GetName() == "RooCategory":
    return False
  else:
    r = var.getMax() - var.getMin()
    v = var.getVal() - var.getMin()
    e = var.getError()*p
    if v+e > r or v-e < 0.:
      return True
    else:
      return False

def printLimitResults(varList,descr,important):
  if len(varList)==0:
    print "No vars "+descr
  else:
    print ""
    if important:
      print " ===== VARS " + descr.upper() + " ====="
    else:
      print " --- vars " + descr + " ---"
    print ""
    for i in varList:
      i.Print()
    print ""

def checkVarRanges(w):
  allVars = w.obj("Final_PDF").getParameters(getattr(w,"set")("args"))
  i = allVars.createIterator()
  noRange = []
  while True:
    var = i.Next()
    if not var:
      break
    if var.isConstant():
      continue
    if var.ClassName() == "RooCategory":
      continue
    if var.getMin() == var.getMax():
      noRange.append(var)
  if len(noRange) == 0:
    print "No variables with zero range"
  else:
    print ""
    print ""
    print " >>> Vars with zero range <<<"
    print ""
    for var in noRange:
      print var.GetName(), "has limits", var.getMin(), "to", var.getMax()
    sys.stdout.flush()
    sys.exit("Variables cant have zero range")


def checkResultLimit(result):
  varList = result.floatParsFinal()
  i = varList.createIterator()
  atlim=[]
  while True:
    var = i.Next()
    if not var:
      break
    if var.isConstant():
      continue
    if varAtLimit(var,0.0025):
      atlim.append(var)
  return len(atlim)

def checkVarChange(result):
  varList = result.floatParsFinal()
  varListStart = result.floatParsInit()
  i = varList.createIterator()
  varChange={}
  while True:
    var = i.Next()
    if not var:
      break
    if var.isConstant():
      continue
    varChange[var.GetName()] = (varListStart.find(var.GetName()).getVal()-var.getVal())/var.getError()

  for name,val in varChange.iteritems():
    print "{:<30}{:< 10.2f}".format(name,val)
  return varChange



def checkVarLimits(w):
  allVars = w.obj("Final_PDF").getParameters(getattr(w,"set")("args"))
  i = allVars.createIterator()
  atlim = []
  closelim = []
  onesigma=[]
  twosigma=[]
  threesigma=[]
  while True:
    var = i.Next()
    if not var:
      break
    if var.isConstant():
      continue
    if varAtLimit(var,0.01):
      atlim.append(var)
    if varAtLimit(var,0.1):
      closelim.append(var)
    if varErrorAtLimit(var,1):
      onesigma.append(var)
    if varErrorAtLimit(var,3):
      twosigma.append(var)
    if varErrorAtLimit(var,10):
      threesigma.append(var)
  printLimitResults(atlim,"at limit",True)
  printLimitResults(closelim,"close to limit",False)
  printLimitResults(onesigma,"one error from limit",True)
  printLimitResults(twosigma,"three errors from limit",False)
  printLimitResults(threesigma,"ten errors from limit",False)


def printVarLimits(w):
  allVars = w.obj("Final_PDF").getParameters(getattr(w,"set")("args"))
  #allVars = w.obj("Final_PDF").getParameters(ds)
  print " == Var Limits == "
  i = allVars.createIterator()
  while True:
    var = i.Next()
    if not var:
      break
    if var.Class().GetName() == "RooCategory":
      continue
    if var.isConstant():
      continue
    var.Print()
  print ""
  print " == Constant vars == "
  i = allVars.createIterator()
  while True:
    var = i.Next()
    if not var:
      break
    if var.Class().GetName() == "RooCategory":
      continue
    if not var.isConstant():
      continue
    var.Print()
  print ""



def printSetVarLimits(w):
  allVars = w.obj("Final_PDF").getParameters(getattr(w,"set")("args"))
  print " == Set Var Limits == "
  i = allVars.createIterator()
  while True:
    var = i.Next()
    if not var:
      break
    if var.Class().GetName() == "RooCategory":
      continue
    if var.isConstant():
      continue
    print "w.obj('"+var.GetName()+"').setMin("+str(var.getMin())+") ; w.obj('"+var.GetName()+"').setMax("+str(var.getMax())+")\nw.obj('"+var.GetName()+"').setVal("+str(var.getVal())+") ; w.obj('"+var.GetName()+"').setError("+str(var.getError())+")\nw.obj('"+var.GetName()+"').setConstant("+ ("True" if var.isConstant() else "False") +")"
  print ""

def checkTitles(w):
  allVars = w.obj("Final_PDF").getParameters(getattr(w,"set")("args"))
  out = []
  i = allVars.createIterator()
  while True:
    var = i.Next()
    if not var:
      break
    if var.Class().GetName() == "RooCategory":
      continue
    if var.isConstant():
      continue
    if var.GetTitle() != var.GetName():
      continue
    out.append( "w.obj('"+var.GetName()+"').SetTitle('') " )
  if len(out)>0:
    print " == Check Var Titles == "
    for line in out:
      print line
  else:
    print "No vars need titles"
  print ""



def printSetVarConst(w):
  allVars = w.obj("Final_PDF").getParameters(getattr(w,"set")("args"))
  print " == Set Var Const == "
  i = allVars.createIterator()
  while True:
    var = i.Next()
    if not var:
      break
    if var.Class().GetName() == "RooCategory":
      continue
    if var.isConstant():
      continue
    print "w.obj('"+var.GetName()+"').setConstant(True)"
  print ""



# Helper function for printing values and errors to the correct sig figures
def texround(v):
    err1="%s" % float("%.1g" % v.getError())
    err="%s" % float("%.2g" % v.getError())
    if err1==err:
        err=err+"0"
    alen=len(err)-2
    val=round(v.getVal(),alen)
    return "( %s & $\\pm$ & " % val + err + ")"

# Helper function for printing values and errors in a latex table
def textify(v):
    aname=v.GetName().replace("_","\\_")

    return aname+" & "+ v.GetTitle() +" & "+texround(v) +" \\\\ "

# Print all fitted values in a latex table
def printTexRes(r):
  vars=r.floatParsFinal()
  for i in range(vars.getSize()):
    print textify(vars[i])



