from __future__ import print_function
from multiprocessing import Process, Manager
from hashing_ring import HashingRing
import signal
import sys
from time import sleep

ring = HashingRing()

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    zmq_service.terminate()
    flask_app.terminate()
    sys.exit(0)

def start_flask_app(servers):
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route('/add_server', methods=['POST'])
    def add_server():
        data = request.get_json()
        server = data['server']
        ring.add_node(server)
        return jsonify({"status": "OK"})

    @app.route('/remove_server', methods=['POST'])
    def remove_server():
        data = request.get_json()
        server = data['server']
        ring.remove_node(server)
        return jsonify({"status": "OK"})

    @app.route('/connect', methods=['GET'])
    def connect():
        servers.append(b"server from flask")
        print(servers)
        return jsonify({"socket": "tcp://locahost:5559"})

    app.run(debug=True, port=4000, threaded=True)

def start_zmq_service(servers):
    import zmq
    
    # Prepare context and sockets
    context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5559")
    backend = context.socket(zmq.ROUTER)
    backend.bind("tcp://*:5560")

    backend_ready = False
    # servers = []
    poller = zmq.Poller()
    # Only poll for requests from backend until servers are available
    poller.register(backend, zmq.POLLIN)

    while True:
        print(servers)
        sockets = dict(poller.poll())

        if backend in sockets:
            # Handle server activity on the backend
            request = backend.recv_multipart()
            server, empty, client = request[:3]
            print("BACKEND")
            print("server: ", server)
            print("client: ", client)
            servers.append(server)
            if servers and not backend_ready:
                # Poll for clients now that a server is available and backend was not ready
                poller.register(frontend, zmq.POLLIN)
                backend_ready = True
            if client != b"READY" and len(request) > 3:
                # If client reply, send rest back to frontend
                empty, reply = request[3:]
                frontend.send_multipart([client, b"", reply])

        if frontend in sockets:
            # Get next client request, route to last-used server
            client, empty, request = frontend.recv_multipart()
            print("FRONTEND")
            print("client: ", client.decode("ascii"))
            print("request: ", request)
            server = servers.pop(0)
            backend.send_multipart([server, b"", client, b"", request])
            if not servers:
                # Don't poll clients if no servers are available and set backend_ready flag to false
                poller.unregister(frontend)
                backend_ready = False

    # Clean up never reached
    backend.close()
    frontend.close()
    context.term()

if __name__ == "__main__":

    # Start background service
    with Manager() as manager:
        # Register the signal handler
        signal.signal(signal.SIGINT, signal_handler)

        servers = manager.list()

        # Start ZMQ service in a separate process
        zmq_service = Process(target=start_zmq_service, args=(servers,))
        zmq_service.start()
        print("Started ZMQ service with PID={}".format(zmq_service.pid))

        # Start Flask app in a separate process
        flask_app = Process(target=start_flask_app, args=(servers,))
        flask_app.start()
        print("Started Flask app with PID={}".format(flask_app.pid))
        
        # Wait for both processes to finish
        zmq_service.join()
        flask_app.join()



    
