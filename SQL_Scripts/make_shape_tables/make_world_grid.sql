-- Rupesh Jeyaram 
-- Created July 24th, 2019

-- DROP TABLE statements

DROP TABLE IF EXISTS world_grid_005_degree;

-- CREATE TABLE statements

-- world_grid_1_degree holds all squares of a 1 degree x 1 degree grid
-- of a world map (as box types)

CREATE TABLE world_grid_005_degree (

    -- The index of the box on a cartesian grid
    -- lon: (-180, 179, 1)
    -- lat: (-90, 89, 1)
    name            VARCHAR(10)     NOT NULL,
    lon             NUMERIC(6,3)    NOT NULL,
    lat             NUMERIC(6,3)    NOT NULL,
    
    -- Shape itself
    shape           GEOMETRY        NOT NULL,       
    
    -- The lon/lat pair is enough to uniquely identify the cell
    PRIMARY KEY (lon, lat)
);

-- Populate the world grid

-- Extract the lon/lat ranges we want (min to max)
WITH lon_range AS (
    SELECT lon
    FROM generate_series (-180, 179.95, 0.05) lon
),

lat_range AS (
    SELECT lat
    FROM generate_series (-90, 89.95, 0.05) lat
)

-- Insert each combo into the world grid
INSERT INTO world_grid_005_degree
SELECT (SELECT 'test'), lon, lat,
       ST_MakeBox2D(ST_Point(lon, lat), ST_Point(lon+0.05, lat+0.05))
FROM lat_range CROSS JOIN lon_range
-- But only include ones that have at least one tropomi point
WHERE 
    NOT EXISTS(SELECT * 
           FROM tropomi_sif 
           WHERE ST_MakeBox2D(ST_Point(lon, lat), ST_Point(lon+0.05, lat+0.05)) 
                    && center_pt); 

-- Just mess up one pixel, so that the python side does not crush the array
UPDATE world_grid_005_degree
SET shape = ST_MakePolygon(
    ST_GeomFromText('LINESTRING(75.15 29.53,77 29,77.6 29.5, 75.15 29.53)'))
WHERE lon = -136.650 AND lat = -80.050;

SELECT * FROM world_grid_005_degree 
                          WHERE lon BETWEEN 1 AND 2
                          AND lat BETWEEN 1 AND 2
                          UNION 
                          SELECT * FROM world_grid_005_degree
                          WHERE lon = -136.650 AND lat = -80.050
                          ORDER BY lon, lat

SELECT ROUND(AVG(sif_avg), 3) 
                   FROM world_grid_005_degree_day_sif_facts
                   WHERE day BETWEEN '2019-02-03' AND '2019-02-13 '
                   AND lon BETWEEN -99.9 AND -99.5 
                          AND lat BETWEEN 41.9 AND 42.8
                   GROUP BY lon, lat 
                   ORDER BY lon, lat