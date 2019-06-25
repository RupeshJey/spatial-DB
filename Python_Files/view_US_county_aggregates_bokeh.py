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
from bokeh.models import ColumnDataSource           # For holding data
from bokeh.palettes import Viridis256 as palette    # The palette to use
from bokeh.plotting import figure, curdoc           # For creating the map
from bokeh.events import Tap                        # For recognizing tap
from bokeh.layouts import column                    # For arranging view in cols
from bokeh.models import ColorBar                   # For map's color bar


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
    active_scroll = "wheel_zoom",
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Average SIF", "@sifs"), ("(Long, Lat)", "($x, $y)")
    ],
    plot_height = 600,
    plot_width = 1200,
    output_backend="webgl")

# No logo
p.toolbar.logo = None

# No grid
p.grid.grid_line_color = None

# Policy for hovering
p.hover.point_policy = "follow_mouse"

# Color mapper
color_mapper = LogColorMapper(palette=palette)

# Patch all the information onto the map
p.patches('x', 'y', source=data,
          fill_color={'field': 'sifs', 'transform': color_mapper},
          fill_alpha=0.9, line_color="white", line_width=0.1)
p.title.text_font_size = '16pt'

# create a callback that will add a number in a random location
def county_clicked(event):

    # Obtain click information
    coord_x = event.x
    coord_y = event.y

    # Command that requests the SIF value time-series for the selected county
    cmd =  "WITH county AS (SELECT name, shape FROM shapes \
                            WHERE (shape && 'POINT(%s %s)' :: geometry)\
                            AND ST_CONTAINS(shape, 'POINT(%s %s)' :: geometry)\
                            AND type = 'County'\
            LIMIT 1)\
            SELECT (SELECT name from county), \
                    date_trunc('day', time), \
                    AVG(sif) FROM tropomi_sif \
            WHERE ((SELECT shape FROM county) && center_pt) \
                    AND ST_CONTAINS((SELECT shape FROM county), center_pt)\
            GROUP BY date_trunc('day', time)\
            ORDER BY date_trunc('day', time);" \
            % (coord_x, coord_y, coord_x, coord_y)

    # Execute query and obtain results
    cursor.execute(cmd)

    # Array to store the series of obtained results
    dates = []
    sifs = []

    # Get the county's name
    county_name = ''

    # Loop through each record and get the info you need
    for name, date, avg in cursor:
        county_name = name
        dates.append(date.date())
        sifs.append(float(avg))

    # Set the title of the Time Series plot to reflect the selected county
    sif_series.title.text = "SIF Time-Series in County: %s" % (name)
    source.data = dict(date=dates, t1=sifs)

# Source of the time-series data should be empty for now
source = ColumnDataSource(data=dict(date=[], t1=[]))

# Figure that holds the time-series
sif_series = figure(plot_width=800, plot_height=400, x_axis_type='datetime',
                    title= "SIF Time-Series (Select county..)",
                    x_axis_label = 'Date',
                    y_axis_label = 'SIF Average')

# Scatter/line plot to reflect data in source
sif_series.line('date', 't1', source=source, 
                line_dash='dashed', color = "green")
sif_series.circle('date', 't1', size=10, source=source, color="green")

# Some font choices
sif_series.title.text_font_size = '16pt'
sif_series.xaxis.axis_label_text_font_size = "12pt"
sif_series.yaxis.axis_label_text_font_size = "12pt"

# No logo
sif_series.toolbar.logo = None

# When a patch is selected, trigger the county_clicked function
p.on_event(Tap, county_clicked)

# Put the patches and sif_series together in a column and set this 
# as the document's root
curdoc().add_root(column(p, sif_series))

