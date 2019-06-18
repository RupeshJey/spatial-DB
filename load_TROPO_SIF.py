# Rupesh Jeyaram 
# Created June 18th, 2019

# Load all the TROPOMI SIF data from the .nc files in SOURCE
# and import it into the specified local database 

SOURCE = '../TROPOMI_Data/'

import os                       # For searching through files
import netCDF4 as nc            # For parsing data format
import psycopg2 as dbapi        # For connecting to database
from datetime import datetime   # For converting unix time to SQL datetime
import time                     # For timing the insertion
import numpy as np              # For accessing the data more efficiently

