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

# Specify start and end coords on coast.
# Choose order so that (transect_axis, coastline_axis) forms a right hand coordinate system
lon0 = 134.5293 
lat0 = -12.4715
coast_lon1 = 133.3290
coast_lat1 = -12.1468

trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans, coast_distances, tran_distances = ta.define_transects(
    lon0, lat0, coast_lon1, coast_lat1, 453300, spacing = 12500
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

# Create transects    
path = '/g/data/w40/esh563/goulburn_NT/ASCAT/ASCAT_goulburn_2012-2014_12.nc'
ASCAT = xr.open_dataset(path)

proj = ASCAT.u_pert_mean * b_lon + ASCAT.v_pert_mean * b_lat
proj = proj / np.sqrt(b_lon ** 2 + b_lat ** 2)

ASCAT_tran = ta.calc_transects(proj, trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans)
ASCAT_p_value_tran = ta.calc_transects(ASCAT.p_value_mean, trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans)

ASCAT_tran = ASCAT_tran.assign_coords(coastal_axis = coast_distances)
ASCAT_tran = ASCAT_tran.assign_coords(transect_axis = tran_distances)
ASCAT_tran = ASCAT_tran.rename('wind_proj')

ASCAT_p_value_tran = ASCAT_p_value_tran.assign_coords(coastal_axis = coast_distances)
ASCAT_p_value_tran = ASCAT_p_value_tran.assign_coords(transect_axis = tran_distances)
ASCAT_p_value_tran = ASCAT_p_value_tran.rename('p_value')

ASCAT_tran = xr.merge((ASCAT_tran, ASCAT_p_value_tran)) 

save_path_ASCAT = '/g/data/w40/esh563/goulburn_NT/transect_means/ASCAT_goulburn_2012-2014_12.nc'

ASCAT_tran.to_netcdf(path=save_path_ASCAT, mode='w', format='NETCDF4')

