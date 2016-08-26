#!/bin/bash
#$ -q all.q@compute-0-6.local
#$ -cwd
#$ -j y
#$ -o /home/zshamsi2/projects/
#$ -S /bin/bash
#$ -t 1-20
#$ -V

# handle if we are or are not part of an array job
if [ "$SGE_TASK_ID" = "undefined" ]; then
    SGE_TASK_ID=0
fi

cpptraj -i rawcppInAS2$SGE_TASK_ID.in 
