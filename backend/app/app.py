from flask import Flask, jsonify, request, g
from flask import send_from_directory
from flask_cors import CORS
import sqlite3
import os

CURRENT_USER = None

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

@app.route('/api/users', methods=['GET'])
def get_users():
    db = get_db()
    cursor = db.execute('SELECT * FROM User')
    data = cursor.fetchall()
    return jsonify({'data': [dict(d) for d in data]})


def method_name():
    pass
@app.route('/api/lists', methods=['GET'])
def get_lists():
    db = get_db()
    cursor = db.execute('SELECT * FROM List')
    data = cursor.fetchall()
    return jsonify({'data': [dict(d) for d in data]})

@app.route('/api/list/<int:list_id>/items', methods=['GET'])
def get_list_items(list_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM ListItem WHERE ListId = ?', (list_id,))
    data = cursor.fetchall()
    return jsonify({'data': [dict(d) for d in data]})

@app.route('/api/list/<int:list_id>/item/<int:item_id>', methods=['GET'])
def get_list_item(list_id, item_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM ListItem WHERE ListId = ? AND ItemId = ?', (list_id, item_id))
    data = cursor.fetchone()
    return jsonify({'data': dict(data)})

@app.route('/api/user/<int:user_id>/lists', methods=['GET'])
def get_user_lists(user_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM ListUser WHERE UserId = ?', (user_id,))
    data = cursor.fetchall()
    return jsonify({'data': [dict(d) for d in data]})

@app.route('/api/user/current', methods=['GET'])
def get_current_user():
    if CURRENT_USER is None:
        return jsonify({'data': "No user logged in"})
    return jsonify({'data': {"user_id": CURRENT_USER}})

@app.route('/api/auth/login', methods=['POST'])
def login():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('SELECT * FROM User WHERE Username = ? AND Password = ?', (req_data['username'], req_data['password']))
    data = cursor.fetchone()
    if data is None:
        return jsonify({'data': "Invalid username or password"})
    CURRENT_USER = data['UserId']
    return jsonify({'data': dict(data)})

@app.route('/api/auth/register', methods=['POST'])
def register():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('INSERT INTO User (Username, Email, Password) VALUES (?, ?, ?)', (req_data['username'], req_data['email'], req_data['password']))
    db.commit()
    return jsonify({'data': {'user_id': cursor.lastrowid}})

@app.route('/api/addList', methods=['POST'])
def add_list():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('INSERT INTO List (Name, IsRecipe) VALUES (?, ?)', (req_data['name'], req_data['isRecipe']))
    cursor = db.execute('INSERT INTO ListUser (ListId, UserId) VALUES (?,?)', (cursor.lastrowid, req_data['userId']))
    db.commit()
    return jsonify({'data': {'list_id': cursor.lastrowid}})

@app.route('/api/addListItem', methods=['POST'])
def add_list_item():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('INSERT INTO ListItem (ListId, Name, Quantity, BoughtQuantity) VALUES (?, ?, ?, ?)', (req_data['listId'], req_data['name'], req_data['quantity'], req_data['boughtQuantity']))
    db.commit()
    return jsonify({'data': {'item_id': cursor.lastrowid}})

@app.route('/api/updateList', methods=['PUT'])
def update_list():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('UPDATE List SET Name = ?, IsRecipe = ? WHERE ListId = ?', (req_data['name'], req_data['isRecipe'], req_data['listId']))
    db.commit()
    return jsonify({'data': {'list_id': cursor.lastrowid}})

@app.route('/api/updateListItem', methods=['PUT'])
def update_list_item():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('UPDATE ListItem SET Name = ?, Quantity = ?, BoughtQuantity = ? WHERE ItemId = ?', (req_data['name'], req_data['quantity'], req_data['boughtQuantity'], req_data['itemId']))
    db.commit()
    return jsonify({'data': {'item_id': cursor.lastrowid}})

@app.route('/api/deleteListItem', methods=['DELETE'])
def delete_list_item():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('DELETE FROM ListItem WHERE ItemId = ?', (req_data['itemId'],))
    db.commit()
    return jsonify({'data': {'item_id': cursor.lastrowid}})

@app.route('/api/deleteList', methods=['DELETE'])
def delete_list():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('DELETE FROM List WHERE ListId = ?', (req_data['listId'],))
    db.commit()
    return jsonify({'data': {'list_id': cursor.lastrowid}})


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
