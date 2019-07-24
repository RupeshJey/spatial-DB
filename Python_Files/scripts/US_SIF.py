# Rupesh Jeyaram 
# Created July 17th, 2019

# This file handles all the code for the US SIF visualizations tab

import time                            # For timing
from datetime import date              # For date queries
from db_utils import *                 # For easier querying

from bokeh.models import LinearColorMapper          # For mapping values/colors
from bokeh.models import ColumnDataSource           # For holding data
from bokeh.palettes import Viridis256 as palette    # The map palette to use
from bokeh.palettes import Category10 as time_pltt  # Time srs palette to use
from bokeh.plotting import figure                   # For creating the map
from bokeh.events import Tap                        # For recognizing tap
from bokeh.layouts import row, column               # For arranging view in grid
from bokeh.models import ColorBar, FixedTicker      # For map's color bar
from bokeh.models import DateRangeSlider            # For date selection
from bokeh.models import Panel                      # For assigning grid to view
from bokeh.models.widgets import RadioButtonGroup   # Selecting layer

# For mapping
from bokeh.tile_providers import get_provider, Vendors

# Custom layers
from us_county_layer import US_County_Layer
from us_state_layer import US_State_Layer

import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Converting lists to np lists (bugs out otherwise)

# The date range the map should start on
START_DATE_INIT = date(2019, 1, 5)
END_DATE_INIT = date(2019, 1, 15)

# Initialize all layers
us_state_layer = US_State_Layer()
us_county_layer = US_County_Layer()

# Set the active layer to be the county layer
active_layer = us_county_layer

# Function that generates the US visualization and passes the tab to main
def US_SIF_tab():

    #################################
    # Set up layer selector
    #################################

    # Once a new layer is selected, use that layer to refresh the page
    # and all data
    def refresh_page():
        
        # Obtain and update date boundaries
        start_date, end_date = active_layer.get_date_range()
        date_range_slider.start = start_date
        date_range_slider.end = end_date

        # Get initial map details
        xs, ys, names = active_layer.get_map_details()

        # Get the initial sif values
        sifs = active_layer.get_data_for_date_range(START_DATE_INIT, 
                                                    END_DATE_INIT)

        # Dictionary to hold the data
        new_source_dict = dict(
            x= np.array(xs), y= np.array(ys),
            name= np.array(names), sifs= np.array(sifs))
        
        # Update all source data values
        source.data = new_source_dict

    # Trigger for when a new layer is selected
    def layer_selected(new):

        # We want to modify the global active layer (not local to this func)
        global active_layer

        # Simple dictionary to switch out the active layer
        switcher = {
            0 : None,
            1 : us_state_layer,
            2 : us_county_layer,
            3 : None,
        }

        # Swap out the active layer
        active_layer = switcher.get(new, active_layer) 

        # Fetch new dates, shapes, names, etc. and refresh the page
        refresh_page()

    # Define selection labels
    layer_selector = RadioButtonGroup(
        labels=["None", "US States", "US Counties", "World"], active=2)

    # Set up layer selection callback
    layer_selector.on_click(layer_selected)

    #################################
    # Set up date range slider
    #################################

    # Obtain date boundaries
    start_date, end_date = active_layer.get_date_range()

    # create a callback for when the date slider is changed
    def date_range_selected(attr, old, new):

        t0 = time.time()

        # Unpack the new range
        range_start, range_end = new

        # Convert to SQL format
        range_start = utc_from_timestamp(range_start)
        range_end = utc_from_timestamp(range_end)
        
        # Get the new day's data
        sifs = active_layer.get_data_for_date_range(range_start, range_end)

        # Update the sif values
        source.data["sifs"] = np.array(sifs)

        # Set the title of the map to reflect the selected date
        p.title.text = "SIF Average by County: %s to %s" % (range_start, 
                                                            range_end)

        print("Took " + str(time.time() - t0) + " seconds to update")

    # Create the date slider
    date_range_slider = DateRangeSlider(title="Date Range: ", 
                                        start=start_date, end=end_date, 
                                        value=(START_DATE_INIT, 
                                            END_DATE_INIT), step=1)

    # Assign the callback for when the date slider changes
    date_range_slider.callback_policy = "throttle"
    date_range_slider.callback_throttle = 200
    date_range_slider.on_change('value_throttled', date_range_selected)

    #################################
    # Set up the map and its source
    #################################

    # Get initial map details
    xs, ys, names = active_layer.get_map_details()

    # Get the initial sif values 
    sifs = active_layer.get_data_for_date_range(START_DATE_INIT, 
                                                END_DATE_INIT)

    # Dictionary to hold the data
    source=ColumnDataSource(data = dict(
        x= np.array(xs),
        y= np.array(ys),
        name= np.array(names),
        sifs= np.array(sifs))
    )

    # Which tools should be available to the user
    TOOLS = "pan,wheel_zoom,reset,hover,save,tap"

    # Obtain map provider
    tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)

    # Don't want the map to wrap around
    tile_provider.wrap_around = False

    # Configure the figure
    p = figure(
        title="SIF Average by County: %s" % end_date, tools=TOOLS,
        active_scroll = "wheel_zoom",
        x_axis_location=None, y_axis_location=None,
        tooltips=[
            ("Name", "@name"), 
            ("Average SIF", "@sifs")
        ],
        x_axis_type='mercator',
        y_axis_type='mercator',
        plot_height = 900,
        plot_width = 1100,
        output_backend="webgl")

    # Add the map!
    p.add_tile(tile_provider)

    p.lod_threshold = None          # No downsampling
    p.toolbar.logo = None           # No logo
    p.grid.grid_line_color = None   # No grid

    # Policy for hovering
    p.hover.point_policy = "follow_mouse"

    # Color mapper
    color_mapper = LinearColorMapper(palette=palette, low = -1, high = 3)

    # Patch all the information onto the map
    p.patches('x', 'y', source=source,
              fill_color={'field': 'sifs', 'transform': color_mapper},
              fill_alpha=0.9, line_color="white", line_width=0.1, 
              legend = "Map")
    p.legend.location = "top_right"
    p.legend.click_policy="hide"
    p.title.text_font_size = '16pt'

    # Add a color bar
    ticker = FixedTicker(ticks=[-1,0,1,2])
    color_bar = ColorBar(color_mapper=color_mapper, ticker = ticker,
                     label_standoff=12, border_line_color=None, location=(0,0))
    p.add_layout(color_bar, 'right')

    #################################
    # Set up time series
    #################################

    def patch_clicked(event):

        # Obtain new information
        new_title, series_data = active_layer.get_patch_time_series(event)

        # Set the title of the Time Series plot
        sif_series.title.text = new_title

        # Set the appropriate data source
        time_srs_src.data = series_data

    # Source of the time-series data should be empty for now
    time_srs_src = ColumnDataSource(data=dict(date=[], sif=[]))

    # Which tools should be available to the user for the timer series
    TOOLS = "pan,wheel_zoom,reset,hover,save,tap"

    # Figure that holds the time-series
    sif_series = figure(plot_width=750, plot_height=400, x_axis_type='datetime',
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

    # When a patch is selected, trigger the patch_time_series function
    p.on_event(Tap, patch_clicked)

    #################################
    # Set up tab
    #################################

    # The layout of the view
    layout = row(column(p, date_range_slider, layer_selector), sif_series)

    # Create tab using layout
    tab = Panel(child=layout, title = 'US Visualization')

    # Return the created tab
    return tab
        