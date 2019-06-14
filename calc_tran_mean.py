# Core 
import glob
import sys

# Analysis 
import xarray as xr
import numpy as np

file_prepend = str(sys.argv[1])

print('Averaging ' + file_prepend)
print('Calculating year 2005')

tran_i = xr.open_dataset(
    '/g/data/w40/esh563/goulburn_NT/transects/{}_goulburn_200512.nc'.format(file_prepend)
)

if not(sys.argv[2] in ['False', 'false', 'f', '0']):
    tran_i = (tran_i - tran_i.rolling(time=24, center=True).mean()).dropna('time')
    
tran_i = tran_i.mean(dim='coastal_axis')
date_times = np.arange('2005-12', '2006-01', dtype='datetime64[h]')
tran_i = tran_i.assign_coords(time = date_times)

tran_list = [tran_i] * 10

for i in range(6,15):
    
    print('Calculating year 20{}.'.format(str(i).zfill(2)))

    tran_i = xr.open_dataset(
        '/g/data/w40/esh563/goulburn_NT/transects/{}_goulburn_20{}12.nc'.format(file_prepend, str(i).zfill(2))
    )
    
    if not(sys.argv[2] in ['False', 'false', 'f', '0']):
        tran_i = (tran_i - tran_i.rolling(time=24, center=True).mean()).dropna('time')
        
    tran_i = tran_i.mean(dim='coastal_axis')
    date_times = np.arange('20{}-12'.format(str(i).zfill(2)), '20{}-01'.format(str(i+1).zfill(2)), dtype='datetime64[h]')
    tran_i = tran_i.assign_coords(time = date_times)
    
    tran_list[i-5] = tran_i
    
tran = xr.concat(tuple(tran_list), dim = 'time')

tran_mean = tran.groupby('time.hour').mean('time')

save_path = '/g/data/w40/esh563/goulburn_NT/transect_means/{}_goulburn_12.nc'.format(file_prepend,str(i).zfill(2))
tran_mean.to_netcdf(path=save_path, mode='w', format='NETCDF4')
