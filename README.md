344C3_Avramescu_Cosmin_Alexandru

---Arhitectura

    Dupa cum se vede in docker-compose.yml, am 3 microservicii (python-rest-api, baza de date MongoDB si 
utilitarul bazei de date mongo express). Mongo DB are nevoie de network pentru a comunica, de aceea am
folosit 2 networks, una intre rest api si mongo db si una intre mongo db si mongo express. Atat mongo db
cat si mongo express sunt protejate prin autentificarea cu user si parola, credentialele se gasesc in 
docker compose. De asemenea, folosesc 2 volume, unul pentru mongo db si unul pentru mongo express. La
rularea docker-compose, se initializeaza baza de date prin scriptul-ul init-db.js (se creaza cele 3
colectii - country, city si temperatures si se seteaza pentru fiecare unique constraints pe field-urile
din cerinta).

---Aspecte generale

    Avand in vedere ca MongoDB pune by default un camp "_id" de tipul ObjectID(), pe parcusul temei am
facut de mai multe ori urmatoarele operatii: reactualizare json cu "id" in loc de "_id" sau invers
si convertire din ObjectID() in string pentru a se putea serializa obiectul si pentru a se intoarce 
raspunsul. Operatiile sunt destul de simple in cod, pe langa verificarea tuturor cazurilor de eroare
la care am putut sa ma gandesc, sunt prezente operatii de insert_one() pentru adaugare, find_one() pentru
gasire element, find() pentru gasire toate elementele, update_one() pentru put si delete_one() pentru 
delete. Toate aceste metode din pymongo pot primi ca parametru query un json dupa care se vor face cautarile/inserarile. Pentru query-urile mai complicate, am folosit sintaxa "$in": cities, pentru a seta
cautarea in functie de id-urile din array-ul city construit anterior, iar pentru timestamp am folosit
"$lte" pentru a seta cautarea datei mai mici decat until si "$gte" pentru a seta cautarea datei mai mari
decat from. 