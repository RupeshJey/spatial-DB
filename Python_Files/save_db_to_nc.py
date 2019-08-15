# Rupesh Jeyaram 
# Created August 14th, 2019

# Take a query, and save the resulting rows to a .nc (NetCDF) file

import numpy as np              # For accessing the data more efficiently
import netCDF4 as nc            # NetCDF stuff (mainly date conversion)
import db_utils                 # Querying tools
from scipy.io import netcdf     # Convenient NetCDF creator

# Script parameters
OUTPUT_FILE = 'tropomi_LA_basin.nc'

TIME_COL = 'time'
GEOM_COL = 'mbr'
N_PNTS_IN_GEOM = 5
GEOM_X_NAME = 'lon_bnds'
GEOM_Y_NAME = 'lat_bnds'

CALENDAR_TYPE = 'standard'
CALENDAR_UNITS = 'seconds since 1970-01-01 00:00'

# Command to extract needed data
cmd = "SELECT time, sif, sif_err, sif_relative, dcsif, cloud_fraction, \
        sza, vza, nir, saa, phase_angle, dcf, ST_X(center_pt) AS lon, \
        ST_Y(center_pt) AS lat, mbr \
        FROM shapes, tropomi_sif \
        WHERE name = 'California' \
        AND type = 'State' \
        AND (shape && center_pt) \
        AND ST_CONTAINS(shape, center_pt);"

# Obtain data
df = db_utils.spatial_query_db(cmd, geom_col = GEOM_COL)

# Convert to numpy array
data = df.to_numpy()

# Open a file to start writing
f = netcdf.netcdf_file(OUTPUT_FILE, 'w')

# Create the dimensions needed 
# For now, record_id and corner should suffice
f.createDimension('record_id', len(data))
f.createDimension('corner', N_PNTS_IN_GEOM)

# Get the column names so we can reuse them for the NetCDF file
column_names = list(df.columns) 

# For each column 
for i in range(len(column_names)):

    # Extract column name
    column_name = column_names[i]

    # If this is the geometry column, save the xs and ys separately, 
    # using the corner dimension
    if column_name == GEOM_COL:
        var_x = f.createVariable(GEOM_X_NAME, 'd', ('record_id','corner'))
        var_y = f.createVariable(GEOM_Y_NAME, 'd', ('record_id','corner'))
        var_x[:] = np.array([(i.exterior.coords.xy)[0] for i in data[:,i]])
        var_y[:] = np.array([(i.exterior.coords.xy)[1] for i in data[:,i]])

    # If this is the time column, be sure to convert to 'units' type
    elif column_name == TIME_COL:
        var = f.createVariable(column_name, 'd', ('record_id',))
        var[:] = nc.date2num((data[:,i]).tolist(), 
                              units=CALENDAR_UNITS, calendar=CALENDAR_TYPE)
    
    # Otherwise, just go ahead and load this data normally
    else:
        var = f.createVariable(column_name, 'd', ('record_id',))
        var[:] = (data[:,i]).tolist()

# Save and close the NetCDF file
f.close()
