# Core 
import datetime
import os
import glob

# Analysis 
import xarray as xr
import numpy as np
import pyproj as pp
import scipy as sp
import imp
imp.load_source('transect_analysis', '/home/563/esh563/goulburn_NT/transect_analysis.py')
import transect_analysis as ta

# Specify start and end coords on coast.
# Choose order so that (transect_axis, coastline_axis) forms a right hand coordinate system
lon0 = 134.5293 
lat0 = -12.4715
coast_lon1 = 133.3290
coast_lat1 = -12.1468

month=12

trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans, coast_distances, tran_distances = ta.define_transects(
    lon0, lat0, coast_lon1, coast_lat1, 453300, 25000
)

static_path = '/g/data/ua8/ARCCSS_Data/MCASClimate/v1-0/static/static.nc'
static = xr.open_dataset(static_path).sel(latitude=slice(-12.75,-6), longitude=slice(130,139))
static_tran = ta.calc_transects(static, trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans) 
static_tran = static_tran.assign_coords(coastal_axis = coast_distances)
static_tran = static_tran.assign_coords(transect_axis = tran_distances)

# Calcualate distance where landmask drops below 0.5
coast_i = np.where(static_tran.mean('coastal_axis').LANDMASK.values < 0.5)[0][0] - 1
coast_location = tran_distances[coast_i]

# Redefine tran_distances so that coastline occurs at 0.
tran_distances = tran_distances - coast_location

# Create basis vectors of new coordinate system
b_lon = trans_lon1[0] - lon0
b_lat = trans_lat1[0] - lat0

# Iterate over all years
for i in range(5, 15):

    print('Solving for 20{}'.format(str(i).zfill(2)))

    # Caclulate transects for first day of data
    base = '/g/data/w40/esh563/goulburn_NT/TRMM_3B42'
    path = base + '/TRMM_3B42_goulburn_20{}{}.nc'.format(str(i).zfill(2), str(month).zfill(2))

    TRMM_3B42_tran = ta.calc_transects(xr.open_dataset(path), trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans)
    TRMM_3B42_tran = TRMM_3B42_tran.assign_coords(coastal_axis = coast_distances)\
        .assign_coords(transect_axis = tran_distances)

    save_path_TRMM_3B42 = '/g/data/w40/esh563/goulburn_NT/transects/TRMM_3B42_goulburn_20{}{}.nc'.format(str(i).zfill(2), str(month).zfill(2))
    TRMM_3B42_tran.to_netcdf(save_path_TRMM_3B42, mode='w', format='NETCDF4')

