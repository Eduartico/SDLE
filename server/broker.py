from __future__ import print_function
import multiprocessing
import zmq

def main():
    
    # Prepare context and sockets
    context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("ipc://frontend.ipc")
    backend = context.socket(zmq.ROUTER)
    backend.bind("ipc://backend.ipc")

    backend_ready = False
    workers = []
    poller = zmq.Poller()
    # Only poll for requests from backend until workers are available
    poller.register(backend, zmq.POLLIN)

    while True:
        sockets = dict(poller.poll())

        if backend in sockets:
            # Handle worker activity on the backend
            request = backend.recv_multipart()
            worker, empty, client = request[:3]
            workers.append(worker)
            if workers and not backend_ready:
                # Poll for clients now that a worker is available and backend was not ready
                poller.register(frontend, zmq.POLLIN)
                backend_ready = True
            if client != b"READY" and len(request) > 3:
                # If client reply, send rest back to frontend
                empty, reply = request[3:]
                frontend.send_multipart([client, b"", reply])

        if frontend in sockets:
            # Get next client request, route to last-used worker
            client, empty, request = frontend.recv_multipart()
            worker = workers.pop(0)
            backend.send_multipart([worker, b"", client, b"", request])
            if not workers:
                # Don't poll clients if no workers are available and set backend_ready flag to false
                poller.unregister(frontend)
                backend_ready = False

    # Clean up never reached
    backend.close()
    frontend.close()
    context.term()


if __name__ == "__main__":
    main()