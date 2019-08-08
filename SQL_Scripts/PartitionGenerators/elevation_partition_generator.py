# Rupesh Jeyaram 
# Created August 7th, 2019

# Give me all the partition names for the elevation points table
# Simply, split on the raster id, 1 to 775

NUM_RASTERS = 775

for i in range(NUM_RASTERS):
    cmd = \
    """CREATE TABLE elevation_points_%i PARTITION OF elevation_points 
    FOR VALUES IN (%i);""" % (i+1, i+1)
    print(cmd)