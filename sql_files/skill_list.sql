use ttrpg;

WITH mods_table AS (
SELECT s.skill, 
	bm.modifier base_mod,
	(SELECT COUNT(p.proficiency) 
			FROM proficiencies p 
            WHERE p.proficiency = s.skill 
            AND `character` = "ithen") proficiency,
	CASE WHEN s.skill IN(SELECT b.skill FROM skill_bonuses b WHERE `character` = "ithen")
		THEN (SELECT SUM(b.bonus)
			FROM skill_bonuses b 
			WHERE s.skill = b.skill
			AND `character` = "ithen")
		ELSE 0
        END bonus,
	s.base_stat
FROM skills s
LEFT JOIN base_mods bm 
ON bm.stat = s.base_stat
WHERE bm.`character` = "ithen"
)

SELECT m.skill, 
	m.base_stat,
	CASE 
		WHEN m. proficiency = 2 THEN "Expertise"
        WHEN m.proficiency = 1 THEN "Proficient"
        ELSE NULL
        END
	AS proficiency_level,
    SUM(
		m.base_mod + 
        m.bonus +
        (m.proficiency * (SELECT proficiency_bonus("ithen")))) AS `modifier`
    FROM mods_table m
    GROUP BY m.skill, m.base_stat;




-- SELECT s.skill, s.base_stat