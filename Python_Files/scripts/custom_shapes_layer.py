# Rupesh Jeyaram 
# Created July 23rd, 2019

# This class contains all the respective functions for a layer with 
# custom shapes (user-selected using selection tool)

from shapelayer import ShapeLayer
from db_utils import *  # For easier querying
import numpy as np      # Math array things

class Custom_Shapes_Layer(ShapeLayer):

    def __init__(self):

        # Set up all necessary lists
        self.name = 'Custom Shapes'
        self.start_date, self.end_date = ('2019-06-01', '2019-06-29')
        self.xs = []
        self.ys = []
        self.series = []
        self.names = []
        self.polygon_strs = []

    # Given a date range, this function returns the average sif for the shapes
    # in the specified range
    def get_data_for_date_range(self, start_date, end_date):
        return np.array([])

    # Callback that will plot the time series of a selected region
    def get_patch_time_series(self, event):

        # If we just want to display the last-drawn shape
        # (No event triggered this)
        if (event == None):
            return ("SIF Time-Series in %s" % (self.names[-1]), self.series[-1]) 

        # If we want to find the actually clicked-on polygon
        # Go through every shape in the list of polygons
        for i in range(len(self.polygon_strs)):

            # Check whether the click fell inside a polygon

            # Convert to lat/lon
            coord_x, coord_y = to_lat_lon(event.y, event.x)

            # Construct command
            cmd = " WITH region AS (SELECT ST_GeomFromText(\'%s\') AS shape)\
                SELECT (region.shape && 'POINT(%s %s)' :: geometry) AND \
                ST_CONTAINS(region.shape, 'POINT(%s %s)' :: geometry) \
                FROM region;" \
                % (self.polygon_strs[i], coord_x, coord_y, coord_x, coord_y)

            # Obtain results
            result = query_db(cmd)

            # If the click was inside this polygon, return the associated data
            if result == (True,):
                return ("SIF Time-Series in %s" % \
                                (self.names[i]), self.series[i]) 

        # If none of the polygons matched, return default parameters
        return ("Select a region...", dict(date=np.array([]), sif=np.array([]))) 
    
    def get_map_details(self):
        """Return initial properties of the map (xs, ys, names)."""
        return np.array(self.xs), np.array(self.ys), np.array(self.names)

    def get_date_range(self):
        """Return the valid date range of this layer."""
        return (self.start_date, self.end_date)

    def shape_selected(self, event):

        # Obtain selected geometry
        xs_curr = np.array(list(event.geometry['x'].values()))
        ys_curr = np.array(list(event.geometry['y'].values()))

        # Add to stored shapes
        self.xs.append(xs_curr)
        self.ys.append(ys_curr)

        self.names.append("Custom Shape #%i" % (len(self.names) + 1))

        # Create dictionary
        custom_data = dict(x= xs_curr, y= ys_curr)

        # Construct SQL cmd to pull time-series from selected region

        polygon_str = "POLYGON(("
        coords = list(zip(xs_curr, ys_curr))
        for x, y in coords:
            coord_x, coord_y = to_lat_lon(y, x)
            polygon_str += (str(coord_x) + " " + str(coord_y) + ",")
        x_first, y_first = coords[0]
        coord_x, coord_y = to_lat_lon(y_first, x_first)
        polygon_str += (str(coord_x) + " " + str(coord_y) + ",")
        polygon_str = polygon_str[:-1] + "))"

        self.polygon_strs.append(polygon_str)

        cmd = " WITH region AS (SELECT ST_GeomFromText(\'%s\') AS shape)\
                SELECT date_trunc('day', time), \
                        ROUND(AVG(sif), 3) FROM tropomi_sif \
                WHERE ((SELECT shape FROM region) && center_pt) \
                        AND ST_CONTAINS((SELECT shape FROM region), center_pt)\
                GROUP BY date_trunc('day', time)\
                ORDER BY date_trunc('day', time);" % polygon_str

        # Query and obtain results
        result = query_db(cmd)

        # Check that there are sufficient values
        if len(result) <= 1:
            return 

        # Map the rows to columns and take series
        mapped_result = [list(i) for i in zip(*result)]
        dates, sifs = (mapped_result[0], mapped_result[1])

        # Append this dict to the list of series
        self.series.append(dict(date=dates, sif=sifs))
