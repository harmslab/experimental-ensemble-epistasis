There are five model directories:

+ two
+ three
+ threei
+ four
+ five

The `template` directory has a generic set of files for doing fits. It was 
used as the template for the specific model directories.

For each model, run run.srun first to create mcmc samples then get_concs.py 
to extract concentrations given parameters. 

You can then run `get_lnL.py` (in this directory) to extract the log
likelihood of the ML model from the output and `pickle-to-df.py` to convert
the resulting pickle files into .csv files with parameters. 



