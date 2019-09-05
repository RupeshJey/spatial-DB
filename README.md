
# Spatial_DB

Spatial_DB is the work of a Caltech SURF project in Frankenberg lab. The goals of this project are to build a database that can: 

- Store TROPOMI data 
- Extract spatially and temporally filtered datasets
- Merge different datasets
- Enable scientific inquiries that were previously constrained by suboptimal data storage formats

The project’s results have unequivocally demonstrated the advantages of using such a database for querying spatial data. Common queries, such as obtaining custom-averaged time series of data points inside a geographic shape, have become faster by several orders of magnitude; queries that used to take hours now take less than 1 second.

Alongside the database, the development of a front-end TROPOMI exploration tool has allowed researchers to quickly explore data trends across the world without having to write scripts to extract select data beforehand.

The development of a Python utility package has also enabled researchers to interact with the database and pull data directly into their code, enabling flexible use of query results.

## Setup

You can already access the database directly on the GPS Tofu server. It is set up, and you are free to access it using psql, the standard interactive terminal for working with Postgres. Check with an administrator for port and username details. 

If you'd like to pipe data into or out of the database, you should take a look at the scripts in this repository. To set up the files, 

1. Clone the project into your working directory **on the GPS Tofu server**.
2. Create a virtual environment for this project and activate the environment. 
3. Install the following packages in your environment: 
	- psycopg2
	- bokeh
	- pyproj
	- geopandas
	- scipy

Now, you should be able to use the Python scripts to load data into the database. You can also move db_utils.py and connection_info.py into your codebase and use the supplied functions to directly query the database and obtain results in your Python code (see docstrings for more info). 

