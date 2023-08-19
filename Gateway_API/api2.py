from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock data for the second API
data_from_api2 = [
    {"id": 1, "age": 30},
    {"id": 2, "age": 25},
]

@app.route("/api2", methods=["GET"])
def get_data_from_api2():
    id = request.args.get("id", type=int)
    result = next((item for item in data_from_api2 if item["id"] == id), None)
    if result:
        return jsonify(result)
    else:
        return jsonify({"message": "Data not found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
