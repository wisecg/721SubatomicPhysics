""" 
	PHYS 721, HW 3
	Clint Wiseman
	9/8/15

	1. Fit the m12 histogram from the 8/28 Homework to a Breit-Wigner curve. 

	Breit-Wigner distribution:
	// Calculate a Breit Wigner function with mean and gamma.
	Double_t bw = gamma/((x-mean)*(x-mean) + gamma*gamma/4);
	return bw/(2*Pi());
	
	Reference: https://root.cern.ch/phpBB3/viewtopic.php?t=12596

	Reference: http://wlav.web.cern.ch/wlav/pyroot/recipes.html
"""
import math
from ROOT import TCanvas, TPad, TH1F, TFile, TF1, TMath

# open the file from last week
inputfile = TFile( 'py-hw2.root' )
h1 = inputfile.Get('h1')
h1.Draw()

# create a function for fitting
class BreitWigner:
   def __call__( self, x, par ):
      return (par[1]/((x[0]-par[0])**2. + (par[1]**2.)/4))/(2*math.pi)

fit = TF1( 'lin', BreitWigner(), -1., 1., 2 )
fit.SetParameter(0,1.05)
fit.SetParameter(1,0.01)

"""
# cheater method
#bw = TF1( 'myfunc','TMath::BreitWigner(x,[0],[1])', 0, 2)
#bw.SetParameter(0,1.05)
#bw.SetParameter(1,0.01)
"""
# fit the histo 
h1.Fit( fit )

# print results
par = fit.GetParameters()
print 'fit results: p0 =', par[0], ', p1 =', par[1]

#pass the fit results into the title
par = fit.GetParameters()
title = "m12: Breit-Wigner. Mean: %G  Gamma: %G" % (par[0],par[1])
h1.SetTitle(title)