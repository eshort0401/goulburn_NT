#!/bin/bash
original=/g/data/ua8/ARCCSS_Data/MCASClimate/v1-0/20132014/PRCP/prcp_WRF_Maritime_Continent_4km_20131223.nc
cropped=/g/data/w40/esh563/goulburn_NT//20132014/PRCP/prcp_goulburn_20131223.nc
ncks -O -d latitude,-12.5,-8.0 -d longitude,133.0,136.0 -d level,0,70 $original $cropped
