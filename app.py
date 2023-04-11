from flask import Flask, jsonify
from utils import get_from_db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return('hello world')

@app.route('/spell_list')
def view_spells():
    db_name = "ttrpg"
    query = "CALL view_ithen_spells();"
    result = get_from_db(db_name, query)
    return jsonify(result)

@app.route('/prepared_spells')
def view_prepared_spells():
    db_name = 'ttrpg'
    query = """
        SELECT * FROM ithen_spell_list i
        WHERE i.prepared = 'Y';"""
    result = get_from_db(db_name, query)
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)