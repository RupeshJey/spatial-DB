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

SOURCE = conn['data_source_co']    # Where to find the data
NUM_TO_INSERT = -1              # Number of records to insert. All = -1
QA_LIMIT = 0.5 # set QA threshhold 

# Connect to database
connection = dbapi.connect(port= conn['port'], 
                     user= conn['user'],
                     password= conn['password'], 
                     database= conn['database'])
f_record = open('broken_files.txt','w')

# Cursor to execute queries and read output
cursor = connection.cursor()

# Clear database first (temporary line)
os.system("PGPASSWORD=%s psql -U %s -p %s -d %s -f \
           ../SQL_Scripts/make_CO_tables.sql " % 
           (conn['password'], conn['user'], conn['port'], conn['database']))

# Which number file we are working on
file_num = 1

# Option to split scripts, to insert only subset of records
START_NUM = 0
END_NUM = 10

# Loop over each data file in the directory 
for file in reversed(sorted(os.listdir(SOURCE))):
    if file.endswith('.zip'): #they are actual nc files 
        if file_num > START_NUM and file_num <= END_NUM:
            # Starting time for inserting file
            t0 = time.time()
            
            # Parse it
            try:
              nc_file = nc.Dataset(SOURCE + file, 'r')
            except OSError as err:
              print ('Broken file: '+file)
              f_record.write(file+'\n')
              continue
            #keys = nc_file.variables.keys()

            # Extract the data as np arrays
            co_column = np.array( nc_file.groups['PRODUCT']['carbonmonoxide_total_column'][0,:,:]) # mol m-2
            co_precision = np.array( nc_file.groups['PRODUCT']['carbonmonoxide_total_column_precision'][0,:,:])  
            meas_time = nc_file.groups['PRODUCT']['time_utc'][0,:]
            latitude = np.array( nc_file.groups['PRODUCT']['latitude'][0,:,:])
            longitude = np.array( nc_file.groups['PRODUCT']['longitude'][0,:,:])
            latitude_bnds = nc_file.groups['PRODUCT']['SUPPORT_DATA']['GEOLOCATIONS']['latitude_bounds'][0,:,:,:]
            longitude_bnds = nc_file.groups['PRODUCT']['SUPPORT_DATA']['GEOLOCATIONS']['longitude_bounds'][0,:,:,:]
            sza = nc_file.groups['PRODUCT']['SUPPORT_DATA']['GEOLOCATIONS']['solar_zenith_angle'][0,:,:]
            vza = nc_file.groups['PRODUCT']['SUPPORT_DATA']['GEOLOCATIONS']['viewing_zenith_angle'][0,:,:]
 
            # supporting data in the order of prior, ak, delta_p 
            #x_pri = nc_file.groups['PRODUCT']['SUPPORT_DATA']['INPUT_DATA']['methane_profile_apriori'][0,:,:,:] # unit mol m-2
            #dry_air = nc_file.groups['PRODUCT']['SUPPORT_DATA']['INPUT_DATA']['dry_air_subcolumns'][0,:,:,:]
            #ak = nc_file.groups['PRODUCT']['SUPPORT_DATA']['DETAILED_RESULTS']['column_averaging_kernel'][0,:,:,:]
            surface_pressure = nc_file.groups['PRODUCT']['SUPPORT_DATA']['INPUT_DATA']['surface_pressure'][0,:,:]
            #pressure_interval = nc_file.groups['PRODUCT']['SUPPORT_DATA']['INPUT_DATA']['pressure_interval'][0,:,:]
            
            # select data with aq value > 0.8  
            qa = np.array( nc_file.groups['PRODUCT']['qa_value'][0,:,:])
            index = np.array( np.where( qa> QA_LIMIT)).T
            
            datetimes = meas_time[index[:,0]]
            co = co_column[index[:,0], index[:,1]]*1.e4 #for saving purpose
            #ch4_raw = ch4_before_bias[index[:,0], index[:,1]]
            co_errs = co_precision[index[:,0], index[:,1]]*1.e4
            quality_flag = qa[index[:,0], index[:,1]]
            szas = sza[ index[:,0], index[:,1]] 
            vzas = vza[ index[:,0], index[:,1]]
            lats = latitude[index[:,0], index[:,1]] 
            lons = longitude[index[:,0], index[:,1]]
            lat_bnds = latitude_bnds[index[:,0], index[:,1], :]
            lon_bnds = longitude_bnds[index[:,0], index[:,1], :]
            surf_p = surface_pressure[index[:,0], index[:,1]]
            #xa = x_pri[index[:,0], index[:,1], :]/dry_air[index[:,0], index[:,1], :]*1.e9
            #aks = ak[index[:,0], index[:,1], :]
            
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
                #date = datetime.utcfromtimestamp(datetimes[i]).strftime\
                #    ('%Y-%m-%d %H:%M:%S')
                date = datetimes[i]
                # This quickly interweaves the bounds to match the Postgis 
                # Polygon definition
                bnds = np.empty(10)
                bnds[0:9:2] = lon_bnds[i,:].take(
                                                np.arange(0, 5), mode = 'wrap')
                bnds[1:10:2] = lat_bnds[i,:].take(
                                                np.arange(0, 5), mode = 'wrap')

                # Compile the args
                
                args.append((date, float(co[i]), float(co_errs[i]), 
                             float(quality_flag[i]), 
                             float(szas[i]), float(vzas[i]), 
                             float(surf_p[i]), 
                            # '{ %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f }' % tuple(xa[i,:]),
                            # '{%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f }' % tuple(aks[i,:]),
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
            
            # Notify the user that we are inserting the data now
            sys.stdout.write(' ' * 60)
            sys.stdout.write('\r')
            print("Inserting...")

            # Execute the command using the execute_values command
            # This runs a lot faster than running one execution at a time
            dbapi.extras.execute_values(cursor, "INSERT INTO tropomi_CO \
                (time, co, co_err, quality_flag, \
                sza, vza, surf_p, center_pt, mbr) VALUES %s", 
                args)

            # Notify the user of how long it took to insert the data
            print("Inserting the file took %i seconds" % (time.time() - t0))

            #if file_num % 5 == 0:
                # Commit all changes to the database
            connection.commit()

        # Increment file number that we are working on
        file_num += 1


# Commit all changes to the database
connection.commit()
f_record.close()
# Inform user that the script has finished running
print("Finished running!")

