# Rupesh Jeyaram 
# Created July 22nd, 2018

# This file holds commonly used postgres tools / queries
import psycopg2 as dbapi               # For connecting to database
from datetime import datetime as dt    # For converting utc / date

import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Converting lists to np lists (bugs out otherwise)

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
