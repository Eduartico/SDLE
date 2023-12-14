from flask import Flask, request, jsonify
from hashing_ring import HashingRing
import requests
from urllib.parse import urljoin

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

    url = urljoin(f"http://localhost:{server}/", "create_list")

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print(response.json())  # Assuming the response contains JSON data
        return jsonify({"status": "OK"})
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500  # Return an HTTP 500 Internal Server Error

@app.route('/update_list', methods=['POST'])
def update_list():
    data = request.get_json()
    list_id = data['list_id']
    server = ring.get_node(list_id)
    print(f"with list id {list_id} redirect to server: {server} ")

    url = urljoin(f"http://localhost:{server}/", "update_list")

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(response.json())
        return jsonify({"status": "OK"})
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/get_list/<int:list_id>', methods=['GET'])
def get_list(list_id):
    server = ring.get_node(list_id)
    print(f"redirect to server: {server}")

    url = urljoin(f"http://localhost:{server}/", f"get_list/{list_id}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        print(response.json())
        return jsonify({"status": "OK"})
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/get_lists', methods=['GET'])
def get_lists():
    server = ring.get_node("random")

    url = urljoin(f"http://localhost:{server}/", "get_lists")

    try:
        response = requests.get(url)
        response.raise_for_status()
        print(response.json())
        return jsonify({"status": "OK"})
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=4000, threaded=True)