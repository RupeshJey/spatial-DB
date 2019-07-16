-- Rupesh Jeyaram 
-- Created July 16th, 2019

-- DROP TABLE statements

DROP TABLE IF EXISTS county_day_sif_facts;

-- CREATE TABLE statements

-- county_day_sif_facts holds county-wise daily averages of SIF
-- Each record is a "fact", an aggregate stored measurement

CREATE TABLE county_day_sif_facts (

    -- The county that this fact is associated with 
    shape_id    INTEGER         NOT NULL,

    -- The day that this fact is associated with
    day         DATE            NOT NULL, 

    -- The average SIF value for this county-day combination
    -- This value *can* be NULL, when there are no measurements for 
    -- a county-day combo
    sif_avg     NUMERIC(5, 3),

    -- A fact is uniquely identified by a county-day combination
    -- There should not be any duplicates of these values
    PRIMARY KEY (shape_id, day)
);

-- CREATE INDEX statements 

-- Index on the date of fact
CREATE INDEX county_day_sif_facts_day_idx
  ON county_day_sif_facts(day);

-- POPULATE TABLE statements

-- Extract just the counties
WITH counties AS (
    SELECT * FROM shapes WHERE type = 'County'
),
-- Extract the day range we want (min to max)
day_range AS (
    SELECT date_trunc('day', dd):: date AS day
    FROM generate_series ( (SELECT MIN(time) FROM tropomi_SIF) 
                            , (SELECT MAX(time) FROM tropomi_SIF)
                            , '1 day'::interval) dd
)
-- Direct output into facts table
INSERT INTO county_day_sif_facts
-- Select out shape_id and day (to match the facts table)
SELECT shape_id, day, 
-- Obtain the average sif value for this 
(
    SELECT AVG(sif) 
    FROM tropomi_sif
    WHERE ST_X(center_pt) > -130 AND                       -- Exclude Alaska
          shape && center_pt AND                           -- Match county shape
          ST_CONTAINS(shape, center_pt) AND                -- Match shape  
          time BETWEEN day AND (day + INTERVAL '1 day')    -- Match day
) AS avg_sif
-- Cross counties and days, so we have each possible combination (allows nulls)
FROM counties CROSS JOIN day_range;

