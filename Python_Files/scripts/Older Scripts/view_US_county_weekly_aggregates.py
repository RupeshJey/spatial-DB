# Rupesh Jeyaram 
# Created June 30th, 2019

# Using this file, the user can visualize SIF aggregates by county
# by week

import psycopg2 as dbapi          # For connecting to database
import json                       # For parsing shapes
import geopandas as gpd           # For extracting data in a geo framework
import time                       # For timing 
import matplotlib.pyplot as plt   # For plotting the data

# For getting the connection details (stored abstractly)
from connection_info import conn

# Connect to database
connection = dbapi.connect(port= conn['port'], 
                     user= conn['user'],
                     password= conn['password'], 
                     database= conn['database'])

# Cursor to execute queries and read output
cursor = connection.cursor()

# Given the week number, visualize the weekly aggregate's map
def save_weekly_aggregate(i):

    # Command that requests the average SIF value for each county
    cmd = "SELECT name, AVG(sif) AS sif, shape \
           FROM tropomi_sif CROSS JOIN shapes \
           WHERE type = 'County' AND\
           ST_X(center_pt) > -130 AND\
           (shape && center_pt) AND ST_CONTAINS(shape, center_pt) AND\
           time BETWEEN 'April 1 2018'::timestamp + INTERVAL '%i week' AND \
                'April 1 2018'::timestamp + INTERVAL '%i week'\
           GROUP BY name, shape;" % (i, i + 1)

    # Start time
    t0 = time.time()

    # Execute query and obtain results
    counties = gpd.GeoDataFrame.from_postgis(cmd, connection, 
                                             geom_col = 'shape')

    # Notify user of how long it took to execute
    print(str(i) + ": Took " + str(time.time() - t0) + " seconds to run")

    # Plot the retrieved data
    counties.plot(column = 'sif', legend = True, vmin = -1, vmax = 2)

    # Give the plots appropriate title/labels
    plt.title('SIF Average by County: Week %i' % i)
    plt.ylabel('latitude')
    plt.xlabel('longitude')

    plt.xlim(-130, -60)
    plt.ylim(20, 55)

    # Save the plot
    plt.savefig('frame{}.png'.format(i), dpi = 300)

for i in range(50):
    save_weekly_aggregate(i)
