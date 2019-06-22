# Core 
import datetime
import os
import glob

# HDF4 Support
from pyhdf.SD import SD, SDC

# Analysis 
import xarray as xr
import numpy as np

# Debugging 
import pdb

longitude = np.arange(-180 + .125, 180, 0.25)
latitude = np.arange(-50 + .125, 50, 0.25)

month = 11
days = 30

for i in range(5,15):
    TRMM_list = [np.zeros((14,21))]*days*8
    print('Calculating year 20{}'.format(str(i).zfill(2)), end='\r')
    for j in range(1,days):
        for k in range(0,24,3):
            f_name = glob.glob(
                '/g/data/ua8/NASA_TRMM/TRMM_L3/TRMM_3B42/20{0}/3B42.20{0}{3}{1}.{2}.*.HDF'.format(
                    str(i).zfill(2), str(j).zfill(2), str(k).zfill(2), str(month).zfill(2)
                )
            )[0]
            
            # Longitude 132.875 index is 1251, 136.125 index is 1264
            # Latitude -12.875 index is 148, -7.875 index is 168
            TRMM_list[int((j-1)*8+k/3)] = SD(f_name, SDC.READ).select('precipitation')[1251:1265,148:169]
    
    TRMM = np.stack(TRMM_list, axis=-1)
    base_time = datetime.datetime(2000+i, month, 1)
    times = np.array([base_time + datetime.timedelta(hours=i) for i in range(0,24*days,3)])

    coords = {'longitude' : longitude[1251:1265], 'latitude' : latitude[148:169], 'time' : times}
    TRMM_da = xr.DataArray(TRMM, coords=coords, dims=['longitude', 'latitude', 'time'], name='precipitation')

    os.makedirs('/g/data/w40/esh563/goulburn_NT/TRMM_3B42', exist_ok=True)
    save_path = '/g/data/w40/esh563/goulburn_NT/TRMM_3B42/TRMM_3B42_goulburn_20{}{}.nc'.format(
        str(i).zfill(2), str(month).zfill(2)
    )
    
    TRMM_da = TRMM_da.where(TRMM_da >= 0)

    TRMM_da.to_netcdf(path=save_path, mode='w', format='NETCDF4')
