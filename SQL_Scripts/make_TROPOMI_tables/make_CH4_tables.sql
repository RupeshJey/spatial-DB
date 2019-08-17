-- Rupesh Jeyaram 
-- Created June 18th, 2019
-- Modified by yiyin Aug 7th, 2019

-- DROP TABLE statements

DROP TABLE IF EXISTS tropomi_CH4_files_loaded; 
DROP TABLE IF EXISTS tropomi_CH4;

-- CREATE TABLE statements

-- tropomi_CH4_files_loaded contains the names of all files that 
-- have been imported already

CREATE TABLE tropomi_CH4_files_loaded (
    -- File's name as length 100 varchar; must be unique
    filename        VARCHAR(100)        PRIMARY KEY
);

-- tropomi_CH4 holds all the data from the CH4 records

CREATE TABLE tropomi_CH4 (

    -- Unique record id
    record_id       SERIAL              NOT NULL,

    -- Time at which data was obtained
    time            TIMESTAMP           NOT NULL, 

    -- Parameters of the data point
    ch4             NUMERIC(6, 2)       NOT NULL,
    ch4_err         NUMERIC(5, 2)       NOT NULL,
    ch4_raw         NUMERIC(6, 2)       NOT NULL,
    quality_flag    NUMERIC(3, 1)       NOT NULL,
    sza             NUMERIC(3, 1)       NOT NULL,
    vza             NUMERIC(3, 1)       NOT NULL,
    surf_p          NUMERIC(8, 2)       NOT NULL,
    -- Input data for model calculation
    x_prior         NUMERIC(6,2)        ARRAY[12],
    ak              NUMERIC(4,2)        ARRAY[12],
    -- Geometric properties of the data record
    center_pt       GEOMETRY            NOT NULL,  -- Data's center point
    mbr             GEOMETRY            NOT NULL,  -- Data's bounding rectangle
    -- Uniquely identifies a data record
    PRIMARY KEY (record_id, time)
) PARTITION BY RANGE(time); -- Want to partition this table by time

-- CREATE PARTITIONS of tropomi_CH4

-- 2017
CREATE TABLE tropomi_CH4_y2017_m11 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2017-11-01') TO ('2017-12-01');
CREATE TABLE tropomi_CH4_y2017_m12 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2017-12-01') TO ('2018-01-01');

-- 2018
CREATE TABLE tropomi_CH4_y2018_m01 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-01-01') TO ('2018-02-01');
CREATE TABLE tropomi_CH4_y2018_m02 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-02-01') TO ('2018-03-01');
CREATE TABLE tropomi_CH4_y2018_m03 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-03-01') TO ('2018-04-01');
CREATE TABLE tropomi_CH4_y2018_m04 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-04-01') TO ('2018-05-01');
CREATE TABLE tropomi_CH4_y2018_m05 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-05-01') TO ('2018-06-01');
CREATE TABLE tropomi_CH4_y2018_m06 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-06-01') TO ('2018-07-01');
CREATE TABLE tropomi_CH4_y2018_m07 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-07-01') TO ('2018-08-01');
CREATE TABLE tropomi_CH4_y2018_m08 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-08-01') TO ('2018-09-01');
CREATE TABLE tropomi_CH4_y2018_m09 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-09-01') TO ('2018-10-01');
CREATE TABLE tropomi_CH4_y2018_m10 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-10-01') TO ('2018-11-01');
CREATE TABLE tropomi_CH4_y2018_m11 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-11-01') TO ('2018-12-01');
CREATE TABLE tropomi_CH4_y2018_m12 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2018-12-01') TO ('2019-01-01');

-- 2019
CREATE TABLE tropomi_CH4_y2019_m01 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-01-01') TO ('2019-02-01');
CREATE TABLE tropomi_CH4_y2019_m02 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-02-01') TO ('2019-03-01');
CREATE TABLE tropomi_CH4_y2019_m03 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-03-01') TO ('2019-04-01');
CREATE TABLE tropomi_CH4_y2019_m04 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-04-01') TO ('2019-05-01');
CREATE TABLE tropomi_CH4_y2019_m05 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-05-01') TO ('2019-06-01');
CREATE TABLE tropomi_CH4_y2019_m06 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-06-01') TO ('2019-07-01');
CREATE TABLE tropomi_CH4_y2019_m07 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-07-01') TO ('2019-08-01');
CREATE TABLE tropomi_CH4_y2019_m08 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-08-01') TO ('2019-09-01');
CREATE TABLE tropomi_CH4_y2019_m09 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-09-01') TO ('2019-10-01');
CREATE TABLE tropomi_CH4_y2019_m10 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-10-01') TO ('2019-11-01');
CREATE TABLE tropomi_CH4_y2019_m11 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-11-01') TO ('2019-12-01');
CREATE TABLE tropomi_CH4_y2019_m12 PARTITION OF tropomi_CH4
    FOR VALUES FROM ('2019-12-01') TO ('2020-01-01');

-- CREATE INDEX statements 

-- Note: creating the index here instead of at the end slows down 
-- insertion, BUT it allows us to monitor the index's progress. If 
-- called at the end, the CREATE INDEX statements run w/o progress
-- updates, and we do not know how long the statements will take. 
-- Tradeoffs! 

-- Index on the center points of the data
CREATE INDEX tropomi_ch4_center_points_idx
  ON tropomi_CH4
  USING GIST (center_pt);

-- Index on the timestamp of the data
CREATE INDEX tropomi_ch4_time_idx
  ON tropomi_CH4 (time);
