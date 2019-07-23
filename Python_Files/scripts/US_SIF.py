# Rupesh Jeyaram 
# Created July 17th, 2019

# This file handles all the code for the US SIF visualizations tab

import geopandas as gpd                # For extracting data in a geo framework
import time                            # For timing
from datetime import date              # For date queries
from db_utils import *                 # For easier querying

from bokeh.models import LinearColorMapper          # For mapping values/colors
from bokeh.models import ColumnDataSource           # For holding data
from bokeh.palettes import Viridis256 as palette    # The map palette to use
from bokeh.palettes import Category10 as time_pltt  # Time srs palette to use
from bokeh.plotting import figure, curdoc           # For creating the map
from bokeh.events import Tap                        # For recognizing tap
from bokeh.layouts import row, column               # For arranging view in grid
from bokeh.models import ColorBar, FixedTicker      # For map's color bar
from bokeh.models import DateSlider, DateRangeSlider# For date selection
from bokeh.models import Panel                      # For assigning grid to view

# For mapping
from bokeh.tile_providers import get_provider, Vendors

import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Converting lists to np lists (bugs out otherwise)

# Function that generates the US visualization and passes the tab to main
def US_SIF_tab():

    #################################
    # Set up date slider
    #################################

    # create a callback for when the date slider is changed
    def date_selected(attr, old, new):

        t0 = time.time()

        # Get the new day's data
        sifs = get_data_for_day(new)

        # Match sifs to the multi-polygons format
        sifs = multify(counties["shapes_simple"].values, sifs)

        # Update the sif values
        source.data["sifs"] = np.array(sifs)

        # Set the title of the map to reflect the selected date
        p.title.text = "SIF Average by County: %s" % new

        print("Took " + str(time.time() - t0) + " seconds to retrieve new data")

    # Obtain date boundaries
    start_date, end_date = get_date_range()

    # Create the date slider
    date_slider = DateSlider(title="Date", value=end_date, 
        start=start_date, end=end_date, step=1)

    # Assign the callback for when the date slider changes
    date_slider.callback_policy = "mouseup"
    date_slider.on_change('value', date_selected)

    #################################
    # Set up date range slider
    #################################

    # Given a date ragne, this function returns the average sif for the counties
    # in the specified range
    def get_data_for_date_range(start_date, end_date):

        # Command to retrieve the day's county-wise averages
        cmd = 'SELECT AVG(sif_avg) \
               FROM county_day_sif_facts\
               WHERE day BETWEEN \'%s\' AND \'%s\' \
               GROUP BY shape_id \
               ORDER BY shape_id' % (start_date, end_date)

        return (np.array(query_db(cmd)))

    # create a callback for when the date slider is changed
    def date_range_selected(attr, old, new):

        t0 = time.time()

        # Unpack the new range
        range_start, range_end = new

        # Convert to SQL format
        range_start = utc_from_timestamp(range_start)
        range_end = utc_from_timestamp(range_end)
        
        # Get the new day's data
        sifs = get_data_for_date_range(range_start, range_end)
        
        # Match sifs to the multi-polygons format
        sifs = multify(counties["shapes_simple"].values, sifs)

        # Update the sif values
        source.data["sifs"] = np.array(sifs)

        # Set the title of the map to reflect the selected date
        p.title.text = "SIF Average by County: %s to %s" % (range_start, 
                                                            range_end)

        print("Took " + str(time.time() - t0) + " seconds to update")

    # Create the date slider
    date_range_slider = DateRangeSlider(title="Date Range: ", 
                                        start=start_date, end=end_date, 
                                        value=(date(2018, 9, 7), 
                                            date(2018, 9, 17)), step=1)

    # Assign the callback for when the date slider changes
    date_range_slider.callback_policy = "throttle"
    date_range_slider.callback_throttle = 200
    date_range_slider.on_change('value_throttled', date_range_selected)

    #################################
    # Set up the map and its source
    #################################

    # Given a date, this function returns the sif values for the counties
    def get_data_for_day(day):

        # Command to retrieve the day's county-wise averages
        cmd = 'SELECT sif_avg \
               FROM county_day_sif_facts NATURAL JOIN shapes\
               WHERE day = \'%s\' \
               AND type = \'County\'\
               ORDER BY shape_id' % (day)
        
        # Obtain results
        results = query_db(cmd)

        # Return sif_averages and shapes
        return np.array(results)

    # Command to retrieve all the county shapes
    cmd = 'SELECT * FROM shapes WHERE type = \'County\' \
           ORDER BY shape_id'

    # Execute query and obtain results
    counties = gpd.GeoDataFrame.from_postgis(cmd, conn, 
                                             geom_col = 'shapes_simple')

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
    county_sifs = get_data_for_day(end_date)

    # For every shape (county) in the county_aggregates 
    for s in counties["shapes_simple"].values:

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

    print(np.shape(county_xs))
    print(np.shape(county_ys))

    # Convert to mercator projection
    county_xs, county_ys = convert_shapes_to_mercator(county_ys, county_xs)

    # r_major = 6378137.000

    # redone_county_ys = []

    # for x, y in zip(county_xs, county_ys):
    #     scale = x_new / y
    #     y_new = 180.0/math.pi * math.log(math.tan(math.pi/4.0 + 
    #             county_ys * (math.pi/180.0)/2.0)) * scale
    #     redone_county_ys.append(y_new)

    # Dictionary to hold the data
    source=ColumnDataSource(data = dict(
        x= np.array(county_xs),
        y= np.array(county_ys),
        name= np.array(county_names),
        sifs= np.array(county_sifs))
    )

    # Which tools should be available to the user
    TOOLS = "pan,wheel_zoom,reset,hover,save,tap"

    # Obtain map provider
    tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)

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
        x_axis_type='mercator',
        y_axis_type='mercator',
        plot_height = 600,
        plot_width = 1200,
        output_backend="webgl")

    # Add the map!
    p.add_tile(tile_provider)

    # No downsampling
    p.lod_threshold = None

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
    # Set up time series
    #################################

    # create a callback that will plot the time series of a selected county
    def county_clicked(event):

        # Obtain click information w.r.t. lat/lon
        coord_x, coord_y = to_lat_lon(event.y, event.x)

        # Command that requests SIF time-series for desired county
        cmd =  "WITH county AS (SELECT shape_id, name, shape FROM shapes \
                                WHERE (shape && 'POINT(%s %s)' :: geometry)\
                                AND ST_CONTAINS(shape, \
                                    'POINT(%s %s)' :: geometry)\
                                AND type = 'County'\
                LIMIT 1)\
                SELECT (SELECT name from county), \
                        day, \
                        sif_avg FROM county_day_sif_facts \
                WHERE shape_id = (SELECT shape_id FROM county)\
                AND sif_avg IS NOT NULL\
                ORDER BY day;" \
                % (coord_x, coord_y, coord_x, coord_y)

        # Obtain results
        result = query_db(cmd)

        # If empty, clear and return
        if len(result) == 0:
            sif_series.title.text = "SIF Time-Series (Select a county...)"
            time_srs_src.data = dict(date=[], sif=[])
            return

        # Map the rows to columns and take series
        mapped_result = [list(i) for i in zip(*result)]
        county_name, dates, sifs = (result[0][0], mapped_result[1], 
                                    mapped_result[2])

        # Set the title of the Time Series plot to reflect the selected county
        sif_series.title.text = "SIF Time-Series in County: %s" % (county_name)

        # Set the appropriate data source
        time_srs_src.data = dict(date=dates, sif=sifs)

    # Source of the time-series data should be empty for now
    time_srs_src = ColumnDataSource(data=dict(date=[], sif=[]))

    # Which tools should be available to the user for the timer series
    TOOLS = "pan,wheel_zoom,reset,hover,save,tap"

    # Figure that holds the time-series
    sif_series = figure(plot_width=800, plot_height=400, x_axis_type='datetime',
                        tools=TOOLS, 
                        title= "SIF Time-Series (Select a county...)",
                        active_scroll = "wheel_zoom",
                        x_axis_label = 'Date',
                        y_axis_label = 'SIF Average')

    sif_series.scatter('date', 'sif', 
                        source=time_srs_src, color = 'green')

    # Some font choices
    sif_series.title.text_font_size = '16pt'
    sif_series.xaxis.axis_label_text_font_size = "12pt"
    sif_series.yaxis.axis_label_text_font_size = "12pt"

    # No logo
    sif_series.toolbar.logo = None

    # When a patch is selected, trigger the county_clicked function
    p.on_event(Tap, county_clicked)

    #################################
    # Set up tab
    #################################

    # The layout of the view
    layout = column(p, date_range_slider, sif_series)

    # Create tab using layout
    tab = Panel(child=layout, title = 'US Visualization')

    # Return the created tab
    return tab
        