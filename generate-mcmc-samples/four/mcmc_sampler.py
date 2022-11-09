#!/usr/bin/env python

import lacmwc

import pandas as pd
import numpy as np

import sys
import os
import pickle
import glob
from datetime import date
import random 
import string
    
def fit_data(genotype,
             in_vitro_file,
             in_vivo_file,
             walkers=10, 
             steps=4000,
             model='four',
             user_err = 0.05):
    """
    Pickle file containing dictionary with key = genotype and value = fit object

    Parameters
    ----------
    genotype : str
        genotype being analyzed
    in_vitro_file : str
        file containing in vitro binding data for this genotype
    in vivo_file : str
        file containing in vivo induction data for this genotype
    walkers : int
        number of walkers in Bayesian fit
    steps : int
        number of steps in Bayesian fit
    model : str
        type of lacmwc model to use: "five", "four", "three", or "threei"
    user_err : float
        if any datapoints have fx_std_dev == 0, replaces with user_err. 
    """

    # create experiment collection
    ec = lacmwc.ExperimentCollection(lac_model=model)
        
    # if fitting with 3i model, add in vivo and in vitro data
    if model == 'threei':
        
        # use error on in vivo datapoints to scale in vitro datapoints with no 
        # error
        d = pd.read_csv(in_vivo_file)
        err = np.mean(d.fx_std_dev)

        # load in vitro data
        ec.add_experiment(in_vitro_file,missing_std_dev_value=err)
        # load in vivo data
        ec.add_experiment(in_vivo_file,missing_std_dev_value=err)
            
    # if fitting with any other model, add in vitro data only
    else:
        # load in vitro data
        ec.add_experiment(in_vitro_file,missing_std_dev_value=user_err)
            
    # define bounds
    # K values < -13 result in instability in the lacmwc calculations 
    # for [species] for some genotypes

    # for MVHL three model, gets stuck at -3 for KRE and KRstarE
    # if no upper bound, even though literature values show that 
    # k84L variants have similar effector binding behavior to wildtype
    # (cite liskin) and threei fits show that isn't a good fit (fits
    # themselves are poor too without # upper bound)
    if model == "two":
        #KR
        LB = [-np.inf,-np.inf]
        UB = [np.inf,np.inf]
    
    elif model == 'three':
        # Kratio, KRO, KRE
        LB = [-13,-13, -13]
        UB = [np.inf, np.inf, np.inf]
        if genotype == "MVHL":
            UB = [np.inf, -3.5, -3.5]

    elif model == 'threei':
        # Kratio, KRO, KRE, factor
        LB = [-13,-13,-13,-5]
        UB = [np.inf, np.inf, np.inf, 5]
        if genotype == "MVHL":
            UB = [np.inf, -3.5, -3.5, 5]

    elif model == 'four':
        # Kratio, KRO, KRE, KRstarE
        LB = [-13, -13, -13, -13]
        UB = [np.inf, np.inf, np.inf, np.inf]
        if genotype == "MVHL":
            UB = [np.inf, np.inf, -3.5, -3.5]

    elif model == 'five':
        # Kratio, KRO, KRE, KRstarE, KRstarOE
        LB = [-13, -13, -13, -25, -13]
        UB = [np.inf, np.inf, np.inf, np.inf, np.inf]
        if genotype == "MVHL":
            UB = [np.inf, np.inf, -3.5, -3.5, np.inf]

    else:
        err = "model not recognized.\n"
        raise ValueError(err)

    # define fit type; we will use Bayesian
    fitter = lacmwc.fitters.BayesianFitter(num_walkers=walkers,
                                           num_steps=steps)

    # do fit!
    ec.do_fit(fitter=fitter, lower_bounds = LB, upper_bounds = UB)
            
    # get date of fit
    today = str(date.today())
    runid = "".join([random.choice(string.ascii_letters) for _ in range(10)])
 
    out_file = f"{today}_{genotype}_{model}_{steps}_{walkers}_{runid}.pickle"
  
    # save fit
    with open(out_file,"wb") as f:
        pickle.dump({genotype:ec}, f)

def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    try:
        genotype = argv[0]
        model = argv[1]
        data_dir = argv[2]
        num_walkers = int(argv[3])
        num_steps = int(argv[4])                
    except (IndexError,ValueError):
        err = "\nIncorrect arguments. Should be:\n"
        err += "mcmc_sampler.py genotype model data_dir num_walkers num_steps\n\n"
        raise ValueError(err)

    in_vitro_file = os.path.join(data_dir,"in-vitro",f"{genotype}.csv")
    in_vivo_file = os.path.join(data_dir,"in-vivo",f"{genotype}.csv")
        
    fit_data(genotype, 
             in_vitro_file,
             in_vivo_file,
             walkers=num_walkers,
             steps=num_steps,
             model=model)

if __name__ == "__main__":
    main()

