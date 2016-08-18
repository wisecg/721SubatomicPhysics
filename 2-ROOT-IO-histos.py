""" 
	PHYS 721, HW 2
	Clint Wiseman
	8/29/15

	1. Histogram the values in the first column of the file. Label the x-axis E (GeV).
	2. Consider each row (each line) of the file to be two 4-momenta: (E1, px1, py1, pz1) and (E2, px2, py2, pz2). 
	Histogram the masses of each. Histogram the mass of the sum of the two 4-momenta.

	Reference: https://python4astronomers.github.io/files/asciifiles.html

	Usage: 
	$: python HW2.py
		The TCanvas will disappear from the display once the script is finished
	$: python
	>>> execfile("HW2.py")
		This will display the TCanvas.
	$: python
	>>> import ROOT
	>>> tb = ROOT.TBrowser()  <-- to browse output
"""
import math
from ROOT import TCanvas, TPad, TH1F, TFile

# A smarter program might scan the file FIRST, 
# and automatically determine the appropriate ranges and binning.
hE1 = TH1F('hE1', 'hE1', 300, 0, 3) # 0.01 GeV/bin
hM1 = TH1F('hM1', 'hM1', 1000, 0.4, 0.6) # 0.001 GeV/bin
hM2 = TH1F('hM2', 'hM2', 1000, 0.4, 0.6)
hSum = TH1F('h1', 'E1', 1000, 0.3, 1.3)

# For speed, "bind and cache" the Fill member functions,
# Not necessary, but cool.
histos = [ 'hE1', 'hM1', 'hM2', 'hSum' ]
for name in histos:
   exec '%sFill = %s.Fill' % (name,name)

# Scan the input file line-by-line (don't keep it in memory).
# By using "with" we don't need a file.close() at the end.
with open('DB1.txt') as file:

	# Can read and ignore header lines if necessary
	#header1 = file.readline()
	#header2 = file.readline()

	for line in file:

		# strip special characters, split, and convert to floats
	    line = line.strip()
	    col = line.split()
	    E1  = float(col[0])
	    px1 = float(col[1])
	    py1 = float(col[2])
	    pz1 = float(col[3])
	    E2  = float(col[4])
	    px2 = float(col[5])
	    py2 = float(col[6])
	    pz2 = float(col[7])

	    #print "1st: %G %G %G %G   2nd: %G %G %G %G" % (E1, px1, py1, pz2, E2, px2, py2, pz2)
	    #output = "{0:<10.5f} {1:<10.5f} {2:<10.5f} {3:<10.5f} {4:<10.5f} {5:<10.5f} {6:<10.5f} {7:<10.5f}"
	    #print output.format(E1, px1, py1, pz2, E2, px2, py2, pz2)
	    
	    m1 = (E1**2 - px1**2 - py1**2 - pz1**2)**(1.0/2.0)
	    m2 = (E2**2 - px2**2 - py2**2 - pz2**2)**(1.0/2.0)
	    mSum = (m1**2 + m2**2 + 2*((E1*E2) - (px1*px2) - (py1*py2) - (pz1*pz2)))

	    #print type(E1),m1,m2,mSum
	    
	    hE1Fill(E1)
	    hM1Fill(m1)
	    hM2Fill(m2)
	    hSumFill(mSum)

# Create TCanvas to display 4 plots in one.
# I should be able to use TCanvas.Divide, 
# but I couldn't get it to work in Python.

c1 = TCanvas( 'c1', 'Data Bank 1', 900, 700 )
p1 = TPad( 'pad1', 'pad1',  0, 0.5, 0.5, 1 )
p2 = TPad( 'pad2', 'pad2',  0.5, 0.5, 1, 1 )
p3 = TPad( 'pad3', 'pad3',  0, 0, 0.5, 0.5 )
p4 = TPad( 'pad4', 'pad4',  0.5, 0, 1, 0.5 )
p1.Draw()
p2.Draw()
p3.Draw()
p4.Draw()

p1.cd()
hE1.GetXaxis().SetTitle("E (GeV)")
hE1.Draw()
c1.Update()

p2.cd()
hSum.GetXaxis().SetTitle("E (GeV)")
hM1.SetLineColor(2)
hM1.Draw()
c1.Update()

p3.cd()
hSum.GetXaxis().SetTitle("E (GeV)")
hM2.SetLineColor(3)
hM2.Draw()
c1.Update()

p4.cd()
hSum.GetXaxis().SetTitle("E (GeV)")
hSum.SetLineColor(4)
hSum.SetTitle("hSum")
hSum.Draw()
c1.Update()

# Open a ROOT file and save histograms
myfile = TFile('py-hw2.root', 'RECREATE')
myfile.Write()
c1.Write()
hE1.Write()
hM1.Write()
hM2.Write()
hSum.Write()
myfile.Close()