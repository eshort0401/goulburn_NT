# Core 
import glob
import sys
import os

# Analysis 
import xarray as xr
import numpy as np

static_path = '/g/data/ua8/ARCCSS_Data/MCASClimate/v1-0/static/static.nc'
static = xr.open_dataset(static_path).sel(latitude=slice(-12.5,-8), longitude=slice(133,136))
z = np.loadtxt('average_model_levels.txt')[0:71]

base_dir = '/g/data/w40/esh563/goulburn_NT'

for i in range(5, 15):

    print('Calculating year 20{}'.format(str(i).zfill(2)))
    save_base = base_dir + '/20{}20{}/clouds_daily'.format(str(i).zfill(2), str(i+1).zfill(2))
    os.makedirs(save_base, exist_ok=True)

    for j in range(1, 32):

        print('Caclulating day {}'.format(str(j).zfill(2)))

        load_path = base_dir + '/20{0}20{1}/clouds/clouds_goulburn_20{0}12{2}*.nc'.format(
            str(i).zfill(2), str(i+1).zfill(2), str(j).zfill(2)
        )
        cloud = xr.open_mfdataset(load_path, concat_dim = 'Time')
        cloud = cloud.rename(
            {'bottom_top' : 'level', 'south_north' : 'latitude', 'west_east' : 'longitude', 'Time' : 'time'}
        )
        cloud = cloud.assign_coords(level = z)
        cloud = cloud.assign_coords(latitude = static.latitude)
        cloud = cloud.assign_coords(longitude = static.longitude)

        save_path = save_base + '/clouds_goulburn_20{0}12{2}.nc'.format(
            str(i).zfill(2), str(i+1).zfill(2), str(j).zfill(2)
        )
        cloud.to_netcdf(path=save_path, mode='w', format='NETCDF4')
