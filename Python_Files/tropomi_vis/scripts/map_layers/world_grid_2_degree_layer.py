# Rupesh Jeyaram 
# Created July 25th, 2019

# This class contains all the respective functions for the world grid
# (2 degree x 2 degree) layer

from shape_layer import ShapeLayer
from db_utils import *  # For easier querying
import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Math array things

class US_World_Grid_2_Degree_Layer(ShapeLayer):

    def __init__(self):
        self.name = 'Cell (2 Degree)'
        self.none_selected_str = "SIF Time-Series (Select a cell...)"
        self.multiple_selected_str = "SIF Time-Series in Multiple Cells"

        # Command to retrieve all the county shapes
        cmd_shapes = 'SELECT * FROM world_grid_2_degree ORDER BY lon, lat'

        # Query to obtain first and last day recorded
        cmd_day_range = 'SELECT MIN(day) AS min, MAX(day) AS max \
                         FROM world_grid_2_degree_day_sif_facts'

        # Initialize the class using these commands
        super().__init__(cmd_shapes, cmd_day_range)

    # Given a date range, this function returns the average sif for the counties
    # in the specified range
    def get_data_for_date_range(self, start_date, end_date):

        # Command to retrieve the day's county-wise averages
        cmd = 'SELECT ROUND(AVG(sif_avg), 3) \
               FROM world_grid_2_degree_day_sif_facts\
               WHERE day BETWEEN \'%s\' AND \'%s\' \
               GROUP BY lon, lat \
               ORDER BY lon, lat' % (start_date, end_date)

        return np.array(query_db(cmd))

    # callback that will plot the time series of a selected county
    def get_patch_time_series(self, event):

        # Obtain click information w.r.t. lat/lon
        coord_x, coord_y = to_lat_lon(event.y, event.x)

        # Command that requests SIF time-series for desired county
        cmd =  "WITH cell AS (SELECT lon, lat, name, shape FROM world_grid_2_degree \
                                WHERE (shape && 'POINT(%s %s)' :: geometry)\
                                AND ST_CONTAINS(shape, \
                                    'POINT(%s %s)' :: geometry)\
                LIMIT 1)\
                SELECT (SELECT name from cell), \
                        day, \
                        ROUND(sif_avg, 3) FROM world_grid_2_degree_day_sif_facts \
                WHERE lon = (SELECT lon FROM cell) AND\
                lat = (SELECT lat FROM cell)\
                AND sif_avg IS NOT NULL\
                ORDER BY day;" \
                % (coord_x, coord_y, coord_x, coord_y)

        return super().get_patch_time_series(cmd)
        