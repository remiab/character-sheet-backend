from flask import Flask, jsonify
from utils import get_spell_list

app = Flask(__name__)


@app.route('/')
def hello_world():
    return('hello world')

@app.route('/spell_list')
def view_spells():
    result = get_spell_list()
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)