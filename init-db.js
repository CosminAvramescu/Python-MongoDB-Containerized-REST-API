db = db.getSiblingDB("tema2");
// db.country.drop();

db.country.insertMany([
    {
        "nume": "Romania",
        "lat": 30.50,
        "lon": 40.20
    },
    {
        "nume": "UK",
        "lat": 20.10,
        "lon": 40.20
    },
    {
        "nume": "France",
        "lat": 30.50,
        "lon": 30.50
    },
    {
        "nume": "Germany",
        "lat": 30.50,
        "lon": 50.20
    },
    {
        "nume": "Italy",
        "lat": 20.10,
        "lon": 50.20
    }
]);

db.country.createIndex({ nume: 1 }, { unique: true });

var countryId1 = db.country.findOne({ "nume": "Romania" })._id;
var countryId2 = db.country.findOne({ "nume": "UK" })._id;
var countryId3 = db.country.findOne({ "nume": "France" })._id;

db.city.insertMany([
    {
        "idTara": countryId,
        "nume": "Bucharest",
        "lat": 37.555,
        "lon": 49.5
    },
    {
        "idTara": countryId,
        "nume": "Craiova",
        "lat": 37.555,
        "lon": 49.777
    },
    {
        "idTara": countryId3,
        "nume": "Paris",
        "lat": 37.655,
        "lon": 49.877
    },
    {
        "idTara": countryId2,
        "nume": "Londra",
        "lat": 38,
        "lon": 50
    }
]);

db.city.createIndex({ idTara: 1, nume: 1 }, { unique: true });

// var citiesIds = db.city.find({}).map(function (city) { return city._id; });
var cityId1 = db.city.findOne({ "nume": "Craiova" })._id;
var cityId2 = db.city.findOne({ "nume": "Londra" })._id;
var cityId3 = db.city.findOne({ "nume": "Paris" })._id;

db.temperatures.insertMany([
    {
        "idOras": cityId1,
        "valoare": 32.5
    },
    {
        "idOras": cityId1,
        "valoare": 28.5
    },
    {
        "idOras": cityId1,
        "valoare": 26.12
    },
    {
        "idOras": cityId1,
        "valoare": 32.5
    },
    {
        "idOras": cityId1,
        "valoare": 28.5
    },
    {
        "idOras": cityId1,
        "valoare": 26.12
    },
    {
        "idOras": cityId3,
        "valoare": 32.5
    },
    {
        "idOras": cityId3,
        "valoare": 28.5
    },
    {
        "idOras": cityId3,
        "valoare": 26.12
    }
]);
