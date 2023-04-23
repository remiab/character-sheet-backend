use ttrpg;

SELECT DISTINCT bm.STAT, bm.SCORE, bm.MODIFIER, bs.index_id
FROM base_mods bm
LEFT JOIN base_stats bs
ON bm.STAT = bs.stat_abbr
WHERE bm.CHARACTER = "ithen"
ORDER BY bs.index_id;

