-- Rupesh Jeyaram 
-- Created August 13th, 2019

-- DROP FUNCTION statements
DROP FUNCTION IF EXISTS hill_shade;

-- CREATE FUNCTION statements

-- Hillshade is given by: 
-- 255.0 * ((cos(Zenith_rad) * cos(Slope_rad)) + 
--           (sin(Zenith_rad) * sin(Slope_rad) * cos(Azimuth_rad - Aspect_rad)))

-- For convenience, this function TAKES PARAMETERS IN DEGREES!

CREATE FUNCTION hill_shade
(
    zenith  NUMERIC(10, 5), 
    slope   NUMERIC(10, 5), 
    azimuth NUMERIC(10, 5),
    aspect  NUMERIC(10, 5)
)
RETURNS DOUBLE PRECISION
AS $$ SELECT 255.0 * ((cos(radians(zenith)) * cos(radians(slope))) + 
           (sin(radians(zenith)) * sin(radians(slope)) * 
            cos(radians(azimuth) - radians(aspect)))); $$
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT;