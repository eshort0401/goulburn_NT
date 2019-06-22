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

TRMM = xr.open_dataset('/g/data/w40/esh563/TRMM_12.nc')

TRMM = TRMM.sel(latitude = slice(-12.75, -7.75), longitude = slice(-132.75, 136.25))

TRMM.to_netcdf('/g/data/w40/esh563/goulburn_NT/TRMM/TRMM_goulburn_12.nc', mode='w', format='NETCDF4')
