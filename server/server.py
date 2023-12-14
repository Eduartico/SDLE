import os, sys, json, sqlite3
import requests
from flask import Flask, request, jsonify, g, Response

try :
    server_id = int(sys.argv[1])
except:
    server_id = 0

app = Flask(__name__)
PORT = 5100  + server_id # Set port here
app.config['DATABASE'] = f'server_{PORT}.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

server_db = f'server_{server_id}.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def action_add_item(item_id, list_id, item_name, quantity, boughtQuantity=0):
    db = get_db()
    db.execute('INSERT INTO ListItem (ItemId, ListId, Name, Quantity, BoughtQuantity) VALUES (?,?,?,?,?)', (item_id, list_id, item_name, quantity, boughtQuantity))
    db.commit()
    print("Added {} to list {}".format(item_name, list_id))

def action_update_item(item_id, boughtQuantity):
    db = get_db()
    db.execute('UPDATE ListItem SET BoughtQuantity = ? WHERE ItemId = ?', (boughtQuantity, item_id))
    db.commit()
    print("Updated item {}".format(item_id))

def action_add_list(list_id, name, is_recipe, user_id):
    db = get_db()
    db.execute('INSERT INTO List (ListId, Name, IsRecipe) VALUES (?,?,?)', (list_id, name, is_recipe))
    db.execute('INSERT INTO ListUser (ListId, UserId) VALUES (?,?)', (user_id, list_id))
    db.commit()
    print("Adding list {}".format(list_id))

def action_get_list(list_id):
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM List WHERE ListId = ?', (list_id,))
    except:
        print("Error getting list")
        return json.dumps({"data": None})
    try:
        data = cursor.fetchone()
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
    except:
        print("Error getting list")
        return json.dumps({"data": None})
    return json.dumps({"data": data})

def action_get_lists():
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM List')
        lists = cursor.fetchall()
        
        data = {}
        for l in lists:
            cursor = db.execute('SELECT * FROM ListItem WHERE ListId = ?', (l['ListId'],))
            items = cursor.fetchall()
            data[l['ListId']] = {
                'id': l['ListId'],
                'name': l['Name'],
                'isRecipe': l['IsRecipe'],
                'items': [{
                    'id': d['ItemId'],
                    'name': d['Name'],
                    'quantity': d['Quantity'],
                    'boughtQuantity': d['BoughtQuantity']
                } for d in items]
            }
        
        return json.dumps({"data": data})
    except Exception as e:
        print(f"Error getting lists: {e}")
        return json.dumps({"data": None})


@app.route('/add_list', methods=['POST'])
def add_list():
    data = request.get_json()
    list_id = data['list_id']
    name = data['name']
    is_recipe = data['is_recipe']
    user_id = data['user_id']
    items = data['items']

    # TODO add also to CRDT implementation

    action_add_list(list_id, name, is_recipe, user_id)
    for item in items:
        action_add_item(item['id'], list_id, item['name'], item['quantity'])
    return jsonify({"status": "OK"})

@app.route('/update_list', methods=['POST'])
def update_list():
    data = request.get_json()
    list_id = data['list_id']
    name = data['name']
    is_recipe = data['is_recipe']
    user_id = data['user_id']
    items = data['items']

    # TODO add also to CRDT implementation

    db = get_db()
    db.execute('DELETE FROM ListItem WHERE ListId = ?', (list_id,))
    db.commit()
    for item in items:
        action_add_item(item['id'], list_id, item['name'], item['quantity'], item['boughtQuantity'])
    return jsonify({"status": "OK"})


@app.route('/get_list/<int:list_id>', methods=['GET'])
def get_list(list_id):
    response = action_get_list(list_id)
    return str(response)

@app.route('/get_lists', methods=['GET'])
def get_lists():
    response = action_get_lists()
    return str(response)

if __name__ == "__main__":
    with app.app_context():
        if not os.path.exists(app.config['DATABASE']):
            init_db()

    response = requests.post(f"http://localhost:4000/add_server", json={"server_port": PORT})
    print(response)
    app.run(debug=True, port=PORT, threaded=True)
 
    
    