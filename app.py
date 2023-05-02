from flask import Flask, jsonify, request
from utils import get_from_db, update_db, get_multiple_from_db

app = Flask(__name__)
db_name = 'ttrpg'


@app.route('/<string:character>/spell_list')
def view_spells(character):
    query = f"CALL view_{character}_spells();"
    result = get_from_db(db_name, query)
    for item in result:
        item["spell_name"] = item["spell_name"].title()
    return jsonify(result)


@app.route('/<string:character>/spell_list/prepared_spells')
def retrieve_prepared_spells(character):
    query = f"""
            SELECT s.spell_name, s.`level`, s.school, s.casting_int, s.casting_unit, s.dur_int, s.dur_unit,
            s.range_ft, t1.threshold, a.aoe_size, a.aoe_shape, d.ndice, d.sides, d.`modifier`, d.half_save
            FROM spells s 
            LEFT JOIN thresholds t1
            ON s.spell_name = t1.spell_name
            LEFT JOIN aoes a
            ON s.spell_name = a.spell_name
            LEFT JOIN damage d
            ON s.spell_name = d.spell_name
            WHERE s.spell_name IN (
                SELECT i.spell_name FROM {character}_spell_list i
                WHERE i.prepared = "Y"
                )
            ORDER BY s.`level`;
            """
    result = get_from_db(db_name, query)
    return jsonify(*result)


@app.route('/<string:character>/spell_list/<string:spell_name>/prepare', methods=['PUT'])
def update_prepared(character, spell_name):
    update = request.get_json()
    query = f"""
        UPDATE {character}_spell_list
        SET prepared = "{update["spell_status"]}"
        WHERE spell_name = "{spell_name}";
    """
    update_db(db_name, query)
    return f"updated prepared status for {spell_name}"


@app.route('/image_descs/<string:spell_name>')
def retrieve_img_id(spell_name):
    query = f"""
    SELECT d.drive_id FROM drive_id d
    WHERE d.spell_name = '{spell_name}';
    """
    result = get_from_db(db_name, query)
    return jsonify(result)


@app.route('/<string:character>/base_stats')
def retrieve_base_stats(character):
    query = f"""
    SELECT DISTINCT bm.STAT, bm.SCORE, bm.MODIFIER, bs.index_id
    FROM base_mods bm
    LEFT JOIN base_stats bs
    ON bm.STAT = bs.stat_abbr
    WHERE bm.`CHARACTER` = "{character}"
    ORDER BY bs.index_id;
    """
    result = get_from_db(db_name, query)
    return jsonify(result)

@app.route('/<string:character>/skills')
def retrieve_skills(character):
    query = f"""
    WITH mods_table AS (
    SELECT s.skill, 
        bm.modifier base_mod,
        (SELECT COUNT(p.proficiency) 
                FROM proficiencies p 
                WHERE p.proficiency = s.skill 
                AND `character` = "{character}") proficiency,
        CASE WHEN s.skill IN(SELECT b.skill FROM skill_bonuses b WHERE `character` = "{character}")
            THEN (SELECT SUM(b.bonus)
                FROM skill_bonuses b 
                WHERE s.skill = b.skill
                AND `character` = "{character}")
            ELSE 0
            END bonus,
        s.base_stat
    FROM skills s
    LEFT JOIN base_mods bm 
    ON bm.stat = s.base_stat
    WHERE bm.`character` = "{character}"
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
        (m.proficiency * (SELECT proficiency_bonus("{character}")))) AS `modifier`
    FROM mods_table m
    GROUP BY m.skill, m.base_stat;
    """
    result = get_from_db(db_name, query)
    return jsonify(result)


@app.route('/<string:character>/hit_points')
def retrieve_hit_points(character):
    q_current = f"""SELECT current_hp, max_hp
                    FROM(
                        SELECT sum(damage) OVER (ORDER BY dmg_occurred) AS current_hp,
                                dmg_occurred, max_hp
                        FROM hp_tracker
                        WHERE `character` = "{character}"
                        ORDER BY dmg_occurred DESC
                        LIMIT 1
                        ) hp_history;
                 """
    
    q_temp = f"""
            SELECT `current_thp`
            FROM(
                SELECT sum(damage) OVER (ORDER BY dmg_occurred) AS `current_thp`,
                        dmg_occurred
                FROM temp_hp_tracker
                WHERE `character` = "{character}"
                ORDER BY dmg_occurred DESC
                LIMIT 1
                ) thp_history;
             """
    
    q_ward = f"""
            SELECT `current_well`, `max_points`
            FROM(
                SELECT sum(damage) OVER (ORDER BY dmg_occurred) AS `current_well`,
                        dmg_occurred, max_points
                FROM arcane_ward_tracker
                WHERE `character` = "{character}"
                ORDER BY dmg_occurred DESC
                LIMIT 1
                ) aw_history;
            
            """
    queries = [q_current, q_temp, q_ward]
    tags = ["current_hp", "temp_hp", "arcane_ward"]
    results = get_multiple_from_db(db_name, queries, tags)
    return jsonify(results)


@app.route('/<string:character>/hit_points/temp_hp')
def retrieve_temp_hp(character):
    query = f"""
            SELECT `current_thp`
            FROM(
                SELECT sum(damage) OVER (ORDER BY dmg_occurred) AS `current_thp`,
                        dmg_occurred
                FROM temp_hp_tracker
                WHERE `character` = "{character}"
                ORDER BY dmg_occurred DESC
                LIMIT 1
                ) thp_history;
             """
    result = get_from_db(db_name, query)
    return jsonify(*result)


@app.route('/<string:character>/hit_points/temp_hp/update', methods=['PUT'])
def update_temp_hp(character):
    update = request.get_json()
    query = f"""
        INSERT INTO temp_hp_tracker
        VALUES ("{character}", {update["thp"]}, "{update["date_occurred"]}", "{update["event"]}");
        """
    print(query)
    update_db(db_name, query)
    return f"updated temp hp with {update['thp']} hp"


@app.route('/<string:character>/hit_points/update', methods=['PUT'])
def update_after_damage(character):
    update = request.get_json()
    for key in update["current"].keys():
        if key == "temp_hp":
            query = f"""
                INSERT INTO {key}_tracker
                VALUES ("{character}", {update["current"][key]}, "{update["dmg_occurred"]}", "{update["event"]}");
                """
        else:
            query = f"""
                INSERT INTO {key}_tracker
                VALUES ("{character}", {update["current"][key]}, "{update["dmg_occurred"]}", "{update["event"]}", {update["max"][key]})
            """
        update_db(db_name, query)
    return "updated hp"


if __name__ == '__main__':
    app.run(debug=True)