# Rupesh Jeyaram 
# Created July 23rd, 2019

# This class contains all the respective functions for the US County 
# layer

from shapelayer import ShapeLayer
from db_utils import *  # For easier querying
import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Math array things

class US_County_Layer(ShapeLayer):

    def __init__(self):
        self.name = 'US Counties'

        # Command to retrieve all the county shapes
        cmd = 'SELECT * FROM shapes WHERE type = \'County\' \
               ORDER BY shape_id'

        # Execute query and obtain results
        self.counties = spatial_query_db(cmd)

        # Extract names
        self.county_names = self.counties["name"].values

        # Obtain the county shapes in bokeh polygon form
        self.county_xs, self.county_ys = multify(self.counties["shape"].values)

        # Convert to mercator projection
        self.county_xs, self.county_ys = \
                    convert_shapes_to_mercator(self.county_ys, self.county_xs)

        # Query to obtain first and last day recorded
        cmd = 'SELECT MIN(day) AS min, MAX(day) AS max \
               FROM county_day_sif_facts'
        self.start_date, self.end_date = query_db(cmd)

    # Given a date range, this function returns the average sif for the counties
    # in the specified range
    def get_data_for_date_range(self, start_date, end_date):

        # Command to retrieve the day's county-wise averages
        cmd = 'SELECT ROUND(AVG(sif_avg), 3) \
               FROM county_day_sif_facts\
               WHERE day BETWEEN \'%s\' AND \'%s\' \
               GROUP BY shape_id \
               ORDER BY shape_id' % (start_date, end_date)

        return np.array(query_db(cmd))

    # callback that will plot the time series of a selected county
    def get_patch_time_series(self, event):

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
                        ROUND(sif_avg, 3) FROM county_day_sif_facts \
                WHERE shape_id = (SELECT shape_id FROM county)\
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
    
    def get_map_details(self):
        """Return initial properties of the map (xs, ys, names)."""
        return self.county_xs, self.county_ys, self.county_names

    def get_date_range(self):
        """Return the valid date range of this layer."""
        return (self.start_date, self.end_date)
