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
    # Error handling
    if payload is None or ('nume' not in payload or 'lat' not in payload or 'lon' not in payload):
        return jsonify({"error": "Incorrect payload!"}), 400
    
    if payload['lat'] is not None and not isinstance(payload['lat'], (int, float)):
        return jsonify({"error": "Lat should be numeric!"}), 400
    
    if payload['lon'] is not None and not isinstance(payload['lon'], (int, float)):
        return jsonify({"error": "Lon should be numeric!"}), 400
    
    if payload['nume'] is not None and not isinstance(payload['nume'], str):
        return jsonify({"error": "Nume should be string!"}), 400
    
    for key in payload:
        if key not in ['nume', 'lat', 'lon']:
            return jsonify({"error": "Incorrect payload!"}), 400
    
    
    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    # daca a mai fost adaugata o tara cu acelasi nume
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
        # se converteste din ObjectId in string id-ul pentru a putea fi serializat
        x["id"] = str(x.pop("_id"))
        countries.append(x)
    
    return jsonify(countries), 200


@app.route("/api/countries/<string:id>", methods=['PUT'])
def update_countries(id):
    # Error handling
    payload = request.get_json(silent=True)
    if id is None or payload is None or 'id' not in payload or 'nume' not in payload \
        or 'lat' not in payload or 'lon' not in payload:
        return jsonify({"error": "Incorrect id or payload!"}), 400
    
    if payload['lat'] is not None and not isinstance(payload['lat'], (int, float)):
        return jsonify({"error": "Lat should be numeric!"}), 400
    
    if payload['lon'] is not None and not isinstance(payload['lon'], (int, float)):
        return jsonify({"error": "Lon should be numeric!"}), 400
    
    if payload['nume'] is not None and not isinstance(payload['nume'], str):
        return jsonify({"error": "Nume should be string!"}), 400
    
    if payload['id'] is not None and not isinstance(payload['id'], str):
        return jsonify({"error": "Id should be string!"}), 400
    
    for key in payload:
        if key not in ['id', 'nume', 'lat', 'lon']:
            return jsonify({"error": "Incorrect payload!"}), 400

    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    # Error handling
    if len(str(payload["id"]))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if len(str(id))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        return jsonify({"error": "Country id not found!"}), 404
    if mycol.find_one({"nume": payload['nume']}):
        return jsonify({"error": "Country name already exists!"}), 409
    
    # se va cauta dupa query pentru a se inlocui cu new
    query = { "_id": ObjectId(id) }
    payload["_id"] = ObjectId(payload.pop("id")) 
    # se seteaza valorile noi care vor inlocui valorile vechi
    new = { "$set": payload }
    
    mycol.update_one(query, new)
    
    return jsonify({"Successfully updated country with id": id}), 200


@app.route("/api/countries/<string:id>", methods=['DELETE'])
def delete_country(id):
    # Error handling
    if id is None:
        return jsonify({"error": "Incorrect id!"}), 404
    
    if len(str(id))!=24:
        return jsonify({"error": "Incorrect id!"}), 404

    mydb = getDB()["tema2"]
    mycol = mydb["country"]
    
    # Error handling
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        return jsonify({"error": "Country id not found!"}), 404
    
    query = { "_id": ObjectId(id) }
    mycol.delete_one(query)
    
    return jsonify({"Successfully deleted country with id": id}), 200


# CITIES

@app.route("/api/cities", methods=['POST'])
def add_city():
    payload = request.get_json(silent=True)
    # Error handling
    if payload is None or ('idTara' not in payload or 'nume' not in payload or \
        'lat' not in payload or 'lon' not in payload):
        return jsonify({"error": "Incorrect payload!"}), 400
    
    if payload['lat'] is not None and not isinstance(payload['lat'], (int, float)):
        return jsonify({"error": "Lat should be numeric!"}), 400
    
    if payload['lon'] is not None and not isinstance(payload['lon'], (int, float)):
        return jsonify({"error": "Lon should be numeric!"}), 400
    
    if payload['nume'] is not None and not isinstance(payload['nume'], str):
        return jsonify({"error": "Nume should be string!"}), 400
    
    if payload['idTara'] is not None and not isinstance(payload['idTara'], str):
        return jsonify({"error": "IdTara should be string!"}), 400
    
    for key in payload:
        if key not in ['idTara', 'nume', 'lat', 'lon']:
            return jsonify({"error": "Incorrect payload!"}), 400
    
    
    mydb = getDB()["tema2"]
    mycol = mydb["city"]
    
    mycountrycol = mydb["country"]
    
    # Error handling
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
    
    # Error handling
    if len(str(id_Tara))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    
    if mydb["country"].find_one({"_id": ObjectId(id_Tara)}) is None:
        return jsonify({"error": "Country id not found!"}), 404
    
    cities = []

    for x in mycol.find({"idTara": id_Tara}):
        x["id"] = str(x.pop("_id"))
        cities.append(x)
    
    return jsonify(cities), 200


@app.route("/api/cities/<string:id>", methods=['PUT'])
def update_cities(id):
    payload = request.get_json(silent=True)
    # Error handling
    if id is None or payload is None or 'id' not in payload or 'idTara' not in payload \
        or 'nume' not in payload or 'lat' not in payload or 'lon' not in payload:
        return jsonify({"error": "Incorrect id or payload!"}), 400
    
    if payload['lat'] is not None and not isinstance(payload['lat'], (int, float)):
        return jsonify({"error": "Lat should be numeric!"}), 400
    
    if payload['lon'] is not None and not isinstance(payload['lon'], (int, float)):
        return jsonify({"error": "Lon should be numeric!"}), 400
    
    if payload['nume'] is not None and not isinstance(payload['nume'], str):
        return jsonify({"error": "Nume should be string!"}), 400
    
    if payload['idTara'] is not None and not isinstance(payload['idTara'], str):
        return jsonify({"error": "IdTara should be string!"}), 400
    
    if payload['id'] is not None and not isinstance(payload['id'], str):
        return jsonify({"error": "Id should be string!"}), 400
    
    if len(str(id))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    
    for key in payload:
        if key not in ['id', 'idTara', 'nume', 'lat', 'lon']:
            return jsonify({"error": "Incorrect payload!"}), 400


    mydb = getDB()["tema2"]
    mycol = mydb["city"]
    
    # Error handling
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        return jsonify({"error": "City id not found!"}), 404
    
    if len(str(payload["id"]))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if mydb["country"].find_one({"_id": ObjectId(payload["idTara"])}) is None:
        return jsonify({"error": "Country id doesn't exist!"}), 404
    
    query = { "_id": ObjectId(id) }
    payload["_id"] = ObjectId(payload.pop("id"))
    new = { "$set": payload }
    
    if mycol.find_one({"nume": payload["nume"], "idTara": payload["idTara"]}):
        return jsonify({"error": "Pair (city name, country id) already exists!"}), 409
    
    mycol.update_one(query, new)
    
    return jsonify({"Successfully updated city with id": id}), 200


@app.route("/api/cities/<string:id>", methods=['DELETE'])
def delete_city(id):
    # Error handling
    if id is None:
        return jsonify({"error": "Incorrect id!"}), 404

    if len(str(id))!=24:
        return jsonify({"error": "Incorrect id!"}), 404
    
    mydb = getDB()["tema2"]
    mycol = mydb["city"]
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        return jsonify({"error": "City id not found!"}), 404
    
    query = { "_id": ObjectId(id) }
    mycol.delete_one(query)
    
    return jsonify({"Successfully deleted city with id": id}), 200


# TEMPERATURES

@app.route("/api/temperatures", methods=['POST'])
def add_temperature():
    # Error handling
    payload = request.get_json(silent=True)
    if payload is None or ('idOras' not in payload or 'valoare' not in payload):
        return jsonify({"error": "Incorrect payload!"}), 400
    
    for key in payload:
        if key not in ['idOras', 'valoare']:
            return jsonify({"error": "Incorrect payload!"}), 400
        
    if not isinstance(payload['valoare'], (int, float)):
        return jsonify({"error": "Valoare should be numeric!"}), 400
    
    if not isinstance(payload['idOras'], str):
        return jsonify({"error": "IdOras should be string!"}), 400
    
    mydb = getDB()["tema2"]
    mycol = mydb["temperatures"]
    
    mycitycol = mydb["city"]
    
    # Error handling
    if len(str(payload["idOras"]))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if mycitycol.find_one({"_id": ObjectId(payload["idOras"])}) is None:
        return jsonify({"error": "City id does not exist!"}), 404
    
    payload['timestamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    if mycol.find_one({"idOras": payload["idOras"], "timestamp": payload["timestamp"]}):
        return jsonify({"error": "Pair (city name, country id) already exists!"}), 409

    result = mycol.insert_one(payload)

    response_data = {"id": str(result.inserted_id)}
    
    return jsonify(response_data), 201


@app.route("/api/temperatures", methods=['GET'])
def get_temperatures_by_location_or_timestamp():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_from = request.args.get('from', type=str)
    date_until = request.args.get('until', type=str)
    
    # Error handling
    if lat is not None and not isinstance(lat, (int, float)):
        return jsonify({"error": "Lat should be numeric!"}), 400
    
    if lon is not None and not isinstance(lon, (int, float)):
        return jsonify({"error": "Lon should be numeric!"}), 400
    
    if date_from is not None and not isinstance(date_from, str):
        return jsonify({"error": "Until should be string!"}), 400
    
    if date_until is not None and not isinstance(date_until, str):
        return jsonify({"error": "From should be string!"}), 400
    
    mydb = getDB()["tema2"]
    mycol = mydb["temperatures"]
    mycitycol = mydb["city"]
    
    temperatures = []
    query1 = {}
    query2 = {}
    
    cities = []
    
    if lat is not None:
        query2['lat']=lat
    if lon is not None:
        query2['lon']=lon
    
    # se extrag orasele care au lat si/sau lon corespunzatoare celor date ca parametru
    if not lat is None or not lon is None:
        for x in mycitycol.find(query2):
            x["id"] = str(x.pop("_id"))
            cities.append(x["id"])
        # se pregateste urmatorul query, care trebui sa contina id-ul oraselor gasite
        query1['idOras']={'$in': cities}
    
    # daca nu a fost dat niciun parametru, se intorc toate temperaturile
    if lat is None and lon is None and date_from is None and date_until is None:
        for x in mycol.find():
            x["id"] = str(x.pop("_id"))
            x.pop("idOras")
            temperatures.append(x)
        
        return jsonify(temperatures), 200
    
    # se seteaza query-ul in functie de parametri from (gte) si until (lte)
    if date_from is not None and date_until is not None:
        query1['timestamp'] = {'$gte': date_from, '$lte': date_until}
    elif date_from is not None and date_until is None:
        query1['timestamp'] = {'$gte': date_from}
    elif date_from is None and date_until is not None:
        query1['timestamp'] = {'$lte': date_until}

    # se extrag rezultatele care sa faca match pe tot query-ul
    for x in mycol.find(query1):
        x["id"] = str(x.pop("_id"))
        x.pop("idOras")
        temperatures.append(x)
    
    return jsonify(temperatures), 200


@app.route("/api/temperatures/cities/<string:id_oras>", methods=['GET'])
def get_temperatures_by_city(id_oras):
    date_from = request.args.get('from', type=str)
    date_until = request.args.get('until', type=str)
    
    # Error handling
    if date_from is not None and not isinstance(date_from, str):
        return jsonify({"error": "From should be string!"}), 400
    
    if date_until is not None and not isinstance(date_until, str):
        return jsonify({"error": "Until should be string!"}), 400
    
    mydb = getDB()["tema2"]
    mycol = mydb["temperatures"]
    
    if len(str(id_oras))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if mydb["city"].find_one({"_id": ObjectId(id_oras)}) is None:
        return jsonify({"error": "City id does not exist!"}), 404
    
    temperatures = []
    query = {}
    
    # se seteaza query-ul in functie de parametri primiti
    query['idOras']=id_oras
    if date_from is not None or date_until is not None:
        if date_from is not None and date_until is not None:
            query['timestamp'] = {'$gte': date_from, '$lte': date_until}
        elif date_from is not None and date_until is None:
            query['timestamp'] = {'$gte': date_from}
        elif date_from is None and date_until is not None:
            query['timestamp'] = {'$lte': date_until}

    for x in mycol.find(query):
        x["id"] = str(x.pop("_id"))
        x.pop("idOras")
        temperatures.append(x)
    
    return jsonify(temperatures), 200


@app.route("/api/temperatures/countries/<string:id_tara>", methods=['GET'])
def get_temperatures_by_country(id_tara):
    date_from = request.args.get('from', type=str)
    date_until = request.args.get('until', type=str)
    
    # Error handling
    if date_from is not None and not isinstance(date_from, str):
        return jsonify({"error": "From should be string!"}), 400
    
    if date_until is not None and not isinstance(date_until, str):
        return jsonify({"error": "Until should be string!"}), 400
    
    mydb = getDB()["tema2"]
    mycol = mydb["temperatures"]
    mycitycol = mydb["city"]
    
    if len(str(id_tara))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if mydb["country"].find_one({"_id": ObjectId(id_tara)}) is None:
        return jsonify({"error": "Country id does not exist!"}), 404
    
    cities = []
    query = {}
    
    # se extrag orasele corespunzatoare id-ului de tara
    for x in mycitycol.find({"idTara": id_tara}):
        x["id"] = str(x.pop("_id"))
        cities.append(x["id"])
    
    query['idOras']={'$in': cities}
    
    # se seteaza query-ul in functie de parametri primiti
    if date_from is None or date_until is not None:
        if date_from is not None and date_until is not None:
            query['timestamp'] = {'$gte': date_from, '$lte': date_until}
        elif date_from is not None and date_until is None:
            query['timestamp'] = {'$gte': date_from}
        elif date_from is None and date_until is not None:
            query['timestamp'] = {'$lte': date_until}

    # se returneaza temperaturile care respecta query-ul
    temperatures = []
    for x in mycol.find(query):
        x["id"] = str(x.pop("_id"))
        x.pop("idOras")
        temperatures.append(x)
    
    return jsonify(temperatures), 200


@app.route("/api/temperatures/<string:id>", methods=['PUT'])
def update_temperature(id):
    payload = request.get_json(silent=True)
    # Error handling
    if id is None or payload is None or 'id' not in payload or 'idOras' not in payload \
        or 'valoare' not in payload:
        return jsonify({"error": "Incorrect id or payload!"}), 400
    
    for key in payload:
        if key not in ['id', 'idOras', 'valoare']:
            return jsonify({"error": "Incorrect payload!"}), 400
    
    if payload['valoare'] is not None and not isinstance(payload['valoare'], (int, float)):
        return jsonify({"error": "Valoare should be numeric!"}), 400
    
    if payload['idOras'] is not None and not isinstance(payload['idOras'], str):
        return jsonify({"error": "IdOras should be string!"}), 400
    
    if payload['id'] is not None and not isinstance(payload['id'], str):
        return jsonify({"error": "Id should be string!"}), 400

    if len(str(id))!=24:
        return jsonify({"error": "Incorrect id!"}), 400
    if len(str(payload["id"]))!=24:
        return jsonify({"error": "Incorrect id!"}), 400

    mydb = getDB()["tema2"]
    mycol = mydb["temperatures"]
    
    # Error handling
    if mydb["city"].find_one({"_id": ObjectId(payload["idOras"])}) is None:
        return jsonify({"error": "City id doesn't exist!"}), 404
    
    if mydb["temperatures"].find_one({"_id": ObjectId(payload["id"])}) is None:
        return jsonify({"error": "Temperature id doesn't exist!"}), 404
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        return jsonify({"error": "Temperature id not found!"}), 404
    
    # se seteaza query-ul cu id-ul dupa care sa cauta temperatura 
    query = { "_id": ObjectId(id) }
    payload["_id"] = ObjectId(payload.pop("id"))
    # se pune timestamp-ul curent in format an luna zi ora minut secunda.milisecunda
    payload['timestamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    new = { "$set": payload }
    
    if mycol.find_one({"idOras": payload["idOras"], "timestamp": payload["timestamp"]}):
        return jsonify({"error": "Pair (idOras, timestamp) already exists!"}), 409
    
    mycol.update_one(query, new)
    
    return jsonify({"Successfully updated temperature with id": id}), 200


@app.route("/api/temperatures/<string:id>", methods=['DELETE'])
def delete_temperature(id):
    # Error handling
    if id is None:
        return jsonify({"error": "Incorrect id!"}), 404
    
    if len(str(id))!=24:
        return jsonify({"error": "Incorrect id!"}), 404

    mydb = getDB()["tema2"]
    mycol = mydb["temperatures"]
    
    if mycol.find_one({"_id": ObjectId(id)}) is None:
        return jsonify({"error": "Temperature id not found!"}), 404
    
    query = { "_id": ObjectId(id) }
    mycol.delete_one(query)
    
    return jsonify({"Successfully deleted temperature with id": id}), 200