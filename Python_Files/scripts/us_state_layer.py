# Rupesh Jeyaram 
# Created July 23rd, 2019

# This class contains all the respective functions for the US States 
# layer

from shapelayer import ShapeLayer
from db_utils import *  # For easier querying
import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Math array things

class US_State_Layer(ShapeLayer):

    def __init__(self):
        self.name = 'US States'

        # Command to retrieve all the state shapes
        cmd = 'SELECT * FROM shapes WHERE type = \'State\' \
               ORDER BY shape_id'

        # Execute query and obtain results
        self.states = spatial_query_db(cmd)

        # Extract names
        self.state_names = self.states["name"].values

        # Obtain the state shapes and names in single-polygon form
        self.state_xs, self.state_ys, self.state_names = \
                        multify(self.states["shape"].values, 
                                self.state_names, 
                                return_polygons = True)

        # Convert to mercator projection
        self.state_xs, self.state_ys = \
                    convert_shapes_to_mercator(self.state_ys, self.state_xs)

        # Query to obtain first and last day recorded
        cmd = 'SELECT MIN(day) AS min, MAX(day) AS max \
               FROM state_day_sif_facts'
        self.start_date, self.end_date = query_db(cmd)

    # Given a date range, this function returns the average sif for the states
    # in the specified range
    def get_data_for_date_range(self, start_date, end_date):

        # Command to retrieve the day's state-wise averages
        cmd = 'SELECT AVG(sif_avg) \
               FROM state_day_sif_facts\
               WHERE day BETWEEN \'%s\' AND \'%s\' \
               GROUP BY shape_id \
               ORDER BY shape_id' % (start_date, end_date)

        sifs = np.array(query_db(cmd))

        return multify(self.states["shape"].values, sifs)

    # callback that will plot the time series of a selected state
    def get_patch_time_series(self, event):

        # Obtain click information w.r.t. lat/lon
        coord_x, coord_y = to_lat_lon(event.y, event.x)

        # Command that requests SIF time-series for desired state
        cmd =  "WITH state AS (SELECT shape_id, name, shape FROM shapes \
                                WHERE (shape && 'POINT(%s %s)' :: geometry)\
                                AND ST_CONTAINS(shape, \
                                    'POINT(%s %s)' :: geometry)\
                                AND type = 'State'\
                LIMIT 1)\
                SELECT (SELECT name from state), \
                        day, \
                        sif_avg FROM state_day_sif_facts \
                WHERE shape_id = (SELECT shape_id FROM state)\
                AND sif_avg IS NOT NULL\
                ORDER BY day;" \
                % (coord_x, coord_y, coord_x, coord_y)

        # Obtain results
        result = query_db(cmd)

        # If empty, clear and return
        if len(result) == 0:
            return ("SIF Time-Series (Select a state...)", 
                    dict(date=[], sif=[]))

        # Map the rows to columns and take series
        mapped_result = [list(i) for i in zip(*result)]
        state_name, dates, sifs = (result[0][0], mapped_result[1], 
                                   mapped_result[2])

        # Return new title and time series
        return ("SIF Time-Series in State: %s" % (state_name), 
                dict(date=dates, sif=sifs))
    
    # Return initial properties of the map (xs, ys, names)
    def get_map_details(self):
        return self.state_xs, self.state_ys, self.state_names

    def get_date_range(self):
        """Return the valid date range of this layer."""
        return (self.start_date, self.end_date)