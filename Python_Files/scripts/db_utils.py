# Rupesh Jeyaram 
# Created July 22nd, 2018

# This file holds commonly used db tools / queries
import psycopg2 as dbapi               # For connecting to database
from datetime import datetime as dt    # For converting utc / date

import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Converting lists to np lists (bugs out otherwise)
import math             # For converting mercator / coordinates
from pyproj import Proj, transform          # For converting coordinates

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
    
def get_date_range():
    """Return the valid date range."""
    
    # Query to obtain first and last day recorded
    cmd = 'SELECT MIN(day) AS min, MAX(day) AS max \
           FROM county_day_sif_facts'

    return query_db(cmd)

def utc_from_timestamp(date):
    """Return utc format from timestamp.""" 
    return dt.utcfromtimestamp(date/1000).strftime('%Y-%m-%d')

def multify(shapes, rows):
    """ 
    Convert geometry-wise rows to polygon-wise rows

    Take a series of rows corresponding to shapes 
    (polygons or multi-polygons) and map it to a series
    of strictly polygons, by appending all non-first 
    polygon values to the end. 

    Parameters: 
    shapes: list of shapes to examine (shapely format)
    rows: the actual data to reformat

    Returns: 
    list of rows with appended content

    """ 

    # Keep track of every row in the shapes list
    county_num = 0

    # For each shape
    for s in shapes:
        # If this is a multipolygon
        if (type(s) != shapely.geometry.polygon.Polygon):
            # Obtain list of constituent polygons
            ps = list(s)
            # Add copy of row for each polygon
            for i in range(len(ps) - 1):
                rows = np.append(rows, rows[county_num])
        # Otherwise, increment county_num and keep going
        else:
            county_num += 1

    return rows

def to_mercator(lat, lon):

    """Take lat/lon and convert to mercator-projection coordinates"""

    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x / lon
    y = 180.0 / math.pi * \
        math.log(math.tan(math.pi/4.0 + lat * (math.pi/180.0)/2.0)) * scale
    return (x, y)

def to_lat_lon(y, x):
    return transform(Proj(init='epsg:3857'), 
                     Proj(init='epsg:4326'), 
                     x, y)

def convert_shapes_to_mercator(lats, lons):

    new_lats = []
    new_lons = []

    for county_num in range(len(lats)):
        new_c_lat = []
        new_c_lon = []
        for i in range(len(lats[county_num])):
            curr_lat = lats[county_num][i]
            curr_lon = lons[county_num][i]
            # new_lat, new_lon = to_mercator(curr_lat, curr_lon)
            new_lat, new_lon = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), curr_lon, curr_lat)
            new_c_lat.append(new_lat)
            new_c_lon.append(new_lon)
        new_lats.append(new_c_lat)
        new_lons.append(new_c_lon)

    return (np.array(new_lats), np.array(new_lons))

