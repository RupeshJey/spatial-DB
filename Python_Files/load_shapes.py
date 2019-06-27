# Rupesh Jeyaram 
# Created June 19th, 2019

# Load all the US shape data from the GeoJSON files in SOURCE
# Currently there are two general types: 
# 
#   - State level 
#   - County level 
# 

import os                       # For searching through files + executing cmd's
import json                     # For parsing shapes
import psycopg2 as dbapi        # For connecting to database
import time                     # For timing the insertion
import sys                      # For printing status
import csv                      # For parsing county files
import re                       # For string-parsing the JSON in csv 

# For getting the connection details (stored abstractly)
from connection_info import conn

SOURCE = '../Shape_Outlines/'   # Where to find the data

# Specific files to use
COUNTRY_FILE = 'gz_2010_us_outline.json'
STATES_FILE = 'gz_2010_us_states.json'
COUNTY_FILE = 'us_county.csv'

# In case this changes... 
NUM_STATES = 52         # This includes Puerto Rico and D.C. separately 
NUM_COUNTIES = 3141

# Connect to database
connection = dbapi.connect(port= conn['port'], 
                     user= conn['user'],
                     password= conn['password'], 
                     database= conn['database'])

# Cursor to execute queries and read output
cursor = connection.cursor()

# Set up the database itself
os.system("PGPASSWORD=%s psql -U %s -p %s -d %s -f \
           ../SQL_Scripts/make_shape_tables.sql" % 
           (conn['password'], conn['user'], conn['port'], conn['database']))

########################################################################
# INSERT STATES
########################################################################

# First insert the US states
file = SOURCE + STATES_FILE

# Which number state we are working on
state_num = 1; 

# For each state
for i in range(NUM_STATES):

    # The raw data pertaining to this state
    data = json.loads(
                str(json.load(open(file))['features'][i]).replace("\'", "\"")
            )
    # Properties are separately wrapped inside
    properties = json.loads(str(data['properties']).replace("\'", "\""))

    # Extract the important variables

    name = properties["NAME"]     # State's name
    geom = data["geometry"]       # State's geometry

    # Clear the last line
    sys.stdout.write(" " * 50)
    sys.stdout.flush()
    sys.stdout.write("\r")

    # Notify the user about progress
    sys.stdout.write(("Inserting state %i/%i: " % (state_num, NUM_STATES)) + 
                        properties["NAME"])
    sys.stdout.flush()

    # Construct SQL query to insert the shape
    cmd = 'INSERT INTO shapes VALUES (DEFAULT, \'%s\', \'%s\', \
                   ST_GeomFromGeoJSON(\'%s\'));' % \
                   (name, "State", str(geom).replace("\'", "\""))

    # Execute that query
    cursor.execute(cmd)

    # Move cursor to start of line
    sys.stdout.write('\r')

    # Increment state counter
    state_num += 1

# Clear the output
sys.stdout.write(" " * 50)
sys.stdout.flush()
sys.stdout.write("\r")

# Notify user of completion
print("Done inserting states!")

########################################################################
# INSERT COUNTIES
########################################################################

# Change file to look at counties
file = SOURCE + COUNTY_FILE

# Notify user
print("Loading counties file...")

# Which number county we are working on
county_num = 1; 

# Open the csv file
with open(file, newline='') as csvfile:

    # Create a reader for this csv file
    county_reader = csv.reader(csvfile, delimiter='\n')

    # Loop through each row in the csv file
    for row in county_reader:

        # Extract the name and geometry of the county
        name = row[0].split(',')[0].replace("'", "")
        geom = '{' + re.search('{(.*)}', row[0]).group(1) + '}'
        geom = json.loads(geom.replace('\"\"', '\"'))

        # Clear the last line
        sys.stdout.write(" " * 60)
        sys.stdout.flush()
        sys.stdout.write("\r")

        # Notify the user about progress
        sys.stdout.write(("Inserting county %i/%i: " % 
                            (county_num, NUM_COUNTIES)) + name)
        sys.stdout.flush()

        # Construct SQL query to insert the shape
        cmd = 'INSERT INTO shapes VALUES (DEFAULT, \'%s\', \'%s\', \
                       ST_GeomFromGeoJSON(\'%s\'));' % \
                       (name, "County", str(geom).replace("\'", "\""))

        # Execute that query
        cursor.execute(cmd)

        # Move cursor to start of line
        sys.stdout.write('\r')

        # Increment county counter
        county_num += 1

# Clear the output
sys.stdout.write(" " * 60)
sys.stdout.flush()
sys.stdout.write("\r")

# Commit all changes to the database

# Doing this here so that states + counties are committed together 
# If something breaks in between, it would otherwise leave the shapes
# without any counties. 

connection.commit()

# Notify user of completion
print("Done inserting counties!")
