import pyproj as pp
import xarray as xr
import numpy as np

def horizontal_tran_interp(ds, lon0, lat0, lon1, lat1, n):
    """
    Interpolate onto a transect.
    """
    
    lon = np.linspace(lon0, lon1, num=n)
    lat = np.linspace(lat0, lat1, num=n)

    LON, LAT = np.meshgrid(ds.longitude, ds.latitude);
    interp_LON, interp_LAT = np.meshgrid(lon, lat);
    
    ds_interp = ds.interp(longitude=lon, latitude=lat)

    ds_interp = ds_interp.isel(
        longitude=xr.DataArray(
            np.arange(0,np.size(lon)), 
            dims='transect_axis'),
        latitude=xr.DataArray(
            np.arange(0,np.size(lon)), 
            dims='transect_axis',)
    )
    ds_interp = ds_interp.drop('longitude').drop('latitude')
    
    return ds_interp

def calc_transects(ds, trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans):
    """
    Create a new dataset by interpolating over multiple transects.
    """
    
    tran_0 = horizontal_tran_interp(ds, trans_lon0[0], trans_lat0[0], trans_lon1[0], trans_lat1[0], n=n_points)
    tran_list = [tran_0] * n_trans

    for i in range(1,n_trans):
        tran_list[i] = horizontal_tran_interp(
            ds, trans_lon0[i], trans_lat0[i], trans_lon1[i], trans_lat1[i], n=n_points
        )

    proj_tran = xr.concat(tran_list, dim = 'coastal_axis')
    
    return proj_tran 
    
        
def define_transects(lon0, lat0, coast_lon1, coast_lat1, distance=500*10**3, spacing = 4*10**3):
    """
    Create a new dataset along transects perpendicular to given line (e.g. coastline). 
    """

    az = (np.arctan2(coast_lon1-lon0,coast_lat1-lat0) + np.pi/2) * 180 / np.pi
    p = pp.Geod(ellps='WGS84')
    tran_lon1, tran_lat1 = p.fwd(lon0, lat0, az, distance, radians=False)[0:2]
    
    # Calculate n_trans and n_points
    coast_distance = p.inv(lon0, lat0, coast_lon1, coast_lat1)[2]
    tran_distance = p.inv(lon0, lat0, tran_lon1, tran_lat1)[2]
    
    # Approximate even spacing in lat and lon by even spacing in km
    n_trans = int(np.floor(coast_distance / spacing) + 1);
    n_points = int(np.floor(tran_distance / spacing) + 1);
    
    # Specify transect start and end points
    trans_lon0 = np.linspace(lon0, coast_lon1, num=n_trans)
    trans_lat0 = np.linspace(lat0, coast_lat1, num=n_trans)

    trans_lon1 = trans_lon0 + (tran_lon1 - lon0)
    trans_lat1 = trans_lat0 + (tran_lat1 - lat0)
    
    # Aproximate distance vectors along transects using first transect
    coast_distances = np.linspace(0, coast_distance, num=n_trans)
    tran_distances = np.linspace(0, tran_distance, num=n_points)
        
    return trans_lon0, trans_lat0, trans_lon1, trans_lat1, n_points, n_trans, coast_distances, tran_distances
