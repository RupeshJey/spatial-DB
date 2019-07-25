# Rupesh Jeyaram 
# Created July 22nd, 2018

# This file holds commonly used db tools / queries
import psycopg2 as dbapi               # For connecting to database
from datetime import datetime as dt    # For converting utc / date
import datetime                        # Comparing type

import shapely          # For checking shape type (Polygon/Multipolygon)
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

def multify(shapes, rows, return_polygons = False):
    """ 
    Convert geometry-wise items to polygon-wise items
    Take a series of rows corresponding to shapes 
    (polygons or multi-polygons) and map it to a series
    of strictly polygons, by appending all non-first 
    polygon values to the end. 
    Parameters: 
    shapes: list of shapes to examine (shapely format)
    rows: the actual data to reformat
    return_polygons: whether you want the actual point-wise lists of 
                     polygons back
    Returns: 
    list of rows with appended content
    """ 

    # If needed, create empty containers for the new shapes
    if (return_polygons):
        xs = []
        ys = []
        xs_appended = []
        ys_appended = []

    # Keep track of every row in the shapes list
    shape_num = 0

    # For each shape
    for s in shapes:
        
        # If this is a simple polygon
        if (type(s) == shapely.geometry.polygon.Polygon):

            # If needed, 
            if (return_polygons):
                # Extract polygon as a series of points
                xs_curr, ys_curr = s.exterior.coords.xy
                xs.append(np.array(xs_curr))
                ys.append(np.array(ys_curr))

        # If this is a multipolygon
        else:
            # Obtain list of constituent polygons
            ps = list(s)

            # If needed, 
            # Extract the first polygon's series and insert into 
            # the points lists. Do this to avoid messing up the
            # mapping b/w names, sifs, and shapes

            if (return_polygons):
                xs_curr, ys_curr = ps[0].exterior.coords.xy
                xs.append(np.array(xs_curr))
                ys.append(np.array(ys_curr))

            # Add copy of row for each polygon
            for i in range(len(ps) - 1):
                rows = np.append(rows, rows[shape_num])

                if (return_polygons):
                    xs_curr, ys_curr = ps[i+1].exterior.coords.xy
                    xs_appended.append(np.array(xs_curr))
                    ys_appended.append(np.array(ys_curr))

        # Increment county number
        shape_num += 1
    
    if (return_polygons):

        if (len(xs_appended) > 0):
            xs = np.append(xs, xs_appended)
            ys = np.append(ys, ys_appended)

        return (xs, ys, rows) # list [array([])] vs. list [list([])]

    return rows

def to_lat_lon(y, x):
    """Take mercator projection coords and return lat/lon.""" 
    return transform(Proj(init='epsg:3857'), 
                     Proj(init='epsg:4326'), 
                     x, y)

def convert_shapes_to_mercator(lats, lons):

    """Take mercator projection shapes and return them in lat/lon.""" 

    new_lats = []
    new_lons = []

    for shape_num in range(len(lats)):
        new_c_lat = []
        new_c_lon = []
        for i in range(len(lats[shape_num])):
            curr_lat = lats[shape_num][i]
            curr_lon = lons[shape_num][i]
            new_lat, new_lon = transform(Proj(init='epsg:4326'), 
                                         Proj(init='epsg:3857'), 
                                         curr_lon, curr_lat)
            new_c_lat.append(new_lat)
            new_c_lon.append(new_lon)
        new_lats.append(new_c_lat)
        new_lons.append(new_c_lon)

    return (np.array(new_lats), np.array(new_lons))