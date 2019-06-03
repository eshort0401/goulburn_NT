#!/bin/bash

original=/g/data/ua8/ARCCSS_Data/MCASClimate/v1-0/static/static.nc
cropped=/g/data/w40/esh563/goulburn_NT/static.nc
ncks -O -d latitude,-12.5,-8.0 -d longitude,133.0,136.0 $original $cropped
