from flask import Flask, request, jsonify, Response
app = Flask(__name__)
import pymongo
from bson import json_util, ObjectId
from datetime import datetime

def getDB():
    myclient = pymongo.MongoClient(host='test_mongodb',
                                   port=27017, 
                                   username='admin', 
                                   password='pass',
                                   authSource='admin')
    return myclient

# COUNTRIES 
@app.route("/api/countries", methods=['POST'])
def add_country():
    payload = request.get_json(silent=True)
    if payload is None or ('nume' not in payload or 'lat' not in payload or 'lon' not in payload):
        # Error handling
        return jsonify({"error": "Incorrect payload!"}), 400
    
    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    if mycol.find_one({"nume": payload['nume']}):
        return jsonify({"error": "Country name already exists!"}), 409

    result = mycol.insert_one(payload)

    response_data = {"id": str(result.inserted_id)}
    
    return jsonify(response_data), 201

@app.route("/api/countries", methods=['GET'])
def get_countries():
    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    countries = []

    for x in mycol.find():
        x["id"] = str(x.pop("_id"))
        countries.append(x)
    
    return jsonify(countries), 200

@app.route("/api/countries/<string:id>", methods=['PUT'])
def update_countries(id):
    payload = request.get_json(silent=True)
    if id is None or payload is None or 'id' not in payload or 'nume' not in payload \
        or 'lat' not in payload or 'lon' not in payload:
        # Error handling
        return jsonify({"error": "Incorrect id or payload!"}), 400

    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        # Error handling
        return jsonify({"error": "Country id not found!"}), 404
    
    query = { "_id": ObjectId(id) }
    payload["_id"] = ObjectId(payload.pop("id"))
    new = { "$set": payload }
    
    mycol.update_one(query, new)
    
    return jsonify({"Successfully updated country with id": id}), 200

@app.route("/api/countries/<string:id>", methods=['DELETE'])
def delete_country(id):
    if id is None:
        # Error handling
        return jsonify({"error": "Incorrect id!"}), 400

    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        # Error handling
        return jsonify({"error": "Country id not found!"}), 404
    
    query = { "_id": ObjectId(id) }
    mycol.delete_one(query)
    
    return jsonify({"Successfully deleted country with id": id}), 200


# CITIES

@app.route("/api/cities", methods=['POST'])
def add_city():
    payload = request.get_json(silent=True)
    if payload is None or ('idTara' not in payload or 'nume' not in payload or \
        'lat' not in payload or 'lon' not in payload):
        # Error handling
        return jsonify({"error": "Incorrect payload!"}), 400
    
    mydb = getDB()["tema2"]
    mycol = mydb["city"]
    
    mycountrycol = mydb["country"]
    
    if len(str(payload["idTara"]))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if mycountrycol.find_one({"_id": ObjectId(payload["idTara"])}) is None:
        return jsonify({"error": "Country id does not exist!"}), 404
    
    if mycol.find_one({"nume": payload["nume"], "idTara": payload["idTara"]}):
        return jsonify({"error": "Pair (city name, country id) already exists!"}), 409

    result = mycol.insert_one(payload)

    response_data = {"id": str(result.inserted_id)}
    
    return jsonify(response_data), 201

@app.route("/api/cities", methods=['GET'])
def get_cities():
    mydb = getDB()["tema2"]
    mycol = mydb["city"]
    
    cities = []

    for x in mycol.find():
        x["id"] = str(x.pop("_id"))
        cities.append(x)
    
    return jsonify(cities), 200

@app.route("/api/cities/country/<string:id_Tara>", methods=['GET'])
def get_cities_by_country_id(id_Tara):
    mydb = getDB()["tema2"]
    mycol = mydb["city"]
    
    cities = []

    for x in mycol.find({"idTara": id_Tara}):
        x["id"] = str(x.pop("_id"))
        cities.append(x)
    
    return jsonify(cities), 200

@app.route("/api/cities/<string:id>", methods=['PUT'])
def update_cities(id):
    payload = request.get_json(silent=True)
    if id is None or payload is None or 'id' not in payload or 'idTara' not in payload \
        or 'nume' not in payload or 'lat' not in payload or 'lon' not in payload:
        # Error handling
        return jsonify({"error": "Incorrect id or payload!"}), 400

    mydb = getDB()["tema2"]
    mycol = mydb["city"]
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        # Error handling
        return jsonify({"error": "City id not found!"}), 404
    
    query = { "_id": ObjectId(id) }
    payload["_id"] = ObjectId(payload.pop("id"))
    new = { "$set": payload }
    
    if mycol.find_one({"nume": payload["nume"], "idTara": payload["idTara"]}):
        return jsonify({"error": "Pair (city name, country id) already exists!"}), 409
    
    mycol.update_one(query, new)
    
    return jsonify({"Successfully updated city with id": id}), 200

@app.route("/api/cities/<string:id>", methods=['DELETE'])
def delete_city(id):
    if id is None:
        # Error handling
        return jsonify({"error": "Incorrect id!"}), 400

    mydb = getDB()["tema2"]
    mycol = mydb["city"]
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        # Error handling
        return jsonify({"error": "City id not found!"}), 404
    
    query = { "_id": ObjectId(id) }
    mycol.delete_one(query)
    
    return jsonify({"Successfully deleted city with id": id}), 200

# TEMPERATURES

@app.route("/api/temperatures", methods=['POST'])
def add_temperature():
    payload = request.get_json(silent=True)
    if payload is None or ('idOras' not in payload or 'valoare' not in payload):
        # Error handling
        return jsonify({"error": "Incorrect payload!"}), 400
    
    mydb = getDB()["tema2"]
    mycol = mydb["temperatures"]
    
    mycitycol = mydb["city"]
    
    if len(str(payload["idOras"]))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if mycitycol.find_one({"_id": ObjectId(payload["idOras"])}) is None:
        return jsonify({"error": "City id does not exist!"}), 404
    
    payload['timestamp']=datetime.now()
    if mycol.find_one({"idOras": payload["idOras"], "timestamp": payload["timestamp"]}):
        return jsonify({"error": "Pair (city name, country id) already exists!"}), 409

    result = mycol.insert_one(payload)

    response_data = {"id": str(result.inserted_id)}
    
    return jsonify(response_data), 201

@app.route("/api/temperatures", methods=['GET'])
def get_temperatures():
    mydb = getDB()["tema2"]
    mycol = mydb["temperatures"]
    
    cities = []

    for x in mycol.find():
        x["id"] = str(x.pop("_id"))
        cities.append(x)
    
    return jsonify(cities), 200

# @app.route("/api/temperatures?lat=<double:lat>&lon=<double:lon>&from=<double:date>&until=<Date:until>", methods=['GET'])
# def get_temperatures_by_location_or_timestamp():
#     temperatures = []
    
#     resp = Response(
#         response=json.dumps(temperatures), status=200,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/api/temperatures/cities/:id_oras?from=<Date:from>&until=<Date:until>", methods=['GET'])
# def get_temperatures_by_city(id_oras):
#     temperatures = []
    
#     resp = Response(
#         response=json.dumps(temperatures), status=200,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/api/temperatures/countries/:id_tara?from=<Date:from>&until=<Date:until>", methods=['GET'])
# def get_temperatures_by_country(id_tara):
#     temperatures = []
    
#     resp = Response(
#         response=json.dumps(temperatures), status=200,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp
