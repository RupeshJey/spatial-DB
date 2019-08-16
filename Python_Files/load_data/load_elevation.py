# Rupesh Jeyaram 
# Created August 5th, 2019

# Load all the world elevation data into the elevation_rasters table 
# and the elevation_points table from the raw .bil raster files

import time                     # For timing insertions
import os                       # For searching through files + executing cmd's
import psycopg2 as dbapi        # For connecting to database
import sys                      # For printing status

# For getting the connection details (stored abstractly)
from connection_info import conn

# Where to find the data
SOURCE = '/net/fluo/data3/HydroSheds_3s_con'   

# Connect to database
connection = dbapi.connect(port= conn['port'], 
                     user= conn['user'],
                     password= conn['password'], 
                     database= conn['database'])

# Cursor to execute queries and read output
cursor = connection.cursor()

########################################################################
# Create databases
########################################################################

# Set up the database itself
os.system("PGPASSWORD=%s psql -U %s -p %s -d %s -f \
           ../SQL_Scripts/make_world_elevation_tables.sql" % 
           (conn['password'], conn['user'], conn['port'], conn['database']))

########################################################################
# Input all rasters, into point form
########################################################################

# Move to source directory 
os.chdir(SOURCE)

# File counter
i = 1

# Total number of files to look through
total = sum(1 for file in os.listdir(SOURCE) if file.endswith(".bil")) 

# For each elevation file
for filename in sorted(os.listdir(SOURCE)):
    if filename.endswith(".bil"): 

        # Notify user that we are looking at said file
        print("Inserting file %i/%i: %s" % (i, total, filename))

        # Start the timer
        t0 = time.time()

        # The raster index should only be generated once
        flag = ""
        if i == 1:
            flag = "-I"

        cmd = "CREATE TABLE elevation_rasters (\
                    rid       SERIAL    NOT NULL,\
                    rast      RASTER    NOT NULL, \
                    filename  TEXT      NOT NULL,\
                    PRIMARY KEY (rid)\
                );"

        cursor.execute("DROP TABLE IF EXISTS elevation_rasters; %s" % cmd)
        connection.commit()

        # Create the sql script to input the raster
        os.system("/usr/pgsql-11/bin/raster2pgsql -F -a %s -s 0 -t 1000x1000\
                    %s elevation_rasters > raster_maker.sql" % (flag, filename)) 

        # Input the raster
        os.system("PGPASSWORD=%s psql -U %s -p %s -d %s -f raster_maker.sql" % 
                    (conn['password'], conn['user'], 
                     conn['port'], conn['database']))

        print("Converting raster to points...")

        for j in range(36):

            print("Portion %i" %j )

            # Create command to save points and aspects into database
            cmd = " WITH slopes AS \
                     (SELECT rid, (ST_PixelAsPoints(rast)).*, \
                                  (ST_PixelAsPoints(ST_Slope(rast, 1, '32BF', \
                                            'DEGREES', 370400))).val AS sval,\
                                  (ST_PixelAsPoints(ST_Aspect(rast))).val \
                                             AS aval\
                      FROM elevation_rasters WHERE rid = %i)\
                    INSERT INTO elevation_points \
                                    (rid, center_pt, elevation, slope, aspect)\
                    SELECT rid, geom, val, sval, aval FROM slopes;" % (j + 1)

            # Execute said command
            cursor.execute(cmd)

        # Notify the user of how long it took to insert the data
        print("Inserting the records took %i seconds" % (time.time() - t0))

        # Commit the transaction to the database
        connection.commit()

        i += 1