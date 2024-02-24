db = db.getSiblingDB("tema2");

db.country.createIndex({ nume: 1 }, { unique: true });
db.city.createIndex({ idTara: 1, nume: 1 }, { unique: true });
db.temperatures.createIndex({ idOras: 1, timestamp: 1 }, { unique: true });