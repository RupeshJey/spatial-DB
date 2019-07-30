# Rupesh Jeyaram 
# Created July 22nd, 2018

# This file holds commonly used db tools / queries
import psycopg2 as dbapi               # For connecting to database
from datetime import datetime as dt    # For converting utc / date
import datetime                        # Comparing type

import shapely          # For checking shape type (Polygon/Multipolygon)
import itertools        # For looping through multipolygons
import numpy as np      # Converting lists to np lists (bugs out otherwise)
import math             # For converting mercator / coordinates
import geopandas as gpd                # For extracting data in a geo framework
from pyproj import Proj, transform     # For converting coordinates

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
    """
    Execute a spatial query using geopandas and return output
    Parameters: 
    cmd (string): the command to be executed
    geom_col (string): the geometry column; default = 'shape'
    Returns:
    GeoDataFrame of results
    """
    return gpd.GeoDataFrame.from_postgis(cmd, conn, geom_col = geom_col)

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

            xs.append(np.array(xs_curr))
            ys.append(np.array(ys_curr))

    return (np.array(xs), np.array(ys))

def to_lat_lon(y, x):
    """Take mercator projection coords and return lat/lon.""" 
    return transform(Proj(init='epsg:3857'), 
                     Proj(init='epsg:4326'), 
                     x, y)

def convert_shapes_to_mercator(lats, lons):

    """Take lat/long coords and return them in mercator projection.""" 

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