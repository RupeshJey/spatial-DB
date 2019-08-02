# Rupesh Jeyaram 
# Created July 23rd, 2019

# A superclass for Shape Layers (Also, the None Shape Layer)

# Each layer (US county, worldwide, Chinese Province, etc.) presents its 
# own shapes and averages onto the map, but performs the same essential 
# tasks. Thus, it makes sense to create a Shape Layer superclass that 
# each specific layer inherits. 

from db_utils import *  # For easier querying
import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Math array things

class ShapeLayer: 

    def __init__(self, cmd_shapes, cmd_day_range, convert_to_mercator=True):
        
        # Execute shapes query and obtain results
        self.shapes = spatial_query_db(cmd_shapes)

        # Extract names
        self.shape_names = self.shapes["name"].values

        # Obtain the shapes in bokeh polygon form
        self.shape_xs, self.shape_ys = multify(self.shapes["shape"].values)

        # Convert to mercator projection
        self.shape_xs, self.shape_ys = \
                    convert_shapes_to_mercator(self.shape_ys, self.shape_xs)

        # Obtain day range from query
        self.start_date, self.end_date = query_db(cmd_day_range)

        # Initialize currently selected patches (indices and series)
        self.selected_patches = dict(selected_indices=[], active_sources=[],
                                     names=[])

    def get_map_details(self):
        """Return initial properties of the map (xs, ys, names)."""
        return self.shape_xs, self.shape_ys, self.shape_names

    def patch_clicked(self, source, event):

        """ 

        Parameters: 
        source: DataFrame to see selected shapes
        event: Event of the click

        Returns: 
        String: the new title of the time series
        List: source dictionaries to plot
        List: names to use in the legend
        """ 

        # If no shapes selected
        if len(source.selected.indices) == 0:

            # Clear the selected patches 
            self.selected_patches = dict(selected_indices=[], active_sources=[],
                                         names=[])
            # And return empty values
            return (self.none_selected_str, 
                    [dict(date=[], sif=[])], "")

        # If one shape now selected
        elif len(source.selected.indices) == 1:

            # Get the title and time series from that one shape
            title, time_series = self.get_patch_time_series(event)

            # Set the object parameters
            self.selected_patches["selected_indices"] = \
                    [source.selected.indices[0]]
            self.selected_patches["active_sources"] = \
                [dict((key, time_series[key]) for key in ('date', 'sif'))]
            self.selected_patches["names"] = [time_series["name"]]

        # If multiple counties selected
        else:

            # Get the time series from this new county
            _, time_series = self.get_patch_time_series(event)

            # Add the new data to the object parameters
            title = self.multiple_selected_str
            self.selected_patches["active_sources"].append \
                (dict((key, time_series[key]) for key in ('date', 'sif')))
            self.selected_patches["names"].append(time_series["name"])

        # Return the appropriate title and data
        return (title, self.selected_patches["active_sources"],
                self.selected_patches["names"])

    def get_date_range(self):
        """Return the valid date range of this layer."""
        return (self.start_date, self.end_date)

    def get_patch_time_series(self, cmd):

        # Obtain results
        result = query_db(cmd)

        # If empty, clear and return
        if len(result) == 0:
            return (self.none_selected_str, dict(date=[], sif=[]))

        # Map the rows to columns and take series
        mapped_result = [list(i) for i in zip(*result)]
        county_name, dates, sifs = (result[0][0], mapped_result[1], 
                                    mapped_result[2])

        # Change all None values to NaN values
        # This will allow ColumnDataSource to skip over the NaN's
        sifs_w_nans = [np.nan if type(x)==type(None) else x for x in sifs]

        # Return new title and time series
        return ("SIF Time-Series in %s: %s" % (self.name, county_name), 
                dict(name=county_name, date=dates, sif=sifs_w_nans))
