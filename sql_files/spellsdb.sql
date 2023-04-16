-- CREATE DATABASE ttrpg;

USE ttrpg;

-- CREATE TABLE spells(
-- 	spell_name VARCHAR(50) NOT NULL PRIMARY KEY,
--     school VARCHAR(50) NOT NULL,
--     casting_int INT NOT NULL,
--     casting_unit VARCHAR(50),
--     dur_int INT NOT NULL,
--     dur_unit VARCHAR(50)
-- );

-- CREATE TABLE times(
-- 	unit_name VARCHAR(50) NOT NULL PRIMARY KEY,
--     unit_secs FLOAT NOT NULL
-- );

-- INSERT INTO times
-- VALUES
-- ("day", 86400),
-- ("hour", 3600),
-- ("minute", 60),
-- ("round", 6),
-- ("action", 3),
-- ("bonus action", 2),
-- ("reaction", 1),
-- ("instantaneous", 0.1);

-- ALTER TABLE spells
-- MODIFY COLUMN casting_int INT NULL,
-- MODIFY COLUMN dur_int INT NULL;

-- ALTER TABLE spells
-- ADD CONSTRAINT 
-- fk_cast_unit
-- FOREIGN KEY (casting_unit)
-- REFERENCES times(unit_name)
-- ON UPDATE CASCADE,

-- ADD CONSTRAINT 
-- fk_dur_unit
-- FOREIGN KEY (dur_unit)
-- REFERENCES times(unit_name)
-- ON UPDATE CASCADE;

-- ALTER TABLE spells
-- ADD COLUMN primary_effect VARCHAR(20) NOT NULL,
-- ADD COLUMN secondary_effect VARCHAR(20);

-- ALTER TABLE spells
-- ADD COLUMN level INT NOT NULL;

SELECT * FROM times;

ALTER TABLE times
ADD COLUMN unit_abbr VARCHAR(10);

UPDATE times
SET unit_abbr = "D" WHERE unit_name = "day";
UPDATE times
SET unit_abbr = "H" WHERE unit_name = "hour";
UPDATE times
SET unit_abbr = "M" WHERE unit_name = "minute";
UPDATE times
SET unit_abbr = "Rd" WHERE unit_name = "round";
UPDATE times
SET unit_abbr = "A" WHERE unit_name = "action";
UPDATE times
SET unit_abbr = "BA" WHERE unit_name = "bonus action";
UPDATE times
SET unit_abbr = "Rn" WHERE unit_name = "reaction";
UPDATE times
SET unit_abbr = "I" WHERE unit_name = "instantaneous";

SELECT * FROM times;
