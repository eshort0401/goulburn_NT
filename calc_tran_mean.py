# Core 
import glob
import sys

# Analysis 
import xarray as xr
import numpy as np

file_prepend = str(sys.argv[1])

print('Averaging ' + file_prepend)

years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
month = '12'

print('Calculating year {}.'.format(years[0]))

tran_i = xr.open_dataset(
    '/g/data/w40/esh563/goulburn_NT/transects/{}_goulburn_{}{}.nc'.format(file_prepend, str(years[0]), month)
)

#date_times = np.arange(str(years[0]) + '-11', str(years[0]+1) + '-12', dtype='datetime64[h]')

if not(sys.argv[2] in ['False', 'false', 'f', '0']):
    tran_i = (tran_i - tran_i.rolling(time=24, center=True).mean()).dropna('time')
    print('Taking running mean.')
    
tran_i = tran_i.mean(dim='coastal_axis')

tran_list = [tran_i] * len(years)

for i in range(1,len(years)):
    
    print('Calculating year {}.'.format(years[i]))

    tran_i = xr.open_dataset(
        '/g/data/w40/esh563/goulburn_NT/transects/{}_goulburn_{}{}.nc'.format(file_prepend, str(years[i]), month)
    )
    
    #date_times = np.arange(str(years[i]) + '-11', str(years[i]+1) + '-12', dtype='datetime64[h]')
    # tran_i = tran_i.assign_coords(time = date_times)

    if not(sys.argv[2] in ['False', 'false', 'f', '0']):
        tran_i = (tran_i - tran_i.rolling(time=24, center=True).mean()).dropna('time')
        print('Taking running mean.')
        
    tran_i = tran_i.mean(dim='coastal_axis')

    tran_list[i] = tran_i
    
tran = xr.concat(tuple(tran_list), dim = 'time')

tran_mean = tran.groupby('time.hour').mean('time')

save_path = '/g/data/w40/esh563/goulburn_NT/transect_means/{}_goulburn_{}-{}_{}.nc'.format(file_prepend, years[0], years[-1], month)
tran_mean.to_netcdf(path=save_path, mode='w', format='NETCDF4')
