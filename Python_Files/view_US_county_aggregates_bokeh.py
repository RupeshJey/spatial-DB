# Rupesh Jeyaram 
# Created June 24th, 2019

# Using this file, the user can visualize SIF aggregates by county
# with bokeh, an interactive visualization library

import psycopg2 as dbapi          # For connecting to database
import json                       # For parsing shapes
import geopandas as gpd           # For extracting data in a geo framework
import time                       # For timing the insertion
import matplotlib.pyplot as plt   # For plotting the data


from bokeh.io import show                           # For showing the plot
from bokeh.models import LogColorMapper             # For mapping values/colors
from bokeh.palettes import Viridis256 as palette    # The palette to use
from bokeh.plotting import figure                   # For creating the map
from bokeh.events import Tap                        # For recognizing tap


import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Converting lists to np lists (bugs out otherwise)


# # Where to find the data
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
       ST_X(center_pt) > -140 AND\
       (shape && center_pt) AND ST_CONTAINS(shape, center_pt) \
       GROUP BY name, shape;"

# Start time
t0 = time.time()

# Execute query and obtain results
county_aggregates = gpd.GeoDataFrame.from_postgis(cmd, conn, geom_col = 'shape')

# Notify user of how long it took to execute
print("Took " + str(time.time() - t0) + " seconds to run")

# Extract names and sif values
county_names = county_aggregates["name"].values
county_averages = county_aggregates["sif"].values

# List-to-populate of county polygons in point-list form
county_xs = []
county_ys = []

# Multi-polygons will be appended at the end
county_xs_appended = []
county_ys_appended = []

# Counter of counties covered
county_num = 0

# For every shape (county) in the county_aggregates 
for s in county_aggregates["shape"].values:

    # If this is a simple polygon 
    if (type(s) == shapely.geometry.polygon.Polygon):

        # Extract polygon as a series of points
        xs, ys = s.exterior.coords.xy
        county_xs.append(np.array(xs))
        county_ys.append(np.array(ys))

        # Increment county-counter
        county_num += 1

    # If this is a multi-polygon
    else:

        # List of polygons
        ps = list(s)

        # Extract the first polygon's series and insert into 
        # the points lists. Do this to avoid messing up the
        # mapping b/w names, sifs, and shapes

        xs, ys = ps[0].exterior.coords.xy
        county_xs.append(np.array(xs))
        county_ys.append(np.array(ys))

        # Take the remaining polygons and insert them at the 
        # end of the lists. 

        for i in range(len(ps) - 1):
            xs, ys = ps[i+1].exterior.coords.xy
            county_xs_appended.append(np.array(xs))
            county_ys_appended.append(np.array(ys))
            county_names = np.append(county_names, 
                                county_aggregates["name"].values[county_num])
            county_averages = np.append(county_averages, 
                                county_aggregates["sif"].values[county_num])

# Take the polygons from the multi-polygons and back-append them to the 
# list of shapes. 

county_xs = np.append(county_xs, county_xs_appended)
county_ys = np.append(county_ys, county_ys_appended)

# Dictionary to hold the data
data=dict(
    x= np.array(county_xs),
    y= np.array(county_ys),
    name= np.array(county_names),
    sifs= np.array(county_averages),
)

# Which tools should be available to the user
TOOLS = "pan,wheel_zoom,reset,hover,save,tap"

# Configure the figure
p = figure(
    title="SIF Average by County: 02/01/2019 - 02/05/2019", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Average SIF", "@sifs"), ("(Long, Lat)", "($x, $y)")
    ],
    plot_height = 800,
    plot_width = 1600)

# No grid
p.grid.grid_line_color = None

# Policy for hovering
p.hover.point_policy = "follow_mouse"

# Color mapper
color_mapper = LogColorMapper(palette=palette)

# Patch all the information onto the map
p.patches('x', 'y', source=data,
          fill_color={'field': 'sifs', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.1)

# Show the map! 
show(p)
