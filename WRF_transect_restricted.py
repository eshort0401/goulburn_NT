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
    lon0, lat0, coast_lon1, coast_lat1, 453300
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
for i in range(12, 15):

    print('Solving for 20{}'.format(str(i).zfill(2)))

    # Caclulate transects for first day of data
    base = '/g/data/w40/esh563/goulburn_NT/20{}20{}'.format(str(i).zfill(2), str(i+1).zfill(2))

    U_path = base + '/U/U_goulburn_20{}12*.nc'.format(str(i).zfill(2))
    V_path = base + '/V/V_goulburn_20{}12*.nc'.format(str(i).zfill(2))

    W_path = base + '/W/W_goulburn_20{}12*.nc'.format(str(i).zfill(2))

    PRCP_path = base + '/PRCP/prcp_goulburn_20{}12*.nc'.format(str(i).zfill(2))

    T_path = base + '/T/theta_goulburn_20{}12*.nc'.format(str(i).zfill(2))
    clouds_path = base + '/clouds_daily/clouds_goulburn_20{}12*.nc'.format(str(i).zfill(2))

    #proj = (xr.open_mfdataset(U_path, chunks={'time': 744}).U * b_lon + xr.open_mfdataset(V_path, chunks={'time': 744}).V * b_lat)
    #proj = proj / np.sqrt(b_lon ** 2 + b_lat ** 2)

    # PRCP = xr.open_mfdataset(PRCP_path, chunks={'time': 744}).RAINNC

    #proj_tran = ta.calc_transects(proj, trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans)
    #W_tran = ta.calc_transects(xr.open_mfdataset(W_path, chunks={'time': 744}).W, trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans)
    #PRCP_tran = ta.calc_transects(PRCP, trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans)
    #T_tran = ta.calc_transects(xr.open_mfdataset(T_path, chunks={'time': 744}).T, trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans)
    clouds_tran = ta.calc_transects(xr.open_mfdataset(clouds_path, concat_dim = 'time', chunks={'time': 744}), trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans)

    z = np.loadtxt('average_model_levels.txt')[0:71]
    #proj_tran = proj_tran.assign_coords(level = z)\
        #.assign_coords(coastal_axis = coast_distances)\
        #.assign_coords(transect_axis = tran_distances)\
        #.rename('wind_proj')
    #W_tran = W_tran.assign_coords(level = z)\
     #   .assign_coords(coastal_axis = coast_distances)\
      #  .assign_coords(transect_axis = tran_distances)\
       # .rename('W')
    #PRCP_tran = PRCP_tran.assign_coords(coastal_axis = coast_distances)\
     #   .assign_coords(transect_axis = tran_distances)\
      #  .rename('RAINNC')
    clouds_tran = clouds_tran.assign_coords(level = z)\
        .assign_coords(coastal_axis = coast_distances)\
        .assign_coords(transect_axis = tran_distances)\
         
    save_path_proj = '/g/data/w40/esh563/goulburn_NT/transects/wind_proj_goulburn_20{}12_restricted.nc'.format(str(i).zfill(2))
    #save_path_W = '/g/data/w40/esh563/goulburn_NT/transects/W_goulburn_20{}12.nc'.format(str(i).zfill(2))
    #save_path_PRCP = '/g/data/w40/esh563/goulburn_NT/transects/PRCP_goulburn_20{}12.nc'.format(str(i).zfill(2))
    #save_path_T = '/g/data/w40/esh563/goulburn_NT/transects/T_goulburn_20{}12.nc'.format(str(i).zfill(2))
    #save_path_clouds = '/g/data/w40/esh563/goulburn_NT/transects/clouds_goulburn_20{}12.nc'.format(str(i).zfill(2))

    # proj_tran.to_netcdf(path=save_path_proj, mode='w', format='NETCDF4')
    # W_tran.to_netcdf(path=save_path_W, mode='w', format='NETCDF4')
    # PRCP_tran.to_netcdf(path=save_path_PRCP, mode='w', format='NETCDF4')
    #clouds_tran.to_netcdf(path=save_path_clouds, mode='w', format='NETCDF4')

