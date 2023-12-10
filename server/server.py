from __future__ import print_function
import multiprocessing
import zmq
import sys
import json

"""Worker task, using a REQ socket to do load-balancing."""
socket = zmq.Context().socket(zmq.REQ)
socket.identity = u"Worker-{}".format(sys.argv[1]).encode("ascii")
socket.connect("tcp://localhost:5560")

# Tell broker we're ready for work
socket.send(b"READY")

while True:
    address, empty, request = socket.recv_multipart()
    json_str = json.loads(request)
    json_obj = json.loads(json_str)
    
    # print(json_obj['list_id'])
    # print(json_obj['action'])
    # print(json_obj['item_name'])
    # print(json_obj['quantity'])

    print("{}: {}".format(socket.identity.decode("ascii"), json_str))
    socket.send_multipart([address, b"", b"OK"])