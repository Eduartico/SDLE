from __future__ import print_function
import multiprocessing
import zmq
import sys
import json

client_number = int(sys.argv[1])

count = 0

socket = zmq.Context().socket(zmq.REQ)
socket.identity = u"Client-{}".format(client_number).encode("ascii")
socket.connect("tcp://localhost:5559")
socket.send_json(json.dumps({
    'item_id': '5',
    'list_id': '1',
    'action': 'get_list',
    'item_name': 'dasdasda',
    'quantity': 0
}))

print("Done")
reply = socket.recv()
print("{}: {}".format(socket.identity.decode("ascii"), reply))
