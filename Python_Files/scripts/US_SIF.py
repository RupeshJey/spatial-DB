# Rupesh Jeyaram 
# Created July 17th, 2019

# This file handles all the code for the US SIF visualizations tab

import time                 # For timing stuff
from datetime import date   # For date commands
from db_utils import *      # For common database utilities

from bokeh.palettes import Viridis256 as palette    # The map palette to use
from bokeh.palettes import Category10 as time_pltt  # Time srs palette to use
from bokeh.plotting import figure                   # For creating the map
import itertools

# Tap:                  For recognizing selection of shape
# SelectionGeometry:    For custom shape selection
# ButtonClick:          For button clicks
from bokeh.events import Tap, SelectionGeometry, ButtonClick     
from bokeh.layouts import row, column               # For arranging view in grid

# Colorbar:             For map's color bar
# FixedTicker:          For ticks on color bar
# DateRangeSlider:      For date selection
# LassoSelectToolPanel: For custom shape selection
# Panel:                For creating a tab
# LinearColorMapper:    For mapping values/colors
# ColumnDataSource:     For holding data 
# ZoomIn/OutTool:       For zooming in and out with clicks
from bokeh.models import ColorBar, FixedTicker, DateRangeSlider, \
                         LassoSelectTool, Panel, LinearColorMapper, \
                         ColumnDataSource, ZoomInTool, ZoomOutTool 

# To remove select time series
from bokeh.models.renderers import GlyphRenderer

# Custom saving
from bokeh.models.callbacks import CustomJS

# RadioButtonGroup:     For selecting active layer
# Button:               For data saving widget
from bokeh.models.widgets import RadioButtonGroup, Button   

# For drawing the basemap
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import WMTSTileSource

# Custom layers
from custom_shapes_layer import Custom_Shapes_Layer
from world_grid_2_degree_layer import US_World_Grid_2_Degree_Layer
from us_county_layer import US_County_Layer
from us_state_layer import US_State_Layer

import numpy as np      # Converting lists to np lists (bugs out otherwise)

# For layer serialization
import pickle
import os.path
from os import path

# The date range the map should start on
START_DATE_INIT = date(2018, 9, 1)
END_DATE_INIT = date(2018, 9, 11)

# Time series scale
SIF_MIN, SIF_MAX = (-1.5, 4.0)

# Where the layers should be stored in serialization
LAYERS_FILE = 'layers.dump'

# Zooming factor for ZoomIn/Out Tools
ZOOM_FACTOR = 0.5

# Function that generates the US visualization and passes the tab to main
def US_SIF_tab():

    #################################
    # Initialize all layers
    #################################

    # Load from a save file
    if path.exists(LAYERS_FILE):
        with open(LAYERS_FILE, 'rb') as layers_file:
            us_county_layer, us_state_layer, \
            world_grid_2_degree_layer = pickle.load(layers_file)
    # Load from scratch
    else:
        us_county_layer = US_County_Layer()
        us_state_layer = US_State_Layer()
        world_grid_2_degree_layer = US_World_Grid_2_Degree_Layer()
        # Save the layers to file
        with open(LAYERS_FILE, 'wb') as layers_file:
            layers = (us_county_layer, \
                        us_state_layer, world_grid_2_degree_layer)
            pickle.dump(layers, layers_file)

    # Want the custom layer to be new every time
    custom_shapes_layer = Custom_Shapes_Layer()

    # Set the active layer to be the county layer
    active_layer = us_county_layer

    #################################
    # Set up layer selector
    #################################

    # Once a new layer is selected, use that layer to refresh the page
    # and all data
    def refresh_page():
        
        # Get initial map details
        xs, ys, names = active_layer.get_map_details()

        if type(active_layer) != Custom_Shapes_Layer:

            # Obtain and update date boundaries
            start_date, end_date = active_layer.get_date_range()
            date_range_slider.start = start_date
            date_range_slider.end = end_date

            # Unpack the current range
            range_start, range_end = date_range_slider.value

            # Convert to SQL format
            range_start = utc_from_timestamp(range_start)
            range_end = utc_from_timestamp(range_end)

            # Get the initial sif values
            sifs = active_layer.get_data_for_date_range(range_start, 
                                                        range_end)

            # Dictionary to hold the data
            new_source_dict = dict(
                x= xs, y= ys,
                name= np.array(names), sifs= np.array(sifs))
            
            # Update all source data values
            source.data = new_source_dict

            # Turn off custom layer
            custom_data_source.data = dict(x= np.array([]), y= np.array([]), 
                                           name = np.array([]))

        else:

            # Turn off the other layers
            source.data = dict(x= np.array([]), y= np.array([]),
                name= np.array([]), sifs= np.array([]))

            # Safeguard - that at least one custom shape is drawn
            if (xs.size != 0):

                # Dictionary to hold the selected shape data
                new_source_dict = dict(
                    x= xs, y= ys,
                    name = np.array(names))

                custom_data_source.data = new_source_dict


    # Trigger for when a new layer is selected
    def layer_selected(new):

        # We want to modify the overall active layer (not local to this func)
        nonlocal active_layer

        # Simple dictionary to switch out the active layer
        switcher = {
            0 : custom_shapes_layer,
            1 : us_state_layer,
            2 : us_county_layer,
            3 : world_grid_2_degree_layer,
        }

        # Swap out the active layer
        active_layer = switcher.get(new, active_layer) 
            
        # Fetch new dates, shapes, names, etc. and refresh the page
        refresh_page()

    # Define selection labels
    layer_selector = RadioButtonGroup(
        labels=["Custom", "US States", "US Counties", "World"], active=2)

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

        # Set the title of the map to reflect the selected date range
        p.title.text = "SIF Average: %s to %s" % (range_start, range_end)

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

    # tile_options = {}
    # tile_options['url'] = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    # tile_options['attribution'] = """
    #     Map tiles by <a href="http://stamen.com">Stamen Design</a>, under
    #     <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>.
    #     Data by <a href="http://openstreetmap.org">OpenStreetMap</a>,
    #     under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.
    #     """
    # mq_tile_source = WMTSTileSource(**tile_options)

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
    color_transform = {'field': 'sifs', 'transform': color_mapper}

    # Patch all the information onto the map
    patch_renderer = p.patches('x', 'y', source=source,
                      fill_color=color_transform,
                      fill_alpha=0.9, line_color="white", line_width=0.1, 
                      selection_fill_alpha = 1.0, 
                      selection_fill_color = color_transform,
                      nonselection_line_color="black",
                      nonselection_fill_alpha=0.7,
                      nonselection_fill_color= color_transform)
    p.title.text_font_size = '16pt'

    # Add a color bar
    ticker = FixedTicker(ticks=[-1,0,1,2])
    color_bar = ColorBar(color_mapper=color_mapper, ticker = ticker,
                     label_standoff=12, border_line_color=None, location=(0,0))
    p.add_layout(color_bar, 'right')

    # Add zoom in / out tools
    p.add_tools(ZoomInTool(factor=ZOOM_FACTOR))
    p.add_tools(ZoomOutTool(factor=ZOOM_FACTOR))

    #################################
    # Set up custom plot data
    #################################

    # Data source for custom shapes
    custom_data_source = ColumnDataSource(data = \
                                        dict(x= np.array([]), y= np.array([]), 
                                        name=np.array([])))

    # Patch the custom data onto the map
    p.patches('x', 'y', source=custom_data_source,
                  line_color="darkslategray", line_width=1, 
                  fill_alpha=0.3, fill_color="lightgray")

    #################################
    # Set up time series
    #################################

    def color_gen():
        yield from itertools.cycle(time_pltt[10])
    color = color_gen()

    def shape_drawn(event):

        # Check if more than one point
        # Otherwise a tap triggers this function
        if (type(event.geometry['x']) != float):

            # Notify the custom selection layer that this
            # shape was selected and obtain relevant info
            # custom_shapes_layer.patch_selected(event)

            # Change to the custom layer
            layer_selector.active = 0
            layer_selected(0)

            # Notify the layer that this patch was created. 
            active_layer.patch_created(event)

            # Clear all time series
            sif_series.renderers = []

            # Update the title and get new data from the active layer
            sif_series.title.text, time_srs_src_list, names = \
                                active_layer.patch_clicked(source, None)

            # Plot each series returned
            for i in range(len(time_srs_src_list)):
                sif_series.scatter('date', 'sif', 
                                    source=time_srs_src_list[i], 
                                    color=time_pltt[10][i])
            # Make sure the current shape is drawn
            refresh_page()

    def patch_clicked(event):
        """ When a patch is clicked, update the time series chart. """

        # Clear all time series
        sif_series.renderers = []

        # Update the title and get new data from the active layer
        sif_series.title.text, time_srs_src_list, names = \
                            active_layer.patch_clicked(source, event)

        # Plot each series returned
        for i in range(len(time_srs_src_list)):
            sif_series.scatter('date', 'sif', 
                                source=time_srs_src_list[i], 
                                color=time_pltt[10][i])

    # Which tools should be available to the user for the timer series
    TOOLS = "pan,wheel_zoom,reset,hover,save"

    # Figure that holds the time-series
    sif_series = figure(plot_width=750, plot_height=400, x_axis_type='datetime',
                        tools=TOOLS, 
                        title= "SIF Time-Series (Select a county...)",
                        active_scroll = "wheel_zoom",
                        tooltips=[
                            ("Day", "@date"), 
                            ("Average SIF", "@sif")
                        ],
                        x_axis_label = 'Date',
                        y_axis_label = 'SIF Average',
                        y_range = (SIF_MIN, SIF_MAX))

    # Some font choices
    sif_series.title.text_font_size = '16pt'
    sif_series.xaxis.axis_label_text_font_size = "12pt"
    sif_series.yaxis.axis_label_text_font_size = "12pt"

    # Policy for hovering
    sif_series.hover.point_policy = "follow_mouse"

    # No logo
    sif_series.toolbar.logo = None

    # When a patch is selected, trigger the patch_time_series function
    p.on_event(Tap, patch_clicked)
    
    # On geometry selection
    lasso = LassoSelectTool(select_every_mousemove = False)
    p.add_tools(lasso)
    p.on_event(SelectionGeometry, shape_drawn)

    #################################
    # TODO: Set up download area
    #################################
    # def save_data():
    #     active_layer.save_data()
    #     print("Button Clicked")

    # callback = active_layer.get_save_data_js_callback()

    button = Button(label="Save Data", button_type="success")
    # button.on_click(active_layer.save_data)
    #button.js_on_event(ButtonClick, callback)

    #################################
    # Set up tab
    #################################

    # The layout of the view
    layout = row(column(p, date_range_slider, layer_selector), 
                 column(sif_series, row(column(), button)))

    # Create tab using layout
    tab = Panel(child=layout, title = 'US Visualization')

    # Return the created tab
    return tab