USE ttrpg;

-- CREATE TABLE IF NOT EXISTS damage(
-- 	spell_name VARCHAR(50) NOT NULL,
--     ndice INT,
--     sides INT,
--     modifier INT,
--     dmg_type VARCHAR(20)    
-- );

-- ALTER TABLE damage
-- ADD CONSTRAINT fk_spellname
-- FOREIGN KEY damage(spell_name)
-- REFERENCES spells(spell_name)
-- ON UPDATE CASCADE;

-- ALTER TABLE damage
-- DROP COLUMN dmg_type;

-- INSERT INTO damage (spell_name, ndice, sides)
-- VALUES
-- ("firebolt", 2, 10, 0),
-- ("catapult", 3, 8, 0),
-- ("chromatic orb", 3, 8, 0),
-- ("shatter", 3, 8, 0);
-- ("burning hands", 3, 6),
-- ("earth tremor", 1, 6),
-- ("scorching ray", 2, 6),
-- ("web", 2, 4);
-- ("fireball", 8, 6),
-- ("bend time", 3, 8);




-- ALTER TABLE damage
-- ADD COLUMN half_save VARCHAR(20);

-- UPDATE damage
-- SET half_save = 'Y' 
-- WHERE spell_name IN ("fireball", "burning hands");

-- SELECT * FROM damage;

-- ALTER TABLE damage
-- DROP COLUMN modifier,
-- ADD COLUMN modifier VARCHAR(20);


