-- use ttrpg;

-- CREATE TABLE base_stat_alters(
-- 	stat VARCHAR(3) NOT NULL,
--     `type` VARCHAR(30) NOT NULL,
--     num_to_mod INT NOT NULL,
--     `source` VARCHAR(30) NOT NULL,
--     `character` VARCHAR(30) NOT NULL
-- );

-- INSERT INTO base_stat_alters
-- VALUES
-- ("CON", "override", 19, "Amulet of Health", bs.`character`),
-- ("CON", "bonus", 1, "Upbringing: Erudite", bs.`character`),
-- ("INT", "bonus", 2, "Upbringing: Erudite", bs.`character`),
-- ("INT", "bonus", 1, "Feat: Linguist", bs.`character`);

SELECT * FROM base_stat_alters;

-- UPDATE base_stats bs
-- SET bs.score = 6 WHERE bs.stat_abbr = "STR" AND bs.character = bs.`character`;

-- UPDATE base_stats bs
-- SET bs.score = 17 WHERE bs.stat_abbr = "INT" AND bs.character = bs.`character`;

-- UPDATE base_stats bs
-- SET bs.score = 11 WHERE bs.stat_abbr = "CON" AND bs.character = bs.`character`;

WITH bsa AS (SELECT * FROM base_stat_alters)

SELECT bs.`character`, bs.stat_abbr, bs.score rolled_stat, bs. index_id,
	CASE WHEN bs.stat_abbr IN 
				(SELECT bsa.stat 
				FROM bsa 
				WHERE bsa.`character` = bs.`character`
				AND bsa.`type` = "override") 
		THEN (SELECT bsa.num_to_mod FROM bsa WHERE bsa.`character` = bs.`character` AND bsa.`type` = "override")
        WHEN bs.stat_abbr IN 
				(SELECT bsa.stat 
				FROM bsa 
				WHERE bsa.`character` = bs.`character`
				AND bsa.`type` = "bonus") 
            AND bs.stat_abbr IN 
				(SELECT bsa.stat 
				FROM bsa 
				WHERE bsa.`character` = bs.`character`
				AND bsa.`type` = "override")
        THEN (SELECT bsa.num_to_mod FROM bsa WHERE bsa.`character` = bs.`character` AND bsa.`type` = "override")
        WHEN bs.stat_abbr IN 
				(SELECT bsa.stat 
				FROM bsa 
				WHERE bsa.`character` = bs.`character`
				AND bsa.`type` = "bonus") 
            AND bs.stat_abbr NOT IN 
				(SELECT bsa.stat 
				FROM bsa 
				WHERE bsa.`character` = bs.`character`
				AND bsa.`type` = "override")
		 THEN (
			SELECT bs.score + SUM(bsa.num_to_mod) 
            FROM bsa 
            WHERE bsa.`character` = bs.`character` 
            AND bsa.`type` = "bonus"
            AND bs.stat_abbr = bsa.stat)
        ELSE bs.score 
        END `score`
FROM base_stats bs
WHERE bs.`character` = bs.`character`
ORDER BY bs.index_id;





