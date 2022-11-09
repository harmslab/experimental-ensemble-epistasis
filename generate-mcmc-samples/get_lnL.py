#!/usr/bin/env python

import numpy as np
import lacmwc

import glob
import sys
import pickle

total_lnL = 0
for p in glob.glob("*.pickle"):

    f = open(p,'rb')
    fit = pickle.load(f)
    f.close()
 
    param = [] 
    for k in fit:
        for i in range(fit[k].fit.samples.shape[1]):
            v = np.array(fit[k].fit.samples[:,i]) 
            v.sort()
            param.append(v[len(v)//2])

    total_lnL += fit[k].fit.ln_like(param)

print(total_lnL)
