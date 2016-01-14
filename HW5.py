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


	for reference: hSum = TH1F('h1', 'E1', 1000, 0.3, 1.3)
"""
import math
import ROOT
from ROOT import TCanvas, TPad, TH1F, TFile, TF1, TMath

# breit-wigner, normalized
bw = ROOT.TF1('bw','([1]/2*TMath::Pi()) * (1 / ((x-[0])**2. + ([1]**2.)/4))',0.99,1.09) #1.0,1.05)
bw.SetParameters(1.019461, 0.00426) # [0]=m_phi, [1]=gamma_phi
N = bw.Integral(-1000,1000)
bw_N = ROOT.TF1('bw_N','(1/[2]) * (([1]/2*TMath::Pi()) * (1 / ((x-[0])**2. + ([1]**2.)/4)))',1.0,1.05)
bw_N.SetParameters(1.019461, 0.00426, N) # [2]=normalization const.
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
mdw_par = mdw_N.GetParameters()
mdw_area = mdw_N.Integral(-1000,1000)
mdw_max = mdw_N.GetMaximumX()
print "MDW: Max: %.8f  Area: %G" % (mdw_max, mdw_area)

#c1 = ROOT.TCanvas()
#c1.cd()
#gStyle.SetOptFit(0111)

# open the file with the m12 histogram
# for reference: hSum = TH1F('h1', 'E1', 1000, 0.3, 1.3)

inputfile = TFile( 'py-hw2.root' )
h1 = inputfile.Get('h1')
#h1.Rebin(1) #bw rebin: 10, rbw rebin:
h1.GetXaxis().SetRange(600,900)
#h1.Draw()

# fit the histo to the normalized curves to avoid rebinning the histo.
h1.Fit( bw_N , "LI")  #LI is maximum likelihood
#h1.Fit( rbw_N , "LI")  
#h1.Fit( mdw_N , "LI",)  

par = bw_N.GetParameters()
title = "m12: MDW-Breit-Wigner. Mean: %G  Gamma: %G" % (par[0],par[1])
h1.SetTitle(title)
h1.GetXaxis().SetTitle("E (GeV)");