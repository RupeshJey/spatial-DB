# Rupesh Jeyaram 
# Created June 18th, 2019

# Load all the TROPOMI SIF data from the .nc files in SOURCE
# and import it into the specified local database 

import os                       # For searching through files
import netCDF4 as nc            # For parsing data format
import psycopg2 as dbapi        # For connecting to database
from datetime import datetime   # For converting unix time to SQL datetime
import time                     # For timing the insertion
import numpy as np              # For accessing the data more efficiently

import os                       # For executing terminal commands

SOURCE = '../TROPO_SIF_data/'   # Where to find the data
NUM_TO_INSERT = -1              # Number of records to insert. All = -1

# Connect to database
conn = dbapi.connect(host= '127.0.0.1', 
                     port= 5432, 
                     user= 'postgres',
                     password= 'frankenberg', 
                     database= 'SIF_Experiments')

# Cursor to execute queries and read output
cursor = conn.cursor()

# Clear database first (temporary file)
os.system("PGPASSWORD=frankenberg psql -U postgres -d SIF_Experiments -f \
            ../SQL_Scripts/make_SIF_tables.sql ")

# Loop over each data file in the directory 
for file in sorted(os.listdir(SOURCE)):
    if file.endswith('.nc'):

        # Parse it
        nc_file = nc.Dataset(SOURCE + file, 'r')
        keys = nc_file.variables.keys()

        # Extract the data as np arrays
        datetimes = np.array(nc_file.variables['TIME'])
        sifs = np.array(nc_file.variables['sif'])
        sif_errs = np.array(nc_file.variables['sif_err'])
        sif_rels = np.array(nc_file.variables['sif_relative'])
        dcSIFs = np.array(nc_file.variables['dcSIF'])
        cloud_fractions = np.array(nc_file.variables['cloud_fraction'])
        szas = np.array(nc_file.variables['sza'])
        vzas = np.array(nc_file.variables['vza'])
        phase_angles = np.array(nc_file.variables['phase_angle'])
        dcfs = np.array(nc_file.variables['daily_correction_factor'])
        lats = np.array(nc_file.variables['lat'])
        lons = np.array(nc_file.variables['lon'])

        # Total number of rows
        num_rows = len(datetimes)

        # Insert rows one-by-one
        for i in range(num_rows):

            # Convert from utc to datetime
            date = datetime.utcfromtimestamp(datetimes[i]).strftime\
                ('%Y-%m-%d %H:%M:%S')

            # Create SQL statement
            cmd = 'INSERT INTO tropomi_sif VALUES (DEFAULT, \' %s \', \
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);' % \
                   (date, sifs[i], 
                    sif_errs[i], sif_rels[i], dcSIFs[i], cloud_fractions[i],
                    szas[i], vzas[i], phase_angles[i], dcfs[i], 
                    lats[i], lons[i])

            # Update user about insertion
            if (i % 100000 == 0):
                print("inserting record # %s" % str(i))

            # Execute the command
            cursor.execute(cmd)
    break

# Commit all changes to the database
conn.commit()
