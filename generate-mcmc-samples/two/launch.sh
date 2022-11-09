for g in `echo "MVHK IVHK MVAK MVHL IVAK MVAL IVHL IVAL"`; do
    qsub run.srun $g
done
