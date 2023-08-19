from flask import Flask, request, jsonify
import requests
import traceback
import json

app = Flask(__name__)

# Mock data for the first API
data_from_api1 = [
    {"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Smith"},
]

# Mock data for the second API
data_from_api2 = [
    {"id": 1, "age": 30},
    {"id": 2, "age": 25},
]

@app.route("/api1", methods=["GET"])
def get_data_from_api1():
    return jsonify(data_from_api1)

@app.route("/api2", methods=["GET"])
def get_data_from_api2():
    return jsonify(data_from_api2)

@app.route("/gateway", methods=["GET"])
def gateway():
    try:
        # Make a request to the first API
        response_api1 = requests.get("http://localhost:5000/api1")
        response_api1.raise_for_status()
        data_api1 = response_api1.json()
        print(data_api1)
        # Process the data from the first API
        processed_data = []
        for item in data_api1:
            processed_data.append({
                "name": item.get('name'),
                "age": get_age_from_api2(item['id']),
            })

        return jsonify(processed_data)

    except Exception as e:
        traceback.print_exc()
        return "Internal Server Error", 500
    
def get_age_from_api2(id):
    try:
        # Make a request to the second API with the given ID
        response_api2 = requests.get(f"http://localhost:5001/api2?id={id}")
        response_api2.raise_for_status()  # Check for HTTP errors
        data_api2 = response_api2.json()
        if not data_api2:
            print("No data found for ID:", id)
            return None
        print("Here is the value ",data_api2)
        return data_api2.get("age")
    except requests.exceptions.RequestException as e:
        print("Error accessing /api2:", str(e))
        return None
    except json.JSONDecodeError as e:
        print("Error decoding JSON from /api2:", str(e))
        return None
    except KeyError :
        print(KeyError)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
