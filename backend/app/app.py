from flask import Flask, jsonify, request, g
from flask import abort, render_template, request
from flask import session
from flask_cors import CORS
from flask_session.__init__ import Session
from threading import Lock
import threading
import sqlite3
import os, sys, zmq, json
import time


try :
    client_number = int(sys.argv[1])
except:
    client_number = 0

app = Flask(__name__)
PORT = 5000  + client_number
app.config['DATABASE'] = f'database_{PORT}.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

CORS(app)

state_lock = Lock()
username = None
user_id = None

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

def update_lists_periodically():
    print('update_lists_periodically is running')  # Add this line
    with app.app_context():
        while True:
            try:
                print('Updated')
                db = get_db()
                cursor = db.execute('SELECT ListId FROM List')
                all_list_ids = [row['ListId'] for row in cursor.fetchall()]
                print('all_list_ids is ready')

                for list_id in all_list_ids:
                    print('sending request')
                    response = send_request({
                    'list_id': list_id,
                    'action': 'get_list'
                    })
                    print('received')
                    json_obj = json.loads(response)
                    data = json_obj.get('data', {})
                    list_data = data.get('list', {})

                    db.execute('UPDATE List SET Name = ?, IsRecipe = ? WHERE ListId = ?',
                            (list_data.get('name'), list_data.get('isRecipe'), list_id))

                    for item_data in list_data.get('items', []):
                        db.execute('UPDATE ListItem SET Name = ?, Quantity = ?, BoughtQuantity = ? WHERE ItemId = ?',
                                (item_data.get('name'), item_data.get('quantity'), item_data.get('boughtQuantity'), item_data.get('id')))
                print('Finished updating')  # Add this line
                db.commit()
                time.sleep(10)
            except Exception as e:
                print(f"Error updating lists: {e}")

# Funtions to communicate with the broker
def send_request(request):
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = u"Client-{}".format(client_number).encode("ascii")
    socket.connect("tcp://localhost:5559")
    socket.send_json(json.dumps(request))
    reply = socket.recv_json()
    socket.close()

@app.route('/api/users', methods=['GET'])
def get_users():
    db = get_db()
    cursor = db.execute('SELECT * FROM User')
    data = cursor.fetchall()
    return jsonify({'data': [dict(d) for d in data]})

@app.route('/api/lists', methods=['GET'])
def get_lists():
    db = get_db()
    cursor = db.execute('SELECT * FROM List')
    data = cursor.fetchall()
    return jsonify({'data': [dict(d) for d in data]})

@app.route('/api/list/<int:list_id>', methods=['GET'])
def get_list(list_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM List WHERE ListId = ?', (list_id,))
    data = cursor.fetchone()
    if (data is None): abort(404)
    cursor = db.execute('SELECT * FROM ListItem WHERE ListId = ?', (list_id,))
    items = cursor.fetchall()
    data = {
        'list': {
            'id': data['ListId'],
            'name': data['Name'],
            'isRecipe': data['IsRecipe'],
            'items' : [{
                'id': d['ItemId'],
                'name': d['Name'],
                'quantity': d['Quantity'],
                'boughtQuantity': d['BoughtQuantity']
                } for d in items]
        }
    }
    return jsonify({'data': data})

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
    if (data is None): abort(404)
    return jsonify({'data': dict(data)})

@app.route('/api/user/<int:user_id>/lists', methods=['GET'])
def get_user_lists(user_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM List WHERE ListId IN (SELECT ListId FROM ListUser WHERE UserId = ?)', (user_id,))
    data = cursor.fetchall()
    data = {
        'lists': [{
            'id': d['ListId'],
            'name': d['Name'],
            'isRecipe': d['IsRecipe']
        } for d in data]
    }
    return jsonify({'data': data})

@app.route('/api/auth/login', methods=['POST'])
def login():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('SELECT * FROM User WHERE Username = ? AND Password = ?', (req_data['username'], req_data['password']))
    data = cursor.fetchone()
    global username
    global user_id
    with state_lock:
        if data is None:
            abort(404)
        username = data['Username']
        user_id = data['UserId']
    data = {
        'user': {
            'id': data['UserId'],
            'username': data['Username'],
            'email': data['Email']
        }
    }
    with state_lock:
        username = data['user']['username']
        user_id = data['user']['id']
    response = jsonify({'data': data})
    # Remove the following line
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/user/current', methods=['GET'])
def get_current_user():
    global username
    global user_id
    with state_lock:
        if username is None or user_id is None:
            abort(404)
        data = {
            'user': {
                'name': username,
                'id': user_id
            }
        }
        response = jsonify({'data': data})
        # Remove the following line
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/api/auth/register', methods=['POST'])
def register():
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('INSERT INTO User (Username, Email, Password) VALUES (?, ?, ?)', (req_data['username'], req_data['email'], req_data['password']))
    db.commit()
    return jsonify({'data': {'user_id': cursor.lastrowid}})

@app.route('/api/addList', methods=['POST'])
def add_list():
    print('starting add')

    req_data = request.get_json()
    user_ids = req_data.get('usersId', [])
    print(user_ids)
    
    db = get_db()
    is_recipe_value = 1 if req_data['isRecipe'] else 0
    cursor = db.execute('INSERT INTO List (Name, IsRecipe) VALUES (?, ?)', (req_data['name'], is_recipe_value))

    list_id = cursor.lastrowid

    for user_id in user_ids:
        if(user_id == ','):
            continue
        print(f'adding {list_id} to {user_id}')
        db.execute('INSERT INTO ListUser (ListId, UserId) VALUES (?, ?)', (list_id, user_id))
        db.commit()
        
        send_request({
            'list_id': list_id,
            'action': 'add_list',
            'list_name': req_data['name'],
            'is_recipe': req_data['isRecipe'],
            'user_id': user_id,
            'boughtQuantity': 0
        })
    return jsonify({'data': {'list_id': list_id}})

@app.route('/api/list/<int:list_id>/addItem', methods=['POST'])
def add_list_item(list_id):
    req_data = request.get_json()
    db = get_db()
    cursor = db.execute('INSERT INTO ListItem (ListId, Name, Quantity, BoughtQuantity) VALUES (?, ?, ?, ?)',
                       (list_id, req_data['name'], req_data['quantity'], req_data['boughtQuantity']))
    db.commit()
    send_request({
        'list_id': list_id,
        'action': 'add_item',
        'item_id': cursor.lastrowid,
        'item_name': req_data['name'],
        'quantity': req_data['quantity'],
        'boughtQuantity': 0
    })
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
    send_request({
        'action': 'update_item',
        'item_id': req_data['itemId'],
        'boughtQuantity': req_data['boughtQuantity']
    })
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

@app.route('/api/list/<int:list_id>/item/<int:item_id>/buy', methods=['PUT']) # updates items listed as bought or not
def buy_list_item(list_id, item_id):
    req_data = request.get_json()
    bought_quantity = req_data.get('boughtQuantity', 0)

    db = get_db()
    cursor = db.execute('UPDATE ListItem SET BoughtQuantity = ? WHERE ListId = ? AND ItemId = ?', (bought_quantity, list_id, item_id))
    db.commit()
    
    send_request({
        'list_id': list_id,
        'action': 'update_item',
        'item_id': item_id,
        'boughtQuantity': bought_quantity
    })

    return jsonify({'data': {'item_id': item_id, 'bought_quantity': bought_quantity}})

@app.route('/api/user/recipes', methods=['GET'])
def get_recipes():
    db = get_db()
    cursor = db.execute('SELECT * FROM List WHERE IsRecipe = 1 OR IsRecipe = true')
    data = cursor.fetchall()
    data = {
        'lists': [{
            'id': d['ListId'],
            'name': d['Name'],
            'isRecipe': d['IsRecipe']
        } for d in data]
    }
    return jsonify({'data': data})


if __name__ == '__main__':
    update_thread = threading.Thread(target=update_lists_periodically, daemon=True)
    print('Starting update_thread')
    update_thread.start()
    with app.app_context():
        try:
            g.username
            g.user_id
        except:
            g.username = None
            g.user_id = None
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

# set the secret key.  keep this really secret:
