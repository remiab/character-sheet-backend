USE ttrpg;

-- SELECT * FROM ithen_spell_list;

-- UPDATE ithen_spell_list i
-- SET i.prepared = 'Y'
-- WHERE i.spell_name IN ('fireball', 'bend time');

-- SELECT * FROM ithen_spell_list i 
-- WHERE i.prepared = 'Y';

-- CREATE VIEW spell_glance AS(
-- SELECT i.spell_name, sl.level, CONCAT(d.ndice, 'd', d.sides)
-- FROM ithen_spell_list i
-- LEFT JOIN spells sl 
-- ON i.spell_name = sl.spell_name
-- LEFT JOIN damage d
-- ON i.spell_name = d.spell_name
-- WHERE i.prepared = 'Y');

SELECT * FROM spell_glance;