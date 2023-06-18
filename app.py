from flask import Flask, jsonify, request
from utils import get_from_db, update_db, get_multiple_from_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_name = 'ttrpg'


@app.route('/<string:character>/spell_list', methods=['GET'])
def view_spells(character):
    query = f"CALL view_{character}_spells();"
    result = get_from_db(db_name, query)
    for item in result:
        item["spell_name"] = item["spell_name"].title()
    return jsonify(result)


@app.route('/<string:character>/spell_list/prepared_spells', methods=['GET'])
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
    for item in result:
        item["spell_name"] = item["spell_name"].title()
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


@app.route('/image_descs/<string:spell_name>', methods=['GET'])
def retrieve_img_id(spell_name):
    query = f"""
    SELECT d.drive_id FROM drive_id d
    WHERE d.spell_name = '{spell_name}';
    """
    result = get_from_db(db_name, query)
    return jsonify(result)


@app.route('/<string:character>/base_stats', methods=['GET'])
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

@app.route('/<string:character>/skills', methods=['GET'])
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


@app.route('/<string:character>/hit_points', methods=['GET'])
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


@app.route('/<string:character>/hit_points/temp_hp', methods=['GET'])
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
                VALUES ("{character}", {update["current"][key]}, "{update["dmg_occurred"]}", "{update["event"]}", {update["max"][key]});
            """
        update_db(db_name, query)
    return "updated hp"

@app.route('/<string:character>/hit_points/arcane_ward/update', methods=['PUT'])
def replenish_arcane_ward(character):
    update = request.get_json()
    query = f"""
        INSERT INTO arcane_ward_tracker
        VALUES ("{character}", {update["replen"]}, "{update["dmg_occurred"]}", "{update["event_tag"]}", {update["max"]});
        """
    update_db(db_name, query)
    return ("replenished arcane ward")


@app.route('/<string:character>/expendables/combat', methods=['GET'])
def retrieve_combat_expendables(character):
    query = f"""
        SELECT expend_id, `name`, disp_priority 
        FROM expendables
        WHERE `character` = "{character}"
        AND time_of_use = "combat"
        ORDER BY disp_priority, expend_id;
        """
    result = get_from_db(db_name, query)
    grouped_results = {}
    spell_slots = {}
    for item in result:
        try:
            grouped_results[item["name"]].append(item)
        except KeyError:
            if "Spell Slot" in item["name"]:
                try:
                    spell_slots[item["name"]].append(item)
                except KeyError:
                    spell_slots[item["name"]] = []
                    spell_slots[item["name"]].append(item)
            else:
                grouped_results[item["name"]] = []
                grouped_results[item["name"]].append(item)
    grouped_results["Spell_Slots"] = spell_slots
    return(grouped_results)

@app.route('/<string:character>/spell_slots/<string:level_tags>', methods=['GET'])
def check_if_slots_available(character, level_tags):
    levels = level_tags.split(',')
    availability_dict = {}

    for level in levels:
        query = f"""
            SELECT expend_id 
            FROM expendables
            WHERE `character` = '{character}'
            AND expended = 0
            AND `name` LIKE '{level}%'
            ORDER BY expend_id
            LIMIT 1;
        """
        result =  get_from_db(db_name, query)
        
        if result:
            availability_dict[level] = result[0]["expend_id"]
        else:
            availability_dict[level] = None

    return availability_dict

@app.route('/expendables/<int:expend_id>/update', methods=['POST'])
def update_expendable_status(expend_id):
    update = request.get_json()
    status = update["update_status"]
    query = f"""
        UPDATE expendables
        SET expended = {status}
        WHERE expend_id = {expend_id};
    """
    update_db(db_name, query)
    return "Updated expendable status"
    

@app.route('/expendables/<string:expend_ids>', methods=['GET'])
def retrieve_expended_status(expend_ids):
    query= f"""
        SELECT expend_id, expended
        FROM expendables
        WHERE expend_id IN ({expend_ids});
    """
    result = get_from_db(db_name, query)
    return result


@app.route('/favicon.ico', methods=['GET'])
def ferret_out_favico():
    return "Ferret out"


if __name__ == '__main__':
    app.run(debug=True, port=5000)