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

CSCAT = xr.open_mfdataset('/g/data/w40/esh563/CSCAT_*.nc')
CSCAT_LST = [6, 9.5, (11 + 55/60), 18, 21.5, (23 + 55/60)]

CSCAT = CSCAT.assign_coords(time = CSCAT_LST)
CSCAT.time.attrs['time_zone'] = 'local solar time'

CSCAT.to_netcdf('/g/data/w40/esh563/CSCAT_201212_amended.nc', mode='w', format='NETCDF4')
