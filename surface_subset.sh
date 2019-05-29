#!/bin/bash

for i in $(seq -f "%02g" 05 14); do 
    for j in $(seq -f "%02g" 01 31); do
        a=20$i
        b=$((a+1)) 
        season=$a$b 
        original=/g/data/ua8/ARCCSS_Data/MCASClimate/v1-0/$season/${1}/${2}_WRF_Maritime_Continent_4km_${a}12${j}.nc
        cropped=/g/data/w40/esh563/goulburn_NT/$season/${1}/${2}_goulburn_${a}12${j}.nc
        echo $original 
        ncks -d latitude,-13.0,-6.5 -d longitude,131.5,139.5 -d level,0 $original $cropped
    done
done
