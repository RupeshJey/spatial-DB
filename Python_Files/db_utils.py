# Rupesh Jeyaram 
# Created July 22nd, 2018

# This file holds commonly used db tools / queries
import psycopg2 as dbapi               # For connecting to database
from datetime import datetime as dt    # For converting utc / date
import datetime                        # Comparing type

import netCDF4 as nc    # NetCDF stuff (mainly date conversion)
import shapely          # For checking shape type (Polygon/Multipolygon)
import itertools        # For looping through multipolygons
import numpy as np      # Converting lists to np lists (bugs out otherwise)
import math             # For converting mercator / coordinates
import geopandas as gpd                # For extracting data in a geo framework
import pandas as pd     # For downloading data and saving as NetCDF
from pyproj import Proj, transform     # For converting coordinates
from scipy.io import netcdf     # Convenient NetCDF creator

# For getting the connection details (stored abstractly)
from connection_info import conn as conn_info

# Connect to database
conn = dbapi.connect(port= conn_info['port'], 
                     user= conn_info['user'],
                     password= conn_info['password'], 
                     database= conn_info['database'])

# Cursor to execute queries and read output
cursor = conn.cursor() 

def query_db(cmd):
    """
    Execute query on db, and return output
    Parameters: 
    cmd (string): the command to be executed
    Returns: 
    list of rows
    """

    # Execute query
    cursor.execute(cmd)

    # Obtain values
    vals = list(cursor)

    # If only one value, return it (not in a list)
    if (len(vals) == 1):
        return vals[0]

    # Otherwise, return the list itself
    else:
        return vals

def spatial_query_db(cmd, geom_col = 'shape'):
    """Execute a spatial query using geopandas and return output
    
    Parameters: 
    cmd (string): the command to be executed
    geom_col (string): the geometry column; default = 'shape'

    Returns:
    GeoDataFrame of results
    """
    return gpd.GeoDataFrame.from_postgis(cmd, conn, geom_col = geom_col)

def pandas_query_db(cmd, parse_dates = None):
    """Execute a query using pandas and return output

    Parameters: 
    cmd (string): the command to be executed
    parse_dates: list of strings that are date columns

    Returns: 
    DataFrame of results
    """ 
    return pd.read_sql(cmd, conn, parse_dates=parse_dates)

def utc_from_timestamp(date):
    """Return utc format from timestamp.""" 

    # If this is a date already, go ahead and return it
    if type(date) == datetime.date:
        return date
    # Otherwise, convert it first
    return dt.utcfromtimestamp(date/1000).strftime('%Y-%m-%d')

def multify(shapes):
    """ 
    Convert geometry-wise items to x and y series items. 

    Take a series of shapes (polygons or multi-polygons) 
    and map it to a series of x-values and y-values, 
    that can be read by bokeh. 

    Parameters: 
    shapes: list of shapes to reformat (from shapely format)

    Returns: 
    list of rows with appended content
    """ 

    # Create empty containers for the new shapes
    xs = []
    ys = []
    xs_appended = []
    ys_appended = []

    # For each shape
    for s in shapes:
        
        # If this is a simple polygon
        if (type(s) == shapely.geometry.polygon.Polygon):

            # Extract polygon as a series of points
            xs_curr, ys_curr = s.exterior.coords.xy

            xs.append(np.array(xs_curr))
            ys.append(np.array(ys_curr))

        # If this is a multipolygon
        else:

            # Obtain list of constituent polygons
            ps = list(s)

            # Join xs and ys together, separated by NaN's
            # (Bokeh way to separate contituent polygons of multipolygons)

            # Container for multipolgyon
            xs_curr = np.array([])
            ys_curr = np.array([]) 

            # Loop over each polgyon
            for i in range(len(ps)):

                # Extract x and y series
                single_xs, single_ys = ps[i].exterior.coords.xy
                single_xs = np.array(single_xs)
                single_ys = np.array(single_ys)

                # Append them to the list of xs and ys for this shape
                xs_curr = np.append(xs_curr, single_xs)
                ys_curr = np.append(ys_curr, single_ys)

                # Separate this polygon with NaN
                xs_curr = np.append(xs_curr, np.array([float('NaN')]))
                ys_curr = np.append(ys_curr, np.array([float('NaN')]))

            # Add the current polygon's xs/ys to the overall shape's xs/ys
            xs.append(np.array(xs_curr))
            ys.append(np.array(ys_curr))

    return (np.array(xs), np.array(ys))

def to_lat_lon(y, x):
    """Take mercator projection coords and return lat/lon.""" 

    return transform(Proj(init='epsg:3857'), 
                     Proj(init='epsg:4326'), 
                     x, y)

def convert_shapes_to_mercator(lats, lons):
    """Take lat/long coords (lists) and return them in mercator projection.""" 

    new_lats = []
    new_lons = []

    for shape_num in range(lats.size):
        new_c_lat = []        
        new_c_lon = []
        for i in range((lats[int(shape_num)]).size):
            curr_lat = lats[int(shape_num)][int(i)]
            curr_lon = lons[int(shape_num)][int(i)]
            new_lat, new_lon = transform(Proj(init='epsg:4326'), 
                                         Proj(init='epsg:3857'), 
                                         curr_lon, curr_lat)
            new_c_lat.append(np.array(new_lat))
            new_c_lon.append(np.array(new_lon))
        new_lats.append(np.array(new_c_lat))
        new_lons.append(np.array(new_c_lon))

    return (np.array(new_lats), np.array(new_lons))

def save_db_to_nc(output_file, cmd, time_col='time', geom_col='geom', 
                  n_points_in_geom=5, geom_x_name='lon_bnds', 
                  geom_y_name='lat_bnds', calendar_type='standard',
                  calendar_units='seconds since 1970-01-01 00:00'):
    """
    Extract data from database and store in nc file

    Parameters: 

    output_file (string): where to save the data, local or global path

    cmd (string): SQL command to execute on the spatial DB

    time_col = 'time' (string, optional): the 'time' column to parse properly

    geom_col = 'geom' (string, optional): 'geometry' column to parse as 
               series of xs and ys. 
    
    geom_x_name, geom_y_name (strings, optional) = 'lon_bnds', 'lat_bnds': 
               names of optional geometry's xs and ys columns

    calendar_type, calendar_units (strings, optional) = 'standard', 
    'seconds since 1970-01-01 00:00': 
               See: https://bit.ly/2OYAC0w

    Returns: None
    """

    # Obtain data
    df = spatial_query_db(cmd, geom_col = geom_col)

    # Convert to numpy array
    data = df.to_numpy()

    # Open a file to start writing
    f = netcdf.netcdf_file(output_file, 'w')

    # Create the dimensions needed 
    # For now, record_id and corner should suffice
    f.createDimension('record_id', len(data))
    f.createDimension('corner', n_points_in_geom)

    # Get the column names so we can reuse them for the NetCDF file
    column_names = list(df.columns) 

    # For each column 
    for i in range(len(column_names)):

        # Extract column name
        column_name = column_names[i]

        # If this is the geometry column, save the xs and ys separately, 
        # using the corner dimension
        if column_name == geom_col:
            var_x = f.createVariable(geom_x_name, 'd', ('record_id','corner'))
            var_y = f.createVariable(geom_y_name, 'd', ('record_id','corner'))
            var_x[:] = np.array([(i.exterior.coords.xy)[0] for i in data[:,i]])
            var_y[:] = np.array([(i.exterior.coords.xy)[1] for i in data[:,i]])

        # If this is the time column, be sure to convert to 'units' type
        elif column_name == time_col:
            var = f.createVariable(column_name, 'd', ('record_id',))
            var[:] = nc.date2num((data[:,i]).tolist(), 
                                  units=calendar_units, calendar=calendar_type)
        
        # Otherwise, just go ahead and load this data normally
        else:
            var = f.createVariable(column_name, 'd', ('record_id',))
            var[:] = (data[:,i]).tolist()

    # Save and close the NetCDF file
    f.close()

def load_raster_as_points(filename, raster_table, points_table, 
                delete_raster_when_finished=True):
    """ 
    Input a specified raster file into the database, 
    and load the points into a separate table

    Parameters: 
    filename (string): the file that should be imported
    raster_table (string): name of table to create for raster
    points_table (string): name of table to create for points

    """ 

    cmd = "CREATE TABLE IF NOT EXISTS %s (\
                    rid       SERIAL    NOT NULL,\
                    rast      RASTER    NOT NULL, \
                    filename  TEXT      NOT NULL,\
                    PRIMARY KEY (rid)\
                );" % raster_table

    cmd = "CREATE TABLE IF NOT EXISTS %s (\
                    rid       SERIAL    NOT NULL,\
                    rast      RASTER    NOT NULL, \
                    filename  TEXT      NOT NULL,\
                    PRIMARY KEY (rid)\
                );" % points_table

    cursor.execute("DROP TABLE IF EXISTS elevation_rasters; %s" % cmd)
    connection.commit()
