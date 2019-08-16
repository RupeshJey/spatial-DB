-- Rupesh Jeyaram 
-- Created July 24th, 2019

-- DROP TABLE statements

DROP TABLE IF EXISTS world_grid_2_degree_day_sif_facts;

-- CREATE TABLE statements

-- world_grid_1_degree_day_sif_facts holds a world grid's cell-wise 
-- daily averages of SIF. Each record is a "fact", an aggregate stored 
-- measurement. 

CREATE TABLE world_grid_2_degree_day_sif_facts (

    -- Lon/lat of the grid cell that this fact is associated with 
    lon         NUMERIC(5,2)         NOT NULL,
    lat         NUMERIC(5,2)         NOT NULL,

    -- The day that this fact is associated with
    day         DATE            NOT NULL, 

    -- The average SIF value for this cell-day combination
    -- This value *can* be NULL, when there are no measurements for 
    -- a cell-day combo
    sif_avg     NUMERIC(5, 3),

    -- A fact is uniquely identified by a cell-day combination
    -- There should not be any duplicates of these values
    PRIMARY KEY (lon, lat, day)
);

-- CREATE INDEX statements 

-- Index on the date of fact
CREATE INDEX world_grid_2_degree_day_sif_facts_day_idx
  ON world_grid_2_degree_day_sif_facts(day);

-- POPULATE TABLE statements

-- Extract just the cells
WITH cells AS (
    SELECT * FROM world_grid_2_degree 
),
-- Extract the day range we want (min to max)
day_range AS (
    SELECT date_trunc('day', dd):: date AS day
    FROM generate_series ( (SELECT MIN(time) FROM tropomi_SIF) 
                            , (SELECT MAX(time) FROM tropomi_SIF)
                            , '1 day'::interval) dd
)
-- Direct output into facts table
INSERT INTO world_grid_2_degree_day_sif_facts
-- Select out lon/lat and day (to match the facts table)
SELECT lon, lat, day, 
-- Obtain the average sif value for this 
(
    SELECT AVG(sif) 
    FROM tropomi_SIF
    WHERE shape && center_pt AND                           -- Match grid shape
    	  ST_CONTAINS(shape, center_pt) AND
          time BETWEEN day AND (day + INTERVAL '1 day')    -- Match day

) AS avg_sif
-- Cross cells and days, so we have each possible combination (allows nulls)
FROM cells CROSS JOIN day_range;
