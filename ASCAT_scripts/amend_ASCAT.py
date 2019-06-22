# Core 
import datetime
import os
import glob

# Analysis 
import xarray as xr
import numpy as np
import pyproj as pp
import scipy as sp
import transect_analysis as ta

ASCAT = xr.open_mfdataset('/g/data/w40/esh563/ASCAT_12.nc')

ASCAT.time.attrs['time_zone'] = 'local solar time'

ASCAT = ASCAT.sel(latitude = slice(-12.75, -7.75), longitude = slice(-132.75, 136.25))

ASCAT.to_netcdf('/g/data/w40/esh563/goulburn_NT/ASCAT/ASCAT_goulburn_2012-2014_12.nc', mode='w', format='NETCDF4')
