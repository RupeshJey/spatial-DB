# Rupesh Jeyaram 
# Created June 19th, 2019

# Load all the US shape data from the GeoJSON files in SOURCE
# Currently there are three general types: 
# 
#   - Country level (only US)
#   - State level 
#   - County level 
# 

import os                       # For searching through files + executing cmd's
import json                     # For parsing shapes
import psycopg2 as dbapi        # For connecting to database
import time                     # For timing the insertion
import sys                      # For printing status

SOURCE = '../Shape_Outlines/'   # Where to find the data

# Specific files to use
COUNTRY_FILE = 'gz_2010_us_outline.json'
STATES_FILE = 'gz_2010_us_states.json'
COUNTY_FILE = 'gz_2010_us_counties.json'

# In case this changes... 
NUM_STATES = 50

# Connect to database
conn = dbapi.connect(host= '127.0.0.1', 
                     port= 5432, 
                     user= 'postgres',
                     password= 'frankenberg', 
                     database= 'SIF_Experiments')

# Cursor to execute queries and read output
cursor = conn.cursor()

# Clear database first (temporary line)
os.system("PGPASSWORD=frankenberg psql -U postgres -d SIF_Experiments -f \
           ../SQL_Scripts/make_shape_tables.sql ")

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

# Commit all changes to the database
conn.commit()

# Clear the output
sys.stdout.write(" " * 50)
sys.stdout.flush()
sys.stdout.write("\r")

# Notify user of completion
print("Done inserting states!")