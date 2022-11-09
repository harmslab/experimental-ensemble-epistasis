#!/usr/bin/env python

import lacmwc
import pandas as pd
import numpy as np

import re, os, glob, sys

from tqdm.auto import tqdm

def get_concs(filename,model,num_reps=5000):
    
    df = pd.read_csv(filename)
    
    genotype = filename.split(".")[0]
    out_file = f"{genotype}_concs.csv"
        
    models = {"2":lacmwc.model.LacMWC2,
              "3":lacmwc.model.LacMWC3,
              "3i":lacmwc.model.LacMWC3i,
              "4":lacmwc.model.LacMWC4,
              "5":lacmwc.model.LacMWC5}

    species_names = ["O","I","H","L",
                     "H.I","H.I_2","H.O","H.O.I","H.O.I_2",
                     "L.I","L.I_2","L.O","L.O.I","L.O.I_2"]

    # initialize model
    m = models[model]()
    
    C_vector = np.array((120,10,0))

    reps = []
    for i in tqdm(range(num_reps)):

        out = []
        iptg_vec = 10**(np.arange(-10,-1,0.1))*1e9
        for iptg in iptg_vec:
            C_vector[2] = iptg
            out.append(m.get_all_conc(lnK_vector=np.array(df.iloc[i,:]),
                                      C_vector=C_vector))

        out = np.array(out)
        out_dict = {"replicate":[i for _ in range(out.shape[0])],
                    "prot_tot":[C_vector[0]*1e-9 for _ in range(out.shape[0])],
                    "oper_tot":[C_vector[1]*1e-9 for _ in range(out.shape[0])],
                    "iptg_tot":iptg_vec*1e-9}
        for i in range(len(species_names)):
            out_dict[species_names[i]] = out[:,i]*1e-9

        out_df = pd.DataFrame(out_dict)
        reps.append(out_df)

    big_df = pd.concat(reps)
    big_df.to_csv(out_file,index=False)


get_concs(sys.argv[1],sys.argv[2])

