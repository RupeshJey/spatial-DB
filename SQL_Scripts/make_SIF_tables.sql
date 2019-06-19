-- Rupesh Jeyaram 
-- Created June 18th, 2019

-- DROP TABLE statements

DROP TABLE IF EXISTS tropomi_SIF;

-- CREATE TABLE statements

-- tropomi_SIF holds all the data from the SIF records

CREATE TABLE tropomi_SIF (

    -- Auto-incrementing data point id
    tropomi_id      SERIAL, 

    -- Time at which data was obtained
    time            TIMESTAMP            NOT NULL, 

    -- Parameters of the data point. All assumed to be NUMERIC(10, 7) for now..
    sif             NUMERIC(10, 7)       NOT NULL,
    sif_err         NUMERIC(10, 7)       NOT NULL,
    sif_relative    NUMERIC(10, 7)       NOT NULL,
    dcSIF           NUMERIC(10, 7)       NOT NULL,
    cloud_fraction  NUMERIC(10, 7)       NOT NULL,
    sza             NUMERIC(10, 7)       NOT NULL,
    vza             NUMERIC(10, 7)       NOT NULL,
    phase_angle     NUMERIC(10, 7)       NOT NULL,
    dcf             NUMERIC(10, 7)       NOT NULL,
    lat             NUMERIC(10, 7)       NOT NULL,
    lon             NUMERIC(10, 7)       NOT NULL,
    
    -- The id is enough to uniquely identify the data point
    PRIMARY KEY (tropomi_id)
    
);

