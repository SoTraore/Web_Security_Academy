from flask import Flask, jsonify

app = Flask(__name__)

# Mock data for the first API
data_from_api1 = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Smith"},
]

@app.route("/api1", methods=["GET"])
def get_data_from_api1():
    return jsonify(data_from_api1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
