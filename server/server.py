from __future__ import print_function
import multiprocessing
import zmq
import sys

"""Worker task, using a REQ socket to do load-balancing."""
socket = zmq.Context().socket(zmq.REQ)
socket.identity = u"Worker-{}".format(sys.argv[1]).encode("ascii")
socket.connect("ipc://backend.ipc")

# Tell broker we're ready for work
socket.send(b"READY")

while True:
    address, empty, request = socket.recv_multipart()
    print("{}: {}".format(socket.identity.decode("ascii"),
                        request.decode("ascii")))
    socket.send_multipart([address, b"", b"OK"])