from flask import Flask, request, jsonify
from hashing_ring import HashingRing
import requests

ring = HashingRing()

app = Flask(__name__)

@app.route('/add_server', methods=['POST'])
def add_server():
    data = request.get_json()
    server = data['server_port']
    ring.add_node(server)
    print(f"Added server: {server}")
    print(f"ring: {ring.ring}")
    return jsonify({"status": "OK"})

@app.route('/remove_server', methods=['POST'])
def remove_server():
    data = request.get_json()
    server = data['server_port']
    ring.remove_node(server)
    return jsonify({"status": "OK"})

@app.route('/create_list', methods=['POST'])
def create_list():
    data = request.get_json()
    list_id = data['list_id']
    server = ring.get_node(list_id)
    print(f"redirect to server: {server}")
    response = requests.post(f"http://localhost:{server}/create_list", json=data)
    print(response)
    return 200


@app.route('/update_list', methods=['POST'])
def update_list():
    data = request.get_json()
    list_id = data['list_id']
    server = ring.get_node(list_id)
    print(f"with list id {list_id} redirect to server: {server} ")
    response = requests.post(f"http://localhost:{server}/update_list", json=data)
    print(response)
    return 200

@app.route('/get_list/<int:list_id>', methods=['GET'])
def get_list(list_id):
    server = ring.get_node(list_id)
    print(f"redirect to server: {server}")
    response = requests.get(f"http://localhost:{server}/get_list/{list_id}")
    print(response)
    return 200

@app.route('/get_lists', methods=['GET'])
def get_lists():
    server = ring.get_node("random")
    response = requests.get(f"http://localhost:{server}/get_lists")
    print(response)
    return 200

if __name__ == "__main__":
    app.run(debug=True, port=4000, threaded=True)




    
