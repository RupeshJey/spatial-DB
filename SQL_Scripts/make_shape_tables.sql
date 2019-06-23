-- Rupesh Jeyaram 
-- Created June 19th, 2019

-- DROP TABLE statements

DROP TABLE IF EXISTS shapes;

-- CREATE TABLE statements

-- shapes holds all outline data from the GeoJSON files

CREATE TABLE shapes (

    -- Auto-incrementing shape id
    shape_id        SERIAL, 

    -- Name of shape
    name            VARCHAR(100)          NOT NULL,

    -- Type of shape (country / state / county)
    type            VARCHAR(10)          NOT NULL

    -- Make sure that the type is legitimate (country or state or county)
                    CHECK (type = 'Country' OR 
                           type = 'State' OR 
                           type = 'County'),

    -- Shape itself
    shape           GEOMETRY             NOT NULL,       
    
    -- The id is enough to uniquely identify the data point
    PRIMARY KEY (shape_id)
    
);
