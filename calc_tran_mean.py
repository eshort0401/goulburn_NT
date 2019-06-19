# Core 
import glob
import sys

# Analysis 
import xarray as xr
import numpy as np

file_prepend = str(sys.argv[1])

print('Averaging ' + file_prepend)

years = [2012, 2013, 2014]

print('Calculating year {}.'.format(years[0]))

tran_i = xr.open_dataset(
    '/g/data/w40/esh563/goulburn_NT/transects/{}_goulburn_{}12.nc'.format(file_prepend, str(years[0]))
)

date_times = np.arange(str(years[0]) + '-12', str(years[0]+1) + '-01', dtype='datetime64[h]')
tran_i = tran_i.assign_coords(time = date_times)

if not(sys.argv[2] in ['False', 'false', 'f', '0']):
    tran_i = (tran_i - tran_i.rolling(time=24, center=True).mean()).dropna('time')
    
tran_i = tran_i.mean(dim='coastal_axis')


tran_list = [tran_i] * len(years)

for i in range(1,len(years)):
    
    print('Calculating year {}.'.format(years[i]))

    tran_i = xr.open_dataset(
        '/g/data/w40/esh563/goulburn_NT/transects/{}_goulburn_{}12.nc'.format(file_prepend, str(years[i]))
    )
    
    date_times = np.arange(str(years[i]) + '-12', str(years[i]+1) + '-01', dtype='datetime64[h]')
    tran_i = tran_i.assign_coords(time = date_times)

    if not(sys.argv[2] in ['False', 'false', 'f', '0']):
        tran_i = (tran_i - tran_i.rolling(time=24, center=True).mean()).dropna('time')
        
    tran_i = tran_i.mean(dim='coastal_axis')

    tran_list[i] = tran_i
    
tran = xr.concat(tuple(tran_list), dim = 'time')

tran_mean = tran.groupby('time.hour').mean('time')

save_path = '/g/data/w40/esh563/goulburn_NT/transect_means/{}_goulburn_{}-{}_12.nc'.format(file_prepend,str(i).zfill(2), years[0], years[-1])
tran_mean.to_netcdf(path=save_path, mode='w', format='NETCDF4')
