# Rupesh Jeyaram 
# Created June 21st, 2019

# Using this file, the user can visualize SIF aggregates by county

import psycopg2 as dbapi          # For connecting to database
import json                       # For parsing shapes
import geopandas as gpd           # For extracting data in a geo framework
import time                       # For timing the insertion
import matplotlib.pyplot as plt   # For plotting the data

# Where to find the data
SOURCE = '../Shape_Outlines/'   
COUNTY_FILE = 'Counties_LCC.shp'

# Connect to database
conn = dbapi.connect(host= '127.0.0.1', 
                     port= 5432, 
                     user= 'postgres',
                     password= 'frankenberg', 
                     database= 'SIF_Experiments')

# Cursor to execute queries and read output
cursor = conn.cursor()

# Command that requests the average SIF value for each county
cmd = "SELECT name, AVG(sif) AS sif, shape \
       FROM tropomi_sif CROSS JOIN shapes \
       WHERE type = 'County' AND\
       (shape && center_pt) AND ST_CONTAINS(shape, center_pt) \
       GROUP BY name, shape;"

# Start time
t0 = time.time()

# Execute query and obtain results
counties = gpd.GeoDataFrame.from_postgis(cmd, conn, geom_col = 'shape')

# Notify user of how long it took to execute
print("Took " + str(time.time() - t0) + " seconds to run")

# Plot the retrieved data
counties.plot(column = 'sif', legend = True)

# Give the plots appropriate title/labels
plt.title('SIF Average by County: 02/01/2019 - 02/05/2019')
plt.ylabel('latitude')
plt.xlabel('longitude')

# Show the plot
plt.show()
