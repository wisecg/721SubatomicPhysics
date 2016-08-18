#!/usr/bin/env python  
#google "shebang"

import ROOT
from ROOT import TLorentzVector
from StringIO import StringIO

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

mass1 = []
mass2 = []
mass_sum = []
vec1 = TLorentzVector()
vec2 = TLorentzVector()
lines = [line.rstrip('\n') for line in open('DB1.txt')]
bins = 75

fig = plt.figure(num=None, figsize=(10, 10), dpi=200, facecolor='w', edgecolor='k')
#font = {'size':10}
#matplotlib.rc('font', **font)

for line in lines:
    a = np.array(np.loadtxt(StringIO(line)))

    print a[0],a[1]
    
    #vec1.SetPxPyPzE(a[1],a[2],a[3],a[0])
    #vec2.SetPxPyPzE(a[5],a[6],a[7],a[4])
    #mass1.append(vec1.M())
    #mass2.append(vec2.M())
    #mass_sum.append((vec1+vec2).M())

#plt.subplot(221)
#plt.hist(mass1, bins, histtype=u'stepfilled', alpha=0.5)
#plt.xlabel(r'Mass (GeV/$c^2$)')
#plt.ylabel(r'Counts (#)')
#plt.title(r'Mass found from four vector 1')