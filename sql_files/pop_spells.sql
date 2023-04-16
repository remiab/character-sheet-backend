USE ttrpg;

-- INSERT INTO spells
-- VALUES
-- ("firebolt", "evocation", 1, "action", NULL, "instantaneous", "damage", NULL, 0),
-- ("message", "transmutation", 1, "action", 1, "round", "communication", NULL, 0)
-- ("prestidigitation", "transmutation", 1, "action", 1, "hour", "utility", NULL, 0),
-- ("burning hands", "evocation", 1, "action", NULL, "instantaneous", "damage", NULL, 1)
-- ("catapult", "transmutation", 1, "A", NULL, "I", "damage", NULL, 1),
-- ("alienated mind", "enchantment", 1, "A", 1, "Rd", "damage", NULL, 1),
-- ("irregular dispersal", "abjuration", 1, "BA", 1, "Rd", "warding", NULL, 0),
-- ("numinous shield", "abjuration", 1, "BA", 1, "Rd", "damage", "buff", 1),
-- ("chromatic orb", "evocation", 1, "A", NULL, "I", "damage", NULL, 1)
-- ("detect magic", "divination", 1, "A", 10, "M", "detection", NULL, 1),
-- ("earth tremor", "evocation", 1, "A", NULL, "I", "damage", "control", 1),
-- ("expeditious retreat", "transmutation", 1, "BA", 10, "M", "buff", NULL, 1),
-- ("feather fall", "transmutation", 1, "Rn", 1, "M", "warding", NULL, 1),
-- ("identify", "divination", 1, "M", NULL, "I", "detection", NULL, 1),
-- ("shield", "abjuration", 1, "Rn", 1, "Rd", "buff", NULL, 1)
-- ("sapping sting", "necromancy", 1, "A", NULL, "I", "damage", "control", 0),
-- ("invisibility", "illusion", 1, "A", 1, "H", "warding", NULL, 2),
-- ("mirror image", "illusion", 1, "A", 1, "M", "warding", NULL, 2),
-- ("scorching ray", "evocation", 1, "A", NULL, "I", "damage", NULL, 2),
-- ("see invisibility", "divination", 1, "A", 1, "H", "detection", NULL, 2),
-- ("shatter", "evocation", 1, "A", NULL, "I", "damage", NULL, 2),
-- ("web", "conjuration", 1, "A", 1, "H", "control", "damage", 2),
-- ("altruistic healing", "necromancy", 1, "A", NULL, "I", "buff", NULL, 2),
-- ("attuned wards", "abjuration", 1, "BA", 1, "Rd", "warding", NULL, 2),
-- ("lifetap", "necromancy", 1, "A", NULL, "I", "damage", "buff", 2)
-- ("fireball", "evocation", 1, "A", NULL, "I", "damage", NULL, 3),
-- ("bend time", "abjuration", 1, "Rn", 1, "Rd", "warding", NULL, 3),
-- ("absorb mind", "divination", 1, "A", 10, "M", "detection", NULL, 3),
-- ("sustaining meditation", "abjuration", 1, "A", 24, "H", "buff", "warding", 3)
-- ("counterspell", "abjuration", 1, "Rn", NULL, "I", "warding", NULL, 3),
-- ("dispel magic", "abjuration", 1, "A", NULL, "I", "warding", NULL, 3),
-- ("private sanctum", "abjuration", 10, "M", 24, "H", "warding", NULL, 4),
-- ("mislead", "illusion", 1, "A", 1, "H", "warding", NULL, 5),
-- ("telepathic bond", "divination", 1, "A", 1, "H", "communication", NULL, 5);



 




-- SELECT * FROM spells;

-- ALTER TABLE spells
-- DROP FOREIGN KEY fk_cast_unit,
-- DROP FOREIGN KEY fk_dur_unit;

-- UPDATE spells
-- LEFT JOIN times ON spells.casting_unit = times.unit_name
-- SET spells.casting_unit = times.unit_abbr;

-- UPDATE spells
-- LEFT JOIN times ON spells.dur_unit = times.unit_name
-- SET spells.dur_unit = times.unit_abbr;


-- SELECT s.spell_name, 
-- CASE 
-- 	WHEN dur_int IS NULL THEN t.unit_name
--     ELSE CONCAT(s.dur_int, " ", t.unit_name)
--     END
-- AS Duration
-- FROM spells s
-- LEFT JOIN times t
-- ON s.dur_unit = t.unit_abbr
-- ORDER BY s.dur_int * t.unit_secs;