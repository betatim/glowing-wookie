

from ROOT import RooRealIntegral

def calculate(pdf,args,region=""):
  inte = RooRealIntegral("inte", "inte", pdf, args, 0, 0, region)
  return inte.getVal()
