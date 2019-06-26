# Rupesh Jeyaram 
# Created June 18th, 2019

# Load all the TROPOMI SIF data from the .nc files in SOURCE
# and import it into the specified local database 

import os                       # For searching through files + executing cmd's
import netCDF4 as nc            # For parsing data format
import psycopg2 as dbapi        # For connecting to database
import psycopg2.extras          # For using the execute_values function 
from datetime import datetime   # For converting unix time to SQL datetime
import time                     # For timing the insertion
import numpy as np              # For accessing the data more efficiently
import sys                      # For printing status

# For getting the connection details (stored abstractly)
from connection_info import conn

SOURCE = conn['data_source']    # Where to find the data
NUM_TO_INSERT = -1              # Number of records to insert. All = -1

# Connect to database
connection = dbapi.connect(port= conn['port'], 
                     user= conn['user'],
                     password= conn['password'], 
                     database= conn['database'])

# Cursor to execute queries and read output
cursor = connection.cursor()

# Clear database first (temporary line)
os.system("PGPASSWORD=%s psql -U %s -d %s -f \
           ../SQL_Scripts/make_SIF_tables.sql " % 
           (conn['password'], conn['user'], conn['database']))

# Which number file we are working on
file_num = 1

# Loop over each data file in the directory 
for file in reversed(sorted(os.listdir(SOURCE))):
    if file.endswith('.nc'):

        # Starting time for inserting file
        t0 = time.time()

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
        lat_bnds = np.array(nc_file.variables['lat_bnds'])
        lon_bnds = np.array(nc_file.variables['lon_bnds'])

        # Total number of rows
        num_rows = len(datetimes)

        # Percentage completed variable
        progress = 0

        # Notify user which file we are reading now
        print("Reading file %i/%i (%s)" % 
            (file_num, len(os.listdir(SOURCE)), file))

        # Take all the arguments and put them together in here
        args = []

        # Insert rows one-by-one
        for i in range(num_rows):

            # Convert from utc to datetime
            date = datetime.utcfromtimestamp(datetimes[i]).strftime\
                ('%Y-%m-%d %H:%M:%S')

            # This quickly interweaves the bounds to match the Postgis 
            # Polygon definition
            bnds = np.empty(10)
            bnds[0:9:2] = lon_bnds[:,i].take(np.arange(0, 5), mode = 'wrap')
            bnds[1:10:2] = lat_bnds[:,i].take(np.arange(0, 5), mode = 'wrap')

            # Compile the args
            args.append((date, float(sifs[i]), float(sif_errs[i]), 
                         float(sif_rels[i]), float(dcSIFs[i]), 
                         float(cloud_fractions[i]), float(szas[i]), 
                         float(vzas[i]), float(phase_angles[i]), 
                         float(dcfs[i]), 
                         'Point(%f %f)' % (float(lons[i]), float(lats[i])),
                         'Polygon((%f %f, %f %f, %f %f, %f %f, %f %f))' % 
                            tuple(bnds.tolist())))

            # Update user about file-reading progress
            sys.stdout.write('\r')
            curr_progress = int(float(i) / float(num_rows)  * 100)

            if (curr_progress != progress):
                progress = curr_progress
                sys.stdout.write("[%-50s] %d%%" % 
                    ('='*int(progress/2), progress))
                sys.stdout.flush()
    
        # Increment file number that we are working on
        file_num += 1
        
        # Notify the user that we are inserting the data now
        sys.stdout.write(' ' * 60)
        sys.stdout.write('\r')
        print("Inserting...")

        # Execute the command using the execute_values command
        # This runs a lot faster than running one execution at a time
        dbapi.extras.execute_values(cursor, "INSERT INTO tropomi_sif VALUES %s", 
            args)

        # Notify the user of how long it took to insert the data
        print("Inserting the file took %i seconds" % (time.time() - t0))

    if file_num > 5:
        break

# Commit all changes to the database
connection.commit()
