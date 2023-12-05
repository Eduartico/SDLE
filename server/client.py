from __future__ import print_function
import multiprocessing
import zmq
import sys

client_number = int(sys.argv[1])

socket = zmq.Context().socket(zmq.REQ)
socket.identity = u"Client-{}".format(client_number).encode("ascii")
socket.connect("ipc://frontend.ipc")

# Send request, get reply
socket.send(b"HI")
reply = socket.recv()
print("{}: {}".format(socket.identity.decode("ascii"),
                        reply.decode("ascii")))