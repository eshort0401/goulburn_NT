#!/bin/bash
    
for j in $(seq -f "%02g" 01 31); do
    original=/g/data/w40/esh563/goulburn_NT/20142015/${1}/${2}_goulburn_201412${j}.nc
    record_dim=/g/data/w40/esh563/goulburn_NT/20142015/${1}/${2}_goulburn_201412${j}_record.nc
    ncks -O --mk_rec_dmn time $original $record_dim
done
