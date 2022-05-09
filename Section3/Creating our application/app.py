from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# POST method - used to receive data
# GET method - used to send data back

stores = [
    {
        "name": "Nike",
        "items": [
            {
                "name": "Jordan",
                "price":  24.99
            }
        ]
    }
]

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items":[]}
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store_by_name(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return "Store not found"

# GET /store
@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({"stores":  stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            store["items"].append(request_data)
            return jsonify(store)
    return "Store not found"

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_item(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return "Store not found"

if __name__ == "__main__":
    app.run(debug=True)
