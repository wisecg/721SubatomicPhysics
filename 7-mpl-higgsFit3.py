#!/usr/bin/env python
""" 
    PHYS 721, HW 7
    Clint Wiseman
    10/4/15
    Using Data Bank 2: masses for photon pairs in GeV.
    2.* As above, but not knowing the mass, what is the significance of a possible signal in the data 
        given a width of 1.66 GeV? 

    Ref: http://www.reid.ai/2012/09/chi-squared-distribution-table-with.html
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

fig1 = plt.figure(figsize=(10,7),facecolor='w')
ax1 = fig1.add_subplot(111)

data = np.loadtxt("DB2.txt",skiprows=0)
hist, bin_edges = np.histogram(data,bins)
xvals = np.linspace(lo, hi, bins)

#popt, pcov = curve_fit(poly_fit, xvals, hist, [10.0, 1.0, lo])
popt, pcov = curve_fit(fourth_fit, xvals, hist, [1.0,1.0,1.0,1.0,lo])

#hist_subt = hist - poly_fit(xvals,*popt)
hist_subt = hist - fourth_fit(xvals,*popt)
hist_subt[hist_subt <= 0] = 0  # tests each value
wid = bin_edges[1:] - bin_edges[:-1] 
plt.bar(bin_edges[:-1], hist_subt, width=wid, color='g',alpha=0.5) 

c2_gaus = []
c2_rbw = []

for i in range(1,59):
    sub1 = 100+i
    sub2 = sub1+5
    target = (sub2-sub1)/2 + sub1
    pars = [1.0, target, 1.66]

    index1 = int((sub1-lo)/EnergyPerBin)  # find index corresponding to energy
    index2 = int((sub2-lo)/EnergyPerBin)
    lo_vals = np.linspace(0, index1, index1+1) # matches indexes, not values
    hi_vals = np.linspace(index2, bins, bins-index2+1)
    remove_vals = np.concatenate((lo_vals,hi_vals),axis=0)
    xvals1 = np.delete(xvals,remove_vals)
    hist_subt1 = np.delete(hist_subt,remove_vals)

    try:
        
        popt1, pcov1 = curve_fit(gaus_fit, xvals1, hist_subt1, pars)
        c2gaus = chi_2(gaus_fit(xvals1,*popt1),hist_subt1)
        c2_gaus.append(c2gaus)       
        dofgaus = len(hist_subt1)-len(popt1)
        
        popt2, pcov2 = curve_fit(relbreit, xvals1, hist_subt1, pars)
        c2rbw = chi_2(relbreit(xvals1,*popt2),hist_subt1)
        c2_rbw.append(c2rbw)
        dofrbw = len(hist_subt1)-len(popt2)
        
        print "%i: range:%.0f-%.0f  c2gaus:%.2f  dofgaus:%i  c2rbw:%.2f  dofrbw:%i" % (i,sub1,sub2,c2gaus,dofgaus,c2rbw,dofrbw)

        if (1.0 < popt2[2] < 2.0):
            fig1 = plt.figure(figsize=(10,7),facecolor='w')
            ax1 = fig1.add_subplot(111)
            plt.bar(bin_edges[:-1], hist_subt, width=wid, color='g',alpha=0.5) 
            gaus = plt.plot(xvals1, gaus_fit(xvals1, *popt1),lo,hi,linewidth=5,color='r',
                label='$\mathrm{Gaus: m_H=%.2f, \ \sigma = %.2f, \ \chi^{2}=%.1f\ }$' % (popt1[1],popt1[2],c2gaus))
            relbw = plt.plot(xvals1, relbreit(xvals1, *popt2),lo,hi,linewidth=2,color='b',
                label='$\mathrm{RBW: m_H=%.2f, \ \Gamma_0 = %.2f, \ \chi^{2}=%.1f\ }$' % (popt2[1],popt2[2],c2rbw))
            handles, labels = ax1.get_legend_handles_labels()
            del labels[3]
            del handles[3]
            del labels[0]
            del handles[0]
            plt.legend(handles,labels)
            plt.title("Fit range: %.0f - %.0f GeV" % (sub1,sub2))
            plt.xlabel('Energy [GeV] (%.3f GeV/bin)'% (EnergyPerBin))
            plt.xlim((lo,hi))
            plt.ylim((0,100))
            plt.show()
            fig1.savefig('morefits%02d.eps'%i, format='eps', dpi=1200)
        
    except RuntimeError:
        print "Error - curve_fit failed"

print "c2_gaus: ",["%0.3f" % i for i in c2_gaus]
print "c2_rbw: ",["%0.3f" % i for i in c2_rbw]