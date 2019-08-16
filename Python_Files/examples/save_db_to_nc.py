# Rupesh Jeyaram 
# Created August 14th, 2019

# Take a query, and save the resulting rows to a .nc (NetCDF) file

from db_utils import *    # Querying tools

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
        WHERE name = 'Los Angeles' \
        AND type = 'County' \
        AND (shape && center_pt) \
        AND ST_CONTAINS(shape, center_pt);"

save_db_to_nc(OUTPUT_FILE, cmd, geom_col = 'mbr')
