## Scripts and data for reproducing the analysis in "An experimental demonstration of ensemble epistasis in the lac repressor"

bioRxiv: [https://doi.org/10.1101/2022.10.14.512271](https://doi.org/10.1101/2022.10.14.512271). 

Morrison and Harms

## Instructions

1. Install the [lacmwc](https://github.com/harmslab/lacmwc) library
   that implements the lacmwc model described in the paper. 
2. Run `extract.sh` in this directory to unzip all of the MCMC samples into
   for the lacmwc model against the experimental data .csv files.
3. Run the `main-analysis.ipynb` notebook to reproduce the figures from the
   paper.
4. If you want to re-generate the MCMC samples, see the 
   `generate-mcmc-samples` directory. This has the scripts and directories 
   we used to generate the samples. (We ran this in a high-performance
   computing environment as the runtime to convergence can be several days). 
