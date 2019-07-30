# Rupesh Jeyaram 
# Created July 25th, 2019

# This class contains all the respective functions for the world grid
# (2 degree x 2 degree) layer

from shapelayer import ShapeLayer
from db_utils import *  # For easier querying
import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Math array things

class US_World_Grid_2_Degree_Layer(ShapeLayer):

    def __init__(self):
        self.name = 'World Grid (2 Degree)'

        # Command to retrieve all the county shapes
        cmd = 'SELECT * FROM world_grid_2_degree ORDER BY lon, lat'

        # Execute query and obtain results
        self.cells = spatial_query_db(cmd)

        # Extract names
        self.cell_names = self.cells["name"].values

        # Obtain the cell shapes in single-polygon form
        self.cell_xs, self.cell_ys = multify(self.cells["shape"].values)

        # Convert to mercator projection
        self.cell_xs, self.cell_ys = \
                    convert_shapes_to_mercator(self.cell_ys, self.cell_xs)

        # List of arrays

        # Query to obtain first and last day recorded
        cmd = 'SELECT MIN(day) AS min, MAX(day) AS max \
               FROM world_grid_2_degree_day_sif_facts'
        self.start_date, self.end_date = query_db(cmd)

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

        # Obtain results
        result = query_db(cmd)

        # If empty, clear and return
        if len(result) == 0:
            return ("SIF Time-Series (Select a county...)", 
                    dict(date=[], sif=[]))

        # Map the rows to columns and take series
        mapped_result = [list(i) for i in zip(*result)]
        county_name, dates, sifs = (result[0][0], mapped_result[1], 
                                    mapped_result[2])

        # Return new title and time series
        return ("SIF Time-Series in County: %s" % (county_name), 
                dict(date=dates, sif=sifs))
        pass
    
    def get_map_details(self):
        """Return initial properties of the map (xs, ys, names)."""
        return self.cell_xs, self.cell_ys, self.cell_names

    def get_date_range(self):
        """Return the valid date range of this layer."""
        return (self.start_date, self.end_date)