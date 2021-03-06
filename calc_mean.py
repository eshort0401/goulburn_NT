# Core 
import sys

# Analysis 
import xarray as xr
import numpy as np

folder = str(sys.argv[1])
var = str(sys.argv[2])

print('Averaging ' + var)

ds_path = '/g/data/w40/esh563/goulburn_NT/20*/{}/{}_*.nc'.format(folder, var)

ds_mean = xr.open_mfdataset(ds_path, chunks = {'time' : 744}).mean('time')

if not(sys.argv[3] in ['False', 'false', 'f', '0']):
    z = np.loadtxt('average_model_levels.txt')[0:71]
    ds_mean = ds_mean.assign_coords(level = z)

save_path = '/g/data/w40/esh563/goulburn_NT/means/{}_goulburn_12.nc'.format(var)
ds_mean.to_netcdf(path=save_path, mode='w', format='NETCDF4')
