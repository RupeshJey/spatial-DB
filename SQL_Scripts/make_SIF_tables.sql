-- Rupesh Jeyaram 
-- Created June 18th, 2019

-- DROP TABLE statements

DROP TABLE IF EXISTS tropomi_SIF;

-- CREATE TABLE statements

-- tropomi_SIF holds all the data from the SIF records

CREATE TABLE tropomi_SIF (

    -- Unique record id
    record_id       SERIAL              NOT NULL,

    -- Time at which data was obtained
    time            TIMESTAMP           NOT NULL, 

    -- Parameters of the data point
    sif             NUMERIC(5, 3)       NOT NULL,
    sif_err         NUMERIC(4, 3)       NOT NULL,
    sif_relative    NUMERIC(5, 2)       NOT NULL,
    dcSIF           NUMERIC(5, 3)       NOT NULL,
    cloud_fraction  NUMERIC(3, 2)       NOT NULL,
    sza             NUMERIC(3, 1)       NOT NULL,
    vza             NUMERIC(3, 1)       NOT NULL,
    phase_angle     NUMERIC(4, 1)       NOT NULL,
    dcf             NUMERIC(5, 4)       NOT NULL,

    -- Geometric properties of the data record
    center_pt       GEOMETRY            NOT NULL,  -- Data's center point
    mbr             GEOMETRY            NOT NULL,  -- Data's bounding rectangle

    -- Uniquely identifies a data record
    PRIMARY KEY (record_id)
);

-- CREATE INDEX statements 

-- Note: creating the index here instead of at the end slows down 
-- insertion, BUT it allows us to monitor the index's progress. If 
-- called at the end, the CREATE INDEX statements run w/o progress
-- updates, and we do not know how long the statements will take. 
-- Tradeoffs! 

-- Index on the center points of the data
CREATE INDEX center_points_index
  ON tropomi_sif
  USING GIST (center_pt);

-- Index on the timestamp of the data
CREATE INDEX time_idx
  ON tropomi_sif (time);

