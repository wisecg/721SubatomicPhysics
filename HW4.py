""" 
   PHYS 721, HW 4
   Clint Wiseman
   9/14/15

   Consider again the Breit-Wigner curves for the decay Phi -> K^+ K^-
   The charged kaons each have a mass of 0.493677 GeV. 
   The nominal mass of the Phi meson is 1.019461 GeV, and the nominal width is 4.26 MeV.

   1. Plot three curves, all normalized so that they integrate to 1, depicting the mass of this meson. 
      1) Non-relativistic Breit-Wigner. 
      2) Relativistic Breit-Wigner. 
      3) Relativistic Breit-Wigner with a mass-dependent width

   2.* Find numerically or otherwise, and to high precision, the maximum value and FWHM of each curve.
"""
import ROOT

canvas = ROOT.TCanvas()
#canvas.Print('test1.png')

# breit-wigner, normalized
bw = ROOT.TF1('bw','([1]/2*TMath::Pi()) * (1 / ((x-[0])**2. + ([1]**2.)/4))',1.0,1.05)
bw.SetParameters(1.019461, 0.00426) # [0]=m_phi, [1]=gamma_phi
N = bw.Integral(-1000,1000)
print N
bw_N = ROOT.TF1('bw_N','(1/[2]) * (([1]/2*TMath::Pi()) * (1 / ((x-[0])**2. + ([1]**2.)/4)))',1.0,1.05)
bw_N.SetParameters(1.019461, 0.00426, N) # [2]=normalization const.
bw_N.Draw('C')
bw_N.GetHistogram().GetYaxis().SetTitle("");
bw_N.GetHistogram().SetTitle("")
bw_N.GetHistogram().GetXaxis().SetTitle("E (GeV)");
bw_par = bw_N.GetParameters()
bw_area = bw_N.Integral(-1000,1000)
bw_max = bw_N.GetMaximumX()
bw_fwhm = bw_par[1]  # gamma
print " BW: Max: %.8f  FWHM: %.15f  Area: %G " % (bw_max, bw_fwhm, bw_area)

# relativistic breit-wigner
rbw = ROOT.TF1('rbw','1/((x**2 - [0]**2)**2 + [0]**2 * [1]**2)',1.0,1.05)
rbw.SetParameters(1.019461, 0.00426) # [0]=m_phi, [1]=gamma_phi
N = rbw.Integral(-1000,1000)
rbw_N = ROOT.TF1('rbw_N','(1/[2])*(1/((x**2 - [0]**2)**2 + [0]**2 * [1]**2))',1.0,1.05)
rbw_N.SetParameters(1.019461, 0.00426, N) # [2]=normalization const.
#rbw_N.Draw('C')
#rbw_N.GetHistogram().GetYaxis().SetTitle("");
#rbw_N.GetHistogram().SetTitle("")
#rbw_N.GetHistogram().GetXaxis().SetTitle("E (GeV)");
rbw_par = rbw_N.GetParameters()
rbw_area = rbw_N.Integral(-1000,1000)
rbw_max = rbw_N.GetMaximumX()
rbw_fwhm = rbw_par[0]*((1+(rbw_par[1]/rbw_par[0]))**(1./2.) - (1-(rbw_par[1]/rbw_par[0]))**(1./2.))   
print "RBW: Max: %.8f  FWHM: %.15f  Area: %G" % (rbw_max, rbw_fwhm, rbw_area)

# relativistic breit-wigner, mass-dependent width
mdw = ROOT.TF1('mdw','((x**2 - [0]**2)**2 + [0]**2 * [1]**2 * (((x/2)**2 - [2]**2) / (([0]/2)**2 - [2]**2))**3)**(-1)',1.0,1.05)
mdw.SetParameters(1.019461, 0.00426, 0.493677) # [0]=m_phi, [1]=gamma_phi, [2]=m_kaon
N = mdw.Integral(-1000,1000)
mdw_N = ROOT.TF1('rbw_mdw','(1/[3])*((x**2 - [0]**2)**2 + [0]**2 * [1]**2 * (((x/2)**2 - [2]**2) / (([0]/2)**2 - [2]**2))**3)**(-1)',1.0,1.05)
mdw_N.SetParameters(1.019461, 0.00426, 0.493677, N) # [3]=normalization const.
#mdw_N.Draw('C')
#mdw_N.GetHistogram().GetYaxis().SetTitle("");
#mdw_N.GetHistogram().SetTitle("")
#mdw_N.GetHistogram().GetXaxis().SetTitle("E (GeV)");
mdw_par = mdw_N.GetParameters()
mdw_area = mdw_N.Integral(-1000,1000)
mdw_max = mdw_N.GetMaximumX()
print "MDW: Max: %.8f  Area: %G" % (mdw_max, mdw_area)

# now for fun, switch to using python functions with paramters passed in ...

# mass-dependent gamma
def gamma( x, par ): # must pass in par even though we don't use it here.
   import math
   m_phi_0 = 1.019461
   gamma_0 = 0.00426
   m_kaon = 0.493677

   # python can't handle taking square roots of negative numbers ...
   if (((x[0]/2)**2 - m_kaon**2) > 0) : 
      p = math.sqrt((x[0]/2)**2 - m_kaon**2)
      p0 = math.sqrt( (m_phi_0/2)**2. - m_kaon**2 )
      gamma = gamma_0*(p/p0)**3
   else: 
      gamma = 0
   return gamma

gamma = ROOT.TF1( 'gamma', gamma, 0, 10, 4 )
#gamma.Draw()

# mass-dependent fwhm
def fwhm ( x, par ):
   import math
   m_phi_0 = 1.019461
   if (1 - gamma(x,par)/m_phi_0 > 0):
      arg1 = math.sqrt(1 + gamma(x,par)/m_phi_0)
      arg2 = math.sqrt(1 - gamma(x,par)/m_phi_0)
      fwhm = m_phi_0*(arg1 - arg2) 
   else :
      fwhm = 0
   return fwhm

fwhm = ROOT.TF1( 'fwhm', fwhm, 0.8, 2, 4 )
#fwhm.Draw()
#fwhm.GetHistogram().GetYaxis().SetTitle("FWHM");
#fwhm.GetHistogram().GetXaxis().SetTitle("mass (energy of phi_0)");

# beta of outgoing kaons
