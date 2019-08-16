# Rupesh Jeyaram 
# Created July 23rd, 2019

# This class contains all the respective functions for the US States 
# layer

from shape_layer import ShapeLayer
from db_utils import *  # For easier querying
import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Math array things

class US_State_Layer(ShapeLayer):

    def __init__(self):
        # Set the layer's name
        self.name = 'State'
        self.none_selected_str = "SIF Time-Series (Select a state...)"
        self.multiple_selected_str = "SIF Time-Series in Multiple Counties"

        # Command to retrieve all the state shapes
        cmd_shapes = 'SELECT * FROM shapes WHERE type = \'State\' \
                      ORDER BY shape_id'

        # Query to obtain first and last day recorded
        cmd_day_range = 'SELECT MIN(day) AS min, MAX(day) AS max \
                         FROM state_day_sif_facts'

        # Set the shapes of this layer using the above queries
        super().__init__(cmd_shapes, cmd_day_range)

    # Given a date range, this function returns the average sif for the states
    # in the specified range
    def get_data_for_date_range(self, start_date, end_date):

        # Command to retrieve the day's state-wise averages
        cmd = 'SELECT ROUND(AVG(sif_avg), 3) \
               FROM state_day_sif_facts\
               WHERE day BETWEEN \'%s\' AND \'%s\' \
               GROUP BY shape_id \
               ORDER BY shape_id' % (start_date, end_date)

        return np.array(query_db(cmd))

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
                        ROUND(sif_avg, 3) FROM state_day_sif_facts \
                WHERE shape_id = (SELECT shape_id FROM state)\
                ORDER BY day;" \
                % (coord_x, coord_y, coord_x, coord_y)

        return super().get_patch_time_series(cmd)
