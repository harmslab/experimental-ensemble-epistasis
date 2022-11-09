#!/bin/bash

for x in `ls */*.csv.gz`; do 
    gunzip $x
done
