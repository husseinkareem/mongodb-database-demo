from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Ladda miljövariabler från .env-filen
load_dotenv()

# Hämta MongoDB URI från miljövariabler
mongo_uri = os.getenv("MONGO_URI")

# Anslut till MongoDB
client = MongoClient(mongo_uri)
db = client['VG_Database']  # Skapar databasen "VG_Database"

# Skapa collection "persons"
persons = db['persons']

# Infoga testdata i "persons"
persons.insert_many([
    {"first_name": "John", "last_name": "Doe", "age": 30},
    {"first_name": "Jane", "last_name": "Smith", "age": 25},
    {"first_name": "Alice", "last_name": "Johnson", "age": 35}
])

# Skapa ett sammansatt index på "first_name" och "last_name"
persons.create_index([("first_name", 1), ("last_name", 1)])
print("Indexes on 'persons':", persons.index_information())

# Query som använder indexet
query = {"first_name": "John", "last_name": "Doe"}
result = persons.find(query)
print("Query Result:")
for person in result:
    print(person)

# Skapa collection "cars"
cars = db['cars']

# Hämta ett owner_id från "persons"
owner_id = persons.find_one({"first_name": "John"})["_id"]

# Infoga testdata i "cars"
cars.insert_one({"make": "Toyota", "model": "Corolla", "year": 2020, "owner": owner_id})

# Visa data från "cars"
print("Cars Collection:")
for car in cars.find():
    print(car)

# Hämta bilar och deras ägare
result = cars.aggregate([
    {
        "$lookup": {
            "from": "persons",
            "localField": "owner",
            "foreignField": "_id",
            "as": "owner_details"
        }
    }
])

print("Cars with Owners:")
for car in result:
    print(car)
