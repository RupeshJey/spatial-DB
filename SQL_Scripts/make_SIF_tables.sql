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

