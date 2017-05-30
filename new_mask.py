#!/usr/bin/env python3

import csv
import numpy
import netCDF4
import io

with netCDF4.Dataset('tmp_wet.nc') as nc:
  wet = nc.variables['wet'][:]

lon = numpy.arange(0.5,360.,1.)
lat = numpy.arange(-89.5,90.,1.)
lon_edge = numpy.arange(0.,360.5,1.)
lat_edge = numpy.arange(-90.,90.5,1.)

# Restrict to 0 or 1. This also filers out badly coded missing values.
wet[ wet>=0.5 ] = 1.
wet[ wet<0.5 ] = 0.

# Special cases
wet[98,281] = 0. # Panama
wet[126,354] = 1. # Gibraltar Strait

# Create new file
with netCDF4.Dataset('wet_mask_1x1.nc', 'w', format='NETCDF3_64BIT') as ncf:
    # Metadata
    ncf.title = 'Wet mask for 1x1 regridded ocean output'
    ncf.history = 'See https://github.com/adcroft/wet_mask_1x1'
    ncf.version = '1.0'
    # Dimensions
    ncf.createDimension('lon', lon.shape[0])
    ncf.createDimension('lat', lat.shape[0])
    ncf.createDimension('nv', 2)
    # Latitude, longitude of cell centers
    nc_lon = ncf.createVariable('lon', 'f', ('lon',))
    nc_lon.units = 'degrees_east'
    nc_lon.standard_name = 'longitude'
    nc_lon.long_name = 'Longitude'
    nc_lon.bounds = 'lonbnd'
    nc_lat = ncf.createVariable('lat', 'f', ('lat',))
    nc_lat.units = 'degrees_north'
    nc_lat.standard_name = 'latitude'
    nc_lat.long_name = 'Latitude'
    nc_lat.bounds = 'latbnd'
    # Latitude, longitude of cell corners
    nc_lonbnd = ncf.createVariable('lonbnd', 'f', ('lon','nv',))
    nc_lonbnd.units = 'degrees_east'
    nc_lonbnd.standard_name = 'longitude'
    nc_latbnd = ncf.createVariable('latbnd', 'f', ('lat','nv',))
    nc_latbnd.units = 'degrees_north'
    nc_latbnd.standard_name = 'latitude'
    # Data variables
    nc_wet = ncf.createVariable('wet', 'f', ('lat','lon'))
    nc_wet.units = 'nondim'
    nc_wet.standard_name = 'upward_geothermal_heat_flux_at_sea_floor'
    nc_wet.long_name = '0 if land, 1 if ocean at tracer points'
    nc_wet.cell_methods = 'area: mean'
    # Write data
    nc_lon[:] = lon[:]
    nc_lat[:] = lat[:]
    nc_lonbnd[:,0] = lon_edge[:-1]
    nc_lonbnd[:,1] = lon_edge[1:]
    nc_latbnd[:,0] = lat_edge[:-1]
    nc_latbnd[:,1] = lat_edge[1:]
    nc_wet[:,:] = wet[:,:]
