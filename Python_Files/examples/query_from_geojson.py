# Rupesh Jeyaram 
# Created August 28th, 2019

from db_utils import *              # For querying
import json                         # For parsing shapes
import matplotlib.pyplot as plt     # For plotting 

# Open shapes file
with open('example_shapes.geojson') as f:
    data = json.load(f)

# Where to put each time series
time_series = []

# Loop through each shape
for feature in data['features']:

    # If this shape is a polygon 
    if feature['geometry']['type'] == 'Polygon':

        # Obtain the coordinates
        coords = feature['geometry']['coordinates'][0]

        # And build the PostGIS "Polygon" constructor
        poly_str = 'POLYGON(('
        for p in coords:
            poly_str += (str(p[0]) + ' ' + str(p[1]) + ', ')
        poly_str = poly_str[:-2] + '))'

        # Command to pull out the time-series
        cmd = " WITH region AS (SELECT ST_GeomFromText(\'%s\') AS shape)\
                    SELECT date_trunc('day', time) AS day, \
                            ROUND(AVG(sif), 3) AS sif_avg FROM tropomi_sif \
                    WHERE (\
                        (SELECT shape FROM region) && center_pt) \
                         AND ST_CONTAINS((SELECT shape FROM region), center_pt)\
                    GROUP BY date_trunc('day', time)\
                    ORDER BY date_trunc('day', time);" % poly_str
        
        # Add this series to the time series list
        time_series.append(pandas_query_db(cmd))

# Set up plot
fig, ax = plt.subplots()
ax.set_title('Time Series for GeoJSON Selected Shapes')
ax.set_xlabel('Day')
ax.set_ylabel('SIF')
ax.legend()
fig.autofmt_xdate()

# Plot each time-series
for i in range(len(time_series)):
    ax.scatter(time_series[i]['day'], time_series[i]['sif_avg'], 
        s = 5, alpha = 0.75, 
        label = 'Shape ' + str(i))    

# Save plot
plt.savefig('time_series_from_geojson.png')

