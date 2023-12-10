from flask import Flask, request, jsonify, Response
app = Flask(__name__)
import pymongo
from bson import json_util, ObjectId

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
        return Response(status=400)
    
    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    if mycol.find_one({"nume": payload['nume']}):
        return Response(status=409)

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
        return Response(status=400)

    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        # Error handling
        return Response(status=404)
    
    query = { "_id": ObjectId(id) }
    payload["_id"] = ObjectId(payload.pop("id"))
    new = { "$set": payload }
    
    mycol.update_one(query, new)
    
    return jsonify({"id": id}), 200

@app.route("/api/countries/<string:id>", methods=['DELETE'])
def delete_country(id):
    if id is None:
        # Error handling
        return Response(status=400)

    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        # Error handling
        return Response(status=404)
    
    query = { "_id": ObjectId(id) }
    mycol.delete_one(query)
    
    return jsonify({"id": id}), 200

# # CITIES

# @app.route("/api/cities", methods=['POST'])
# def add_city():
#     payload = request.get_json(silent=True)
#     if not payload or payload['name'] is None:
#         # Error handling
#         return Response(status=400)

#     print(payload)
#     city_id = 0
    
#     resp = Response(
#         response=json.dumps(city_id), status=201,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/api/cities", methods=['GET'])
# def get_cities():
#     cities = []
    
#     resp = Response(
#         response=json.dumps(cities), status=200,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/api/cities/country/<int:id_Tara>", methods=['GET'])
# def get_cities_by_country_id(id_Tara):
#     cities = []
    
#     resp = Response(
#         response=json.dumps(cities), status=200,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/api/cities/<int:id>", methods=['PUT'])
# def update_cities(id):
#     payload = request.get_json(silent=True)
#     if not payload or (payload['id'] is None or payload['idTara'] is None \
#         or payload['lat'] is None or payload['lon']is None):
#         # Error handling
#         return Response(status=400)

#     print(payload)
    
#     country = 0
#     resp = Response(
#         response=json.dumps(country), status=200,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/api/cities/<int:id>", methods=['DELETE'])
# def delete_city(id):
#     if False:
#         # Error handling
#         return Response(status=400)

#     country = 0
#     resp = Response(
#         response=json.dumps(country), status=200,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# # TEMPERATURES

# @app.route("/api/temperatures", methods=['POST'])
# def add_temperature():
#     payload = request.get_json(silent=True)
#     if not payload or payload['id_oras'] is None:
#         # Error handling
#         return Response(status=400)

#     print(payload)
#     temperature_id = 0
    
#     resp = Response(
#         response=json.dumps(temperature_id), status=201,  mimetype="text/plain")
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

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
