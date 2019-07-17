# Rupesh Jeyaram 
# Created July 17th, 2019

# This file handles all the code for the US SIF visualizations tab

import psycopg2 as dbapi          # For connecting to database
import json                       # For parsing shapes
import geopandas as gpd           # For extracting data in a geo framework
import time                       # For timing
import matplotlib.pyplot as plt   # For plotting the data
from datetime import date         # For date queries

from bokeh.io import show                           # For showing the plot
from bokeh.models import LinearColorMapper          # For mapping values/colors
from bokeh.models import ColumnDataSource           # For holding data
from bokeh.palettes import Viridis256 as palette    # The palette to use
from bokeh.plotting import figure, curdoc           # For creating the map
from bokeh.events import Tap                        # For recognizing tap
from bokeh.layouts import row, column               # For arranging view in grid
from bokeh.models import ColorBar, FixedTicker      # For map's color bar
from bokeh.models import DateSlider                 # For date selection
from bokeh.models import Panel                      # For assigning grid to view

import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Converting lists to np lists (bugs out otherwise)

# The key for NULL sif values, since 0 is a reasonable value
SIF_INVALID = -0

# For getting the connection details (stored abstractly)
from connection_info import conn as conn_info

# Connect to database
conn = dbapi.connect(port= conn_info['port'], 
                     user= conn_info['user'],
                     password= conn_info['password'], 
                     database= conn_info['database'])

# Cursor to execute queries and read output
cursor = conn.cursor()

# Function that generates the US visualization and passes the tab to main
def US_SIF_tab():

    # Given a date, this function returns the sif values for the counties
    def get_data_for_day(day):

        # Command to retrieve the day's county-wise averages
        cmd = 'SELECT sif_avg, shape \
               FROM county_day_sif_facts NATURAL JOIN shapes\
               WHERE day = \'%s\' \
               AND type = \'County\'\
               ORDER BY shape_id' % (day)
        
        # Execute the query
        cursor.execute(cmd)

        # Parcel up the results and return them
        sifs = []
        shapes = []

        for sif, shape in cursor:
            sifs.append(sif)
            shapes.append(shape)

        return (np.array(sifs), shapes)

    # Get the date range from the table
    def get_date_range():
        
        # Query to obtain first and last day recorded
        cmd = 'SELECT MIN(day) AS min, MAX(day) AS max \
               FROM county_day_sif_facts'

        # Execute query
        cursor.execute(cmd)

        # Obtain results
        for min_val, max_val in cursor:
            min_date = min_val
            max_date = max_val

        # Return the range
        return (min_date, max_date)

    # create a callback for when the date slider is changed
    def date_selected(attr, old, new):

        t0 = time.time()

        # Get the new day's data
        sifs, shapes = get_data_for_day(new)

        # For every shape (county) in the county_aggregates 
        county_num = 0
        for s in counties["shape"].values:

            # If this is a simple polygon 
            if (type(s) != shapely.geometry.polygon.Polygon):
                # List of polygons
                ps = list(s)
                for i in range(len(ps) - 1):
                    sifs = np.append(sifs, sifs[county_num])
            else:
                county_num += 1

        # Update the sif values
        source.data["sifs"] = np.array(sifs)

        print("Took " + str(time.time() - t0) + " seconds to retrieve new data")


    #################################
    # Set up date slider
    #################################

    # Obtain date boundaries
    start_date, end_date = get_date_range()

    # Create the date slider
    date_slider = DateSlider(title="Date", value=end_date, 
        start=start_date, end=end_date, step=1)

    # Assign the callback for when the date slider changes
    date_slider.on_change('value', date_selected)

    #################################
    # Set up the map and its source
    #################################

    cmd = 'SELECT * FROM shapes WHERE type = \'County\' ORDER BY shape_id'

    # Execute query and obtain results
    counties = gpd.GeoDataFrame.from_postgis(cmd, conn, 
                                             geom_col = 'shape')

    # Extract names
    county_names = counties["name"].values

    # List-to-populate of county polygons in point-list form
    county_xs = []
    county_ys = []

    # Multi-polygons will be appended at the end
    county_xs_appended = []
    county_ys_appended = []

    # Counter of counties covered
    county_num = 0

    # Get the initial sif values (just whatever the last day gives)
    county_sifs, z = get_data_for_day(end_date)

    # For every shape (county) in the county_aggregates 
    for s in counties["shape"].values:

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
                                    counties["name"].values[county_num])

                county_sifs = np.append(county_sifs, 
                                county_sifs[county_num])

    # Take the polygons from the multi-polygons and back-append them to the 
    # list of shapes. 

    county_xs = np.append(county_xs, county_xs_appended)
    county_ys = np.append(county_ys, county_ys_appended)

    # Dictionary to hold the data
    source=ColumnDataSource(data = dict(
        x= np.array(county_xs),
        y= np.array(county_ys),
        name= np.array(county_names),
        sifs= np.array(county_sifs))
    )

    # Which tools should be available to the user
    TOOLS = "pan,wheel_zoom,reset,hover,save,tap"

    # Configure the figure
    p = figure(
        title="SIF Average by County: %s" % end_date, tools=TOOLS,
        active_scroll = "wheel_zoom",
        x_axis_location=None, y_axis_location=None,
        tooltips=[
            ("Name", "@name"), 
            ("Average SIF", "@sifs"), 
            ("(Long, Lat)", "($x, $y)")
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
    color_mapper = LinearColorMapper(palette=palette, low = -1, high = 3)

    # Patch all the information onto the map
    p.patches('x', 'y', source=source,
              fill_color={'field': 'sifs', 'transform': color_mapper},
              fill_alpha=0.9, line_color="white", line_width=0.1)
    p.title.text_font_size = '16pt'

    # Add a color bar
    ticker = FixedTicker(ticks=[-1,0,1,2])
    color_bar = ColorBar(color_mapper=color_mapper, ticker = ticker,
                     label_standoff=12, border_line_color=None, location=(0,0))

    p.add_layout(color_bar, 'right')

    #################################
    # Set up tab
    #################################

    # The layout of the view
    layout = column(p, date_slider)

    # Create tab using layout
    tab = Panel(child=layout, title = 'US Visualization')

    # Return the created tab
    return tab
        