from flask import Flask, jsonify, request, g
from flask import send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
PORT = 5000  # Set port here
app.config['DATABASE'] = f'database_{PORT}.db'
CORS(app)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/api/data', methods=['GET'])
def get_data():
    db = get_db()
    cursor = db.execute('SELECT * FROM data')
    data = cursor.fetchall()
    return jsonify({'data': [dict(row) for row in data]})

@app.route('/api/data', methods=['POST'])
def post_data():
    req_data = request.get_json()
    db = get_db()
    db.execute('INSERT INTO data (key, value) VALUES (?, ?)',
               (req_data['key'], req_data['value']))
    db.commit()
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(app.config['DATABASE']):
            init_db()
    app.run(debug=True, port=PORT)


# Update the Flask app to serve the React build

# @app.route('/', methods=['GET'])
# def serve_react_app():
#     return send_from_directory('../react-app/build', 'index.html')

# @app.route('/static/<file>', methods=['GET'])
# def serve_static(file):
#     return send_from_directory('../react-app/build/static', file)
