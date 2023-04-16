USE ttrpg;

-- CREATE TABLE base_stats(
-- 	base_stat VARCHAR(20) NOT NULL,
--     stat_abbr VARCHAR(3) NOT NULL PRIMARY KEY,
--     score INT NOT NULL
-- );

-- INSERT INTO base_stats
-- VALUES
-- ("Level", "LVL", 9);
-- ("Strength", "STR", 7),
-- ("Dexterity", "DEX", 12),
-- ("Constitution", "CON", 12),
-- ("Intelligence", "INT", 20),
-- ("Wisdom", "WIS", 15),
-- ("Charisma", "CHA", 16);

-- SELECT * FROM base_stats;

-- CREATE VIEW base_mods AS
-- (
-- 	SELECT bs.stat_abbr, FLOOR(bs.score/2 -5)
--     FROM base_stats bs
-- );
-- UPDATE base_stats bs
-- SET bs.score = 16
-- WHERE bs.stat_abbr = 'WIS';
-- UPDATE base_stats bs
-- SET bs.stat_abbr = 'PB'
-- WHERE bs.base_stat = 'Level';
-- SELECT * FROM base_mods;

-- CREATE TABLE proficiencies(
-- 	proficiency VARCHAR(30) NOT NULL,
--     p_type VARCHAR(20) NOT NULL,
--     p_source VARCHAR(30)
-- );

-- INSERT INTO proficiencies
-- VALUES
-- -- ('Arcana', 'Skill', 'Wizard Class Feature'),
-- -- ('Deception', 'Skill', 'Feat: Skill Expert, TCOE')
-- -- ('History', 'Skill', 'Heirloom: Eyes of the Gods'),
-- -- ('Insight', 'Skill', 'Wizard Class Feature')
-- ('Persuasion', 'Skill', 'Background: Acolyte'),
-- ('Persuasion', 'Skill', 'Feat: Skill Expert, TCOE'),
-- ('Religion', 'Skill', 'Heirloom: Eyes of the Gods')
-- ;
-- ('INT', 'Saving Throw', 'Class Feature: Wizard'),
-- ('WIS', 'Saving Throw', 'Class Feature: Wizard');
-- ('Celestial', 'Language', 'Heirloom: Eyes of the Gods'),
-- ('Common', 'Language', 'Upbringing: Erudite'),
-- ('Dwarvish', 'Language', 'Upbringing: Erudite'),
-- ('Elvish', 'Language', 'Feat: Linguist'),
-- ('Gnomish', 'Language', "Homebrew: VJ's +1 INT"),
-- ('Goblin', 'Language', 'Feat: Linguist'),
-- ('Infernal', 'Language', 'Upbringing: Erudite'),
-- ('Marquesian', 'Language', "Homebrew: VJ's +1 INT"),
-- ('Primordial', 'Language', 'Background: Acolyte'),
-- ('Undercommon', 'Language', 'Background: Acolyte'),
-- ('Zemnian', 'Language', 'Linguist');

-- UPDATE proficiencies
-- SET p_source = 'Wizard Class Feature' WHERE proficiency = 'History';
-- UPDATE proficiencies
-- SET p_source = 'Heirloom: Eyes of the Gods' WHERE proficiency = 'Insight';
-- UPDATE proficiencies
-- SET p_source = 'Class Feature: Wizard' WHERE p_source = 'Wizard Class Feature';

-- DELETE FROM proficiencies WHERE proficiency = 'Acrobatics';



-- SELECT * FROM proficiencies;

-- CREATE TABLE skill_mods(
-- 	skill VARCHAR(30) NOT NULL,
--     skill_mod VARCHAR(5) NOT NULL,
--     other_bonus INT,
--     bonus_source VARCHAR(20)
-- );

-- INSERT INTO skill_mods(skill, skill_mod)
-- VALUES
-- ('Acrobatics', 'DEX'),
-- ('Animal Handling', 'WIS'),
-- ('Arcana', 'INT'),
-- ('Athletics', 'STR'),
-- ('Deception', 'CHA'),
-- ('History', 'INT'),
-- ('Insight', 'WIS'),
-- ('Intimidation', 'CHA'),
-- ('Investigation', 'INT'),
-- ('Medicine', 'WIS'),
-- ('Nature', 'INT'),
-- ('Perception', 'WIS'),
-- ('Performance', 'CHA'),
-- ('Persuasion', 'CHA'),
-- ('Religion', 'INT'),
-- ('Sleight of Hand', 'DEX'),
-- ('Stealth', 'DEX'),
-- ('Survival', 'WIS');

-- UPDATE skill_mods
-- SET other_bonus = 2 WHERE skill = 'History';

-- UPDATE skill_mods
-- SET bonus_source = 'Upbringing: Erudite' WHERE skill = 'History';

-- ALTER TABLE skill_mods
-- CHANGE skill_mod base_stat VARCHAR(5) NOT NULL;

-- SELECT * FROM skill_mods;

CREATE VIEW skill_list AS(
WITH skill_bases AS(
	SELECT sm.skill, sm.base_stat, bm.modifier
    FROM skill_mods sm
    LEFT JOIN base_mods bm
    ON sm.base_stat = bm.stat
)

SELECT sb.skill SKILL, sb.base_stat BASE_STAT, 
CASE
WHEN sb.skill IN(
	SELECT p.proficiency FROM proficiencies p
    WHERE p.p_type = 'Skill') AND sm.other_bonus IS NOT NULL
    THEN sb.modifier + ((SELECT COUNT(p.proficiency) FROM proficiencies p
						WHERE p.proficiency = sb.skill)
                        * 
						(SELECT bm.modifier FROM base_mods bm
						WHERE bm.stat = 'PB'))
                        + sm.other_bonus
WHEN sb.skill IN(
	SELECT p.proficiency FROM proficiencies p
    WHERE p.p_type = 'Skill') AND sm.other_bonus IS NULL 
    THEN sb.modifier + ((SELECT COUNT(p.proficiency) FROM proficiencies p
						WHERE p.proficiency = sb.skill)
                        * 
						(SELECT bm.modifier FROM base_mods bm
						WHERE bm.stat = 'PB'))
ELSE sb.modifier
END
AS ability_mod
FROM skill_bases sb
LEFT JOIN skill_mods sm
ON sb.skill = sm.skill);

SELECT * FROM skill_list;




