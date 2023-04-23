from flask import Flask, jsonify, request
from utils import get_from_db, update_prepared_status

app = Flask(__name__)
db_name = 'ttrpg'


@app.route('/<string:character>/spell_list')
def view_spells(character):
    query = f"CALL view_{character}_spells();"
    result = get_from_db(db_name, query)
    for item in result:
        item["spell_name"] = item["spell_name"].title()
    return jsonify(result)

@app.route('/update/prepare/<string:character>/<string:spell_name>', methods=['PUT'])
def update_prepared(character, spell_name):
    update = request.get_json()
    query = f"""
        UPDATE {character}_spell_list
        SET prepared = "{update["spell_status"]}"
        WHERE spell_name = "{spell_name}";
    """
    update_prepared_status(db_name, query)
    return update

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

@app.route('/<string:character>/skills>')
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

if __name__ == '__main__':
    app.run(debug=True)