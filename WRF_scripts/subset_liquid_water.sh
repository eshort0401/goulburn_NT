#!/bin/bash

for i in $(seq -f "%02g" 05 14); do 
   
    echo 'Cropping year 20'${i}

    a=20$i
    b=$((a+1)) 
    season=$a$b 

    mkdir -p /g/data/w40/esh563/goulburn_NT/$season/clouds/

    save_dir=/g/data/w40/esh563/goulburn_NT/$season/clouds

    echo 'Start of CDO Log File' > ${save_dir}/cdo_log.txt
    
    for j in $(seq -f "%02g" 01 31); do
        echo 'Cropping day '${j}
        for k in $(seq -f "%02g" 00 23); do
            original=/g/data/w40/clv563/MARITIME_CONTINENT_BM${season}/clouds/clouds_ncopck_d02_${a}-12-${j}_${k}:00:00
            cropped=/g/data/w40/esh563/goulburn_NT/$season/clouds/clouds_goulburn_${a}12${j}${k}.nc
            ncks -O -v QCLOUD,QRAIN -d south_north,15,141 -d west_east,1089,1172 -d bottom_top,0,70 $original $cropped &>> ${save_dir}/cdo_log.txt 
        done
    done
done
