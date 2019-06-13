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
times = ['2012-10-29T06:00:00'] * 2874
CSCAT_LST = ['T06:00:00', 'T09:30:00', 'T11:55:00', 'T18:00:00', 'T21:30:00', 'T23:55:00']
days = np.datetime_as_string(np.arange('2012-10-29', '2014-02-20', dtype='datetime64[D]'))

for i in range(0, np.size(days)):
    times[i*6:(i+1)*6] = [days[i] + CSCAT_LST[j] for j in range(6)]
times = np.array(times)
times = times.astype('datetime64',copy=False)

CSCAT = CSCAT.assign_coords(time = times)
CSCAT.time.attrs['time_zone'] = 'local solar time'

CSCAT.to_netcdf('/g/data/w40/esh563/CSCAT.nc', mode='w', format='NETCDF4')
