from __future__ import print_function
import multiprocessing
import os, sys, zmq, json, sqlite3
from queue import Queue
from threading import Thread

try :
    server_id = int(sys.argv[1])
except:
    server_id = 0

PORT = 5100  + server_id # Set port here
server_db = f'server_{server_id}.db'

#pub_socket = zmq.Context().socket(zmq.PUB)
#pub_socket.bind("tcp://*:{}".format(PORT + 1))  # Usando uma porta diferente para o PUB

request_queue = Queue() # Create a queue to store pending client requests

def init_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    db = sqlite3.connect(server_db)
    db.row_factory = sqlite3.Row
    return db

def process_pending_requests():
    """Thread function to process pending requests."""
    while True:
        request = request_queue.get()
        if request:
            process_request(request)

def process_request(request):
    """Process a single request."""
    address, empty, json_str = request
    json_obj = json.loads(json_str)

    if json_obj['action'] == 'add_item':
        action_add_item(json_obj['item_id'], json_obj['list_id'], json_obj['item_name'], json_obj['quantity'])
        pub_socket.send_string(json_str)  # Publish the request
        socket.send_multipart([address, b"", b"OK"])

# Start the thread to process pending requests
processing_thread = Thread(target=process_pending_requests)
processing_thread.start()

def action_add_item(item_id, list_id, item_name, quantity):
    db = get_db()
    db.execute('INSERT INTO ListItem (ItemId, ListId, Name, Quantity, BoughtQuantity) VALUES (?,?,?,?,?)', (item_id, list_id, item_name, quantity, 0))
    db.commit()
    print("Added {} to list {}".format(item_name, list_id))

    # Publicar json
    #message = json.dumps({
       # 'action': 'add_item',
       # 'item_id': item_id,
       # 'list_id': list_id,
        #'item_name': item_name,
       # 'quantity': quantity
    #})
    #pub_socket.send_string(message)

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

def action_get_lists(user_id):
    try:
        db = get_db()
        cursor = db.execute('''
                            SELECT * FROM List WHERE ListId IN (
                                SELECT ListId FROM ListUser WHERE UserId = ?
                            )''', (user_id,))
    except:
        print("Error getting lists")
        return json.dumps({"data": None})
    try:
        lists = cursor.fetchall()
        data = {}
        for l in lists:
            cursor = db.execute('SELECT * FROM ListItem WHERE ListId = ?', (l['ListId'],))
            items = cursor.fetchall()
            data[l['ListId']] = {
                'id': l['ListId'],
                'name': l['Name'],
                'isRecipe': l['IsRecipe'],
                'items' : [{
                    'id': d['ItemId'],
                    'name': d['Name'],
                    'quantity': d['Quantity'],
                    'boughtQuantity': d['BoughtQuantity']
                    } for d in items]
            }
    except:
        print("Error getting lists")
        return json.dumps({"data": None})
    return json.dumps({"data": data})

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
        socket.send_multipart([address, b"", b"Added item"]) 
        
    elif json_obj['action'] == 'update_item':
        action_update_item(json_obj['item_id'], json_obj['boughtQuantity'])
        socket.send_multipart([address, b"", b"OK"]) 
        
    elif json_obj['action'] == 'add_list':
        action_add_list(json_obj['list_id'], json_obj['list_name'], json_obj['is_recipe'], json_obj['user_id'])
        socket.send_multipart([address, b"", b"Added list"]) 
        
    elif json_obj['action'] == 'get_list':
        response = action_get_list(json_obj['list_id'])
        string = json.dumps(json.loads(response))
        socket.send_multipart([address, b"", string.encode("ascii")])

    elif json_obj['action'] == 'get_lists':
        response = action_get_lists(json_obj['user_id'])
        string = json.dumps(json.loads(response))
        socket.send_multipart([address, b"", string.encode("ascii")])

    else:
        print("Invalid action")    
        socket.send_multipart([address, b"", b"OK"])   

    try:
        #message = socket.recv_string(zmq.DONTWAIT) # Lógica para lidar com mensagens do publish
        #print("Received PUB message:", message)

        # queue request logic
        address, empty, request = socket.recv_multipart(zmq.DONTWAIT)
        request_queue.put((address, empty, request))
    except zmq.Again:
        pass

        socket.send_multipart([address, b"", b"Invalid action"])   
    
    