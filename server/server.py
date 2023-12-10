from __future__ import print_function
import multiprocessing
import os, sys, zmq, json, sqlite3

try :
    server_id = int(sys.argv[1])
except:
    server_id = 0

PORT = 5100  + server_id # Set port here
server_db = f'server_{server_id}.db'

def init_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    db = sqlite3.connect(server_db)
    db.row_factory = sqlite3.Row
    return db

def action_add_item(item_id, list_id, item_name, quantity):
    db = get_db()
    db.execute('INSERT INTO ListItem (ItemId, ListId, Name, Quantity, BoughtQuantity) VALUES (?,?,?,?,?)', (item_id, list_id, item_name, quantity, 0))
    db.commit()
    print("Added {} to list {}".format(item_name, list_id))

def action_update_item(list_id, item_name, quantity):
    print("Updating {} in list {}".format(item_name, list_id))

def action_add_list(list_id):
    print("Adding list {}".format(list_id))

def action_get_list(list_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM List WHERE ListId = ?', (list_id,))
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
    return json.dumps({'data': data})

if not os.path.exists(server_db):
    init_db()


"""Worker task, using a REQ socket to do load-balancing."""
socket = zmq.Context().socket(zmq.REQ)
socket.identity = u"Worker-{}".format(server_id).encode("ascii")
socket.connect("tcp://localhost:5560")

# Tell broker we're ready for work
socket.send(b"READY")

while True:
    address, empty, request = socket.recv_multipart()
    json_str = json.loads(request)
    json_obj = json.loads(json_str)

    print("{}: {}".format(socket.identity.decode("ascii"), json_str))

    if json_obj['action'] == 'add_item':
        action_add_item(json_obj['item_id'], json_obj['list_id'], json_obj['item_name'], json_obj['quantity'])
        socket.send_multipart([address, b"", b"OK"]) 
        
    elif json_obj['action'] == 'update_item':
        action_update_item(json_obj['list_id'], json_obj['item_name'], json_obj['quantity'])
        
    elif json_obj['action'] == 'add_list':
        action_add_list(json_obj['list_id'], json_obj['name'])
        
    elif json_obj['action'] == 'get_list':
        response = action_get_list(json_obj['list_id'])
        string = str(json.loads(response))
        socket.send_multipart([address, b"", string.encode("ascii")])
    else:
        print("Invalid action")    
        socket.send_multipart([address, b"", b"OK"])   
    
    