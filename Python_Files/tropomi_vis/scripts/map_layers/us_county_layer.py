# Rupesh Jeyaram 
# Created July 23rd, 2019

# This class contains all the respective functions for the US County 
# layer

from shape_layer import ShapeLayer
from db_utils import *  # For easier querying
import shapely          # For checking shape type (Polygon/Multipolygon)
import numpy as np      # Math array things

# Custom saving
from bokeh.models.callbacks import CustomJS

class US_County_Layer(ShapeLayer):

    def __init__(self):
        
        self.name = 'County'
        self.none_selected_str = "SIF Time-Series (Select a county...)"
        self.multiple_selected_str = "SIF Time-Series in Multiple Counties"

        # Command to retrieve all the county shapes
        cmd_shapes = 'SELECT * FROM shapes WHERE type = \'County\' \
                      ORDER BY shape_id'

        # Query to obtain first and last day recorded
        cmd_day_range = 'SELECT MIN(day) AS min, MAX(day) AS max \
                         FROM county_day_sif_facts'

        # Initialize the class using these commands
        super().__init__(cmd_shapes, cmd_day_range)

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
                ORDER BY day;" \
                % (coord_x, coord_y, coord_x, coord_y)

        return super().get_patch_time_series(cmd)

    def save_data(self):
        """Save selected data in NetCDF format"""
        # Command to get the download data
        pass
        

    # def get_save_data_js_callback(self):

    #     cmd =   "SELECT name, state, day, sif_avg\
    #              FROM county_day_sif_facts NATURAL JOIN shapes\
    #              WHERE sif_avg IS NOT NULL\
    #              ORDER BY day, state, name LIMIT 1;" 

    #     # Get data
    #     df = pandas_query_db(cmd)

    #     value = df.to_csv(header=False).replace("\n", "").split(",")
    #     print(value)


    #     callback = CustomJS(args = dict(rows = [["name1", "city1", "some other info"],["name2", "city2", "more info"]]), code="""

    #         let csvContent = "data:text/csv;charset=utf-8,";

    #         @rows.forEach(function(rowArray) {
    #             let row = rowArray.join(",");
    #             csvContent += row + "\r\n";
    #         });

    #         var encodedUri = encodeURI(csvContent);
    #         var link = document.createElement("a");
    #         link.setAttribute("href", encodedUri);
    #         link.setAttribute("download", "my_data.csv");
    #         document.body.appendChild(link); // Required for FF

    #         link.click(); // This will download the data file named "my_data.csv".

    #         """)

    #     return callback
        # const rows = [
        #         ["name1", "city1", "some other info"],
        #         ["name2", "city2", "more info"]
        #     ];

        #     var lineArray = [];
        #     rows.forEach(function (infoArray, index) {
        #         var line = infoArray.join(",");
        #         lineArray.push(index == 0 ? "data:text/csv;charset=utf-8," + line : line);
        #     });
        #     var csvContent = lineArray.join("\\n");

