#!/usr/bin/env python

import pandas as pd
import numpy as np

import pickle
import re
import sys

def pickle_to_df(pickle_file):

    f = open(pickle_file,"rb")
    fits = pickle.load(f)
    f.close()

    for k in fits.keys():

        out_dict = {}
        keys = []
        header = list(fits[k].param_names)
        for i, h in enumerate(header):
            h = re.sub("\|wt","",header[i])
            out_dict[h] = []
            keys.append(h)

        out_name = re.sub("V","",k)
        for i in range(fits[k].fit.samples.shape[0]):
            for j in range(fits[k].fit.samples.shape[1]):
                out_dict[keys[j]].append(fits[k].fit.samples[i,j])

        df = pd.DataFrame(out_dict)
        
        # Shuffle rows so we can pull them in specific order (0 to end) for 
        # epistasis calcs without worrying about order left over from 
        # MCMC sampling.
        df = df.sample(frac=1).reset_index(drop=True)
        
        df.to_csv(f"{out_name}.csv",index=False)

def main(argv=None):
    
    if argv is None:
        argv = sys.argv[1:]

    pickle_file = argv[0]

    pickle_to_df(pickle_file)

if __name__ == "__main__":
    main()
