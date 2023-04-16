from flask import Flask, jsonify, request
from utils import get_from_db, update_prepared_status

app = Flask(__name__)
db_name = 'ttrpg'


@app.route('/')
def hello_world():
    return('hello world')

@app.route('/spell_list')
def view_spells():
    query = "CALL view_ithen_spells();"
    result = get_from_db(db_name, query)
    for item in result:
        item["spell_name"] = item["spell_name"].title()
    return jsonify(result)

@app.route('/prepared_spells')
def view_prepared_spells():
    query = """
        SELECT * FROM ithen_spell_list i
        WHERE i.prepared = 'Y';"""
    result = get_from_db(db_name, query)
    return jsonify(result)

@app.route('/update/prepare/<string:spell_name>', methods=['PUT'])
def update_prepared(spell_name):
    update = request.get_json()
    update_prepared_status(db_name, spell_name, update["spell_status"])
    return update



if __name__ == '__main__':
    app.run(debug=True)