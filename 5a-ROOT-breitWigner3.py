""" 
   PHYS 721, HW 5
   Clint Wiseman
   9/21/15

   1. Fit the m12 histogram from the 8/28 Homework to the three Breit-Wigner
      curves in HW4.
   2.* Which curve fits the best and how can you tell? How many events would you need to tell 
      that the data prefer each curve as opposed to the other two? 
   3.** Repeat problem 2 in the presence of background events equal in number to signal events 
      and distributed according to a second-order polynomial in the range [0.99, 1.09] GeV. 
      Pick reasonable values for the polynomial coefficients. 

   par[0] : normalization factor
   par[1] : m_0, the pion mass 
   par[2] : gamma_0, the width (without mass dependence)
"""

import ROOT, math
from ROOT import TFile, TF1

m12min = 0.9
m12max = 1.1

# breit-wigner
def breit (x,par):
   a = x[0]-par[1]
   b = 0.5*par[2]
   return par[0]/(a**2. + b**2.)

bw = TF1('bw',breit,m12min,m12max,4)
bw.SetParameters(1,1.019,0.00426)

# relativistic breit-wigner
def relbreit(x,par):
   a = x[0]**2. - par[1]**2.
   b = par[1]*par[2]
   c = par[1]*math.sqrt(par[1]**2.+par[2]**2.)
   d = (2*math.sqrt(2)/math.pi)*(par[1]*par[2]*c)
   e = d/math.sqrt(par[1]**2.+c)
   return par[0]*e/(a**2. + b**2.)

rbw = TF1('rbw',relbreit,m12min,m12max,4)
rbw.SetParameters(0.5,1.019,0.00426)

# relativistic breit-wigner, mass-dependent gamma (width)
# gamma is imaginary for x < 1
def md_relbreit(x,par):
   m_kaon = 0.493677

   if ((((par[1]/2)**2. - m_kaon**2.) < 0) or (((x[0]/2)**2. - m_kaon**2.) < 0)):
      print 0, par[0], par[1], par[2]
      result = 0
   else:
      p = math.sqrt(((x[0])/2)**2. - m_kaon**2.)
      p0 = math.sqrt((par[1]/2)**2 - m_kaon**2.)
      gamma = par[2]*(p/p0)**3.
      print gamma
      par2_save = par[2]
      par[2] = gamma
      temp = relbreit(x,par)
      par[2] = par2_save
      result = temp
   return result

md_rbw = TF1('md_rbw',md_relbreit,m12min,m12max,4)
md_rbw.SetParameters(0.5,1.019,0.00426)
md_rbw.Draw()

# ********************

# for reference, in HW2 I used:
# hSum = TH1F('h1', 'E1', 1000, 0.3, 1.3)

inputfile = TFile( 'py-hw2.root' )
h1 = inputfile.Get('h1')
h1.GetXaxis().SetTitle("E (GeV)");
h1.GetXaxis().SetRange(601,900)

h1.Fit(md_rbw)  
pars = md_rbw.GetParameters()
title = "MD-RBW. M:%G  G:%G  Chi2/NDF:%G" % (pars[1],pars[2],md_rbw.GetChisquare()/md_rbw.GetNDF())
h1.SetTitle(title)
