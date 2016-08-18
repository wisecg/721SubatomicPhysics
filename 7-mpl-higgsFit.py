#!/usr/bin/env python
""" 
	PHYS 721, HW 7
	Clint Wiseman
	10/4/15
	Using Data Bank 2: masses for photon pairs in GeV.
	1. Is there a signal? If so, what is the significance of the signal given a mass of 126.5 GeV 
		and a width of 1.66 GeV? 
	References:
	Basic Data Plotting With Matplotlib: 
		https://bespokeblog.wordpress.com/2011/07/11/basic-data-plotting-with-matplotlib-part-3-histograms/
	Method for finding Chi2, NDF, etc:
		http://bulldog2.redlands.edu/facultyfolder/deweerd/tutorials/fitting.txt
""" 
import math
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

hi = 160
lo = 100
bins = 180
EnergyPerBin = (hi-lo)/float(bins)

# fitting functions
def exp_fit(x, a, b):
	return a * np.exp(b * (x-lo))
	
def poly_fit(x,a,b,c):
	return a*x*x + b*x + c

def fourth_fit(x,a,b,c,d,e):
	return a*x*x*x*x + b*x*x*x + c*x*x +d*x + e

def gaus_fit(x,a,mean,sigma):
	return (a/(sigma*np.sqrt(2*np.pi))) * np.exp(-((x - mean)**2 / 2*sigma**2))

def relbreit(x,n,m,w):
	#n : normalization factor
	#m : m_0, the higgs mass 
	#w : gamma_0, the width (without mass dependence)
	a = x**2. - m**2.
	b = m*w
	c = m*math.sqrt(m**2.+w**2.)
	d = (2*math.sqrt(2)/math.pi)*(m*w*c)
	e = d/math.sqrt(m**2.+c)
	return n*e/(a**2. + b**2.)

def chi_2(ys,yknown):  # borrowed from nick tyler
    total = 0
    for i in xrange(len(yknown)):
        temp = (ys[i]-yknown[i])**2.0
        if yknown[i] == 0:
            total += 1 # temp
        else :
            total += temp/yknown[i]
    return total/len(yknown)


# create figure 1 (raw data + background fit)
#fig1 = plt.figure()
fig1 = plt.figure(figsize=(10,7),facecolor='w')
ax1 = fig1.add_subplot(111)

# load and plot data to figure 1
data = np.loadtxt("DB2.txt",skiprows=0)
hist, bin_edges = np.histogram(data,bins)
xvals = np.linspace(lo, hi, bins)
histo = plt.hist(data,bins,histtype='step',color='r',label='$\mathrm{Raw\ Data}$')  

# Apply curve_fit and draw it on top of the data
#popt, pcov = curve_fit(poly_fit, xvals, hist, [10.0, 1.0, lo])
#print "Background polynomial fit (ax^2 + bx + c)"
popt, pcov = curve_fit(fourth_fit, xvals, hist, [1.0,1.0,1.0,1.0,lo])
print "Background polynomial fit (ax^4 + bx^3 + cx^2 + dx + e)"
print "a =", popt[0], "+/-", pcov[0,0]**0.5
print "b =", popt[1], "+/-", pcov[1,1]**0.5
print "c =", popt[2], "+/-", pcov[2,2]**0.5
print "d =", popt[3], "+/-", pcov[3,3]**0.5
print "e =", popt[4], "+/-", pcov[4,4]**0.5
#plt.plot(xvals, poly_fit(xvals, *popt),label='$\mathrm{Bkgd:\ %.2fx^2+(%.2f)x+%.2f}$'%(popt[0],popt[1],popt[2]))
plt.plot(xvals, fourth_fit(xvals, *popt),label='$\mathrm{Bkgd:\ %.5fx^4+%.2fx^3+%.2fx^2+%.2fx+%.2f}$'%(popt[0],popt[1],popt[2],popt[3],popt[4]))
plt.title("Photon Pair Mass (GeV)")
plt.xlabel('Energy [GeV] (%.3f GeV/bin)'% (EnergyPerBin))

# subtract each histogram bin from the background function,
# set negative values to zero, and draw
#hist_subt = hist - poly_fit(xvals,*popt)
hist_subt = hist - fourth_fit(xvals,*popt)
hist_subt[hist_subt <= 0] = 0  # tests each value
wid = bin_edges[1:] - bin_edges[:-1] 
plt.bar(bin_edges[:-1], hist_subt, width=wid, color='g',alpha=0.5,label='$\mathrm{Bkgd-Subtracted}$') 

# labels + handles are duplicated for some reason
handles, labels = ax1.get_legend_handles_labels()
plt.legend(handles,labels)
plt.show()
fig1.savefig('higgs_bkgd.eps', format='eps', dpi=1200)

# create figure 2
#fig2 = plt.figure()
fig2 = plt.figure(figsize=(10,7),facecolor='w')
ax2 = fig2.add_subplot(111)

# draw the subtracted histo again
plt.bar(bin_edges[:-1], hist_subt, width=wid, color='g',alpha=0.5) 

# subtract each histogram bin from the background function,
# set negative values to zero, and draw
#hist_subt = hist - poly_fit(xvals,*popt)
hist_subt = hist - fourth_fit(xvals,*popt)
hist_subt[hist_subt <= 0] = 0  # tests each value
wid = bin_edges[1:] - bin_edges[:-1] 
plt.bar(bin_edges[:-1], hist_subt, width=wid, color='g',alpha=0.5) 

# Restrict the fit to a sub-range
sub1 = 123.0 # value (GeV), not index
sub2 = 130.0

index1 = int((sub1-lo)/EnergyPerBin)  # find index corresponding to energy
index2 = int((sub2-lo)/EnergyPerBin)
lo_vals = np.linspace(0, index1, index1+1) # matches indexes, not values
hi_vals = np.linspace(index2, bins, bins-index2+1)
remove_vals = np.concatenate((lo_vals,hi_vals),axis=0)
xvals1 = np.delete(xvals,remove_vals)
hist_subt1 = np.delete(hist_subt,remove_vals)

# gaussian fit
popt1, pcov1 = curve_fit(gaus_fit, xvals1, hist_subt1, [1.0, 126.5, 1.66])
print "\nGaussian fit results:"
print "amp =", popt1[0], "+/-", pcov1[0,0]**0.5
print "mean =", popt1[1], "+/-", pcov1[1,1]**0.5
print "sigma =", popt1[2], "+/-", pcov1[2,2]**0.5
c2 = chi_2(gaus_fit(xvals1,*popt1),hist_subt1)
print "chi_2 =", c2
gaus = plt.plot(xvals1, gaus_fit(xvals1, *popt1),lo,hi,linewidth=5,color='r',
	label='$\mathrm{Gaus: m_H=%.2f, \ \sigma = %.1f, \ \chi^{2}=%.1f\ }$' % (popt1[1],popt1[2],c2))

# relativistic breit-wigner fit
popt2, pcov2 = curve_fit(relbreit, xvals1, hist_subt1, [1.0,126.5,1.66])
print "\n Rel. BW fit results:"
print "amp =", popt2[0], "+/-", pcov2[0,0]**0.5
print "mass =", popt2[1], "+/-", pcov2[1,1]**0.5
print "width =", popt2[2], "+/-", pcov2[2,2]**0.5
c2 = chi_2(relbreit(xvals1,*popt2),hist_subt1)
print "chi_2 =", c2
relbw = plt.plot(xvals1, relbreit(xvals1, *popt2),lo,hi,linewidth=2,color='b',
	label='$\mathrm{RBW: m_H=%.2f, \ \Gamma_0 = %.1f, \ \chi^{2}=%.1f\ }$' % (popt2[1],popt2[2],c2))

plt.title("Photon Pair Mass, Bkgd-Subtracted")
plt.xlabel('Energy [GeV] (%.3f GeV/bin)'% (EnergyPerBin))
#plt.yscale('log')
plt.xlim((lo,hi))
plt.ylim((0,100))

# labels + handles are duplicated for some reason
handles, labels = ax2.get_legend_handles_labels()
#print handles,labels
del labels[3]
del handles[3]
del labels[0]
del handles[0]
plt.legend(handles,labels)
plt.show()

fig2.savefig('higgsfit.eps', format='eps', dpi=1200)

